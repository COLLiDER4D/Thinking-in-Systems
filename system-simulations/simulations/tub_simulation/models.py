# simulations/tub_simulation/models.py

from dataclasses import dataclass, field
from typing import List

@dataclass
class Fluid:
    """
    Properties of the fluid.
    - density: mass density (kg/m^3)
    - viscosity: dynamic viscosity (Pa·s) [unused in ideal flow]
    """
    name: str = "Water"
    density: float = 1000.0       # kg/m^3 (water at ~20°C)
    viscosity: float = 0.001002   # Pa·s (ignored in basic sim)
    temperature: float = 20.0     # °C (not used in calculation here)

@dataclass
class Pipe:
    """
    Represents an inlet pipe or source of fluid.
    - diameter: pipe diameter (m).
    - flow_rate: volumetric inflow rate (m^3/s).
    - position_height: vertical position of pipe outlet (m above tub bottom).
    """
    diameter: float           # m (not directly used in simple model)
    flow_rate: float          # m^3/s
    position_height: float = 0.0  # If pipe height matters for stratification (ignored here)

@dataclass
class Hole:
    """
    Represents an outlet hole.
    - diameter: hole diameter (m).
    - height_from_bottom: vertical position of hole bottom (m above tub bottom).
      If zero, hole is at tub bottom.
    - discharge_coefficient: dimensionless (typically 0.6-0.62 for sharp-edged).
    - is_open: whether the hole is open (can be toggled).
    """
    diameter: float           # m
    height_from_bottom: float # m (hole height above tub bottom)
    discharge_coefficient: float = 0.62
    is_open: bool = True

@dataclass
class Tub:
    """
    Represents the container (tub).
    - width, length, height: dimensions (m).
      Volume capacity = width * length * height.
    - holes: list of Hole objects (outlets).
    """
    width: float              # m
    length: float             # m
    height: float             # m (max water height, i.e., tub depth)
    holes: List[Hole] = field(default_factory=list)

    @property
    def base_area(self) -> float:
        """Cross-sectional base area of tub (m^2)."""
        return self.width * self.length

    @property
    def capacity(self) -> float:
        """Maximum volume capacity of tub (m^3)."""
        return self.base_area * self.height

@dataclass
class Environment:
    """
    External conditions.
    - gravity: acceleration due to gravity (m/s^2).
    - atmospheric_pressure: (Pa) [not actively used, but could be].
    """
    gravity: float = 9.81            # m/s² (Earth gravity)
    atmospheric_pressure: float = 101325.0  # Pa

@dataclass
class SimulationState:
    """
    Represents the state at a point in time during simulation.
    - time: current simulation time (s).
    - water_volume: current water volume in tub (m^3).
    - water_height: current water height (m) -- can be derived, but we store for convenience.
    - inflow_rate: current inflow rate (m^3/s).
    - outflow_rate: current total outflow (m^3/s).
    - is_overflowing: flag if tub is full (volume >= capacity).
    """
    time: float = 0.0
    water_volume: float = 0.0
    water_height: float = 0.0
    inflow_rate: float = 0.0
    outflow_rate: float = 0.0
    is_overflowing: bool = False
