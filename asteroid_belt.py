import numpy as np
#kirkwood_gap小行星带
KIRKWOOD_GAPS = [
    (2.06, 0.03),
    (2.50, 0.04),
    (2.82, 0.04),
    (2.96, 0.03),
    (3.27, 0.04),
]

def in_kirkwood_gaps(a):
    for center, width in KIRKWOOD_GAPS:
        if np.abs(a - center) < 0.1:
            return True
    return False

def add_main_belt(sim, N=20000, primary=None, rng=None):
    if rng is None:
        rng = np.random.default_rng()

    added=0
    while added < N:
        a = rng.uniform(2.0, 3.4)
        if in_kirkwood_gaps(a):
            continue
        e = rng.uniform(0.0, 0.2)
        inc = rng.uniform(0.0, 0.25)

        sim.add(
            m=0,
            a=a,
            e=e,
            inc=inc,
            Omega=rng.uniform(0, 2 * np.pi),
            omega=rng.uniform(0, 2 * np.pi),
            f=rng.uniform(0, 2 * np.pi),
            primary=primary
        )
        added += 1
# Generate a dynamically evolved main asteroid belt
# with Kirkwood gaps already cleared by Jupiter resonances
def add_hilda_group(sim, N=3000, jupiter=None, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    centers = [0, 2 * np.pi / 3, 4 * np.pi / 3]
    for _ in range(N):
        a=rng.normal(3.97,0.05)
        e=rng.uniform(0.1, 0.31)
        inc = rng.uniform(0.0, 0.3)
        center=rng.choice(centers)
        f=center+rng.normal(0,0.2)
        sim.add(
            m=0,
            a=a,
            e=e,
            inc=inc,
            f=f,
            primary=jupiter
        )

def add_trojans(sim, N=5000, jupiter=None, rng=None):
    if rng is None:
        rng = np.random.default_rng()

    for _ in range(N):
        a = rng.normal(jupiter.a, 0.02)
        e = rng.uniform(0.0, 0.15)
        inc = rng.uniform(0.0, 0.35)

        # L4 / L5
        offset = rng.choice([np.pi/3, -np.pi/3])
        f = jupiter.f + offset + rng.normal(0, 0.2)

        sim.add(
            m=0,
            a=a,
            e=e,
            inc=inc,
            f=f,
            primary=jupiter
        )