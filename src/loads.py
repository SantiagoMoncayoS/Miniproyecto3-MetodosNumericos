
import numpy as np
def f1d(x):
    return 10.0*np.sin(np.pi*x)
def f2d_hex(x,y,alpha=100.0,beta=50.0,gamma=0.3,theta=np.pi/4.0):
    r=np.sqrt(x*x+y*y); phi=np.arctan2(y,x)
    return alpha*(1.0+beta*r*r+gamma*np.cos(phi-theta))
