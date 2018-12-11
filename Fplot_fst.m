function Fplot(st, Bg, Fg, prm, frame)

%% image
img           = imread(sprintf('%s/%06d.png', st.dr.img, frame - 1));
% subplot(3, 1, 1); 
imshow(img)
Fpli(st, Bg, frame, [1, 0, 0]) 
Fpli(st, Fg, frame, [0, 1, 0])
%% grid
% subplot(3, 1, 2:3);
% Fplt(st, Bg, prm, frame, [1,0,0])
% Fplt(st, Fg, prm, frame, [0,1,0])
% hold on; plot(st.mdl); hold off
pause(0.005)

end

function Fplt(st, In, slp, frame, clr)
% clf
%% plot
In.mat.occ       = In.mat.occ / max(In.mat.occ(:));
hold on
% FIsurf(slp, st);                               % plot surface
FIgrd(In, st, clr);                              % plot grid
hold off;
xlabel('X'); ylabel('Y'); zlabel('Z');           % (-55, 25) view(-25, 45) view(0, 90) view(-105, 10) view(-80, 25)
view(-76, 18); axis equal tight; grid on;
% pause(0.005)

end

function FIsurf(slp, st)

%% piecewise surface
for pci        = 1 : st.rd.no
sp             = st.vm.xb + (pci - 1) * st.rd.pc;                          % start of the current piece (sp) x   
ep             = sp + st.rd.pc;                                            % end of the current piece (ep) x    
pln            = slp(pci, :);   
t              = .1;
[xx, yy]       = meshgrid(sp : t : ep, st.vm.yr : t : st.vm.yl);
zz             = pln(1) * xx + pln(2) * yy + pln(3);
surf(xx, yy, zz, 'edgecolor', 'none')
end

end

function FIgrd(In, st, clr)

%% plot grid
[uni, unq, mat] = FIpst(In.pts.uni, In.pts.unq, In.mat, st);                                    % make grid ready to show
unq(:, 3)      = unq(:, 3) + 1.73;

for i           = 1 : size(uni, 1)                                           % plot voxels 
FIvxl(unq(i, 1:3), [st.vx.x st.vx.y st.vx.z], eye(3), mat.occ(uni(i, 1), uni(i, 2), uni(i, 3))*clr, 0.5);
end

end

function [unq, unw, mat] = FIpst(unq, unw, mat, st)

%% define box
unq(end + 1, :) = [1, 1, 1];                                               % unique locations: indexes
unq(end + 1, :) = [st.vx.ix, st.vx.iy, st.vx.iz];
unw(end + 1, :) = [st.vm.xb, st.vm.yr, - st.bias];                         % unique locations: real position
unw(end + 1, :) = [st.vm.xf, st.vm.yl, st.vm.zu];
%% transparent
mat.red(1, 1, 1) = 1; mat.gre(1, 1, 1) = 1; 
mat.blu(1, 1, 1) = 1; mat.occ(1, 1, 1) = 1;
mat.red(st.vx.ix, st.vx.iy, st.vx.iz) = 1; 
mat.gre(st.vx.ix, st.vx.iy, st.vx.iz) = 1; 
mat.blu(st.vx.ix, st.vx.iy, st.vx.iz) = 1;
mat.occ(st.vx.ix, st.vx.iy, st.vx.iz) = 1;

end

function FIvxl(sr, sz, rtn, cl, al)  

%% voxel
vt.o  = [ 0 0 0; sz(1) 0 0; sz(1) sz(2) 0; 0 sz(2) 0; 0 sz(2) sz(3); 
          0 0 sz(3); sz(1) 0 sz(3); sz(1) sz(2) sz(3)];           % vertices
