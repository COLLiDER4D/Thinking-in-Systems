# simulations/tub_simulation/simulation.py
from typing import List
from .models import SimulationState, Tub, Pipe, Hole, Fluid, Environment
from .physics import volume_to_height, outflow_rate_by_height, clamp_volume, inflow_rate

def simulate_euler(tub: Tub, pipe: Pipe, fluid: Fluid, env: Environment,
                   dt: float, total_time: float) -> List[SimulationState]:
    """
    Run the simulation using explicit Euler integration.
    Returns a list of SimulationState at each time step.
    """
    # Initialize state
    state = SimulationState()
    state.water_volume = 0.0
    state.water_height = 0.0
    state.inflow_rate = pipe.flow_rate

    history: List[SimulationState] = []
    time = 0.0

    while time <= total_time + 1e-9:
        # Record current state
        state.time = time
        history.append(SimulationState(**state.__dict__))
        # Calculate flows
        Q_in = inflow_rate(pipe.flow_rate)
        # Current water height (for outflow calc)
        h = volume_to_height(state.water_volume, tub)
        Q_out = outflow_rate_by_height(h, tub.holes, fluid, env.gravity)
        # Update rates in state
        state.inflow_rate = Q_in
        state.outflow_rate = Q_out
        # Compute volume change
        dV = (Q_in - Q_out) * dt
        state.water_volume = state.water_volume + dV
        # Handle overflow/empty
        if state.water_volume > tub.capacity:
            state.is_overflowing = True
        state.water_volume = clamp_volume(state.water_volume, tub)
        state.water_height = volume_to_height(state.water_volume, tub)
        # Increment time
        time += dt

    return history

def simulate_rk4(tub: Tub, pipe: Pipe, fluid: Fluid, env: Environment,
                 dt: float, total_time: float) -> List[SimulationState]:
    """
    Run the simulation using 4th-order Runge-Kutta integration for dV/dt.
    Returns a list of SimulationState at each dt.
    """
    # Helper: compute derivative dV/dt at given volume
    def dV_dt(volume):
        h = volume_to_height(volume, tub)
        Qin = pipe.flow_rate
        Qout = outflow_rate_by_height(h, tub.holes, fluid, env.gravity)
        return Qin - Qout

    state = SimulationState()
    state.water_volume = 0.0
    state.water_height = 0.0
    state.inflow_rate = pipe.flow_rate

    history: List[SimulationState] = []
    time = 0.0

    while time <= total_time + 1e-9:
        # Record state
        state.time = time
        history.append(SimulationState(**state.__dict__))
        # RK4 steps to compute next volume
        V = state.water_volume
        k1 = dV_dt(V)
        k2 = dV_dt(V + 0.5 * dt * k1)
        k3 = dV_dt(V + 0.5 * dt * k2)
        k4 = dV_dt(V + dt * k3)
        V_next = V + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)
        # Update state
        state.water_volume = V_next
        if state.water_volume > tub.capacity:
            state.is_overflowing = True
        state.water_volume = clamp_volume(state.water_volume, tub)
        state.water_height = volume_to_height(state.water_volume, tub)
        state.inflow_rate = pipe.flow_rate
        state.outflow_rate = outflow_rate_by_height(state.water_height, tub.holes, fluid, env.gravity)
        # Increment time
        time += dt

    return history