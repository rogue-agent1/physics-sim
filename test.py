from physics_sim import Vec2, Particle, World
w = World(bounds=(800, 600))
p = w.add(Particle(Vec2(400, 0), Vec2(0, 0)))
for _ in range(100): w.step(1/60)
assert p.pos.y > 0, "Gravity should pull particle down"
assert p.pos.y <= 600, "Should stay in bounds"
print("Physics sim tests passed")