#!/usr/bin/env python3
"""2D physics simulator with gravity, collision, and springs."""
import sys, math

class Vec2:
    def __init__(self, x=0, y=0): self.x, self.y = x, y
    def __add__(s, o): return Vec2(s.x+o.x, s.y+o.y)
    def __sub__(s, o): return Vec2(s.x-o.x, s.y-o.y)
    def __mul__(s, t): return Vec2(s.x*t, s.y*t)
    def dot(s, o): return s.x*o.x + s.y*o.y
    def norm(s): return math.sqrt(s.dot(s))
    def unit(s): n=s.norm(); return Vec2(s.x/n, s.y/n) if n>0 else Vec2()

class Body:
    def __init__(self, pos, vel=None, mass=1, radius=0.5, fixed=False):
        self.pos = pos; self.vel = vel or Vec2(); self.mass = mass
        self.radius = radius; self.fixed = fixed; self.force = Vec2()

class World:
    def __init__(self, gravity=Vec2(0, 9.81), bounds=(0,0,20,15)):
        self.gravity = gravity; self.bodies = []; self.springs = []
        self.bounds = bounds; self.dt = 0.01; self.restitution = 0.8

    def add_body(self, body): self.bodies.append(body); return body

    def add_spring(self, a, b, k=50, rest_length=None):
        if rest_length is None: rest_length = (a.pos - b.pos).norm()
        self.springs.append((a, b, k, rest_length))

    def step(self):
        for b in self.bodies:
            b.force = Vec2()
            if not b.fixed: b.force = self.gravity * b.mass
        for a, b, k, rl in self.springs:
            d = b.pos - a.pos; dist = d.norm()
            if dist < 0.001: continue
            f = d.unit() * (k * (dist - rl))
            a.force = a.force + f; b.force = b.force + f * -1
        for b in self.bodies:
            if b.fixed: continue
            acc = b.force * (1/b.mass)
            b.vel = b.vel + acc * self.dt
            b.pos = b.pos + b.vel * self.dt
            # Bounds
            x0,y0,x1,y1 = self.bounds
            if b.pos.x - b.radius < x0: b.pos.x = x0+b.radius; b.vel.x *= -self.restitution
            if b.pos.x + b.radius > x1: b.pos.x = x1-b.radius; b.vel.x *= -self.restitution
            if b.pos.y - b.radius < y0: b.pos.y = y0+b.radius; b.vel.y *= -self.restitution
            if b.pos.y + b.radius > y1: b.pos.y = y1-b.radius; b.vel.y *= -self.restitution
        # Collisions
        for i in range(len(self.bodies)):
            for j in range(i+1, len(self.bodies)):
                a, b = self.bodies[i], self.bodies[j]
                d = b.pos - a.pos; dist = d.norm()
                if dist < a.radius + b.radius and dist > 0:
                    n = d.unit(); overlap = a.radius + b.radius - dist
                    if not a.fixed: a.pos = a.pos - n*(overlap/2)
                    if not b.fixed: b.pos = b.pos + n*(overlap/2)
                    rv = b.vel - a.vel; vn = rv.dot(n)
                    if vn > 0: continue
                    j_imp = -(1+self.restitution)*vn / (1/a.mass + 1/b.mass)
                    if not a.fixed: a.vel = a.vel - n*(j_imp/a.mass)
                    if not b.fixed: b.vel = b.vel + n*(j_imp/b.mass)

    def ascii_render(self, w=60, h=20):
        x0,y0,x1,y1 = self.bounds
        grid = [["." for _ in range(w)] for _ in range(h)]
        for b in self.bodies:
            px = int((b.pos.x-x0)/(x1-x0)*(w-1))
            py = int((b.pos.y-y0)/(y1-y0)*(h-1))
            if 0 <= px < w and 0 <= py < h:
                grid[py][px] = "O" if not b.fixed else "#"
        return "\n".join("".join(row) for row in grid)

def demo():
    print("=== 2D Physics Simulation ===")
    w = World()
    b1 = w.add_body(Body(Vec2(5, 1), Vec2(3, 0), mass=2, radius=0.8))
    b2 = w.add_body(Body(Vec2(15, 1), Vec2(-2, 0), mass=1, radius=0.5))
    b3 = w.add_body(Body(Vec2(10, 0), fixed=True, radius=0.3))
    b4 = w.add_body(Body(Vec2(10, 3), mass=0.5, radius=0.4))
    w.add_spring(b3, b4, k=30, rest_length=2)
    for frame in range(500):
        w.step()
        if frame % 100 == 0:
            print(f"\nt={frame*w.dt:.2f}s")
            print(w.ascii_render())
    ke = sum(0.5*b.mass*(b.vel.norm()**2) for b in w.bodies if not b.fixed)
    print(f"\nFinal KE: {ke:.2f} J")

def main(): demo()

if __name__ == "__main__": main()
