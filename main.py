import rebound
import numpy as np
import astropy.units as u
from astroquery.simbad import Simbad
sim = rebound.Simulation()
sim.units='AU'

sim.add(m=1.)           # 太阳
sim.add(m=3.003e-6, a=1., e=0.0167)  # 地球
sim.add(m=9.543e-4, a=5.203, e=0.048)  # 木星

  # 设置积分器
sim.integrator = "whfast"  # 快速且精确
sim.dt = 0.01             # 时间步长

  # 积分100个时间单位
sim.integrate(100)
  # 输出结果
for i, p in enumerate(sim.particles):
      print(f"粒子 {i}: 位置 = ({p.x:.3f}, {p.y:.3f}, {p.zmz:.3f})")