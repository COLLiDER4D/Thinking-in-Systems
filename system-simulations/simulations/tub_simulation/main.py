# simulations/tub_simulation/main.py

import argparse
from .config import SimulationConfig
from .models import Pipe, Hole, Tub, Fluid, Environment
from .simulation import simulate_euler, simulate_rk4
from .utils import format_time, volume_to_liters, print_state, configure_rich
from rich.table import Table

def main():
    parser = argparse.ArgumentParser(description="Tub Flow Simulation")
    parser.add_argument("--method", choices=["euler", "rk4"], default="euler",
                        help="Numerical integration method")
    parser.add_argument("--scenario", choices=["constant", "overflow", "multiple"], default="constant",
                        help="Scenario to simulate")
    args = parser.parse_args()

    # Load default config
    config = SimulationConfig()

    # Setup models based on scenario
    if args.scenario == "constant":
        pipe = Pipe(diameter=0.05, flow_rate=0.001)
        hole = Hole(diameter=0.02, height_from_bottom=0.0)
        tub = Tub(width=1.0, length=1.0, height=1.0, holes=[hole])
    elif args.scenario == "overflow":
        pipe = Pipe(diameter=0.05, flow_rate=0.01)
        hole = Hole(diameter=0.005, height_from_bottom=0.0)
        tub = Tub(width=0.5, length=0.5, height=0.5, holes=[hole])
    elif args.scenario == "multiple":
        pipe = Pipe(diameter=0.05, flow_rate=0.002)
        hole1 = Hole(diameter=0.02, height_from_bottom=0.0)
        hole2 = Hole(diameter=0.015, height_from_bottom=0.3)
        tub = Tub(width=1.0, length=1.0, height=1.0, holes=[hole1, hole2])
    else:
        raise ValueError("Unknown scenario")

    fluid = Fluid()
    env = Environment(gravity=config.gravity)

    # Run simulation
    if args.method == "euler":
        history = simulate_euler(tub, pipe, fluid, env, dt=config.time_step, total_time=config.total_time)
    elif args.method == "rk4":
        history = simulate_rk4(tub, pipe, fluid, env, dt=config.time_step, total_time=config.total_time)
    else:
        raise ValueError("Unknown method")

    # Prepare table for output
    console = configure_rich()
    table = Table(title="Simulation Results")
    table.add_column("Time (s)", style="cyan")
    table.add_column("Height (m)", style="blue")
    table.add_column("Volume (L)", style="blue")
    table.add_column("Inflow (m³/s)", style="green")
    table.add_column("Outflow (m³/s)", style="red")
    table.add_column("Overflow", style="yellow")

    for state in history[::int(config.output_interval/config.time_step)]:
        print_state(table, state)
        
        # This prints every output_interval seconds; adjust as needed

    console.print(table)

    # Optionally: plot results with matplotlib (not shown here for brevity)
    console.print(f"\nSimulation completed at t = {format_time(history[-1].time)}")
    if history[-1].is_overflowing:
        console.print("[bold red]Overflow occurred![/bold red]")

if __name__ == "__main__":
    main()
