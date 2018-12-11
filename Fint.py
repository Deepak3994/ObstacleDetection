# Generated with SMOP  0.41
from libsmop import *
# Fint.m

    
@function
def Fint(st=None,frame=None,*args,**kwargs):
    varargin = Fint.varargin
    nargin = Fint.nargin

    # use temporal information: integrate points
# output: hst.[pts] croped integrated points
    
    ## load and integrate points
    ref=FIloa(st,frame)
# Fint.m:7
    
    hst.pts = copy([])
# Fint.m:8
    
    for frm in arange(frame,frame - st.rd.dl + 1,- 1).reshape(-1):
        if frm > 0:
            prv=FIloa(st,frm)
# Fint.m:11
            prv=FItns(prv,ref)
# Fint.m:12
            hst.pts = copy(concat([[hst.pts],[prv.prj]]))
# Fint.m:13
    
    hst=FIcrp(hst,st,frame)
# Fint.m:16
    
    prm=FIprm(hst.pts,st)
# Fint.m:17
    
    In=Fvox(prm,st,hst.pts)
# Fint.m:18
    return In,prm
    
if __name__ == '__main__':
    pass
    
    
@function
def FIloa(st=None,frame=None,*args,**kwargs):
    varargin = FIloa.varargin
    nargin = FIloa.nargin

    # simple load
# output: pts.[pts ptn rtn trn] all points
    
    ## transformation matrixes [rotation 3x3, translation 3x1]
    transform=st.dt.pose(arange(),arange(),frame)
# Fint.m:28
    
    pts.rtn = copy(transform(arange(1,3),arange(1,3)))
# Fint.m:29
    
    pts.trn = copy(transform(arange(1,3),4))
# Fint.m:30
    
    ## velodyne points [x, y, z, r] total number of pointsx4
    fid.pts = copy(fopen(sprintf('%s/%06d.bin',st.dr.pts,frame - 1),'rb'))
# Fint.m:32
    
    velodyne=fread(fid.pts,concat([4,inf]),'single').T
# Fint.m:33
    
    fclose(fid.pts)
    
    pts.pts = copy(velodyne(arange(),arange(1,3)))
# Fint.m:35
    
    pts.ptn = copy(dot(pts.pts,pts.rtn.T) + repmat(pts.trn.T,size(pts.pts,1),1))
# Fint.m:36
    
    return pts
    
if __name__ == '__main__':
    pass
    
    
@function
def FItns(prv=None,ref=None,*args,**kwargs):
    varargin = FItns.varargin
    nargin = FItns.nargin

    # transform previous points on the current coordinates
# output: prv.[new] that is projected points on the current coordinate
    
    ## translate and rotate previous points using current transformation
    prv.prj[arange(),arange(1,3)]=prv.ptn(arange(),arange(1,3)) - repmat(ref.trn.T,size(prv.pts,1),1)
# Fint.m:46
    
    prv.prj[arange(),arange(1,3)]=(numpy.linalg.solve(ref.rtn,prv.prj(arange(),arange(1,3)).T)).T
# Fint.m:47
    
    return prv
    
if __name__ == '__main__':
    pass
    
    
@function
def FIcrp(hst=None,st=None,frame=None,*args,**kwargs):
    varargin = FIcrp.varargin
    nargin = FIcrp.nargin

    # crop points to the inside the local grid and image
# output: hst.[pts] that is croped integrated points
    
    ## velodyne points [x, y, z, r total number of pointsx4]
    ins.grd = copy((logical_and(logical_and(logical_and(logical_and(logical_and((hst.pts(arange(),1) > (st.vm.xb)),(hst.pts(arange(),1) < st.vm.xf)),(hst.pts(arange(),2) > (st.vm.yr))),(hst.pts(arange(),2) < st.vm.yl)),(hst.pts(arange(),3) > (st.vm.zd))),(hst.pts(arange(),3) < st.vm.zu))))
# Fint.m:57
    hst.pts = copy(hst.pts(ins.grd,arange(1,3)))
# Fint.m:60
    
    ## incorporate image and color data [pts col ref pxs]
    pixel=dot(hst.pts,st.dt.clb)
# Fint.m:62
    
    pixel[arange(),1]=pixel(arange(),1) / pixel(arange(),3)
# Fint.m:63
    pixel[arange(),2]=pixel(arange(),2) / pixel(arange(),3)
# Fint.m:63
    
    pixel=round(pixel(arange(),arange(1,2)))
# Fint.m:64
    
    image=imread(sprintf('%s/%06d.png',st.dr.img,frame - 1))
# Fint.m:65
    
    ins.img = copy(logical_and(logical_and(logical_and((pixel(arange(),1) >= 1),(pixel(arange(),1) <= size(image,2))),(pixel(arange(),2) >= 1)),(pixel(arange(),2) <= size(image,1))))
# Fint.m:66
    hst.pts = copy(hst.pts(ins.img,arange()))
# Fint.m:68
    
    return hst
    
if __name__ == '__main__':
    pass
    
    
@function
def FIprm(pts=None,st=None,*args,**kwargs):
    varargin = FIprm.varargin
    nargin = FIprm.nargin

    # compute surface pieces' parameters
# output: parameters
# clf
## compute each surface piece parameters using least square method
    prm=zeros(st.rd.no,3)
# Fint.m:78
    
    base=- st.bias
