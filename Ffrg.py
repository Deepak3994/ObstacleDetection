# Generated with SMOP  0.41
from libsmop import *
# Ffrg.m

    
@function
def Ffrg(bmat=None,prm=None,st=None,frame=None,*args,**kwargs):
    varargin = Ffrg.varargin
    nargin = Ffrg.nargin

    # compute foreground
# output: foreground
    
    ## compute foreground
    pnt=FKloa(st,frame)
# Ffrg.m:7
    
    pnt=FKcrp(pnt,st,frame)
# Ffrg.m:8
    
    __,lmat=Fvox(prm,st,pnt.pts,nargout=2)
# Ffrg.m:9
    
    idx.occ = copy((lmat.occ - bmat.occ) > 0)
# Ffrg.m:11
    
    rmat.occ = copy(multiply((idx.occ),lmat.occ))
# Ffrg.m:12
    ## vectorize
    I,J,K=ind2sub(size(rmat.occ),find(rmat.occ),nargout=3)
# Ffrg.m:14
    rpts.uni = copy(concat([I,J,K]))
# Ffrg.m:14
    
    rpts.unq = copy(concat([dot(st.vx.x,(I - 1)) + st.vm.xb,dot(st.vx.y,(J - 1)) + st.vm.yr,dot(st.vx.z,(K - 1)) + st.vm.zd]))
# Ffrg.m:15
    ## compact
    L.mat = copy(rmat)
# Ffrg.m:18
    L.pts = copy(rpts)
# Ffrg.m:19
    return L
    
if __name__ == '__main__':
    pass
    
    
@function
def FKloa(st=None,frame=None,*args,**kwargs):
    varargin = FKloa.varargin
    nargin = FKloa.nargin

    # simple load
# output: pts.[pts ptn rtn trn] all points
    
    ## transformation matrixes [rotation 3x3, translation 3x1]
    transform=st.dt.pose(arange(),arange(),frame)
# Ffrg.m:29
    
    pts.rtn = copy(transform(arange(1,3),arange(1,3)))
# Ffrg.m:30
    
    pts.trn = copy(transform(arange(1,3),4))
# Ffrg.m:31
    
    ## velodyne points [x, y, z, r] total number of pointsx4
    fid.pts = copy(fopen(sprintf('%s/%06d.bin',st.dr.pts,frame - 1),'rb'))
# Ffrg.m:33
    
    velodyne=fread(fid.pts,concat([4,inf]),'single').T
# Ffrg.m:34
    
    fclose(fid.pts)
    
    pts.pts = copy(velodyne(arange(),arange(1,3)))
# Ffrg.m:36
    
    pts.ptn = copy(dot(pts.pts,pts.rtn.T) + repmat(pts.trn.T,size(pts.pts,1),1))
# Ffrg.m:37
    
    return pts
    
if __name__ == '__main__':
    pass
    
    
@function
def FKcrp(hst=None,st=None,frame=None,*args,**kwargs):
    varargin = FKcrp.varargin
    nargin = FKcrp.nargin

    # crop points to the inside the local grid and image
# output: hst.[pts] that is croped integrated points
    
    ## velodyne points [x, y, z, r total number of pointsx4]
    ins.grd = copy((logical_and(logical_and(logical_and(logical_and(logical_and((hst.pts(arange(),1) > st.vm.xb),(hst.pts(arange(),1) < st.vm.xf)),(hst.pts(arange(),2) > st.vm.yr)),(hst.pts(arange(),2) < st.vm.yl)),(hst.pts(arange(),3) > st.vm.zd)),(hst.pts(arange(),3) < st.vm.zu))))
# Ffrg.m:47
    hst.pts = copy(hst.pts(ins.grd,arange(1,3)))
# Ffrg.m:50
    
    ## incorporate image and color data [pts col ref pxs]
    pixel=dot(hst.pts,st.dt.clb)
# Ffrg.m:52
    
    pixel[arange(),1]=pixel(arange(),1) / pixel(arange(),3)
# Ffrg.m:53
    pixel[arange(),2]=pixel(arange(),2) / pixel(arange(),3)
# Ffrg.m:53
    
    pixel=round(pixel(arange(),arange(1,2)))
