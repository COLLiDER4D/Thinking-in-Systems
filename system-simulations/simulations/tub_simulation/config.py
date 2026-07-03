# simulations/tub_simulation/config.py

from pydantic import BaseModel, Field
import pathlib

class SimulationConfig(BaseModel):
    """
    Configuration parameters for the simulation.
    These can be loaded from a file or environment if needed.
    """
    # Time settings
    time_step: float = Field(0.1, description="Simulation time step (s)")
    total_time: float = Field(100.0, description="Total simulation time (s)")
    output_interval: float = Field(1.0, description="Interval for recording output (s)")

    # Environment
    gravity: float = Field(9.81, description="Acceleration due to gravity (m/s^2)")

    # Tub initial conditions
    initial_water_height: float = Field(0.0, description="Starting water height (m)")
    initial_water_volume: float = Field(0.0, description="Starting water volume (m^3)")
    
    # (Optional) path to external config file
    # config_file: pathlib.Path = None
