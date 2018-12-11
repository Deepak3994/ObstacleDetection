# Generated with SMOP  0.41
from libsmop import *
# Fmdl.m

    
@function
def Fmdl(imat=None,prm=None,st=None,frame=None,*args,**kwargs):
    varargin = Fmdl.varargin
    nargin = Fmdl.nargin

    # model background
# output: purified integrated points
    
    ## purify integraed voxels
    ref=FJloa(st,frame)
# Fmdl.m:7
    
    for frm in arange(frame,frame - st.rd.dl + 1,- 1).reshape(-1):
        if frm > 0:
            pnt=FJloa(st,frm)
# Fmdl.m:11
            pnt=FJtns(pnt,ref)
# Fmdl.m:12
            pnt=FJcrp(pnt,st,frame)
# Fmdl.m:13
            __,lmat=Fvox(prm,st,pnt.pts,nargout=2)
# Fmdl.m:14
            idx.occ = copy((imat.occ - dot(st.fr.frg,lmat.occ)) > 0)
# Fmdl.m:16
            imat.occ = copy(multiply((idx.occ),imat.occ))
# Fmdl.m:17
    
    ## vectorize
    I,J,K=ind2sub(size(imat.occ),find(imat.occ),nargout=3)
# Fmdl.m:22
    ipts.uni = copy(concat([I,J,K]))
# Fmdl.m:22
    
    ipts.unq = copy(concat([dot(st.vx.x,(I - 1)) + st.vm.xb,dot(st.vx.y,(J - 1)) + st.vm.yr,dot(st.vx.z,(K - 1)) + st.vm.zd]))
# Fmdl.m:23
    ## compact
    L.mat = copy(imat)
# Fmdl.m:26
    L.pts = copy(ipts)
# Fmdl.m:27
    return L
    
if __name__ == '__main__':
    pass
    
    
@function
def FJloa(st=None,frame=None,*args,**kwargs):
    varargin = FJloa.varargin
    nargin = FJloa.nargin

    # simple load
# output: pts.[pts ptn rtn trn] all points
    
    ## transformation matrixes [rotation 3x3, translation 3x1]
    transform=st.dt.pose(arange(),arange(),frame)
# Fmdl.m:37
    
    pts.rtn = copy(transform(arange(1,3),arange(1,3)))
# Fmdl.m:38
    
    pts.trn = copy(transform(arange(1,3),4))
# Fmdl.m:39
    
    ## velodyne points [x, y, z, r] total number of pointsx4
    fid.pts = copy(fopen(sprintf('%s/%06d.bin',st.dr.pts,frame - 1),'rb'))
# Fmdl.m:41
    
    velodyne=fread(fid.pts,concat([4,inf]),'single').T
# Fmdl.m:42
    
    fclose(fid.pts)
    
    pts.pts = copy(velodyne(arange(),arange(1,3)))
# Fmdl.m:44
    
    pts.ptn = copy(dot(pts.pts,pts.rtn.T) + repmat(pts.trn.T,size(pts.pts,1),1))
# Fmdl.m:45
    
    return pts
    
if __name__ == '__main__':
    pass
    
    
@function
def FJtns(pts=None,ref=None,*args,**kwargs):
    varargin = FJtns.varargin
    nargin = FJtns.nargin

    # transform previous points on the current coordinates
# output: prv.[new] that is projected points on the current coordinate
    
    ## translate and rotate previous points using current transformation
    temp[arange(),arange(1,3)]=pts.ptn(arange(),arange(1,3)) - repmat(ref.trn.T,size(pts.pts,1),1)
# Fmdl.m:55
    
    pts.pts[arange(),arange(1,3)]=(numpy.linalg.solve(ref.rtn,temp(arange(),arange(1,3)).T)).T
# Fmdl.m:56
    
    return pts
    
if __name__ == '__main__':
    pass
    
    
@function
def FJcrp(hst=None,st=None,frame=None,*args,**kwargs):
    varargin = FJcrp.varargin
    nargin = FJcrp.nargin

    # crop points to the inside the local grid and image
# output: hst.[pts] that is croped integrated points
    
    ## velodyne points [x, y, z, r total number of pointsx4]
    ins.grd = copy((logical_and(logical_and(logical_and(logical_and(logical_and((hst.pts(arange(),1) > st.vm.xb),(hst.pts(arange(),1) < st.vm.xf)),(hst.pts(arange(),2) > st.vm.yr)),(hst.pts(arange(),2) < st.vm.yl)),(hst.pts(arange(),3) > st.vm.zd)),(hst.pts(arange(),3) < st.vm.zu))))
# Fmdl.m:66
    hst.pts = copy(hst.pts(ins.grd,arange(1,3)))
