"""
MAIN PROGRAM
============

Project 3: Vehicle Wake and Turbulence

Execution sequence:
1. Load user configuration.
2. Generate vehicle geometry.
3. Run the numerical solver.
4. Analyse the vehicle wake.
5. Generate visualisations and output files.
"""

from config import CFDConfig, validate_config
from geometry import create_geometry, save_geometry
from solver import run_simulation
from postprocess import save_results


def main():

    print("=" * 60)
    print("PROJECT 3: VEHICLE WAKE ANALYSIS")
    print("=" * 60)

    # Step 1: Load and validate inputs
    cfg = CFDConfig()
    validate_config(cfg)

    # Step 2: Calculate physical parameters
    nu = cfg.dynamic_viscosity / cfg.density

    reynolds_number = (
        cfg.inlet_velocity * cfg.vehicle_length / nu
    )

    dx = cfg.domain_length / (cfg.nx - 1)
    dy = cfg.domain_height / (cfg.ny - 1)

    print("\nFLOW CONDITIONS")
    print("-" * 40)
    print(f"Inlet velocity: {cfg.inlet_velocity:.3f} m/s")
    print(f"Air density: {cfg.density:.4f} kg/m3")
    print(f"Kinematic viscosity: {nu:.6e} m2/s")
    print(f"Vehicle Reynolds number: {reynolds_number:.3e}")
    print(f"Grid spacing dx: {dx:.5f} m")
    print(f"Grid spacing dy: {dy:.5f} m")

    # Step 3: Generate geometry
    geometry = create_geometry(cfg)

    save_geometry(cfg, geometry[-1])

    print("\nVehicle geometry created.")

    # Step 4: Run solver
    print("\nStarting numerical simulation...")

    result = run_simulation(cfg, geometry)

    # Step 5: Generate results
    save_results(cfg, result)

    print("\nSimulation finished.")
    print("Check the results folder for figures and data.")

    print(
        "\nIMPORTANT: This educational laminar solver "
        "does not resolve realistic turbulent vehicle wakes."
    )


if __name__ == "__main__":
    main()
