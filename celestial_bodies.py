#模型和注册表

from dataclasses import dataclass
from typing import Optional, List
import rebound
import numpy as np


@dataclass
class CelestialBodyConfig:
    """星体配置数据类"""
    name: str
    mass: float  # Solar masses
    semi_major_axis: Optional[float] = None  # AU
    eccentricity: Optional[float] = None
    inclination: Optional[float] = None  # degrees
    longitude_of_ascending_node: Optional[float] = None  # degrees (Omega)
    argument_of_pericenter: Optional[float] = None  # degrees (omega)
    mean_anomaly: Optional[float] = None  # degrees (M)
    color: Optional[str] = None
    primary: Optional[str] = None  # 主天体名称（用于卫星）

    def add_to_simulation(self, sim: rebound.Simulation, primary_particle=None, **kwargs):
        """将天体添加到 REBOUND 模拟中"""
        params = {'m': self.mass}

        # 轨道参数
        if self.semi_major_axis is not None:
            params['a'] = self.semi_major_axis
        if self.eccentricity is not None:
            params['e'] = self.eccentricity
        if self.inclination is not None:
            params['inc'] = np.radians(self.inclination)
        if self.longitude_of_ascending_node is not None:
            params['Omega'] = np.radians(self.longitude_of_ascending_node)
        if self.argument_of_pericenter is not None:
            params['omega'] = np.radians(self.argument_of_pericenter)
        if self.mean_anomaly is not None:
            params['M'] = np.radians(self.mean_anomaly)

        # 如果有主天体，指定 primary
        if primary_particle is not None:
            params['primary'] = primary_particle

        params.update(kwargs)

        sim.add(**params)
        return sim.particles[-1]


