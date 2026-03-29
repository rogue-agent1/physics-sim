#!/usr/bin/env python3
"""2D physics simulation (particles, gravity, collisions). Zero dependencies."""
import math, sys

class Vec2:
    def __init__(self, x=0, y=0): self.x, self.y = float(x), float(y)
    def __add__(self, o): return Vec2(self.x+o.x, self.y+o.y)
    def __sub__(self, o): return Vec2(self.x-o.x, self.y-o.y)
    def __mul__(self, s): return Vec2(self.x*s, self.y*s)
    def dot(self, o): return self.x*o.x + self.y*o.y
    def mag(self): return math.sqrt(self.x**2 + self.y**2)
    def norm(self):
        m = self.mag()
        return Vec2(self.x/m, self.y/m) if m > 0 else Vec2()
    def __repr__(self): return f"({self.x:.2f}, {self.y:.2f})"

class Particle:
    def __init__(self, pos, vel=None, mass=1, radius=5):
        self.pos = pos
        self.vel = vel or Vec2()
        self.mass = mass
        self.radius = radius
        self.acc = Vec2()

    def apply_force(self, force):
        self.acc = self.acc + force * (1/self.mass)

    def update(self, dt):
        self.vel = self.vel + self.acc * dt
        self.pos = self.pos + self.vel * dt
        self.acc = Vec2()

class World:
    def __init__(self, gravity=Vec2(0, 9.81), bounds=None):
        self.gravity = gravity
        self.particles = []
        self.bounds = bounds  # (width, height)

    def add(self, p):
        self.particles.append(p); return p

    def step(self, dt=0.016):
        for p in self.particles:
            p.apply_force(self.gravity * p.mass)
            p.update(dt)
            if self.bounds:
                w, h = self.bounds
                if p.pos.x - p.radius < 0:
                    p.pos.x = p.radius; p.vel.x *= -0.8
                if p.pos.x + p.radius > w:
                    p.pos.x = w - p.radius; p.vel.x *= -0.8
                if p.pos.y + p.radius > h:
                    p.pos.y = h - p.radius; p.vel.y *= -0.8
                if p.pos.y - p.radius < 0:
                    p.pos.y = p.radius; p.vel.y *= -0.8
        self._collisions()

    def _collisions(self):
        ps = self.particles
        for i in range(len(ps)):
            for j in range(i+1, len(ps)):
                d = ps[j].pos - ps[i].pos
                dist = d.mag()
                if dist < ps[i].radius + ps[j].radius and dist > 0:
                    n = d.norm()
                    rv = ps[j].vel - ps[i].vel
                    vn = rv.dot(n)
                    if vn > 0: continue
                    e = 0.8
                    j_imp = -(1+e)*vn / (1/ps[i].mass + 1/ps[j].mass)
                    ps[i].vel = ps[i].vel - n * (j_imp/ps[i].mass)
                    ps[j].vel = ps[j].vel + n * (j_imp/ps[j].mass)
                    overlap = (ps[i].radius + ps[j].radius - dist) / 2
                    ps[i].pos = ps[i].pos - n * overlap
                    ps[j].pos = ps[j].pos + n * overlap

if __name__ == "__main__":
    w = World(bounds=(800, 600))
    w.add(Particle(Vec2(100, 100), Vec2(50, 0), mass=2, radius=10))
    w.add(Particle(Vec2(200, 100), Vec2(-30, 0), mass=1, radius=8))
    for i in range(60):
        w.step(1/60)
    for p in w.particles:
        print(f"pos={p.pos} vel={p.vel}")
