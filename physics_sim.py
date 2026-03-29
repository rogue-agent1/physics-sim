#!/usr/bin/env python3
"""2D physics simulation."""
import math

class Vec2:
    def __init__(self, x=0, y=0): self.x, self.y = x, y
    def __add__(self, o): return Vec2(self.x+o.x, self.y+o.y)
    def __sub__(self, o): return Vec2(self.x-o.x, self.y-o.y)
    def __mul__(self, s): return Vec2(self.x*s, self.y*s)
    def mag(self): return math.sqrt(self.x**2 + self.y**2)
    def norm(self):
        m = self.mag()
        return Vec2(self.x/m, self.y/m) if m > 0 else Vec2()
    def dot(self, o): return self.x*o.x + self.y*o.y

class Body:
    def __init__(self, pos, vel=None, mass=1.0, radius=1.0):
        self.pos = pos
        self.vel = vel or Vec2()
        self.mass = mass
        self.radius = radius
        self.force = Vec2()

    def apply_force(self, f):
        self.force = self.force + f

class World:
    def __init__(self, gravity=Vec2(0, -9.81)):
        self.gravity = gravity
        self.bodies = []

    def add(self, body):
        self.bodies.append(body)
        return body

    def step(self, dt):
        for b in self.bodies:
            b.apply_force(self.gravity * b.mass)
            acc = b.force * (1.0/b.mass)
            b.vel = b.vel + acc * dt
            b.pos = b.pos + b.vel * dt
            b.force = Vec2()
        # Simple collision detection
        for i in range(len(self.bodies)):
            for j in range(i+1, len(self.bodies)):
                self._collide(self.bodies[i], self.bodies[j])

    def _collide(self, a, b):
        d = b.pos - a.pos
        dist = d.mag()
        if dist < a.radius + b.radius and dist > 0:
            n = d.norm()
            rel_vel = a.vel - b.vel
            vn = rel_vel.dot(n)
            if vn > 0:
                imp = (2 * vn) / (a.mass + b.mass)
                a.vel = a.vel - n * (imp * b.mass)
                b.vel = b.vel + n * (imp * a.mass)

if __name__ == "__main__":
    w = World()
    b = w.add(Body(Vec2(0, 10)))
    for _ in range(10):
        w.step(0.1)
        print(f"y={b.pos.y:.2f} vy={b.vel.y:.2f}")

def test():
    w = World(gravity=Vec2(0, -10))
    b = w.add(Body(Vec2(0, 100), mass=1))
    w.step(1.0)
    assert b.pos.y < 100
    assert b.vel.y < 0
    # Collision
    w2 = World(gravity=Vec2(0, 0))
    a = w2.add(Body(Vec2(0, 0), Vec2(1, 0), mass=1, radius=1))
    b = w2.add(Body(Vec2(1.5, 0), Vec2(-1, 0), mass=1, radius=1))
    w2.step(0.01)
    # After collision, velocities should swap (equal mass)
    assert a.vel.x < 1  # slowed down or reversed
    # Vec2
    v = Vec2(3, 4)
    assert abs(v.mag() - 5) < 1e-10
    n = v.norm()
    assert abs(n.mag() - 1) < 1e-10
    print("  physics_sim: ALL TESTS PASSED")
