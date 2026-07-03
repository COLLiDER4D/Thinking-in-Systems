# simulations/tub_simulation/scenarios.py

from .models import Pipe, Hole, Tub, Fluid, Environment
from .simulation import simulate_euler, simulate_rk4, simulate_scipy

def scenario_constant_inflow_euler():
    """
    Constant inflow, one outlet hole at bottom.
    Simulate with Euler method.
    """
    # Define models
    pipe = Pipe(diameter=0.05, flow_rate=0.001)  # 0.001 m^3/s inflow
    hole = Hole(diameter=0.02, height_from_bottom=0.0)
    tub = Tub(width=1.0, length=1.0, height=1.0, holes=[hole])
    fluid = Fluid()  # default water
    env = Environment()

    # Run simulation (e.g. 100 seconds, dt=0.1s)
    history = simulate_euler(tub, pipe, fluid, env, dt=0.1, total_time=100.0)
    return history

def scenario_overflow_test():
    """
    Inflow greater than max outflow: tub will overflow.
    """
    pipe = Pipe(diameter=0.05, flow_rate=0.01)  # large inflow
    hole = Hole(diameter=0.005, height_from_bottom=0.0)
    tub = Tub(width=0.5, length=0.5, height=0.5, holes=[hole])
    fluid = Fluid()
    env = Environment()

    history = simulate_rk4(tub, pipe, fluid, env, dt=0.05, total_time=30.0)
    return history

def scenario_variable_inlet_scipy():
    """
    Variable inflow: simulate on/off pulses using SciPy solver.
    """
    # We will simulate piecewise by splitting into segments
    # (Demonstration: this function shows approach, not run directly)
    pass  # Implementation depends on events; see SimPy example below

def scenario_multiple_holes_euler():
    """
    Two holes at different heights, constant inflow.
    """
    pipe = Pipe(diameter=0.05, flow_rate=0.002)
    hole1 = Hole(diameter=0.02, height_from_bottom=0.0)
    hole2 = Hole(diameter=0.015, height_from_bottom=0.3)
    tub = Tub(width=1.0, length=1.0, height=1.0, holes=[hole1, hole2])
    fluid = Fluid()
    env = Environment()

    history = simulate_euler(tub, pipe, fluid, env, dt=0.1, total_time=100.0)
    return history

# ... Add more scenarios as needed ...
