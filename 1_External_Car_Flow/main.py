"""
MAIN PROGRAM
============

Run this file to:
1. Load user settings.
2. Build the computational geometry.
3. Run the Lattice Boltzmann solver.
4. Save visualisations and numerical output.
"""

from config import CFDConfig, validate_config
from geometry import create_solid_mask
from solver import run_simulation
from postprocess import save_results


def main():
    print("=" * 55)
    print("AUTOMOTIVE AERODYNAMICS CFD")
    print("Project 1: External Flow Around a Simplified Body")
    print("=" * 55)

    # Step 1: Read and validate settings
    cfg = CFDConfig()
    validate_config(cfg)

    # Step 2: Create the geometry
    solid = create_solid_mask(cfg)

    print(f"Domain: {cfg.nx} x {cfg.ny} nodes")
    print(f"Solid nodes: {solid.sum()}")
    print(f"Fluid nodes: {(~solid).sum()}")

    # Step 3: Run the flow solver
    print("\nStarting simulation...")
    result = run_simulation(cfg, solid)

    # Step 4: Generate plots and save data
    save_results(cfg, result)

    print("\nSimulation finished.")
    print(
        "Note: this model does not predict validated "
        "real-car aerodynamic drag."
    )


if __name__ == "__main__":
    main()