class SolarSystemBodies:
    """太阳系星体注册表"""

    # ==================== 太阳 ====================
    SUN = CelestialBodyConfig(
        name="Sun",
        mass=1.0,
        color="#FFD700"
    )

    # ==================== 八大行星 ====================

    # 水星 (Mercury)
    MERCURY = CelestialBodyConfig(
        name="Mercury",
        mass=1.6601367e-7,
        semi_major_axis=0.387098,
        eccentricity=0.205630,
        inclination=7.005,
        longitude_of_ascending_node=48.331,
        argument_of_pericenter=29.124,
        mean_anomaly=174.796,
        color="#B5B5B5"
    )

    # 金星 (Venus)
    VENUS = CelestialBodyConfig(
        name="Venus",
        mass=2.4478383e-6,
        semi_major_axis=0.723332,
        eccentricity=0.006773,
        inclination=3.394,
        longitude_of_ascending_node=76.680,
        argument_of_pericenter=54.884,
        mean_anomaly=50.115,
        color="#E6C87A"
    )

    # 地球 (Earth)
    EARTH = CelestialBodyConfig(
        name="Earth",
        mass=3.0034896e-6,
        semi_major_axis=1.000000,
        eccentricity=0.016708,
        inclination=0.000,
        longitude_of_ascending_node=174.873,
        argument_of_pericenter=288.064,
        mean_anomaly=357.517,
        color="#6B93D6"
    )

    # 火星 (Mars)
    MARS = CelestialBodyConfig(
        name="Mars",
        mass=3.2271538e-7,
        semi_major_axis=1.523679,
        eccentricity=0.093405,
        inclination=1.850,
        longitude_of_ascending_node=49.558,
        argument_of_pericenter=286.502,
        mean_anomaly=19.412,
        color="#C1440E"
    )

    # 木星 (Jupiter)
    JUPITER = CelestialBodyConfig(
        name="Jupiter",
        mass=9.5479194e-4,
        semi_major_axis=5.204267,
        eccentricity=0.048498,
        inclination=1.303,
        longitude_of_ascending_node=100.464,
        argument_of_pericenter=273.867,
        mean_anomaly=20.020,
        color="#D8CA9D"
    )

    # 土星 (Saturn)
    SATURN = CelestialBodyConfig(
        name="Saturn",
        mass=2.8588594e-4,
        semi_major_axis=9.582017,
        eccentricity=0.055546,
        inclination=2.485,
        longitude_of_ascending_node=113.665,
        argument_of_pericenter=339.392,
        mean_anomaly=317.020,
        color="#F4D59E"
    )

    # 天王星 (Uranus)
    URANUS = CelestialBodyConfig(
        name="Uranus",
        mass=4.3662442e-5,
        semi_major_axis=19.229411,
        eccentricity=0.047318,
        inclination=0.773,
        longitude_of_ascending_node=74.006,
        argument_of_pericenter=96.998,
        mean_anomaly=142.590,
        color="#D1E7E7"
    )

    # 海王星 (Neptune)
    NEPTUNE = CelestialBodyConfig(
        name="Neptune",
        mass=5.1513888e-5,
        semi_major_axis=30.103662,
        eccentricity=0.008606,
        inclination=1.770,
        longitude_of_ascending_node=131.784,
        argument_of_pericenter=273.187,
        mean_anomaly=256.228,
        color="#5B5DDF"
    )
    # ==================== 主要卫星 ====================

    # 地球卫星：月球 (Moon)
    MOON = CelestialBodyConfig(
        name="Moon",
        mass=3.6948e-8,
        semi_major_axis=0.002569,  # AU (~384,400 km)
        eccentricity=0.0549,
        inclination=5.145,
        color="#C0C0C0",
        primary="Earth"
    )

    # 火星卫星
    PHOBOS = CelestialBodyConfig(
        name="Phobos",
        mass=1.0659e-14,
        semi_major_axis=1.55e-5,  # AU (~9,376 km)
        eccentricity=0.0151,
        inclination=1.093,
        color="#8B7355",
        primary="Mars"
    )

    DEIMOS = CelestialBodyConfig(
        name="Deimos",
        mass=2.0933e-15,
        semi_major_axis=3.95e-5,  # AU (~23,463 km)
        eccentricity=0.0003,
        inclination=1.793,
        color="#A09070",
        primary="Mars"
    )

    # 木星卫星：伽利略卫星
    IO = CelestialBodyConfig(
        name="Io",
        mass=4.7079e-8,
        semi_major_axis=0.002819,  # AU (~421,700 km)
        eccentricity=0.0041,
        inclination=0.050,
        color="#FFFF99",
        primary="Jupiter"
    )

    EUROPA = CelestialBodyConfig(
        name="Europa",
        mass=2.5298e-8,
        semi_major_axis=0.004486,  # AU (~671,100 km)
        eccentricity=0.0094,
        inclination=0.470,
        color="#F0E68C",
        primary="Jupiter"
    )

    GANYMEDE = CelestialBodyConfig(
        name="Ganymede",
        mass=7.7818e-8,
        semi_major_axis=0.007178,  # AU (~1,070,400 km)
        eccentricity=0.0013,
        inclination=0.195,
        color="#C0C0C0",
        primary="Jupiter"
    )

    CALLISTO = CelestialBodyConfig(
        name="Callisto",
        mass=5.7626e-8,
        semi_major_axis=0.012529,  # AU (~1,882,700 km)
        eccentricity=0.0072,
        inclination=0.192,
        color="#808080",
        primary="Jupiter"
    )

    # 土星卫星
    TITAN = CelestialBodyConfig(
        name="Titan",
        mass=2.3665e-8,
        semi_major_axis=0.008168,  # AU (~1,221,870 km)
        eccentricity=0.0288,
        inclination=0.306,
        color="#DEB887",
        primary="Saturn"
    )

    ENCELADUS = CelestialBodyConfig(
        name="Enceladus",
        mass=1.9004e-10,
        semi_major_axis=0.000795,  # AU (~238,020 km)
        eccentricity=0.0047,
        inclination=0.019,
        color="#FFFFFF",
        primary="Saturn"
    )

    MIMAS = CelestialBodyConfig(
        name="Mimas",
        mass=7.3130e-11,
        semi_major_axis=0.000323,  # AU (~185,520 km)
        eccentricity=0.0202,
        inclination=1.537,
        color="#D3D3D3",
        primary="Saturn"
    )

    RHEA = CelestialBodyConfig(
        name="Rhea",
        mass=4.4163e-9,
        semi_major_axis=0.003543,  # AU (~527,040 km)
        eccentricity=0.0013,
        inclination=0.345,
        color="#C0C0C0",
        primary="Saturn"
    )

    # 天王星卫星
    TITANIA = CelestialBodyConfig(
        name="Titania",
        mass=7.6118e-10,
        semi_major_axis=0.002913,  # AU (~435,910 km)
        eccentricity=0.0011,
        inclination=0.340,
        color="#D8BFD8",
        primary="Uranus"
    )

    OBERON = CelestialBodyConfig(
        name="Oberon",
        mass=6.2559e-10,
        semi_major_axis=0.003839,  # AU (~583,520 km)
        eccentricity=0.0014,
        inclination=0.058,
        color="#C0C0C0",
        primary="Uranus"
    )

    ARIEL = CelestialBodyConfig(
        name="Ariel",
        mass=2.4841e-10,
        semi_major_axis=0.001911,  # AU (~190,900 km)
        eccentricity=0.0012,
        inclination=0.260,
        color="#E6E6FA",
        primary="Uranus"
    )

    UMBRIEL = CelestialBodyConfig(
        name="Umbriel",
        mass=2.2250e-10,
        semi_major_axis=0.002668,  # AU (~266,000 km)
        eccentricity=0.0039,
        inclination=0.205,
        color="#A9A9A9",
        primary="Uranus"
    )

    # 海王星卫星
    TRITON = CelestialBodyConfig(
        name="Triton",
        mass=1.0690e-7,
        semi_major_axis=0.002371,  # AU (~354,759 km)
        eccentricity=0.0000,
        inclination=156.885,  # 逆行轨道
        color="#FFC0CB",
        primary="Neptune"
    )
    # ==================== 矮行星 ====================

    # 谷神星 (Ceres) - 小行星带
    CERES = CelestialBodyConfig(
        name="Ceres",
        mass=4.72e-10,
        semi_major_axis=2.767,
        eccentricity=0.076,
        inclination=10.593,
        longitude_of_ascending_node=80.306,
        argument_of_pericenter=73.597,
        mean_anomaly=95.989,
        color="#8B8682"
    )

    # 冥王星 (Pluto)
    PLUTO = CelestialBodyConfig(
        name="Pluto",
        mass=1.30900e-8,
        semi_major_axis=39.482,
        eccentricity=0.2488,
        inclination=17.140,
        longitude_of_ascending_node=110.303,
        argument_of_pericenter=113.835,
        mean_anomaly=14.882,
        color="#9CA6B7"
    )

    # 厄里斯 (Eris)
    ERIS = CelestialBodyConfig(
        name="Eris",
        mass=1.6542e-8,
        semi_major_axis=67.89,
        eccentricity=0.4408,
        inclination=44.187,
        longitude_of_ascending_node=35.873,
        argument_of_pericenter=151.094,
        mean_anomaly=204.266,
        color="#E6E6FA"
    )

    # 妊神星 (Haumea)
    HAUMEA = CelestialBodyConfig(
        name="Haumea",
        mass=2.01e-8,
        semi_major_axis=43.34,
        eccentricity=0.191,
        inclination=28.22,
        longitude_of_ascending_node=122.19,
        argument_of_pericenter=239.28,
        mean_anomaly=16.54,
        color="#D3D3D3"
    )

    # 鸟神星 (Makemake)
    MAKEMAKE = CelestialBodyConfig(
        name="Makemake",
        mass=3.65e-8,
        semi_major_axis=45.79,
        eccentricity=0.159,
        inclination=28.96,
        longitude_of_ascending_node=145.81,
        argument_of_pericenter=85.92,
        mean_anomaly=5.64,
        color="#DEB887"
    )

    @classmethod
    def get_all_planets(cls) -> List[CelestialBodyConfig]:
        """获取所有八大行星"""
        return [
            cls.MERCURY, cls.VENUS, cls.EARTH, cls.MARS,
            cls.JUPITER, cls.SATURN, cls.URANUS, cls.NEPTUNE
        ]

    @classmethod
    def get_terrestrial_planets(cls) -> List[CelestialBodyConfig]:
        """获取类地行星（内行星）"""
        return [cls.MERCURY, cls.VENUS, cls.EARTH, cls.MARS]

    @classmethod
    def get_gas_giants(cls) -> List[CelestialBodyConfig]:
        """获取气态巨行星"""
        return [cls.JUPITER, cls.SATURN, cls.URANUS, cls.NEPTUNE]

    @classmethod
    def get_all_moons(cls) -> List[CelestialBodyConfig]:
        """获取所有主要卫星"""
        return [
            cls.MOON,  # 地球
            cls.PHOBOS, cls.DEIMOS,  # 火星
            cls.IO, cls.EUROPA, cls.GANYMEDE, cls.CALLISTO,  # 木星
            cls.TITAN, cls.ENCELADUS, cls.MIMAS, cls.RHEA,  # 土星
            cls.TITANIA, cls.OBERON, cls.ARIEL, cls.UMBRIEL,  # 天王星
            cls.TRITON  # 海王星
        ]

    @classmethod
    def get_galilean_moons(cls) -> List[CelestialBodyConfig]:
        """获取伽利略卫星（木星四大卫星）"""
        return [cls.IO, cls.EUROPA, cls.GANYMEDE, cls.CALLISTO]

    @classmethod
    def get_dwarf_planets(cls) -> List[CelestialBodyConfig]:
        """获取所有矮行星"""
        return [cls.CERES, cls.PLUTO, cls.ERIS, cls.HAUMEA, cls.MAKEMAKE]

    @classmethod
    def get_kuiper_belt_objects(cls) -> List[CelestialBodyConfig]:
        """获取柯伊伯带天体"""
        return [cls.PLUTO, cls.ERIS, cls.HAUMEA, cls.MAKEMAKE]

    @classmethod
    def get_by_name(cls, name: str) -> Optional[CelestialBodyConfig]:
        """根据名称获取天体配置"""
        all_bodies = (
            [cls.SUN] +
            cls.get_all_planets() +
            cls.get_all_moons() +
            cls.get_dwarf_planets()
        )
        for body in all_bodies:
            if body.name.lower() == name.lower():
                return body
        return None


