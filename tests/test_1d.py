from src.mesh1d import random_mesh_1d
from src.fem1d import solve_1d

def test_1d_runs():
    x,_=random_mesh_1d(10,seed=1); u=solve_1d(x); assert u.shape[0]==x.shape[0]
