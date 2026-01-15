import rebound
import numpy as np
from celestial_bodies import add_solar_system
from asteroid_belt import add_main_belt, add_hilda_group,add_trojans
# 创建模拟
sim = rebound.Simulation()
sim.units = ('yr', 'AU', 'Msun')
sim.integrator ="ias15"
add_solar_system(sim, include_sun=True)
def create_realistic_asteroid_system(seed=42):
    rng = np.random.default_rng(seed)

    sim = rebound.Simulation()
    sim.units = ('AU', 'yr', 'Msun')
    sim.integrator = "whfast"
    sim.dt = 0.02

    sun = sim.add(m=1.0)
    jupiter = sim.add(m=9.5e-4, a=5.2, e=0.048)

    add_main_belt(sim, N=20000, primary=sun, rng=rng)
    add_hilda_group(sim, N=3000, jupiter=jupiter, rng=rng)
    add_trojans(sim, N=5000, jupiter=jupiter, rng=rng)

    sim.move_to_com()
    return sim

sun = sim.particles[0]
earth = sim.particles[3]
# 验证积分器的准确性
r = np.linalg.norm([
    earth.x - sun.x,
    earth.y - sun.y,
    earth.z - sun.z
])

print(r, "AU")
