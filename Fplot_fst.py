# Generated with SMOP  0.41
from libsmop import *
# Fplot_fst.m

    
@function
def Fplot(st=None,Bg=None,Fg=None,prm=None,frame=None,*args,**kwargs):
    varargin = Fplot.varargin
    nargin = Fplot.nargin

    ## image
    img=imread(sprintf('%s/%06d.png',st.dr.img,frame - 1))
# Fplot_fst.m:4
    # subplot(3, 1, 1);
    imshow(img)
    Fpli(st,Bg,frame,concat([1,0,0]))
    Fpli(st,Fg,frame,concat([0,1,0]))
    ## grid
# subplot(3, 1, 2:3);
# Fplt(st, Bg, prm, frame, [1,0,0])
# Fplt(st, Fg, prm, frame, [0,1,0])
# hold on; plot(st.mdl); hold off
    pause(0.005)
    return
    
if __name__ == '__main__':
    pass
    
    
@function
def Fplt(st=None,In=None,slp=None,frame=None,clr=None,*args,**kwargs):
    varargin = Fplt.varargin
    nargin = Fplt.nargin

    # clf
## plot
    In.mat.occ = copy(In.mat.occ / max(ravel(In.mat.occ)))
# Fplot_fst.m:21
    hold('on')
    # FIsurf(slp, st);                               # plot surface
    FIgrd(In,st,clr)
    
    hold('off')
    xlabel('X')
    ylabel('Y')
    zlabel('Z')
    
    view(- 76,18)
    axis('equal','tight')
    grid('on')
    # pause(0.005)
    
    return
    
if __name__ == '__main__':
    pass
    
    
@function
def FIsurf(slp=None,st=None,*args,**kwargs):
    varargin = FIsurf.varargin
    nargin = FIsurf.nargin

    ## piecewise surface
    for pci in arange(1,st.rd.no).reshape(-1):
        sp=st.vm.xb + dot((pci - 1),st.rd.pc)
# Fplot_fst.m:36
        ep=sp + st.rd.pc
# Fplot_fst.m:37
        pln=slp(pci,arange())
# Fplot_fst.m:38
        t=0.1
# Fplot_fst.m:39
        xx,yy=meshgrid(arange(sp,ep,t),arange(st.vm.yr,st.vm.yl,t),nargout=2)
# Fplot_fst.m:40
        zz=dot(pln(1),xx) + dot(pln(2),yy) + pln(3)
# Fplot_fst.m:41
        surf(xx,yy,zz,'edgecolor','none')
    
    return
    
if __name__ == '__main__':
    pass
    
    
@function
def FIgrd(In=None,st=None,clr=None,*args,**kwargs):
    varargin = FIgrd.varargin
    nargin = FIgrd.nargin

    ## plot grid
    uni,unq,mat=FIpst(In.pts.uni,In.pts.unq,In.mat,st,nargout=3)
# Fplot_fst.m:50
    
    unq[arange(),3]=unq(arange(),3) + 1.73
# Fplot_fst.m:51
    for i in arange(1,size(uni,1)).reshape(-1):
        FIvxl(unq(i,arange(1,3)),concat([st.vx.x,st.vx.y,st.vx.z]),eye(3),dot(mat.occ(uni(i,1),uni(i,2),uni(i,3)),clr),0.5)
    
    return
    
if __name__ == '__main__':
    pass
    
    
@function
def FIpst(unq=None,unw=None,mat=None,st=None,*args,**kwargs):
    varargin = FIpst.varargin
    nargin = FIpst.nargin

    ## define box
    unq[end() + 1,arange()]=concat([1,1,1])
# Fplot_fst.m:62
    
    unq[end() + 1,arange()]=concat([st.vx.ix,st.vx.iy,st.vx.iz])
# Fplot_fst.m:63
    unw[end() + 1,arange()]=concat([st.vm.xb,st.vm.yr,- st.bias])
# Fplot_fst.m:64
    
    unw[end() + 1,arange()]=concat([st.vm.xf,st.vm.yl,st.vm.zu])
# Fplot_fst.m:65
    ## transparent
    mat.red[1,1,1]=1
# Fplot_fst.m:67
    mat.gre[1,1,1]=1
# Fplot_fst.m:67
    mat.blu[1,1,1]=1
# Fplot_fst.m:68
    mat.occ[1,1,1]=1
# Fplot_fst.m:68
    mat.red[st.vx.ix,st.vx.iy,st.vx.iz]=1
# Fplot_fst.m:69
    mat.gre[st.vx.ix,st.vx.iy,st.vx.iz]=1
# Fplot_fst.m:70
    mat.blu[st.vx.ix,st.vx.iy,st.vx.iz]=1
# Fplot_fst.m:71
    mat.occ[st.vx.ix,st.vx.iy,st.vx.iz]=1
# Fplot_fst.m:72
    return unq,unw,mat
    
if __name__ == '__main__':
    pass
    
    
@function
def FIvxl(sr=None,sz=None,rtn=None,cl=None,al=None,*args,**kwargs):
    varargin = FIvxl.varargin
    nargin = FIvxl.nargin

    ## voxel
    vt.o = copy(concat([[0,0,0],[sz(1),0,0],[sz(1),sz(2),0],[0,sz(2),0],[0,sz(2),sz(3)],[0,0,sz(3)],[sz(1),0,sz(3)],[sz(1),sz(2),sz(3)]]))
# Fplot_fst.m:79
    
    vt.t = copy((dot(rtn,vt.o.T)).T)
# Fplot_fst.m:81
    
    vt.t = copy(vt.t + repmat(concat([sr(1),sr(2),sr(3)]),8,1))
