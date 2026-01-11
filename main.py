import rebound

sim = rebound.Simulation()
sim.units = ('yr', 'AU', 'Msun')
sim.integrator = "whfast"
sim.dt = 0.01

sim.add(m=1.0)  # Sun

planets = [
    ("Mercury", 1.6601e-7, 0.3871, 0.2056),
    ("Venus",   2.4478e-6, 0.7233, 0.0068),
    ("Earth",   3.0035e-6, 1.0000, 0.0167),
    ("Mars",    3.2271e-7, 1.5237, 0.0934),
    ("Jupiter", 9.5458e-4, 5.2028, 0.0489),
    ("Saturn",  2.8589e-4, 9.5388, 0.0565),
    ("Uranus",  4.3662e-5, 19.191, 0.0472),
    ("Neptune", 5.1514e-5, 30.068, 0.0086),
]

for name, m, a, e in planets:
    sim.add(m=m, a=a, e=e)

sim.move_to_com()

import numpy as np

sun = sim.particles[0]
earth = sim.particles[3]

r = np.linalg.norm([
    earth.x - sun.x,
    earth.y - sun.y,
    earth.z - sun.z
])

print(r, "AU")
