#!/usr/bin/env python3
"""RAFAELIA spectral-geometry experiment (stdlib-only, fail-closed)."""
from __future__ import annotations
import argparse, hashlib, itertools, json, math
from pathlib import Path
from typing import Any

SCHEMA="rafaelia.spectral-geometry-experiment.v1"
DIGITS=10
MATCH_TOL=1e-2

def canon(v:Any)->bytes:
    return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
def h(v:Any)->str: return hashlib.sha256(canon(v)).hexdigest()
def r(x:float)->float:
    return 0.0 if abs(x)<5e-11 else round(float(x),DIGITS)
def norm(v): return math.sqrt(sum(x*x for x in v))
def unit(v):
    n=norm(v)
    if n<=0: raise ValueError("zero vector")
    return tuple(x/n for x in v)
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def area(a,b,c): return .5*norm(cross(sub(b,a),sub(c,a)))
def cot(a,b,c):
    u,v=sub(b,a),sub(c,a); d=norm(cross(u,v))
    if d<=1e-15: raise ValueError("degenerate triangle")
    return dot(u,v)/d

def tetra():
    v=[unit(x) for x in ((1,1,1),(-1,-1,1),(-1,1,-1),(1,-1,-1))]
    return v,[(0,1,2),(0,3,1),(0,2,3),(1,3,2)]

def octa():
    v=[(1.,0.,0.),(-1.,0.,0.),(0.,1.,0.),(0.,-1.,0.),(0.,0.,1.),(0.,0.,-1.)]
    f=[(4,0,2),(4,2,1),(4,1,3),(4,3,0),(5,2,0),(5,1,2),(5,3,1),(5,0,3)]
    return v,f

