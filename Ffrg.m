function L    = Ffrg(bmat, prm, st, frame)

% compute foreground
% output: foreground

%% compute foreground
pnt           = FKloa(st, frame);                       % load points
pnt           = FKcrp(pnt, st, frame);                  % crop points to the inside the local grid and image
[~, lmat]     = Fvox(prm, st, pnt.pts);                 % remove ground and voxelize points

idx.occ       = (lmat.occ - bmat.occ) > 0;              % remove dynamic cells from integrated grid
rmat.occ      = (idx.occ) .* lmat.occ;
%% vectorize
[I, J, K]     = ind2sub(size(rmat.occ), find(rmat.occ)); rpts.uni = [I, J, K]; % unique indexes 
rpts.unq      = [st.vx.x * (I - 1) + st.vm.xb, st.vx.y * (J - 1) + ...         % unique start point locations
                 st.vm.yr, st.vx.z * (K - 1) + st.vm.zd]; 
%% compact
L.mat         = rmat;
L.pts         = rpts; 

end

function pts  = FKloa(st, frame)

% simple load
% output: pts.[pts ptn rtn trn] all points 

%% transformation matrixes [rotation 3x3, translation 3x1]
transform     = st.dt.pose(:, :, frame);                                     % transformation matrix in camera coordinate
pts.rtn       = transform(1:3, 1:3);                                         % rotation    3x3
pts.trn       = transform(1:3, 4);                                           % translation 3x1
%% velodyne points [x, y, z, r] total number of pointsx4
fid.pts       = fopen(sprintf('%s/%06d.bin', st.dr.pts, frame - 1), 'rb');   % read from directory of points (number of frames in each seq.)
velodyne      = fread(fid.pts, [4 inf], 'single')';                          % velodyne points [x, y, z, r] (total number of pointsx4)
fclose(fid.pts);                                                               % close fid
pts.pts       = velodyne(:, 1:3);                                            % velodyne points [x, y, z] (total number of pointsx3)
pts.ptn       = pts.pts * pts.rtn' + repmat(pts.trn', size(pts.pts, 1), 1);  % transformed velodyne points (Xp = RX + T)

end

function hst    = FKcrp(hst, st, frame)

% crop points to the inside the local grid and image
% output: hst.[pts] that is croped integrated points

%% velodyne points [x, y, z, r total number of pointsx4]
ins.grd         = ((hst.pts(:,1) > st.vm.xb) & (hst.pts(:,1) < st.vm.xf) & ...       % filter points to inside/outside the local grid
                  (hst.pts(:,2) > st.vm.yr) & (hst.pts(:,2) < st.vm.yl) & ...
                  (hst.pts(:,3) > st.vm.zd) & (hst.pts(:,3) < st.vm.zu));
hst.pts         = hst.pts(ins.grd, 1:3);                                             % velodyne points in local grid           
%% incorporate image and color data [pts col ref pxs]
pixel           = hst.pts * st.dt.clb;                                               % velodyne points on image plane
pixel(:, 1)     = pixel(:, 1)./pixel(:, 3); pixel(:, 2) = pixel(:, 2)./pixel(:, 3);  % point's x & y are cor. to image's c & nr - r (nr: nnumber of raws)
pixel           = round(pixel(:, 1:2));                                              % interpolate (it is not that much precise, round is enough!)
image           = imread(sprintf('%s/%06d.png', st.dr.img, frame - 1));              % load image (number of frames in each seq.)
ins.img         = (pixel(:, 1) >= 1) & (pixel(:, 1) <= size(image, 2)) & (pixel ...  % index of pixels inside grid and image
                  (:, 2) >= 1) & (pixel(:, 2) <= size(image, 1));
hst.pts         = hst.pts(ins.img, :);                                               % velodyne points in local grid & image

end

function [pts, mat] = Fvox(prm, st, input)

%% remove ground points 
pts.pts        = [];
for pci        = 1 : st.rd.no                                                                  % index of the first piece : index of the last piece
sp             = st.vm.xb + (pci - 1) * st.rd.pc;                                              % start of the current piece (sp) x   
ep             = sp + st.rd.pc;                                                                % end of the current piece (ep) x
pc             = input((input(:, 1) > sp) & (input(:, 1) < ep), :);                            % take the current piece's points
pln            = prm(pci, :);                                                                  % take the current estimated piece's parameter
nrm            = cross([0 0 pln(3)] - [1 1 sum(pln)], [0 0 pln(3)] - [0 1 pln(2) + pln(3)]);   % surface normal (the slope of normal line) 
t              = (pc(:, 3) - pln(1) .* pc(:,1) - pln(2) * pc(:, 2) - pln(3)) ...               % t is a variable
                 ./ ( pln(1) .* nrm(1)+ pln(2) .* nrm(2) - nrm(3));
pp             = [pc(:, 1) + nrm(1) .* t, pc(:, 2) + nrm(2) * t, pc(:, 3) + nrm(3) * t];       % projected points on the surface
id             = ((pc(:, 3) - pp(:, 3)) < st.rd.rm) | (abs((pc(:, 3) - pp(:, 3))) < st.rd.rm); % remove points under height                      
pc(id, :)      = []; 
pts.pts        = [pts.pts; pc];                                                                % velodyne points in local grid
end
%% voxelize points 
pts.idx        = floor([(pts.pts(:,1) - st.vm.xb)/st.vx.x + 1, (pts.pts(:,2) - ...             % quantize and transform point's index 
                 st.vm.yr)/st.vx.y + 1, (pts.pts(:,3) - st.vm.zd) / st.vx.z + 1]);
pts.idx(pts.idx(:, 1) > st.vx.ix, 1) = st.vx.ix;            
pts.idx(pts.idx(:, 2) > st.vx.iy, 2) = st.vx.iy; 
pts.idx(pts.idx(:, 3) > st.vx.iz, 3) = st.vx.iz;
mat.occ        = accumarray(pts.idx, 1, [st.vx.ix, st.vx.iy, st.vx.iz]);                       % matrix with number of points in each cell
% pts.ids        = floor([pts.pts(:,1) / st.vx.x, pts.pts(:,2) / st.vx.y, pts.pts(:,3) / st.vx.z]);    % quantize start point
% pts.ids(:, 1)  = pts.ids(:, 1) * st.vx.x;                                                      % x voxel start points in real coordinate
% pts.ids(:, 2)  = pts.ids(:, 2) * st.vx.y;                                                      % y voxel start points in real coordinate
% pts.ids(:, 3)  = pts.ids(:, 3) * st.vx.z;                                                      % z voxel start points in real coordinate
pts.ids        = (floor(pts.pts / st.vx.x)) * st.vx.x;                                         % fast 
[uni, idx, ~]  = unique(pts.idx, 'rows'); pts.uni = uni;                                       % unique indexes
unq            = pts.ids(idx, :);         pts.unq = unq;                                       % unique start point locations

end



