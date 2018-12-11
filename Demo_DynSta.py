# Generated with SMOP  0.41
from libsmop import *
# Demo_DynSta.m

    ## 3D Voxel Grid
# Inputs: Velodyne points and GPS/IMU localization
# Output: Static / Dynamic environment modeling
# Alireza Asvadi, 2015 July
## clear memory & command window
    clc
    clear('all')
    close_('all')
    ## setting
    st=copy(Fstt)
# Demo_DynSta.m:10
    ## main
    for frame in arange(st.st.st,st.st.tn).reshape(-1):
        ## dynamic / static modeling
        In,prm=Fint(st,frame,nargout=2)
# Demo_DynSta.m:15
        Bm=Fmdl(In.mat,prm,st,frame)
# Demo_DynSta.m:16
        Fm=Ffrg(Bm.mat,prm,st,frame)
# Demo_DynSta.m:17
        ## discriminative analysis
        Bg,__,__=Fltr(Bm,Fm,st,100,nargout=3)
# Demo_DynSta.m:19
        Fg,__,__=Fltr(Fm,Bm,st,5,nargout=3)
# Demo_DynSta.m:20
        ## plot
# Fplot(st, Bg, Fg, prm, frame)
        Fplot_fst(st,Bg,Fg,prm,frame)
    