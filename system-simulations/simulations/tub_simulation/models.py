from dataclasses import dataclass, field
from typing import List


@dataclass
class Fluid:
    """Properties of the fluid."""
    name: str = "Water"
    density: float = 1000.0          # kg/m^3
    viscosity: float = 0.001         # Pa·s
    temperature: float = 20.0        # °C


@dataclass
class Pipe:
    """Represents an inlet pipe."""
    diameter: float                  # m
    flow_rate: float                 # m^3/s
    position_height: float = 0.0     # m


@dataclass
class Hole:
    """Represents an outlet hole."""
    diameter: float                  # m
    height_from_bottom: float        # m
    discharge_coefficient: float = 0.62
    is_open: bool = True


@dataclass
class Tub:
    """Represents the container."""
    width: float                     # m
    length: float                    # m
    height: float                    # m
    holes: List[Hole] = field(default_factory=list)

    @property
    def base_area(self) -> float:
        return self.width * self.length

    @property
    def capacity(self) -> float:
        return self.base_area * self.height


@dataclass
class Environment:
    """Environmental conditions."""
    gravity: float = 9.81            # m/s²
    atmospheric_pressure: float = 101325.0  # Pa


@dataclass
class SimulationState:
    """Current state of the simulation."""
    time: float = 0.0                # s
    water_volume: float = 0.0        # m^3
    water_height: float = 0.0        # m
    inflow_rate: float = 0.0         # m^3/s
    outflow_rate: float = 0.0        # m^3/s
    is_overflowing: bool = False