# Fmdl.m:69
    
    ## incorporate image and color data [pts col ref pxs]
    pixel=dot(hst.pts,st.dt.clb)
# Fmdl.m:71
    
    pixel[arange(),1]=pixel(arange(),1) / pixel(arange(),3)
# Fmdl.m:72
    pixel[arange(),2]=pixel(arange(),2) / pixel(arange(),3)
# Fmdl.m:72
    
    pixel=round(pixel(arange(),arange(1,2)))
# Fmdl.m:73
    
    image=imread(sprintf('%s/%06d.png',st.dr.img,frame - 1))
# Fmdl.m:74
    
    ins.img = copy(logical_and(logical_and(logical_and((pixel(arange(),1) >= 1),(pixel(arange(),1) <= size(image,2))),(pixel(arange(),2) >= 1)),(pixel(arange(),2) <= size(image,1))))
# Fmdl.m:75
    hst.pts = copy(hst.pts(ins.img,arange()))
# Fmdl.m:77
    
    return hst
    
if __name__ == '__main__':
    pass
    
    
@function
def Fvox(prm=None,st=None,input_=None,*args,**kwargs):
    varargin = Fvox.varargin
    nargin = Fvox.nargin

    ## remove ground points
    pts.pts = copy([])
# Fmdl.m:84
    for pci in arange(1,st.rd.no).reshape(-1):
        sp=st.vm.xb + dot((pci - 1),st.rd.pc)
# Fmdl.m:86
        ep=sp + st.rd.pc
# Fmdl.m:87
        pc=input_(logical_and((input_(arange(),1) > sp),(input_(arange(),1) < ep)),arange())
# Fmdl.m:88
        pln=prm(pci,arange())
# Fmdl.m:89
        nrm=cross(concat([0,0,pln(3)]) - concat([1,1,sum(pln)]),concat([0,0,pln(3)]) - concat([0,1,pln(2) + pln(3)]))
# Fmdl.m:90
        t=(pc(arange(),3) - multiply(pln(1),pc(arange(),1)) - dot(pln(2),pc(arange(),2)) - pln(3)) / (multiply(pln(1),nrm(1)) + multiply(pln(2),nrm(2)) - nrm(3))
# Fmdl.m:91
        pp=concat([pc(arange(),1) + multiply(nrm(1),t),pc(arange(),2) + dot(nrm(2),t),pc(arange(),3) + dot(nrm(3),t)])
# Fmdl.m:93
        id=logical_or(((pc(arange(),3) - pp(arange(),3)) < st.rd.rm),(abs((pc(arange(),3) - pp(arange(),3))) < st.rd.rm))
# Fmdl.m:94
        pc[id,arange()]=[]
# Fmdl.m:95
        pts.pts = copy(concat([[pts.pts],[pc]]))
# Fmdl.m:96
    
    ## voxelize points
    pts.idx = copy(floor(concat([(pts.pts(arange(),1) - st.vm.xb) / st.vx.x + 1,(pts.pts(arange(),2) - st.vm.yr) / st.vx.y + 1,(pts.pts(arange(),3) - st.vm.zd) / st.vx.z + 1])))
# Fmdl.m:99
    pts.idx[pts.idx(arange(),1) > st.vx.ix,1]=st.vx.ix
# Fmdl.m:101
    pts.idx[pts.idx(arange(),2) > st.vx.iy,2]=st.vx.iy
# Fmdl.m:102
    pts.idx[pts.idx(arange(),3) > st.vx.iz,3]=st.vx.iz
# Fmdl.m:103
    mat.occ = copy(accumarray(pts.idx,1,concat([st.vx.ix,st.vx.iy,st.vx.iz])))
# Fmdl.m:104
    
    # pts.ids        = floor([pts.pts(:,1) / st.vx.x, pts.pts(:,2) / st.vx.y, pts.pts(:,3) / st.vx.z]);    # quantize start point
# pts.ids(:, 1)  = pts.ids(:, 1) * st.vx.x;                                                      # x voxel start points in real coordinate
# pts.ids(:, 2)  = pts.ids(:, 2) * st.vx.y;                                                      # y voxel start points in real coordinate
# pts.ids(:, 3)  = pts.ids(:, 3) * st.vx.z;                                                      # z voxel start points in real coordinate
    pts.ids = copy(dot((floor(pts.pts / st.vx.x)),st.vx.x))
# Fmdl.m:109
    
    uni,idx,__=unique(pts.idx,'rows',nargout=3)
# Fmdl.m:110
    pts.uni = copy(uni)
# Fmdl.m:110
    
    unq=pts.ids(idx,arange())
# Fmdl.m:111
    pts.unq = copy(unq)
# Fmdl.m:111
    
    return pts,mat
    
if __name__ == '__main__':
    pass
    