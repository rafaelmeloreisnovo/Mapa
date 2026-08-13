#!/usr/bin/env python3
# RAFAELIA evidence-gate toy numerical reproduction.
# Standard library only. This is NOT a reproduction of the paper's turbulence experiment.
import argparse, json, math

PI = math.pi

def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],
            a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])

def dot(a,b):
    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

def norm(v):
    s=math.sqrt(dot(v,v))
    if s < 1e-15:
        return (0.0,0.0,0.0)
    return (v[0]/s,v[1]/s,v[2]/s)

def field(N, x, y, R=1.5, warp=0.0, L=8.0):
    X=x + warp*0.12*math.sin(PI*y/L)
    Y=y + warp*0.10*math.sin(PI*x/L)
    r=math.hypot(X,Y)
    if r < 1e-14:
        return (0.0,0.0,-1.0)
    phi=math.atan2(Y,X)
    theta=2.0*math.atan((R/r)**abs(N))
    st=math.sin(theta)
    ang=N*phi
    return (st*math.cos(ang), st*math.sin(ang), math.cos(theta))

def rot(v, axis=(1.0,2.0,3.0), angle=1.1):
    ax=norm(axis); x,y,z=ax
    c=math.cos(angle); s=math.sin(angle); C=1.0-c
    M=((c+x*x*C, x*y*C-z*s, x*z*C+y*s),
       (y*x*C+z*s, c+y*y*C, y*z*C-x*s),
       (z*x*C-y*s, z*y*C+x*s, c+z*z*C))
    return tuple(sum(M[i][j]*v[j] for j in range(3)) for i in range(3))

def generate(N, n=181, L=8.0, warp=0.0, rotation=False, shift=0.0, recenter=False):
    step=2*L/(n-1)
    d=norm((1.0,0.4,-0.2))
    grid=[]
    for iy in range(n):
        y=-L+iy*step
        row=[]
        for ix in range(n):
            x=-L+ix*step
            v=field(N,x,y,warp=warp,L=L)
            if rotation:
                v=rot(v)
            if shift:
                raw=(v[0]+shift*d[0],v[1]+shift*d[1],v[2]+shift*d[2])
                if recenter:
                    raw=(raw[0]-shift*d[0],raw[1]-shift*d[1],raw[2]-shift*d[2])
                v=norm(raw)
            row.append(v)
        grid.append(row)
    return grid, step

def q_finite_difference(grid, step):
    n=len(grid)
    total=0.0
    inv=1.0/(2.0*step)
    for iy in range(1,n-1):
        for ix in range(1,n-1):
            b=grid[iy][ix]
            bxm=grid[iy][ix-1]; bxp=grid[iy][ix+1]
            bym=grid[iy-1][ix]; byp=grid[iy+1][ix]
            dx=tuple((bxp[k]-bxm[k])*inv for k in range(3))
            dy=tuple((byp[k]-bym[k])*inv for k in range(3))
            total += dot(b,cross(dx,dy))
    return total*step*step/(4.0*PI)

def measure(N, **kw):
    grid,step=generate(N,**kw)
    return q_finite_difference(grid,step)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--grid",type=int,default=181)
    args=ap.parse_args()
    n=args.grid
    base={str(N):measure(N,n=n) for N in (1,2,3,5,-1,-2,-3,-5)}
    warp={str(a):measure(3,n=n,warp=a) for a in (0.0,0.3,0.7,1.2,2.0)}
    rotation=measure(3,n=n,rotation=True)
    shifts={}
    for a in (0.2,0.5,0.9,1.2,1.5):
        shifts[str(a)]={"without_recenter":measure(3,n=n,shift=a),
                        "with_recenter":measure(3,n=n,shift=a,recenter=True)}
    out={
      "kind":"TOY_NUMERICAL_REPRODUCTION",
      "claim_allowed":False,
      "grid":n,
      "finite_domain_L":8.0,
      "profile_R":1.5,
      "sign_convention":"positive winding N yields negative computed Q for this theta convention; compare |Q|",
      "base":base,
      "smooth_coordinate_warp_N3":warp,
      "global_SO3_rotation_N3":rotation,
      "bloch_constant_shift_N3":shifts,
      "scope":"Tests the mathematical topological-degree mechanism only; does not reproduce experimental turbulence, QST, raw photon counts, or paper figures."
    }
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__":
    main()
