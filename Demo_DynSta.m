%% 3D Voxel Grid
% Inputs: Velodyne points and GPS/IMU localization
% Output: Static / Dynamic environment modeling
% Alireza Asvadi, 2015 July
%% clear memory & command window
clc
clear all
close all
%% setting 
st           = Fstt;
%% main
for frame    =  st.st.st : st.st.tn;             % frame number 1: 25

%% dynamic / static modeling    
[In, prm]    = Fint(st, frame);                  % ground parameters and voxelize integrate points 
Bm           = Fmdl(In.mat, prm, st, frame);     % remove dynamic voxels and build the background model
Fm           = Ffrg(Bm.mat, prm, st, frame);     % compute foreground voxels
%% discriminative analysis
[Bg, ~, ~]   = Fltr(Bm, Fm, st, 100);            % background model
[Fg, ~, ~]   = Fltr(Fm, Bm, st, 5);              % foreground model
%% plot
% Fplot(st, Bg, Fg, prm, frame)
Fplot_fst(st, Bg, Fg, prm, frame)

end

