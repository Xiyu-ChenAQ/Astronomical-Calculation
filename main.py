import rebound
import numpy as np
from celestial_bodies import SolarSystemBodies, add_solar_system

# 创建模拟
sim = rebound.Simulation()
sim.units = ('yr', 'AU', 'Msun')
sim.integrator ="ias15"
add_solar_system(sim, include_sun=True)

sun = sim.particles[0]
earth = sim.particles[3]
# 验证积分器的准确性
r = np.linalg.norm([
    earth.x - sun.x,
    earth.y - sun.y,
    earth.z - sun.z
])

print(r, "AU")
