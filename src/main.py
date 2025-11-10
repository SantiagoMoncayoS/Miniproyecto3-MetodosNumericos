
import argparse, numpy as np
from pathlib import Path
from .mesh1d import random_mesh_1d
from .fem1d import solve_1d
from .fem2d import solve_hex, triangulate_hex
from .loads import f2d_hex
from .plotting import plot_fem1d, plot_mesh1d, plot_hex_solution, plot_hex_load

def cmd_fem1d(args):
    x,_=random_mesh_1d(args.nint, seed=args.seed); u=solve_1d(x)
    if args.plot: plot_fem1d(x,u); plot_mesh1d(x)
    Path('outputs').mkdir(exist_ok=True, parents=True)
    np.savez('outputs/fem1d.npz', x=x, u=u)

def deterministic(args):
    R,alpha,beta,gamma,theta = 0.6,100.0,50.0,0.3,np.pi/4.0
    pts,tri,_ = triangulate_hex(R,args.nx,args.ny)
    pts2,tri2,u,_ = solve_hex(R,args.nx,args.ny,alpha,beta,gamma,theta)
    fvals = f2d_hex(pts[:,0], pts[:,1], alpha,beta,gamma,theta)
    plot_hex_solution(pts2,tri2,u,fname='det_potential.png')
    plot_hex_load(pts,tri,fvals,fname='det_load.png')
    umax=float(np.max(np.abs(u))); Path('outputs').mkdir(exist_ok=True, parents=True)
    np.savez(f'outputs/{args.save_prefix}.npz', pts=pts2, tri=tri2, u=u, umax=umax)
    print('umax =', umax)

def monte_carlo(args):
    N=args.N; rng=np.random.default_rng(args.seed); umax_list=[]; params=[]
    for i in range(N):
        R=rng.normal(0.6,0.01); a=rng.normal(100.0,10.0); b=rng.normal(50.0,5.0)
        g=rng.normal(0.3,0.05); t=rng.normal(np.pi/4.0,np.pi/12.0)
        pts,tri,u,_ = solve_hex(R,args.nx,args.ny,a,b,g,t)
        umax=float(np.max(np.abs(u))); umax_list.append(umax); params.append([R,a,b,g,t])
        print(f'[{i+1}/{N}] umax={umax:.5f}')
    umax_arr=np.array(umax_list); params=np.array(params)
    mean=float(umax_arr.mean()); std=float(umax_arr.std(ddof=1))
    lo,hi=np.quantile(umax_arr,[0.025,0.975])
    corr=np.corrcoef(params.T, umax_arr)[-1,:-1]
    import matplotlib.pyplot as plt; Path('figures').mkdir(exist_ok=True, parents=True)
    plt.figure(figsize=(7,4)); plt.hist(umax_arr,bins=16,alpha=.8)
    plt.axvline(mean,ls='--',label=f'mean={mean:.3g}'); plt.axvspan(lo,hi,color='k',alpha=.1,label='95% CI')
    plt.xlabel('u_max'); plt.ylabel('count'); plt.legend(); plt.title('Monte Carlo of u_max')
    plt.tight_layout(); plt.savefig('figures/mc_hist.png',dpi=180); plt.close()
    Path('outputs').mkdir(exist_ok=True, parents=True)
    np.savez(f'outputs/{args.save_prefix}.npz', umax=umax_arr, params=params, mean=mean, std=std, ci95=(lo,hi), corr=corr)
    print('mean=',mean,'std=',std,'ci95=',(lo,hi)); print('corr (R,alpha,beta,gamma,theta)->u_max =',corr)

def parametric(args):
    rng=np.random.default_rng(args.seed)
    Rm,am,bm,gm,tm=0.6,100.0,50.0,0.3,np.pi/4.0
    N=args.N; xs=[]; ys=[]
    for i in range(N):
        R, a,b,g,t = Rm,am,bm,gm,tm
        if args.param=='R': R=rng.normal(Rm,0.01); x=R
        elif args.param=='alpha': a=rng.normal(am,10.0); x=a
        elif args.param=='beta': b=rng.normal(bm,5.0); x=b
        elif args.param=='gamma': g=rng.normal(gm,0.05); x=g
        elif args.param=='theta': t=rng.normal(tm,np.pi/12.0); x=t
        else: raise ValueError('param must be one of R, alpha, beta, gamma, theta')
        pts,tri,u,_ = solve_hex(R,args.nx,args.ny,a,b,g,t)
        xs.append(x); ys.append(float(np.max(np.abs(u)))); print(f'[{i+1}/{N}] umax={ys[-1]:.5f}')
    import matplotlib.pyplot as plt; Path('figures').mkdir(exist_ok=True, parents=True)
    plt.figure(figsize=(6,4)); plt.scatter(xs,ys,s=14); plt.xlabel(args.param); plt.ylabel('u_max')
    plt.title(f'u_max vs {args.param}'); plt.tight_layout(); plt.savefig('figures/param_scatter.png',dpi=180); plt.close()
    Path('outputs').mkdir(exist_ok=True, parents=True)
    np.savez(f'outputs/{args.save_prefix}.npz', param=args.param, x=np.array(xs), umax=np.array(ys))

def main():
    p=argparse.ArgumentParser(description='Miniproyecto 3 FEM 1D y Hex FEM 2D estocástico')
    sub=p.add_subparsers(dest='cmd', required=True)
    q=sub.add_parser('fem1d'); q.add_argument('--nint',type=int,default=30); q.add_argument('--seed',type=int,default=0); q.add_argument('--plot',action='store_true'); q.set_defaults(func=cmd_fem1d)
    d=sub.add_parser('det2d'); d.add_argument('--nx',type=int,default=45); d.add_argument('--ny',type=int,default=45); d.add_argument('--save-prefix',type=str,default='det_hex'); d.set_defaults(func=deterministic)
    m=sub.add_parser('mc'); m.add_argument('--N',type=int,default=100); m.add_argument('--nx',type=int,default=40); m.add_argument('--ny',type=int,default=40); m.add_argument('--seed',type=int,default=0); m.add_argument('--save-prefix',type=str,default='mc_hex'); m.set_defaults(func=monte_carlo)
    r=sub.add_parser('param'); r.add_argument('--param',type=str,choices=['R','alpha','beta','gamma','theta'],default='gamma'); r.add_argument('--N',type=int,default=100); r.add_argument('--nx',type=int,default=40); r.add_argument('--ny',type=int,default=40); r.add_argument('--seed',type=int,default=0); r.add_argument('--save-prefix',type=str,default='par_hex'); r.set_defaults(func=parametric)
    args=p.parse_args(); args.func(args)
if __name__=='__main__': main()
