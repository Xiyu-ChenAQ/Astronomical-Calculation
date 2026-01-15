"""
太阳系天文模拟
使用 REBOUND 进行 N-body 模拟
"""
import rebound
import numpy as np
from celestial_bodies import (
    add_solar_system,
    add_planets_by_name,
    SolarSystemBodies
)
from asteroid_belt import add_main_belt, add_hilda_group, add_trojans


def create_solar_system_simulation():
    """创建完整的太阳系模拟"""
    sim = rebound.Simulation()
    sim.units = ('yr', 'AU', 'Msun')
    sim.integrator = "ias15"

    # 添加太阳和八大行星
    add_solar_system(sim, include_sun=True, include_planets=True)

    return sim


def create_solar_system_with_moons():
    """创建包含主要卫星的太阳系模拟"""
    sim = rebound.Simulation()
    sim.units = ('yr', 'AU', 'Msun')
    sim.integrator = "ias15"

    # 添加太阳、行星和卫星
    add_solar_system(
        sim,
        include_sun=True,
        include_planets=True,
        include_moons=True
    )

    return sim


def create_solar_system_with_dwarfs():
    """创建包含矮行星的太阳系模拟"""
    sim = rebound.Simulation()
    sim.units = ('yr', 'AU', 'Msun')
    sim.integrator = "ias15"

    # 添加太阳、行星和矮行星
    add_solar_system(
        sim,
        include_sun=True,
        include_planets=True,
        include_dwarfs=True
    )

    return sim


def create_custom_system():
    """创建自定义天体系统（示例：内行星+木星+伽利略卫星）"""
    sim = rebound.Simulation()
    sim.units = ('yr', 'AU', 'Msun')
    sim.integrator = "ias15"

    # 添加太阳
    sun = SolarSystemBodies.SUN.add_to_simulation(sim)

    # 添加内行星和木星
    bodies = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter']
    for body_name in bodies:
        body = SolarSystemBodies.get_by_name(body_name)
        body.add_to_simulation(sim)

    # 添加木星的伽利略卫星
    jupiter = sim.particles[5]  # 太阳+4个内行星后木星是第6个
    galilean_moons = SolarSystemBodies.get_galilean_moons()

    for moon in galilean_moons:
        moon.add_to_simulation(sim, primary_particle=jupiter)

    sim.move_to_com()
    return sim


def create_realistic_asteroid_system(seed=42):
    """创建带有小行星带的真实系统"""
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


def verify_orbital_elements():
    """验证轨道要素的准确性"""
    sim = create_solar_system_simulation()

    sun = sim.particles[0]
    earth = sim.particles[3]

    # 计算日地距离
    r = np.linalg.norm([
        earth.x - sun.x,
        earth.y - sun.y,
        earth.z - sun.z
    ])

    print(f"日地距离: {r:.6f} AU")
    print(f"理论值:   1.000000 AU")
    print(f"误差:     {abs(r - 1.0):.6e} AU")

    # 输出所有行星信息
    print("\n所有行星轨道信息:")
    print("-" * 80)
    print(f"{'天体':<12} {'质量':<15} {'半长轴':<12} {'离心率':<10}")
    print("-" * 80)

    for planet in SolarSystemBodies.get_all_planets():
        print(f"{planet.name:<12} {planet.mass:.6e}    {planet.semi_major_axis:.4f}      {planet.eccentricity:.4f}")

    print(f"\n模拟中共有 {len(sim.particles)} 个天体")


def list_all_available_bodies():
    """列出数据库中所有可用的天体"""
    db = SolarSystemBodies()

    print("=" * 80)
    print("太阳系天体数据库")
    print("=" * 80)

    print("\n【恒星】")
    print(f"  • {db.SUN.name}")

    print("\n【八大行星】")
    for planet in db.get_all_planets():
        print(f"  • {planet.name}")

    print("\n【主要卫星】")
    for moon in db.get_all_moons():
        primary = moon.primary if moon.primary else "N/A"
        print(f"  • {moon.name:<15} (主天体: {primary})")

    print("\n【矮行星】")
    for dwarf in db.get_dwarf_planets():
        print(f"  • {dwarf.name}")

    print("\n【统计】")
    print(f"  总天体数: {1 + len(db.get_all_planets()) + len(db.get_all_moons()) + len(db.get_dwarf_planets())}")
    print("=" * 80)


if __name__ == "__main__":
    # 列出所有可用天体
    list_all_available_bodies()

    print("\n" + "=" * 80)
    print("验证轨道要素")
    print("=" * 80)
    verify_orbital_elements()

    # 示例：创建不同的模拟
    print("\n" + "=" * 80)
    print("模拟示例")
    print("=" * 80)

    # 1. 基本太阳系
    sim1 = create_solar_system_simulation()
    print(f"\n1. 基本太阳系: {len(sim1.particles)} 个天体")

    # 2. 包含卫星的太阳系
    sim2 = create_solar_system_with_moons()
    print(f"2. 包含卫星: {len(sim2.particles)} 个天体")

    # 3. 包含矮行星的太阳系
    sim3 = create_solar_system_with_dwarfs()
    print(f"3. 包含矮行星: {len(sim3.particles)} 个天体")

    # 4. 自定义系统（内行星+木星+伽利略卫星）
    sim4 = create_custom_system()
    print(f"4. 自定义系统: {len(sim4.particles)} 个天体")

