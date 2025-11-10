
import numpy as np
def hexagon_vertices(R: float):
    ang=np.arange(6)*np.pi/3.0
    return np.c_[R*np.cos(ang), R*np.sin(ang)]
def point_in_poly(x,y,poly):
    n=len(poly); inside=False; j=n-1
    for i in range(n):
        xi,yi=poly[i]; xj,yj=poly[j]
        intersect=((yi>y)!=(yj>y)) and (x < (xj-xi)*(y-yi)/(yj-yi+1e-15)+xi)
        if intersect: inside=not inside
        j=i
    return inside
def generate_points_hex(R,nx=40,ny=40,margin=0.0):
    poly=hexagon_vertices(R)
    xs=np.linspace(-R-margin,R+margin,nx); ys=np.linspace(-R-margin,R+margin,ny)
    XX,YY=np.meshgrid(xs,ys); X=XX.ravel(); Y=YY.ravel()
    mask=np.array([point_in_poly(x,y,poly) for x,y in zip(X,Y)])
    x_in=X[mask]; y_in=Y[mask]
    verts=poly
    xv=np.r_[x_in, verts[:,0]]; yv=np.r_[y_in, verts[:,1]]
    return xv,yv,poly
