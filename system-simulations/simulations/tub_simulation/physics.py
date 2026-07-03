# simulations/tub_simulation/physics.py

import math
from typing import List
from .models import Fluid, Hole, Tub, SimulationState

def volume_to_height(volume: float, tub: Tub) -> float:
    """
    Convert water volume to height (assuming uniform cross-section).
    h = V / A, capped by tub height.
    """
    if tub.base_area <= 0:
        raise ValueError("Tub base area must be positive")
    height = volume / tub.base_area
    # Don't exceed the physical height of the tub
    return min(height, tub.height)

def height_to_volume(height: float, tub: Tub) -> float:
    """
    Convert water height to volume: V = A * h.
    """
    if height < 0:
        return 0.0
    return tub.base_area * height

def inflow_rate(pipe_flow_rate: float) -> float:
    """
    Returns the inflow rate (could be time-dependent or constant).
    Here it's a constant flow given by the pipe.
    """
    return pipe_flow_rate

def outflow_rate(volume: float, holes: List[Hole], fluid: Fluid, gravity: float) -> float:
    """
    Calculate total outflow through all open holes given current water volume.
    Uses Torricelli's law: Q = C_d * A_h * sqrt(2 g h_eff).
    If water height is below a hole's height, that hole is inactive.
    """
    if volume <= 0:
        return 0.0
    total_Q = 0.0
    # Compute current water height
    # We assume one tub is in context; use any hole's tub via height formula
    # (Actually, tubs share the same base area concept)
    # We approximate by asking user to provide tub context if needed.
    # Here, for simplicity, assume holes know tub height indirectly (all holes share tub area).
    # Alternatively, call this function with height directly.
    # For clarity, we compute height outside and pass in instead in simulation.
    # So we will use a modified version below that takes height instead of volume.
    raise NotImplementedError("Use outflow_rate_by_height(height, holes, fluid, gravity).")

def outflow_rate_by_height(height: float, holes: List[Hole], fluid: Fluid, gravity: float) -> float:
    """
    Calculate total outflow given water height.
    Summation of Q = C_d * A * sqrt(2*g*(h - hole_height)).
    """
    Q_total = 0.0
    for hole in holes:
        if not hole.is_open:
            continue
        # Effective head for this hole:
        effective_h = height - hole.height_from_bottom
        if effective_h <= 0:
            # Water not reaching this hole
            continue
        # Area of the hole:
        area = math.pi * (hole.diameter/2)**2
        # Torricelli velocity: sqrt(2 g h)
        velocity = math.sqrt(2 * gravity * effective_h)
        # Flow rate through this hole:
        Q = hole.discharge_coefficient * area * velocity
        Q_total += Q
    return Q_total

def pressure_at_depth(height: float, fluid: Fluid, gravity: float) -> float:
    """
    Hydrostatic pressure at given depth h: P = rho * g * h.
    """
    return fluid.density * gravity * height

def clamp_volume(volume: float, tub: Tub) -> float:
    """
    Ensure volume stays between 0 and capacity.
    """
    if volume < 0:
        return 0.0
    return min(volume, tub.capacity)
