# tests/test_tub.py
import math
from simulations.tub_simulation.physics import volume_to_height, height_to_volume, outflow_rate_by_height
from simulations.tub_simulation.models import Tub, Hole, Fluid, Environment

def test_volume_height_conversion():
    # Create a tub 1m x 1m base, height 2m
    tub = Tub(width=1.0, length=1.0, height=2.0, holes=[])
    # Volume 1 m^3 should give height 1m
    assert math.isclose(volume_to_height(1.0, tub), 1.0)
    # Volume 0.5 m^3 -> height 0.5m
    assert math.isclose(volume_to_height(0.5, tub), 0.5)
    # Height to volume
    assert math.isclose(height_to_volume(1.0, tub), 1.0)
    assert math.isclose(height_to_volume(0.5, tub), 0.5)

def test_outflow_rate_single_hole():
    tub = Tub(width=1.0, length=1.0, height=1.0, holes=[])
    hole = Hole(diameter=0.1, height_from_bottom=0.0, discharge_coefficient=1.0)
    tub.holes = [hole]
    fluid = Fluid(density=1000.0)
    env = Environment(gravity=9.81)
    # For height = 1.0 m, velocity = sqrt(2*9.81*1) ~ 4.429 m/s
    area = math.pi * (0.1/2)**2
    expected_Q = area * math.sqrt(2 * env.gravity * 1.0)  # C_d=1
    Q = outflow_rate_by_height(1.0, tub.holes, fluid, env.gravity)
    assert math.isclose(Q, expected_Q, rel_tol=1e-3)

def test_outflow_rate_below_hole():
    hole = Hole(diameter=0.1, height_from_bottom=0.5, discharge_coefficient=1.0)
    tub = Tub(width=1, length=1, height=2, holes=[hole])
    fluid = Fluid(density=1000.0)
    env = Environment(gravity=9.81)
    # Height below hole height: no flow
    Q = outflow_rate_by_height(0.4, tub.holes, fluid, env.gravity)
    assert math.isclose(Q, 0.0, abs_tol=1e-9)
    # Height above: positive flow
    Q2 = outflow_rate_by_height(0.6, tub.holes, fluid, env.gravity)
    assert Q2 > 0.0

def test_capacity_and_overflow():
    hole = Hole(diameter=0.1, height_from_bottom=0.0)
    tub = Tub(width=1, length=1, height=1, holes=[hole])
    # Capacity = 1 m^3
    assert tub.capacity == 1.0
    # If volume exceeds capacity, it should be clamped (tested via simulate functions)
    # We simulate a quick scenario: (not writing full sim, but checking capacity)
    from simulations.tub_simulation.physics import clamp_volume
    assert clamp_volume(1.5, tub) == 1.0
    assert clamp_volume(-0.1, tub) == 0.0
