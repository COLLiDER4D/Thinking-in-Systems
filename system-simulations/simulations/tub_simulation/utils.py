# simulations/tub_simulation/utils.py

import logging
from rich.table import Table
from rich.console import Console
from datetime import timedelta

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("tub_sim")

def volume_to_liters(m3: float) -> float:
    """Convert cubic meters to liters."""
    return m3 * 1000.0

def format_time(seconds: float) -> str:
    """Convert time in seconds to a human-readable H:M:S format."""
    return str(timedelta(seconds=seconds))

def print_state(state_table: Table, sim_state):
    """
    Add a row to a Rich Table given a SimulationState.
    Expects sim_state as a models.SimulationState instance.
    """
    state_table.add_row(
        f"{sim_state.time:.1f}",
        f"{sim_state.water_height:.3f}",
        f"{volume_to_liters(sim_state.water_volume):.1f}",
        f"{sim_state.inflow_rate:.3f}",
        f"{sim_state.outflow_rate:.3f}",
        "✅" if sim_state.is_overflowing else ""
    )

def configure_rich():
    """Configure rich console appearance (could add colors)."""
    console = Console()
    console.rule("[bold yellow]Tub Simulation[/bold yellow]")
    return console