# Ffrg.m:54
    
    image=imread(sprintf('%s/%06d.png',st.dr.img,frame - 1))
# Ffrg.m:55
    
    ins.img = copy(logical_and(logical_and(logical_and((pixel(arange(),1) >= 1),(pixel(arange(),1) <= size(image,2))),(pixel(arange(),2) >= 1)),(pixel(arange(),2) <= size(image,1))))
# Ffrg.m:56
    hst.pts = copy(hst.pts(ins.img,arange()))
# Ffrg.m:58
    
    return hst
    
if __name__ == '__main__':
    pass
    
    
@function
def Fvox(prm=None,st=None,input_=None,*args,**kwargs):
    varargin = Fvox.varargin
    nargin = Fvox.nargin

    ## remove ground points
    pts.pts = copy([])
# Ffrg.m:65
    for pci in arange(1,st.rd.no).reshape(-1):
        sp=st.vm.xb + dot((pci - 1),st.rd.pc)
# Ffrg.m:67
        ep=sp + st.rd.pc
# Ffrg.m:68
        pc=input_(logical_and((input_(arange(),1) > sp),(input_(arange(),1) < ep)),arange())
# Ffrg.m:69
        pln=prm(pci,arange())
# Ffrg.m:70
        nrm=cross(concat([0,0,pln(3)]) - concat([1,1,sum(pln)]),concat([0,0,pln(3)]) - concat([0,1,pln(2) + pln(3)]))
# Ffrg.m:71
        t=(pc(arange(),3) - multiply(pln(1),pc(arange(),1)) - dot(pln(2),pc(arange(),2)) - pln(3)) / (multiply(pln(1),nrm(1)) + multiply(pln(2),nrm(2)) - nrm(3))
# Ffrg.m:72
        pp=concat([pc(arange(),1) + multiply(nrm(1),t),pc(arange(),2) + dot(nrm(2),t),pc(arange(),3) + dot(nrm(3),t)])
# Ffrg.m:74
        id=logical_or(((pc(arange(),3) - pp(arange(),3)) < st.rd.rm),(abs((pc(arange(),3) - pp(arange(),3))) < st.rd.rm))
# Ffrg.m:75
        pc[id,arange()]=[]
# Ffrg.m:76
        pts.pts = copy(concat([[pts.pts],[pc]]))
# Ffrg.m:77
    
    ## voxelize points
    pts.idx = copy(floor(concat([(pts.pts(arange(),1) - st.vm.xb) / st.vx.x + 1,(pts.pts(arange(),2) - st.vm.yr) / st.vx.y + 1,(pts.pts(arange(),3) - st.vm.zd) / st.vx.z + 1])))
# Ffrg.m:80
    pts.idx[pts.idx(arange(),1) > st.vx.ix,1]=st.vx.ix
# Ffrg.m:82
    pts.idx[pts.idx(arange(),2) > st.vx.iy,2]=st.vx.iy
# Ffrg.m:83
    pts.idx[pts.idx(arange(),3) > st.vx.iz,3]=st.vx.iz
# Ffrg.m:84
    mat.occ = copy(accumarray(pts.idx,1,concat([st.vx.ix,st.vx.iy,st.vx.iz])))
# Ffrg.m:85
    
    # pts.ids        = floor([pts.pts(:,1) / st.vx.x, pts.pts(:,2) / st.vx.y, pts.pts(:,3) / st.vx.z]);    # quantize start point
# pts.ids(:, 1)  = pts.ids(:, 1) * st.vx.x;                                                      # x voxel start points in real coordinate
# pts.ids(:, 2)  = pts.ids(:, 2) * st.vx.y;                                                      # y voxel start points in real coordinate
# pts.ids(:, 3)  = pts.ids(:, 3) * st.vx.z;                                                      # z voxel start points in real coordinate
    pts.ids = copy(dot((floor(pts.pts / st.vx.x)),st.vx.x))
# Ffrg.m:90
    
    uni,idx,__=unique(pts.idx,'rows',nargout=3)
# Ffrg.m:91
    pts.uni = copy(uni)
# Ffrg.m:91
    
    unq=pts.ids(idx,arange())
# Ffrg.m:92
    pts.unq = copy(unq)
# Ffrg.m:92
    
    return pts,mat
    
if __name__ == '__main__':
    pass
    