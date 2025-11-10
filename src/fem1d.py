
import numpy as np
from .loads import f1d
def assemble_1d(x):
    ne=len(x)-1; nn=len(x)
    K=np.zeros((nn,nn)); F=np.zeros(nn)
    for e in range(ne):
        i,j=e,e+1; h=x[j]-x[i]
        ke=(1.0/h)*np.array([[1.0,-1.0],[-1.0,1.0]])
        xm=0.5*(x[i]+x[j]); fe_val=f1d(xm)
        fe=fe_val*h*0.5*np.array([1.0,1.0])
        K[i:i+2,i:i+2]+=ke; F[i:i+2]+=fe
    for d in [0,nn-1]:
        K[d,:]=0.0; K[:,d]=0.0; K[d,d]=1.0; F[d]=0.0
    return K,F
def solve_1d(x):
    K,F=assemble_1d(x); u=np.linalg.solve(K,F); return u
