"""
MAIN PROGRAM
============

Project 4: Wheel and Underbody Aerodynamics

Workflow:
1. Load user settings.
2. Validate configuration.
3. Generate wheel and underbody geometry.
4. Calculate wheel rotation.
5. Calculate underbody flow.
6. Calculate diffuser performance.
7. Generate visualisations.
8. Save numerical results.
"""

from config import CFDConfig, validate_config

from geometry import create_geometry

from wheel_rotation import calculate_wheel_parameters

from underbody import (
    calculate_underbody_flow,
    calculate_diffuser_performance
)

from postprocess import save_results


def main():

    print("=" * 65)
    print("PROJECT 4: WHEEL AND UNDERBODY AERODYNAMICS")
    print("=" * 65)

    # ----------------------------------
    # 1. Load configuration
    # ----------------------------------

    cfg = CFDConfig()

    validate_config(cfg)

    # ----------------------------------
    # 2. Calculate Reynolds number
    # ----------------------------------

    kinematic_viscosity = (
        cfg.dynamic_viscosity / cfg.air_density
    )

    reynolds_number = (
        cfg.air_density
        * cfg.inlet_velocity
        * (2 * cfg.wheel_radius)
        / cfg.dynamic_viscosity
    )

    print("\nFLOW CONDITIONS")
    print("-" * 45)

    print(f"Freestream velocity: {cfg.inlet_velocity:.3f} m/s")
    print(f"Air density: {cfg.air_density:.4f} kg/m3")

    print(
        f"Kinematic viscosity: "
        f"{kinematic_viscosity:.6e} m2/s"
    )

    print(f"Wheel Reynolds number: {reynolds_number:.3e}")

    # ----------------------------------
    # 3. Wheel rotational parameters
    # ----------------------------------

    wheel = calculate_wheel_parameters(cfg)

    print("\nWHEEL PARAMETERS")
    print("-" * 45)

    print(
        f"Angular velocity: "
        f"{wheel['angular_velocity_rad_s']:.3f} rad/s"
    )

    print(
        f"Wheel speed: "
        f"{wheel['rotation_rpm']:.2f} RPM"
    )

    print(
        f"Peripheral velocity: "
        f"{wheel['peripheral_speed_m_s']:.3f} m/s"
    )

    # ----------------------------------
    # 4. Generate geometry
    # ----------------------------------

    geometry = create_geometry(cfg)

    print("\nGEOMETRY GENERATED")

    # ----------------------------------
    # 5. Underbody flow calculation
    # ----------------------------------

    flow = calculate_underbody_flow(cfg)

    performance = calculate_diffuser_performance(cfg)

    print("\nUNDERBODY RESULTS")
    print("-" * 45)

    print(
        f"Outlet velocity: "
        f"{performance['outlet_velocity']:.3f} m/s"
    )

    print(
        f"Pressure rise: "
        f"{performance['pressure_rise']:.3f} Pa"
    )

    print(
        f"Pressure recovery coefficient: "
        f"{performance['pressure_recovery_coefficient']:.4f}"
    )

    # ----------------------------------
    # 6. Save results
    # ----------------------------------

    save_results(
        cfg,
        geometry,
        flow,
        performance
    )

    print("\nPROJECT 4 COMPLETED")

    print(
        "\nNOTE: The current version combines wheel "
        "kinematics, geometry visualisation and an "
        "idealised one-dimensional underbody model. "
        "It does not solve the coupled airflow around "
        "the wheel and vehicle."
    )


if __name__ == "__main__":
    main()
