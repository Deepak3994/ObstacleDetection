# Generated with SMOP  0.41
from libsmop import *
# Fplot.m

    
@function
def Fplot(st=None,Bg=None,Fg=None,prm=None,frame=None,*args,**kwargs):
    varargin = Fplot.varargin
    nargin = Fplot.nargin

    ## image
    img=imread(sprintf('%s/%06d.png',st.dr.img,frame - 1))
# Fplot.m:4
    subplot(3,1,1)
    imshow(img)
    Fpli(st,Bg,frame,concat([1,0,0]))
    Fpli(st,Fg,frame,concat([0,1,0]))
    ## grid
    subplot(3,1,arange(2,3))
    Fplt(st,Bg,prm,frame,concat([1,0,0]))
    Fplt(st,Fg,prm,frame,concat([0,1,0]))
    hold('on')
    plot(st.mdl)
    hold('off')
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
# Fplot.m:20
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
# Fplot.m:35
        ep=sp + st.rd.pc
# Fplot.m:36
        pln=slp(pci,arange())
# Fplot.m:37
        t=0.1
# Fplot.m:38
        xx,yy=meshgrid(arange(sp,ep,t),arange(st.vm.yr,st.vm.yl,t),nargout=2)
# Fplot.m:39
        zz=dot(pln(1),xx) + dot(pln(2),yy) + pln(3)
# Fplot.m:40
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
# Fplot.m:49
    
    unq[arange(),3]=unq(arange(),3) + 1.73
# Fplot.m:50
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
# Fplot.m:61
    
    unq[end() + 1,arange()]=concat([st.vx.ix,st.vx.iy,st.vx.iz])
# Fplot.m:62
    unw[end() + 1,arange()]=concat([st.vm.xb,st.vm.yr,- st.bias])
# Fplot.m:63
    
    unw[end() + 1,arange()]=concat([st.vm.xf,st.vm.yl,st.vm.zu])
# Fplot.m:64
    ## transparent
    mat.red[1,1,1]=1
# Fplot.m:66
    mat.gre[1,1,1]=1
# Fplot.m:66
    mat.blu[1,1,1]=1
# Fplot.m:67
    mat.occ[1,1,1]=1
# Fplot.m:67
    mat.red[st.vx.ix,st.vx.iy,st.vx.iz]=1
# Fplot.m:68
    mat.gre[st.vx.ix,st.vx.iy,st.vx.iz]=1
# Fplot.m:69
    mat.blu[st.vx.ix,st.vx.iy,st.vx.iz]=1
# Fplot.m:70
    mat.occ[st.vx.ix,st.vx.iy,st.vx.iz]=1
# Fplot.m:71
    return unq,unw,mat
    
if __name__ == '__main__':
    pass
    
    
@function
def FIvxl(sr=None,sz=None,rtn=None,cl=None,al=None,*args,**kwargs):
    varargin = FIvxl.varargin
    nargin = FIvxl.nargin

    ## voxel
    vt.o = copy(concat([[0,0,0],[sz(1),0,0],[sz(1),sz(2),0],[0,sz(2),0],[0,sz(2),sz(3)],[0,0,sz(3)],[sz(1),0,sz(3)],[sz(1),sz(2),sz(3)]]))
# Fplot.m:78
    
    vt.t = copy((dot(rtn,vt.o.T)).T)
# Fplot.m:80
    
    vt.t = copy(vt.t + repmat(concat([sr(1),sr(2),sr(3)]),8,1))
# Fplot.m:81
    fc=concat([[1,2,3,4],[3,4,5,8],[1,4,5,6],[1,6,7,2],[2,3,8,7],[5,6,7,8]])
# Fplot.m:82
    
    h=patch('Vertices',vt.t,'Faces',fc,'FaceColor',cl)
# Fplot.m:83
    
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
# Fplot.m:91
    img=imread(sprintf('%s/%06d.png',st.dr.img,frame - 1))
# Fplot.m:92
    
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
# Fplot.m:106
        sz=concat([st.vx.x,st.vx.y,st.vx.z])
# Fplot.m:107
        rtn=eye(3)
# Fplot.m:108
        cl=dot(In.mat.occ(In.pts.uni(i,1),In.pts.uni(i,2),In.pts.uni(i,3)),clr)
# Fplot.m:109
        al=0.75
# Fplot.m:110
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
# Fplot.m:119
    
    vt.t = copy((dot(rtn,vt.o.T)).T)
# Fplot.m:121
    
    vt.t = copy(vt.t + repmat(concat([sr(1),sr(2),sr(3)]),8,1))
# Fplot.m:122
    pxs=clb(st,vt.t,img)
# Fplot.m:123
    if size(pxs,1) == 8:
        fc=concat([[1,2,3,4],[3,4,5,8],[1,4,5,6],[1,6,7,2],[2,3,8,7],[5,6,7,8]])
# Fplot.m:125
        h=patch('Vertices',pxs,'Faces',fc,'FaceColor',cl)
# Fplot.m:126
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
# Fplot.m:134
    else:
        fl=0
# Fplot.m:134
    
    T=zeros(4)
# Fplot.m:135
    T[arange(1,3),arange()]=st.dt.clb
# Fplot.m:136
    T[4,arange()]=concat([0,0,0,1])
# Fplot.m:137
    T=T.T
# Fplot.m:138
    pxs=ind(T,pnt,img,fl)
# Fplot.m:139
    
    return pxs
    
if __name__ == '__main__':
    pass
    
    
@function
def ind(T=None,pnt=None,img=None,fl=None,*args,**kwargs):
    varargin = ind.varargin
    nargin = ind.nargin

    ## filter a
    pne=concat([pnt,zeros(size(pnt,1),1)])
# Fplot.m:145
    
    pne[arange(),3]=pne(arange(),3)
# Fplot.m:146
    
    idx.f = copy(pne(arange(),1) >= 0)
# Fplot.m:147
    
    pnt=pne(idx.f,arange())
# Fplot.m:148
    
    ## projection
    pxs=(dot(T,pnt.T)).T
# Fplot.m:150
    
    pxs[arange(),1]=pxs(arange(),1) / pxs(arange(),3)
# Fplot.m:151
    
    pxs[arange(),2]=pxs(arange(),2) / pxs(arange(),3)
# Fplot.m:152
    pxs=round(pxs(arange(),arange(1,2)))
# Fplot.m:153
    
    ## filter b
    if fl == 0:
        idx.i = copy(logical_and(logical_and(logical_and((pxs(arange(),1) >= 1),(pxs(arange(),1) <= size(img,2))),(pxs(arange(),2) >= 1)),(pxs(arange(),2) <= size(img,1))))
# Fplot.m:156
        pxs=pxs(idx.i,arange())
# Fplot.m:158
    
    return pxs
    
if __name__ == '__main__':
    pass
    