def add_solar_system(
    sim: rebound.Simulation,
    include_sun: bool = True,
    include_planets: bool = True,
    include_moons: bool = False,
    include_dwarfs: bool = False
):
    """
    添加太阳系天体到模拟中

    Parameters:
    -----------
    sim : rebound.Simulation
        REBOUND 模拟对象
    include_sun : bool
        是否包含太阳
    include_planets : bool
        是否包含八大行星
    include_moons : bool
        是否包含主要卫星
    include_dwarfs : bool
        是否包含矮行星
    """
    db = SolarSystemBodies()

    # 添加太阳
    if include_sun:
        db.SUN.add_to_simulation(sim)

    # 添加行星
    if include_planets:
        for planet in db.get_all_planets():
            planet.add_to_simulation(sim)

    # 添加卫星（需要找到对应的主天体）
    if include_moons:
        # 按顺序添加卫星，映射主天体
        name_to_index = {
            "Earth": 3,  # 水星、金星、地球
            "Mars": 4,
            "Jupiter": 5,
            "Saturn": 6,
            "Uranus": 7,
            "Neptune": 8
        }

        moon_configs = db.get_all_moons()
        for moon in moon_configs:
            primary_name = moon.primary
            if primary_name in name_to_index:
                idx = name_to_index[primary_name]
                if idx < len(sim.particles):
                    primary_particle = sim.particles[idx]
                    moon.add_to_simulation(sim, primary_particle=primary_particle)

    # 添加矮行星
    if include_dwarfs:
        for dwarf in db.get_dwarf_planets():
            dwarf.add_to_simulation(sim)

    # 移动到质心系
    sim.move_to_com()


def add_planets_by_name(sim: rebound.Simulation, names: list, primary_map: dict = None):
    """
    根据名称列表添加天体到模拟中

    Parameters:
    -----------
    sim : rebound.Simulation
        REBOUND 模拟对象
    names : list
        天体名称列表
    primary_map : dict
        主天体映射字典，用于卫星（格式：{'Moon': sim.particles[3]}）
    """
    db = SolarSystemBodies()

    if primary_map is None:
        primary_map = {}

    for name in names:
        body = db.get_by_name(name)
        if body is not None:
            # 如果是卫星且提供了主天体映射
            if body.primary and body.name in primary_map:
                body.add_to_simulation(sim, primary_particle=primary_map[body.name])
            else:
                body.add_to_simulation(sim)
        else:
            print(f"警告：未找到天体 '{name}'")

    sim.move_to_com()
