
import numpy as np
def random_mesh_1d(nint:int, seed=None):
    rng=np.random.default_rng(seed)
    x_internal=np.sort(rng.random(nint))
    x=np.concatenate(([0.0], x_internal, [1.0]))
    ne=len(x)-1
    elems=np.stack([np.arange(ne), np.arange(1,ne+1)], axis=1)
    return x, elems