# Fplot_fst.m:82
    fc=concat([[1,2,3,4],[3,4,5,8],[1,4,5,6],[1,6,7,2],[2,3,8,7],[5,6,7,8]])
# Fplot_fst.m:83
    
    h=patch('Vertices',vt.t,'Faces',fc,'FaceColor',cl)
# Fplot_fst.m:84
    
    set(h,'FaceAlpha',al)
    return
    
if __name__ == '__main__':
    pass
    
    
@function
def Fpli(st=None,In=None,frame=None,clr=None,*args,**kwargs):
    varargin = Fpli.varargin
    nargin = Fpli.nargin

    ## project voxels on image
    In.mat.occ = copy(In.mat.occ / max(ravel(In.mat.occ)))
# Fplot_fst.m:92
    img=imread(sprintf('%s/%06d.png',st.dr.img,frame - 1))
# Fplot_fst.m:93
    
    hold('on')
    gds(In,st,img,clr)
    hold('off')
    title(concat(['measurement no. ',num2str(frame),'/',num2str(st.st.tn)]))
    # pause(0.005)
    
    return
    
if __name__ == '__main__':
    pass
    
    
@function
def gds(In=None,st=None,img=None,clr=None,*args,**kwargs):
    varargin = gds.varargin
    nargin = gds.nargin

    ## plot grid
    for i in arange(1,size(In.pts.uni,1)).reshape(-1):
        sr=In.pts.unq(i,arange(1,3))
# Fplot_fst.m:107
        sz=concat([st.vx.x,st.vx.y,st.vx.z])
# Fplot_fst.m:108
        rtn=eye(3)
# Fplot_fst.m:109
        cl=dot(In.mat.occ(In.pts.uni(i,1),In.pts.uni(i,2),In.pts.uni(i,3)),clr)
# Fplot_fst.m:110
        al=0.75
# Fplot_fst.m:111
        FIvxll(sr,sz,rtn,cl,al,img,st)
    
    return
    
if __name__ == '__main__':
    pass
    
    
@function
def FIvxll(sr=None,sz=None,rtn=None,cl=None,al=None,img=None,st=None,*args,**kwargs):
    varargin = FIvxll.varargin
    nargin = FIvxll.nargin

    ## voxel
    vt.o = copy(concat([[0,0,0],[sz(1),0,0],[sz(1),sz(2),0],[0,sz(2),0],[0,sz(2),sz(3)],[0,0,sz(3)],[sz(1),0,sz(3)],[sz(1),sz(2),sz(3)]]))
# Fplot_fst.m:120
    
    vt.t = copy((dot(rtn,vt.o.T)).T)
# Fplot_fst.m:122
    
    vt.t = copy(vt.t + repmat(concat([sr(1),sr(2),sr(3)]),8,1))
# Fplot_fst.m:123
    pxs=clb(st,vt.t,img)
# Fplot_fst.m:124
    if size(pxs,1) == 8:
        fc=concat([[1,2,3,4],[3,4,5,8],[1,4,5,6],[1,6,7,2],[2,3,8,7],[5,6,7,8]])
# Fplot_fst.m:126
        h=patch('Vertices',pxs,'Faces',fc,'FaceColor',cl)
# Fplot_fst.m:127
        set(h,'FaceAlpha',al)
    
    return
    
if __name__ == '__main__':
    pass
    
    
@function
def clb(st=None,pnt=None,img=None,flag=None,*args,**kwargs):
    varargin = clb.varargin
    nargin = clb.nargin

    ## calibration
    if nargin == 4:
        fl=copy(flag)
# Fplot_fst.m:135
    else:
        fl=0
# Fplot_fst.m:135
    
    T=zeros(4)
# Fplot_fst.m:136
    T[arange(1,3),arange()]=st.dt.clb
# Fplot_fst.m:137
    T[4,arange()]=concat([0,0,0,1])
# Fplot_fst.m:138
    T=T.T
# Fplot_fst.m:139
    pxs=ind(T,pnt,img,fl)
# Fplot_fst.m:140
    
    return pxs
    
if __name__ == '__main__':
    pass
    
    
@function
def ind(T=None,pnt=None,img=None,fl=None,*args,**kwargs):
    varargin = ind.varargin
    nargin = ind.nargin

    ## filter a
    pne=concat([pnt,zeros(size(pnt,1),1)])
# Fplot_fst.m:146
    
    pne[arange(),3]=pne(arange(),3)
# Fplot_fst.m:147
    
    idx.f = copy(pne(arange(),1) >= 0)
# Fplot_fst.m:148
    
    pnt=pne(idx.f,arange())
# Fplot_fst.m:149
    
    ## projection
    pxs=(dot(T,pnt.T)).T
# Fplot_fst.m:151
    
    pxs[arange(),1]=pxs(arange(),1) / pxs(arange(),3)
# Fplot_fst.m:152
    
    pxs[arange(),2]=pxs(arange(),2) / pxs(arange(),3)
# Fplot_fst.m:153
    pxs=round(pxs(arange(),arange(1,2)))
# Fplot_fst.m:154
    
    ## filter b
    if fl == 0:
        idx.i = copy(logical_and(logical_and(logical_and((pxs(arange(),1) >= 1),(pxs(arange(),1) <= size(img,2))),(pxs(arange(),2) >= 1)),(pxs(arange(),2) <= size(img,1))))
# Fplot_fst.m:157
        pxs=pxs(idx.i,arange())
# Fplot_fst.m:159
    
    return pxs
    
if __name__ == '__main__':
    pass
    