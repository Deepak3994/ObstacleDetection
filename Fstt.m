function st = Fstt                                                              % setting [directory, number of frames, map setting]

%% main directories [1: moving, 18: car stoped] 
st.dr.dnm  = 1;    % (14) 1 - 12 - 17 - 18  % setting   % 1, 12, 17, [18-curve], [20-downtown]        % sub-directory number (dname - 1)
st.dr.cam  = 2;                                                                                     % left/right camera
st.dr.dst  = 'training'; %  'testing'                                                              % training/testing dataset
st.dr.mdr  = '/media/ali/TOSHIBA EXT/dataset_ext/dataset_tracking/';                                % main directoy of dataset
% st.dr.mdr  = 'F:\dataset_ext\dataset_tracking';
st.dr.pts  = fullfile(st.dr.mdr, st.dr.dst, sprintf('velodyne/%04d', st.dr.dnm - 1));               % directory of velodyne points
st.dr.img  = fullfile(st.dr.mdr, st.dr.dst, sprintf('image_%02d/%04d', st.dr.cam, st.dr.dnm - 1));  % directory of color images
st.dr.lbl  = fullfile(st.dr.mdr, st.dr.dst, sprintf('label_%02d', st.dr.cam));                      % directory of tracklet labels
st.dr.oxt  = fullfile(st.dr.mdr, st.dr.dst, 'oxts');                                                % directory of pose
st.dr.clb  = fullfile(st.dr.mdr, st.dr.dst, 'calib');                                               % directory of calibration
st.dr.rec  = fullfile(st.dr.mdr, 'result', filesep);                                                % directory of record
st.dr.nsq  = numel(dir(fullfile(st.dr.mdr, st.dr.dst, sprintf('image_%02d', st.dr.cam)))) - 2;      % total number of tracking sequences
%% start and end frames
st.st.st   = 1;                                                                                     % start frames
st.st.tn   = size(dir(sprintf('%s/*.png',st.dr.img)), 1);                                           % number of frames
%% local grid
st.bias    = 1.73;
st.vm.xf   = +25;                                                                                   % x direction and front (x: +5 ~ +55)
st.vm.xb   = +5;                                                                                    % x direction and behind
st.vm.yl   = +10;                                                                                   % y direction and left  (y: -15 ~ +15)
st.vm.yr   = -10;                                                                                   % y direction and right
st.vm.zu   = +2   - st.bias;                                                                        % z direction and up, bias: 1.73 (z: -1 ~ +2.5)
st.vm.zd   = -1   - st.bias;                                                                        % z direction and down
st.vm.bs   = +3;                                                                                    % blind spot radius
%% surface fitting
st.rd.dl   = 25;                                                                                     % number of frames to integrate
st.rd.pc   = 4;                                                                                     % every piece's length
st.rd.no   = (st.vm.xf - st.vm.xb) / st.rd.pc;                                                      % number of pieces
st.rd.ou   = 0.4;                                                                                   % outlier rejection
st.rd.sd   = pi / 16;                                                                               % slope diff. between two consecutive pieces
st.rd.vd   = 0.1;                                                                                   % total slope diff. 
st.rd.rm   = 0.2;                                                                                   % remove points under height        
%% voxel size
st.vx.x    = 0.1;   % 0.2
st.vx.y    = 0.1;   % 0.2
st.vx.z    = 0.1;   % 0.2
st.vx.ix   = ceil((st.vm.xf - st.vm.xb) / st.vx.x);                                                 % matrix size 
st.vx.iy   = ceil((st.vm.yl - st.vm.yr) / st.vx.y); 
st.vx.iz   = ceil((st.vm.zu - st.vm.zd) / st.vx.z);
%% foreground detection
st.fr.sz   = 0.5;                                                                                   % neighbourhood in meter
st.fr.bsz  = ceil(st.fr.sz / min([st.vx.x, st.vx.y, st.vx.z]));                                     % radiuos of volume to search (size of cells)
st.fr.frg  = 1;
%% calibration
clb        = dlmread(sprintf('%s/%04d.txt', st.dr.clb, st.dr.dnm - 1), ' ', 0, 1);                  % [read data, delimiter, row offset, column offset]
t.p2       = reshape(clb(st.dr.cam + 1, 1 : 12), [4, 3])'; t.p2(4, :) = [0 0 0 1];                  % load 3x4 P2 camera calibration matrix
t.rct      = reshape(clb(5, 1 : 9), [3, 3])'; t.rct(:, 4) = 0; t.rct(4,:) = [0 0 0 1];              % load 3x3 image calibration matrix
t.v2c      = reshape(clb(6, 1 : 12), [4, 3])'; t.v2c(4,:) = [0 0 0 1];                              % load 3x4 velodyne to camera matrix (R|t)
t.clb      = t.p2 * t.rct * t.v2c; st.dt.clb = t.clb(1:4, 1:3)';                                    % project velodyne points to image plane
%% pose
trm        = load(sprintf('%s/%04d', fullfile(st.dr.mdr, st.dr.dst, 'pose'), st.dr.dnm - 1));       % read from directory of poses           
st.dt.pose = trm.pose;                                                                              % transformation matrix in camera coordinate
%% vehicle model
st.mdl     = model3d(fullfile('model3d', 'passat.3ds'));
st.mdl     = qrot(st.mdl, [0 0 1], pi/2);
%% plot
figure('units','normalized','outerposition',[0 0 1 1])

end