vt.t  = (rtn * vt.o')';                                           % transform  
vt.t  = vt.t + repmat([sr(1) sr(2) sr(3)], 8, 1);
fc    = [ 1 2 3 4; 3 4 5 8; 1 4 5 6; 1 6 7 2; 2 3 8 7; 5 6 7 8];  % voxel faces 
h     = patch('Vertices', vt.t, 'Faces', fc, 'FaceColor', cl);    % plot faces
set( h, 'FaceAlpha', al);

end

function Fpli(st, In, frame, clr)

%% project voxels on image
In.mat.occ     = In.mat.occ / max(In.mat.occ(:));
img            = imread(sprintf('%s/%06d.png', st.dr.img, frame - 1));   % load image (number of frames in each seq.)
hold on
gds(In, st, img, clr)      % bars (1 to show density): rsl.his, rsl.hei, rsl.max
hold off 
title(['measurement no. ', num2str(frame), '/',num2str(st.st.tn)])
% pause(0.005)

end

function gds(In, st, img, clr) 

%% plot grid
for  i  = 1 : size(In.pts.uni, 1)                              % initialize

sr  = In.pts.unq(i, 1:3);
sz  = [st.vx.x st.vx.y st.vx.z];
rtn = eye(3);
cl  = In.mat.occ(In.pts.uni(i, 1), In.pts.uni(i, 2), In.pts.uni(i, 3)) * clr;
al  = 0.75;

FIvxll(sr, sz, rtn, cl, al, img, st);
end
end

function FIvxll(sr, sz, rtn, cl, al, img, st)  

%% voxel
vt.o  = [ 0 0 0; sz(1) 0 0; sz(1) sz(2) 0; 0 sz(2) 0; 0 sz(2) sz(3); 
          0 0 sz(3); sz(1) 0 sz(3); sz(1) sz(2) sz(3)];           % vertices
vt.t  = (rtn * vt.o')';                                           % transform  
vt.t  = vt.t + repmat([sr(1) sr(2) sr(3)], 8, 1);
pxs   = clb(st, vt.t, img);
if size(pxs, 1) == 8
fc    = [ 1 2 3 4; 3 4 5 8; 1 4 5 6; 1 6 7 2; 2 3 8 7; 5 6 7 8];           % voxel faces 
h     = patch('Vertices', pxs, 'Faces', fc, 'FaceColor', cl);              % plot faces
set( h, 'FaceAlpha', al);
end
end

function pxs = clb(st, pnt, img, flag)                                     % calibration - velodyne to image

%% calibration
if nargin == 4; fl = flag; else fl = 0; end                                % remove points outside image or not? (flag = 1 -> remove)                                                           % read and provide calibration matrixes P2 & Tr
T   = zeros(4);
T(1:3, :) = st.dt.clb;
T(4, :)   = [0 0 0 1];
T = T';
pxs = ind(T, pnt, img, fl);                                                % projection of points on image

end

function pxs = ind(T, pnt, img, fl)                                        % project velodyne points on image
%% filter a
pne        = [pnt zeros(size(pnt, 1), 1)];                                 % points extended
pne(:, 3)  = pne(:, 3) ;                                                   % send back to velodyne coordinate (for valid transformation)
idx.f      = pne(:,1) >= 0;                                                % index of points in front of the car (points visible on the image)
pnt        = pne(idx.f, :);                                                % points visible on the image 
%% projection
pxs        = (T * pnt')';                                                  % map a point X from the velodyne scanner to image plane: x = Pi * Tr * X
pxs(:,1)   = pxs(:,1) ./ pxs(:,3);                                         % point's x & y are cor. to image's c & nr - r (nr: number of raws)
pxs(:,2)   = pxs(:,2) ./ pxs(:,3);
pxs        = round(pxs(:, 1:2));                                           % interpolate (it is not that much precise, round is enough!)
%% filter b
if fl == 0;                                                                % default
idx.i      = (pxs(:,1) >= 1) & (pxs(:,1) <= size(img, 2)) & ...            % index of points that are inside image 
             (pxs(:,2) >= 1) & (pxs(:,2) <= size(img, 1));                 % index of points that r inside local grid & in front of car & inside image
pxs        = pxs(idx.i, :);                                                % pixels 
end
end