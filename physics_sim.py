#!/usr/bin/env python3
"""Physics simulations — projectile, pendulum, spring oscillation."""
import sys, math
def projectile(v0, angle_deg, g=9.81, dt=0.01):
    angle=math.radians(angle_deg); vx=v0*math.cos(angle); vy=v0*math.sin(angle)
    x=y=0; t=0; max_h=0; points=[]
    while y>=0:
        points.append((x,y)); max_h=max(max_h,y)
        x+=vx*dt; vy-=g*dt; y+=vy*dt; t+=dt
    return {"range":x,"max_height":max_h,"time":t,"points":points}
def pendulum(L, theta0_deg, g=9.81, dt=0.01, duration=5):
    theta=math.radians(theta0_deg); omega=0; points=[]
    for _ in range(int(duration/dt)):
        alpha=-g/L*math.sin(theta); omega+=alpha*dt; theta+=omega*dt
        points.append(math.degrees(theta))
    return points
def spring(k, m, x0, v0=0, dt=0.01, duration=5):
    x=x0; v=v0; points=[]
    for _ in range(int(duration/dt)):
        a=-k/m*x; v+=a*dt; x+=v*dt; points.append(x)
    return points
def cli():
    cmd=sys.argv[1] if len(sys.argv)>1 else "projectile"
    if cmd=="projectile":
        v=float(sys.argv[2]) if len(sys.argv)>2 else 50; a=float(sys.argv[3]) if len(sys.argv)>3 else 45
        r=projectile(v,a)
        print(f"  v0={v}m/s angle={a}°"); print(f"  Range: {r['range']:.1f}m  Max height: {r['max_height']:.1f}m  Time: {r['time']:.2f}s")
    elif cmd=="pendulum":
        pts=pendulum(1.0, 30)
        mn,mx=min(pts),max(pts)
        print(f"  Pendulum L=1m θ0=30°  Range: [{mn:.1f}°, {mx:.1f}°]")
    elif cmd=="spring":
        pts=spring(10, 1, 5)
        print(f"  Spring k=10 m=1 x0=5  Range: [{min(pts):.2f}, {max(pts):.2f}]")
if __name__=="__main__": cli()
