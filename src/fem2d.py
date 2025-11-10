
import numpy as np
from scipy.spatial import Delaunay
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from .mesh2d_hex import hexagon_vertices, generate_points_hex, point_in_poly
from .loads import f2d_hex
def triangulate_hex(R,nx,ny):
    x,y,poly=generate_points_hex(R,nx,ny)
    pts=np.c_[x,y]
    tri=Delaunay(pts)
    triangles=tri.simplices.copy()
    cent=pts[triangles].mean(axis=1)
    mask=np.array([point_in_poly(cx,cy,poly) for cx,cy in cent])
    tri_ok=triangles[mask]
    return pts, tri_ok, poly
def assemble_p1(pts, tri, R, alpha, beta, gamma, theta):
    nn=len(pts); K=lil_matrix((nn,nn),dtype=float); F=np.zeros(nn)
    for t in tri:
        x1,y1=pts[t[0]]; x2,y2=pts[t[1]]; x3,y3=pts[t[2]]
        mat=np.array([[x2-x1,x3-x1],[y2-y1,y3-y1]]); area=0.5*abs(np.linalg.det(mat))
        b1=y2-y3; c1=x3-x2; b2=y3-y1; c2=x1-x3; b3=y1-y2; c3=x2-x1
        grads=np.array([[b1,c1],[b2,c2],[b3,c3]])/(2.0*area)
        ke=area*(grads@grads.T)
        xc,yc=(x1+x2+x3)/3.0,(y1+y2+y3)/3.0; fe_val=f2d_hex(xc,yc,alpha,beta,gamma,theta)
        fe=fe_val*area/3.0*np.ones(3)
        for a in range(3):
            A=t[a]; F[A]+=fe[a]
            for b in range(3):
                B=t[b]; K[A,B]+=ke[a,b]
    poly=hexagon_vertices(R)
    def dist_point_segment(px,py,ax,ay,bx,by):
        apx,apy=px-ax,py-ay; abx,aby=bx-ax,by-ay
        t=(apx*abx+apy*aby)/(abx*abx+aby*aby+1e-15); t=np.clip(t,0.0,1.0)
        cx,cy=ax+t*abx, ay+t*aby
        return np.hypot(px-cx,py-cy)
    xs=pts[:,0]; tol=(xs.max()-xs.min())/max(10,len(xs)**0.5)
    boundary=np.zeros(len(pts),dtype=bool)
    for i,(px,py) in enumerate(pts):
        mind=1e9
        for k in range(6):
            ax,ay=poly[k]; bx,by=poly[(k+1)%6]
            d=dist_point_segment(px,py,ax,ay,bx,by); mind=min(mind,d)
        if mind<tol*1.2: boundary[i]=True
    for idx in np.where(boundary)[0]:
        K[idx,:]=0.0; K[idx,idx]=1.0; F[idx]=0.0
    return K.tocsr(), F, boundary
def solve_hex(R,nx,ny,alpha,beta,gamma,theta):
    pts,tri,poly=triangulate_hex(R,nx,ny)
    K,F,boundary=assemble_p1(pts,tri,R,alpha,beta,gamma,theta)
    u=spsolve(K,F)
    return pts,tri,u,boundary
