# Generated with SMOP  0.41
from libsmop import *
# Fltr.m

    
@function
def Fltr(B=None,A=None,st=None,ep=None,*args,**kwargs):
    varargin = Fltr.varargin
    nargin = Fltr.nargin

    ## filter
    Ln,Ho,Hb=Fllr(B.mat,A.mat,st,ep,nargout=3)
# Fltr.m:4
    
    Lo=Fflt(Ln,B,st)
# Fltr.m:5
    
    return Lo,Ho,Hb
    
if __name__ == '__main__':
    pass
    
    
@function
def Fllr(fmat=None,bmat=None,st=None,ep=None,*args,**kwargs):
    varargin = Fllr.varargin
    nargin = Fllr.nargin

    ## log-likelihood ratio
    
    Ho.mat.occ = copy(sum(fmat.occ,3))
# Fltr.m:13
    Hb.mat.occ = copy(sum(bmat.occ,3))
# Fltr.m:14
    ## plot
    Hpo=Ho.mat
# Fltr.m:16
    Hpo=FIvec(Hpo,st)
# Fltr.m:16
    
    Hpb=Hb.mat
# Fltr.m:17
    Hpb=FIvec(Hpb,st)
# Fltr.m:17
    ## boost object
# Ho.mat.occ    = 5 * Ho.mat.occ;
## LLR
# Ho.mat.occ(Ho.mat.occ == 0) = 1;                         # Epsilon
# Hb.mat.occ(Hb.mat.occ == 0) = 1;
    Ho.mat.occ[Ho.mat.occ < ep]=1
# Fltr.m:23
    
    Hb.mat.occ[Hb.mat.occ < 5]=1
# Fltr.m:24
    L=log(Ho.mat.occ / Hb.mat.occ)
# Fltr.m:25
    
    L=double(L > 0)
# Fltr.m:26
    
    ## extend to 3d
    L=repmat(L,concat([1,1,size(bmat.occ,3)]))
# Fltr.m:28
    ## vectorize
    I,J,K=ind2sub(size(L),find(L),nargout=3)
# Fltr.m:30
    pts.uni = copy(concat([I,J,K]))
# Fltr.m:30
    
    pts.unq = copy(concat([dot(st.vx.x,(I - 1)) + st.vm.xb,dot(st.vx.y,(J - 1)) + st.vm.yr,dot(st.vx.z,(K - 1)) + st.vm.zd]))
# Fltr.m:31
    ## compact
    Lr.mat.occ = copy(L)
# Fltr.m:34
    Lr.pts = copy(pts)
# Fltr.m:35
    return Lr,Hpo,Hpb
    
if __name__ == '__main__':
    pass
    
    
@function
def Fflt(Ln=None,Lr=None,st=None,*args,**kwargs):
    varargin = Fflt.varargin
    nargin = Fflt.nargin

    ## filter
    L=multiply(Ln.mat.occ,Lr.mat.occ)
# Fltr.m:42
    ## post process - morphological operators
# se.dx        = strel('rectangle',[2, 1]);           # extension in x direction
# se.dy        = strel('rectangle',[1, 2]);           # extension in y direction
# L           = imdilate(L, se.dx); L = imfill(L, 'holes');         # dilation and fill holes: x
# L           = imdilate(L, se.dy); L = imfill(L, 'holes');         # dilation and fill holes: y
## vectorize
    I,J,K=ind2sub(size(L),find(L),nargout=3)
# Fltr.m:49
    pts.uni = copy(concat([I,J,K]))
# Fltr.m:49
    
    pts.unq = copy(concat([dot(st.vx.x,(I - 1)) + st.vm.xb,dot(st.vx.y,(J - 1)) + st.vm.yr,dot(st.vx.z,(K - 1)) + st.vm.zd]))
# Fltr.m:50
    ## compact
    Lo.mat.occ = copy(L)
# Fltr.m:53
    Lo.pts = copy(pts)
# Fltr.m:54
    return Lo
    
if __name__ == '__main__':
    pass
    
    
@function
def FIvec(H=None,st=None,*args,**kwargs):
    varargin = FIvec.varargin
    nargin = FIvec.nargin

    ## vectorize
    I,J,K=ind2sub(size(H.occ),find(H.occ),nargout=3)
# Fltr.m:61
    H.uni = copy(concat([I,J,K]))
# Fltr.m:61
    
    H.unq = copy(concat([dot(st.vx.x,(I - 1)) + st.vm.xb,dot(st.vx.y,(J - 1)) + st.vm.yr,dot(st.vx.z,(K - 1)) + st.vm.zd]))
# Fltr.m:62
    return H
    
if __name__ == '__main__':
    pass
    