# Fint.m:79
    
    for pci in arange(1,st.rd.no).reshape(-1):
        sp=st.vm.xb + dot((pci - 1),st.rd.pc)
# Fint.m:81
        ep=sp + st.rd.pc
# Fint.m:82
        pc=pts(logical_and((pts(arange(),1) > sp),(pts(arange(),1) < ep)),arange())
# Fint.m:83
        pc[logical_or((pc(arange(),3) < base - st.rd.ou),(pc(arange(),3) > base + st.rd.ou)),arange()]=[]
# Fint.m:84
        pln=(numpy.linalg.solve(concat([pc(arange(),1),pc(arange(),2),ones(size(pc,1),1)]),pc(arange(),3))).T
# Fint.m:85
        prm[pci,arange()]=pln
# Fint.m:86
        ## check to see if two consecutive pieces' parameters are acceptable or not
        if pci > 1:
            if (abs(atan(prm(pci,1)) - atan(prm(pci - 1,1))) > st.rd.sd) or (sqrt(sum((prm(pci,arange()) - prm(pci - 1,arange())) ** 2)) > st.rd.vd):
                prm[pci,arange()]=prm(pci - 1,arange())
# Fint.m:91
                pln=prm(pci - 1,arange())
# Fint.m:92
        base=dot(pln(1),ep) + pln(3)
# Fint.m:95
        ## plot
# t              = 1;
# [xx, yy]       = meshgrid(sp : t : ep, st.vm.yr : t : st.vm.yl);
# zz             = pln(1) * xx + pln(2) * yy + pln(3);
# hold on
# surf(xx, yy, zz, 'edgecolor', 'none')
# hold off
    
    return prm
    
if __name__ == '__main__':
    pass
    
    
@function
def Fvox(prm=None,st=None,input_=None,*args,**kwargs):
    varargin = Fvox.varargin
    nargin = Fvox.nargin

    ## remove ground points
    pts.pts = copy([])
# Fint.m:110
    for pci in arange(1,st.rd.no).reshape(-1):
        sp=st.vm.xb + dot((pci - 1),st.rd.pc)
# Fint.m:112
        ep=sp + st.rd.pc
# Fint.m:113
        pc=input_(logical_and((input_(arange(),1) > sp),(input_(arange(),1) < ep)),arange())
# Fint.m:114
        pln=prm(pci,arange())
# Fint.m:115
        nrm=cross(concat([0,0,pln(3)]) - concat([1,1,sum(pln)]),concat([0,0,pln(3)]) - concat([0,1,pln(2) + pln(3)]))
# Fint.m:116
        t=(pc(arange(),3) - multiply(pln(1),pc(arange(),1)) - dot(pln(2),pc(arange(),2)) - pln(3)) / (multiply(pln(1),nrm(1)) + multiply(pln(2),nrm(2)) - nrm(3))
# Fint.m:117
        pp=concat([pc(arange(),1) + multiply(nrm(1),t),pc(arange(),2) + dot(nrm(2),t),pc(arange(),3) + dot(nrm(3),t)])
# Fint.m:119
        id=logical_or(((pc(arange(),3) - pp(arange(),3)) < st.rd.rm),(abs((pc(arange(),3) - pp(arange(),3))) < st.rd.rm))
# Fint.m:120
        pc[id,arange()]=[]
# Fint.m:121
        pts.pts = copy(concat([[pts.pts],[pc]]))
# Fint.m:122
    
    ## voxelize points
    pts.idx = copy(floor(concat([(pts.pts(arange(),1) - st.vm.xb) / st.vx.x + 1,(pts.pts(arange(),2) - st.vm.yr) / st.vx.y + 1,(pts.pts(arange(),3) - st.vm.zd) / st.vx.z + 1])))
# Fint.m:125
    pts.idx[pts.idx(arange(),1) > st.vx.ix,1]=st.vx.ix
# Fint.m:127
    pts.idx[pts.idx(arange(),2) > st.vx.iy,2]=st.vx.iy
# Fint.m:128
    pts.idx[pts.idx(arange(),3) > st.vx.iz,3]=st.vx.iz
# Fint.m:129
    mat.occ = copy(accumarray(pts.idx,1,concat([st.vx.ix,st.vx.iy,st.vx.iz])))
# Fint.m:130
    
    # pts.ids        = floor([pts.pts(:,1) / st.vx.x, pts.pts(:,2) / st.vx.y, pts.pts(:,3) / st.vx.z]);    # quantize start point
# pts.ids(:, 1)  = pts.ids(:, 1) * st.vx.x;                                                      # x voxel start points in real coordinate
# pts.ids(:, 2)  = pts.ids(:, 2) * st.vx.y;                                                      # y voxel start points in real coordinate
# pts.ids(:, 3)  = pts.ids(:, 3) * st.vx.z;                                                      # z voxel start points in real coordinate
    pts.ids = copy(dot((floor(pts.pts / st.vx.x)),st.vx.x))
# Fint.m:135
    
    uni,idx,__=unique(pts.idx,'rows',nargout=3)
# Fint.m:136
    pts.uni = copy(uni)
# Fint.m:136
    
    unq=pts.ids(idx,arange())
# Fint.m:137
    pts.unq = copy(unq)
# Fint.m:137
    
    ## compact
    In.pts = copy(pts)
# Fint.m:139
    In.mat = copy(mat)
# Fint.m:140
    return In
    
if __name__ == '__main__':
    pass
    