def cube():
    v=[unit(x) for x in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),
                          (-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
    q=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    f=[]
    for a,b,c,d in q: f += [(a,b,c),(a,c,d)]
    return v,f

def icosa():
    p=(1+math.sqrt(5))/2; raw=[]
    for a in (-1,1):
        for b in (-1,1): raw += [(0,a,b*p),(a,b*p,0),(a*p,0,b)]
    v=[]
    for x in raw:
        if x not in v: v.append(x)
    v=[unit(x) for x in v]
    ds=[norm(sub(v[i],v[j])) for i,j in itertools.combinations(range(12),2)]
    e=min(x for x in ds if x>1e-12)
    edges={(i,j) for i,j in itertools.combinations(range(12),2) if abs(norm(sub(v[i],v[j]))-e)<1e-8}
    f=[(i,j,k) for i,j,k in itertools.combinations(range(12),3)
       if (i,j) in edges and (i,k) in edges and (j,k) in edges]
    if (len(v),len(f))!=(12,20): raise AssertionError("icosahedron invariant")
    return v,f

def geodesic(v,f,levels):
    v=list(v); f=list(f)
    for _ in range(levels):
        mid={}; out=[]
        def m(i,j):
            key=tuple(sorted((i,j)))
            if key not in mid:
                mid[key]=len(v); v.append(unit(tuple((v[i][k]+v[j][k])/2 for k in range(3))))
            return mid[key]
        for i,j,k in f:
            a,b,c=m(i,j),m(j,k),m(k,i)
            out += [(i,a,c),(a,j,b),(c,b,k),(a,b,c)]
        f=out
    return v,f

def cot_matrix(v,f):
    n=len(v); L=[[0.0]*n for _ in range(n)]; M=[0.0]*n; A=0.0
    for i,j,k in f:
        ar=area(v[i],v[j],v[k]); A+=ar
        for x in (i,j,k): M[x]+=ar/3
        ci,cj,ck=cot(v[i],v[j],v[k]),cot(v[j],v[k],v[i]),cot(v[k],v[i],v[j])
        for a,b,w in ((j,k,.5*ci),(k,i,.5*cj),(i,j,.5*ck)):
            L[a][a]+=w; L[b][b]+=w; L[a][b]-=w; L[b][a]-=w
    if any(x<=0 for x in M): raise ValueError("non-positive mass")
    s=[1/math.sqrt(x) for x in M]
    return [[L[i][j]*s[i]*s[j] for j in range(n)] for i in range(n)],A

def graph_matrix(v,f):
    n=len(v); adj=[set() for _ in range(n)]
    for i,j,k in f:
        for a,b in ((i,j),(j,k),(k,i)): adj[a].add(b); adj[b].add(a)
    d=[len(x) for x in adj]
    if any(x==0 for x in d): raise ValueError("isolated vertex")
    A=[[0.0]*n for _ in range(n)]
    for i in range(n):
        A[i][i]=1.0
        for j in adj[i]: A[i][j]=-1/math.sqrt(d[i]*d[j])
    return A

def eig(A,tol=1e-10,max_sweeps=80):
    n=len(A); a=[x[:] for x in A]
    for sweep in range(max_sweeps):
        changed=False; mx=0.0
        for p in range(n-1):
            for q in range(p+1,n):
                z=a[p][q]; mx=max(mx,abs(z))
                if abs(z)<=tol: continue
                app,aqq=a[p][p],a[q][q]; tau=(aqq-app)/(2*z)
                t=(1 if tau>=0 else -1)/(abs(tau)+math.sqrt(1+tau*tau))
                c=1/math.sqrt(1+t*t); s=t*c
                for k in range(n):
                    if k in (p,q): continue
                    x,y=a[k][p],a[k][q]
                    a[k][p]=a[p][k]=c*x-s*y; a[k][q]=a[q][k]=s*x+c*y
                a[p][p]=app-t*z; a[q][q]=aqq+t*z; a[p][q]=a[q][p]=0.0; changed=True
        if not changed or mx<tol: break
    else: raise RuntimeError("Jacobi solver did not converge")
    return sorted(0.0 if abs(a[i][i])<1e-9 else a[i][i] for i in range(n)),sweep+1

def ratios(vals,n=12):
    p=[x for x in vals if x>1e-8]
    return [r(x/p[0]) for x in p[:n]] if p else []

def mesh(name,v,f):
    C,A=cot_matrix(v,f); cv,cs=eig(C); gv,gs=eig(graph_matrix(v,f))
    return {"geometry":name,"vertex_count":len(v),"face_count":len(f),"surface_area":r(A),
            "area_relative_error_vs_unit_sphere":r(abs(A-4*math.pi)/(4*math.pi)),
            "cotangent_lumped_mass":{"first_eigenvalues":[r(x) for x in cv[:20]],"positive_ratios":ratios(cv),"jacobi_sweeps":cs},
            "normalized_graph":{"first_eigenvalues":[r(x) for x in gv[:20]],"positive_ratios":ratios(gv),"jacobi_sweeps":gs},
            "_cot":cv}

def mean(vals,start,count):
    x=vals[start:start+count]
    return sum(x)/count if len(x)==count else None
def rel(x,target): return None if x is None else abs(x-target)/target

def convergence(rows):
    out=[]
    for m in rows:
        v=m["_cot"]; l1,l2,l3=mean(v,1,3),mean(v,4,5),mean(v,9,7)
        out.append({"geometry":m["geometry"],"vertex_count":m["vertex_count"],
                    "area_relative_error":m["area_relative_error_vs_unit_sphere"],
                    "l1_mean":None if l1 is None else r(l1),"l1_relative_error":None if l1 is None else r(rel(l1,2)),
                    "l2_mean":None if l2 is None else r(l2),"l2_relative_error":None if l2 is None else r(rel(l2,6)),
                    "l3_mean":None if l3 is None else r(l3),"l3_relative_error":None if l3 is None else r(rel(l3,12))})
    ae=[x["area_relative_error"] for x in out]; e2=[x["l2_relative_error"] for x in out if x["l2_relative_error"] is not None]
    e3=[x["l3_relative_error"] for x in out if x["l3_relative_error"] is not None]
    return {"rows":out,"observed":{
        "surface_area_error_monotone_decrease":all(b<a for a,b in zip(ae,ae[1:])),
        "l2_error_monotone_decrease":all(b<a for a,b in zip(e2,e2[1:])),
        "l3_error_monotone_decrease_where_defined":all(b<a for a,b in zip(e3,e3[1:]))}}

def scan(rows):
    targets={"sqrt3_over_2":math.sqrt(3)/2,"phi":(1+math.sqrt(5))/2,"633":633.0,"999":999.0}
    c=[]
    for m in rows:
        for op in ("cotangent_lumped_mass","normalized_graph"):
            for i,x in enumerate(m[op]["positive_ratios"]): c.append((m["geometry"],op,i,float(x)))
    res={}
    for label,t in targets.items():
        z=min(c,key=lambda q:abs(q[3]-t)/abs(t)); err=abs(z[3]-t)/abs(t)
        res[label]={"target":r(t),"nearest":{"geometry":z[0],"operator":z[1],"ratio_index":z[2],"value":r(z[3])},
                    "relative_error":r(err),"match_within_experiment_v1_tolerance":err<=MATCH_TOL}
    return {"relative_tolerance":MATCH_TOL,
            "tolerance_provenance":"SET_IN_EXPERIMENT_V1_BEFORE_REMOTE_REPRODUCTION_NOT_BEFORE_REFERENCE_RUN",
            "scope":"positive_eigenvalue_ratios_only",
            "statistical_inference_performed":False,
            "multiple_comparison_correction":"NOT_APPLICABLE_DESCRIPTIVE_DISTANCE_ONLY",
            "results":res,
            "any_match":any(x["match_within_experiment_v1_tolerance"] for x in res.values()),
            "claim_allowed":False}

def sphere():
    levels=[]; n=0
    for l in range(5):
        g=2*l+1; n+=g; levels.append({"l":l,"lambda":float(l*(l+1)),"degeneracy":g,"cumulative_modes":n})
    return {"manifold":"unit_sphere_S2","radius":1.0,"area":r(4*math.pi),"levels":levels,
            "weyl_leading_law":"N(lambda) ~ A*lambda/(4*pi)"}

def build(context="REFERENCE_RUNTIME"):
    iv,ifc=icosa(); ov,ofc=octa()
    rows=[mesh("tetrahedron",*tetra()),mesh("cube",*cube()),mesh("icosahedron",iv,ifc),
          mesh("geodesic_l1",*geodesic(iv,ifc,1)),mesh("geodesic_l2",*geodesic(iv,ifc,2))]
    controls=[mesh("octahedron_control",ov,ofc),
              mesh("octa_geodesic_l1_control",*geodesic(ov,ofc,1)),
              mesh("octa_geodesic_l2_control",*geodesic(ov,ofc,2))]
    c1=convergence([x for x in rows if x["geometry"] in ("icosahedron","geodesic_l1","geodesic_l2")])
    c2=convergence(controls)
    conv={"families":{"icosahedral_refinement":c1,"octahedral_control_refinement":c2},
          "observed":{"icosahedral_all_monotone":all(c1["observed"].values()),
                      "octahedral_control_all_monotone_where_defined":all(c2["observed"].values())}}
    s=scan(rows)
    for x in rows+controls: x.pop("_cot")
    out={"schema":SCHEMA,"execution_context":context,"claim_allowed":False,"automatic_promotion":False,
         "dependency_profile":{"third_party_runtime_dependencies":[],"python_standard_library_only":True,
                               "license_added_by_experiment":False,"repository_license_override":False},
         "epistemic_boundaries":{"hash_is_not_truth":True,"numerical_convergence_is_not_physical_confirmation":True,
            "same_area_scaling_is_not_bekenstein_hawking_derivation":True,
            "individual_eigenvectors_in_degenerate_spaces_are_not_basis_invariant":True,
            "visual_similarity_is_not_spectral_equivalence":True},
         "reference":sphere(),"meshes":rows,"remeshing_controls":controls,
         "continuous_discrete_convergence":conv,"constant_scan":s,
         "control_assessment":{"multiple_sphere_triangulation_families":2,
            "operator_sensitivity_control":"COTANGENT_VS_NORMALIZED_GRAPH",
            "statistical_null_model":"TOKEN_VAZIO_JUSTIFIED_NULL_DISTRIBUTION_NOT_DEFINED",
            "claim_allowed":False},
         "hypothesis_assessment":{"H1":"PARTIAL_NUMERICAL_SUPPORT_FOR_CONTINUUM_DISCRETE_CONVERGENCE_ONLY",
             "rafaelia_constants_as_spectral_invariants":"INVESTIGATE" if s["any_match"] else "REJECT_CURRENT_PREREGISTERED_SCAN",
             "claim_allowed":False},
         "token_vazio":["INDEPENDENT_IMPLEMENTATION_REPLICATION","HIGHER_REFINEMENT_WITH_SPARSE_SOLVER",
            "JUSTIFIED_STATISTICAL_NULL_MODEL","NODAL_INVARIANTS_WITH_DEGENERATE_EIGENSPACE_GAUGE_CONTROL",
            "MICROSCOPIC_BLACK_HOLE_STATE_MAP","BEKENSTEIN_HAWKING_FACTOR_ONE_QUARTER_DERIVATION",
            "PHYSICAL_DEGREES_OF_FREEDOM_PER_MODE"]}
    out["receipt_sha256"]=h(out); return out

def validate(x):
    if x.get("claim_allowed") is not False: raise ValueError("claim promotion")
    z=dict(x); expected=z.pop("receipt_sha256",None)
    if not isinstance(expected,str) or h(z)!=expected: raise ValueError("receipt hash mismatch")
    for k,v in x["continuous_discrete_convergence"]["observed"].items():
        if v is not True: raise ValueError("convergence gate failed: "+k)
    if x["constant_scan"]["any_match"] is not False: raise ValueError("constant scan match requires review")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--output",type=Path,required=True); p.add_argument("--context",default="REFERENCE_RUNTIME")
    a=p.parse_args(); x=build(a.context); validate(x); a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"decision":"EXECUTED_NUMERICAL_REFERENCE","receipt_sha256":x["receipt_sha256"],
                      "constant_scan_any_match":x["constant_scan"]["any_match"],
                      "H1":x["hypothesis_assessment"]["H1"],"claim_allowed":False},indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
