
import numpy as np, matplotlib.pyplot as plt
from pathlib import Path
def ensure(d): Path(d).mkdir(parents=True, exist_ok=True)
def plot_fem1d(x,u,outdir='figures',prefix='fem1d'):
    ensure(outdir); plt.figure(figsize=(7,4)); plt.plot(x,u,'-o',ms=3); plt.grid(True,alpha=.3)
    plt.xlabel('x'); plt.ylabel('u'); plt.title('FEM 1D'); p=Path(outdir)/f'{prefix}_solution.png'
    plt.tight_layout(); plt.savefig(p,dpi=180); plt.close()
def plot_mesh1d(x,outdir='figures',prefix='fem1d'):
    ensure(outdir); plt.figure(figsize=(7,1.5)); plt.plot(x,0*x,'|',ms=18)
    plt.xlim(0,1); plt.yticks([]); plt.xlabel('x'); plt.title('Nodos 1D')
    p=Path(outdir)/f'{prefix}_mesh.png'; plt.tight_layout(); plt.savefig(p,dpi=180); plt.close()
def plot_hex_solution(pts,tri,u,outdir='figures',fname='det_potential.png'):
    ensure(outdir); import matplotlib.tri as mtri; triang=mtri.Triangulation(pts[:,0],pts[:,1],tri)
    plt.figure(figsize=(6,6)); tpc=plt.tricontourf(triang,u,levels=40); plt.colorbar(tpc,label='u')
    plt.triplot(triang,color='k',alpha=.2,linewidth=.3); plt.gca().set_aspect('equal','box'); plt.title('u(x,y)')
    p=Path(outdir)/fname; plt.tight_layout(); plt.savefig(p,dpi=220); plt.close()
def plot_hex_load(pts,tri,fvals,outdir='figures',fname='det_load.png'):
    ensure(outdir); import matplotlib.tri as mtri; triang=mtri.Triangulation(pts[:,0],pts[:,1],tri)
    plt.figure(figsize=(6,6)); tpc=plt.tricontourf(triang,fvals,levels=40); plt.colorbar(tpc,label='f')
    plt.triplot(triang,color='k',alpha=.2,linewidth=.3); plt.gca().set_aspect('equal','box'); plt.title('f(x,y)')
    p=Path(outdir)/fname; plt.tight_layout(); plt.savefig(p,dpi=220); plt.close()
