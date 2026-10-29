"""
MAIN PROGRAM
============

Project 2: Race-Car Aerodynamics

Run this file to:
1. Validate user inputs.
2. Generate an airfoil.
3. Calculate idealised lift and drag estimates.
4. Calculate diffuser pressure recovery.
5. Generate figures and CSV data.
"""

from config import WingConfig, validate_config

from aerodynamics import (
    calculate_coefficients,
    calculate_forces,
)

from diffuser import calculate_diffuser
from postprocess import save_all_plots


def main():

    print("=" * 60)
    print("PROJECT 2: RACE-CAR AERODYNAMICS")
    print("=" * 60)

    # ----------------------------------
    # 1. Load user inputs
    # ----------------------------------

    cfg = WingConfig()
    validate_config(cfg)

    # ----------------------------------
    # 2. Calculate wing coefficients
    # ----------------------------------

    cl, cd = calculate_coefficients(
        cfg.angle_of_attack
    )

    # Example reference span.
    # Change this to your selected wing span.
    wing_span = 1.5

    lift, drag = calculate_forces(
        cfg.air_density,
        cfg.velocity,
        cfg.chord,
        wing_span,
        cl,
        cd
    )

    # ----------------------------------
    # 3. Calculate diffuser performance
    # ----------------------------------

    diffuser = calculate_diffuser(
        inlet_area=0.20,
        outlet_area=0.35,
        inlet_velocity=cfg.velocity,
        density=cfg.air_density,
        inlet_pressure=cfg.static_pressure
    )

    # ----------------------------------
    # 4. Print results
    # ----------------------------------

    print("\nWING RESULTS")
    print("-" * 40)

    print(f"Airfoil: NACA {cfg.airfoil_code}")
    print(f"Freestream velocity: {cfg.velocity:.2f} m/s")
    print(f"Angle of attack: {cfg.angle_of_attack:.2f} degrees")
    print(f"Lift coefficient: {cl:.5f}")
    print(f"Drag coefficient: {cd:.5f}")
    print(f"Idealised lift: {lift:.3f} N")
    print(f"Modelled profile drag: {drag:.3f} N")

    print("\nDIFFUSER RESULTS")
    print("-" * 40)

    print(
        f"Outlet velocity: "
        f"{diffuser['outlet_velocity']:.3f} m/s"
    )

    print(
        f"Outlet pressure: "
        f"{diffuser['outlet_pressure']:.3f} Pa"
    )

    print(
        f"Ideal pressure recovery: "
        f"{diffuser['pressure_recovery']:.3f} Pa"
    )

    # ----------------------------------
    # 5. Generate figures
    # ----------------------------------

    save_all_plots(cfg)

    print("\nProject 2 completed.")
    print(
        "These are analytical estimates, not validated "
        "race-car CFD predictions."
    )


if __name__ == "__main__":
    main()
