function [Lo, Ho, Hb]   = Fltr(B, A, st, ep)

%% filter
[Ln, Ho, Hb]  = Fllr(B.mat, A.mat, st, ep);   % llr 2d
Lo            = Fflt(Ln, B, st);              % filter

end

function [Lr, Hpo, Hpb] = Fllr(fmat, bmat, st, ep)

%% log-likelihood ratio

Ho.mat.occ        = sum(fmat.occ, 3);
Hb.mat.occ        = sum(bmat.occ, 3);
%% plot
Hpo = Ho.mat; Hpo = FIvec(Hpo, st);   % vectorize
Hpb = Hb.mat; Hpb = FIvec(Hpb, st);
%% boost object
% Ho.mat.occ    = 5 * Ho.mat.occ;
%% LLR
% Ho.mat.occ(Ho.mat.occ == 0) = 1;                         % Epsilon
% Hb.mat.occ(Hb.mat.occ == 0) = 1;
Ho.mat.occ(Ho.mat.occ < ep) = 1;                         % Epsilon
Hb.mat.occ(Hb.mat.occ < 5) = 1;
L     = log(Ho.mat.occ./Hb.mat.occ);                     % Log - Liklihood Ratio
L     = double(L > 0);                                         % Remove Negative (binary mask)
%% extend to 3d
L     = repmat(L, [1, 1, size(bmat.occ, 3)]);
%% vectorize
[I, J, K]     = ind2sub(size(L), find(L)); pts.uni = [I, J, K]; % unique indexes 
pts.unq       = [st.vx.x * (I - 1) + st.vm.xb, st.vx.y * (J - 1) + ...         % unique start point locations
                 st.vm.yr, st.vx.z * (K - 1) + st.vm.zd]; 
%% compact
Lr.mat.occ    = L;
Lr.pts        = pts;

end

function Lo   = Fflt(Ln, Lr, st)

%% filter
L             = Ln.mat.occ .* Lr.mat.occ;
%% post process - morphological operators
% se.dx        = strel('rectangle',[2, 1]);           % extension in x direction
% se.dy        = strel('rectangle',[1, 2]);           % extension in y direction
% L           = imdilate(L, se.dx); L = imfill(L, 'holes');         % dilation and fill holes: x
% L           = imdilate(L, se.dy); L = imfill(L, 'holes');         % dilation and fill holes: y
%% vectorize
[I, J, K]     = ind2sub(size(L), find(L)); pts.uni = [I, J, K]; % unique indexes 
pts.unq       = [st.vx.x * (I - 1) + st.vm.xb, st.vx.y * (J - 1) + ...         % unique start point locations
                 st.vm.yr, st.vx.z * (K - 1) + st.vm.zd]; 
%% compact
Lo.mat.occ    = L;
Lo.pts        = pts;

end

function H = FIvec(H, st)

%% vectorize
[I, J, K]    = ind2sub(size(H.occ), find(H.occ)); H.uni = [I, J, K]; % unique indexes 
H.unq        = [st.vx.x * (I - 1) + st.vm.xb, st.vx.y * (J - 1) + ...         % unique start point locations
                 st.vm.yr, st.vx.z * (K - 1) + st.vm.zd]; 

end