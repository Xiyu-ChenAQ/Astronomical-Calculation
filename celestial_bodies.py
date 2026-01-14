"""
星体数据模型和注册表
"""
from dataclasses import dataclass
from typing import Optional
import rebound


@dataclass
class CelestialBodyConfig:
    """星体配置数据类"""
    name: str
    mass: float  # Solar masses
    semi_major_axis: Optional[float] = None  # AU
    eccentricity: Optional[float] = None
    color: Optional[str] = None

    def add_to_simulation(self, sim: rebound.Simulation, **kwargs):
        params = {'m': self.mass}

        if self.semi_major_axis is not None:
            params['a'] = self.semi_major_axis
        if self.eccentricity is not None:
            params['e'] = self.eccentricity

        params.update(kwargs)

        sim.add(**params)
        return sim.particles[-1]


class SolarSystemBodies:
    """太阳系星体注册表"""

    # 太阳
    SUN = CelestialBodyConfig(
        name="Sun",
        mass=1.0,
        color="#FFD700"
    )

    # 类地行星
    MERCURY = CelestialBodyConfig(
        name="Mercury",
        mass=1.6601e-7,
        semi_major_axis=0.3871,
        eccentricity=0.2056,
        color="#B5B5B5"
    )

    VENUS = CelestialBodyConfig(
        name="Venus",
        mass=2.4478e-6,
        semi_major_axis=0.7233,
        eccentricity=0.0068,
        color="#E6C87A"
    )

    EARTH = CelestialBodyConfig(
        name="Earth",
        mass=3.0035e-6,
        semi_major_axis=1.0000,
        eccentricity=0.0167,
        color="#6B93D6"
    )

    MARS = CelestialBodyConfig(
        name="Mars",
        mass=3.2271e-7,
        semi_major_axis=1.5237,
        eccentricity=0.0934,
        color="#C1440E"
    )

    # 气态巨行星
    JUPITER = CelestialBodyConfig(
        name="Jupiter",
        mass=9.5458e-4,
        semi_major_axis=5.2028,
        eccentricity=0.0489,
        color="#D8CA9D"
    )

    SATURN = CelestialBodyConfig(
        name="Saturn",
        mass=2.8589e-4,
        semi_major_axis=9.5388,
        eccentricity=0.0565,
        color="#F4D59E"
    )

    URANUS = CelestialBodyConfig(
        name="Uranus",
        mass=4.3662e-5,
        semi_major_axis=19.191,
        eccentricity=0.0472,
        color="#D1E7E7"
    )

    NEPTUNE = CelestialBodyConfig(
        name="Neptune",
        mass=5.1514e-5,
        semi_major_axis=30.068,
        eccentricity=0.0086,
        color="#5B5DDF"
    )
    # 卫星
    MOON = CelestialBodyConfig(
        name="Moon",
        mass=6.0223e-7,
        semi_major_axis=6.0223e-7,
        eccentricity=0.0072,
        color="#E6C87A"
    )
    # 矮行星
    PLUTO = CelestialBodyConfig(
        name="Pluto",
        mass=1.309e-8,
        semi_major_axis=39.48,
        eccentricity=0.2488,
        color="#9CA6B7"
    )

    @classmethod
    def get_all_planets(cls):
        """获取所有行星（不包括太阳）"""
        return [
            cls.MERCURY, cls.VENUS, cls.EARTH, cls.MARS,
            cls.JUPITER, cls.SATURN, cls.URANUS, cls.NEPTUNE
        ]

    @classmethod
    def get_terrestrial_planets(cls):
        """获取类地行星"""
        return [cls.MERCURY, cls.VENUS, cls.EARTH, cls.MARS]

    @classmethod
    def get_gas_giants(cls):
        """获取气态巨行星"""
        return [cls.JUPITER, cls.SATURN, cls.URANUS, cls.NEPTUNE]

    @classmethod
    def get_by_name(cls, name: str) -> Optional[CelestialBodyConfig]:
        """根据名称获取星体配置"""
        for body in cls.get_all_planets() + [cls.SUN]:
            if body.name.lower() == name.lower():
                return body
        return None


def add_solar_system(sim: rebound.Simulation, include_sun: bool = True):
    """添加整个太阳系到模拟中"""

    if include_sun:
        SolarSystemBodies.SUN.add_to_simulation(sim)

    for planet in SolarSystemBodies.get_all_planets():
        planet.add_to_simulation(sim)

    sim.move_to_com()
