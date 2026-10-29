"""
PROJECT 4 POST-PROCESSING
=========================

Creates:
1. Wheel and underbody geometry
2. Underbody velocity distribution
3. Underbody pressure distribution
4. Pressure coefficient distribution
5. Wheel surface velocity visualisation
6. Numerical CSV results
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from wheel_rotation import (
    calculate_angular_velocity,
    calculate_surface_velocity
)


def save_geometry_plot(cfg, geometry, output):

    X = geometry["X"]
    Y = geometry["Y"]
    solid = geometry["solid"]

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.contourf(
        X, Y, solid.astype(float),
        levels=[0.5, 1.5],
        colors=["grey"]
    )

    ax.set_title("Wheel and Underbody Geometry")
    ax.set_xlabel("Streamwise position [m]")
    ax.set_ylabel("Vertical position [m]")
    ax.set_aspect("equal")

    fig.tight_layout()
    fig.savefig(output / "geometry.png", dpi=200)
    plt.close(fig)


def save_underbody_plots(flow, output):

    # Velocity
    fig, ax = plt.subplots(figsize=(9, 4))

    ax.plot(
        flow["x"],
        flow["velocity"],
        linewidth=2,
        color="royalblue"
    )

    ax.set_title("Idealised Underbody Velocity Distribution")
    ax.set_xlabel("Streamwise position [m]")
    ax.set_ylabel("Velocity [m/s]")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(output / "underbody_velocity.png", dpi=200)
    plt.close(fig)

    # Pressure
    fig, ax = plt.subplots(figsize=(9, 4))

    ax.plot(
        flow["x"],
        flow["pressure"],
        linewidth=2,
        color="darkred"
    )

    ax.set_title("Idealised Underbody Static Pressure")
    ax.set_xlabel("Streamwise position [m]")
    ax.set_ylabel("Pressure [Pa]")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(output / "underbody_pressure.png", dpi=200)
    plt.close(fig)

    # Pressure coefficient
    fig, ax = plt.subplots(figsize=(9, 4))

    ax.plot(
        flow["x"],
        flow["pressure_coefficient"],
        linewidth=2,
        color="darkgreen"
    )

    ax.set_title("Underbody Pressure Coefficient")
    ax.set_xlabel("Streamwise position [m]")
    ax.set_ylabel("Pressure coefficient, Cp")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(output / "pressure_coefficient.png", dpi=200)
    plt.close(fig)


def save_wheel_velocity_plot(cfg, output):

    theta = np.linspace(0, 2 * np.pi, 100)

    radius = cfg.wheel_radius

    x = (
        cfg.wheel_center_x
        + radius * np.cos(theta)
    )

    y = (
        cfg.wheel_center_y
        + radius * np.sin(theta)
    )

    # For a road moving in +x, a freely rolling
    # wheel rotates clockwise in the stationary-car frame.
    omega = -calculate_angular_velocity(
        cfg.ground_velocity,
        radius,
        cfg.wheel_rotation_factor
    )

    vx, vy = calculate_surface_velocity(
        x,
        y,
        cfg.wheel_center_x,
        cfg.wheel_center_y,
        omega
    )

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.plot(x, y, color="black", linewidth=2)

    ax.quiver(
        x[::5],
        y[::5],
        vx[::5],
        vy[::5],
        color="royalblue",
        angles="xy",
        scale_units="xy",
        scale=100
    )

    ax.set_title("Rotating Wheel Surface Velocity")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(output / "wheel_rotation.png", dpi=200)
    plt.close(fig)


def save_results(cfg, geometry, flow, performance):

    output = (
        Path(__file__).resolve().parent
        / cfg.output_directory
    )

    output.mkdir(parents=True, exist_ok=True)

    save_geometry_plot(cfg, geometry, output)
    save_underbody_plots(flow, output)
    save_wheel_velocity_plot(cfg, output)

    # Save underbody numerical data
    df = pd.DataFrame({
        "x_m": flow["x"],
        "underbody_height_m": flow["height"],
        "velocity_m_s": flow["velocity"],
        "pressure_pa": flow["pressure"],
        "pressure_coefficient": flow["pressure_coefficient"]
    })

    df.to_csv(
        output / "underbody_results.csv",
        index=False
    )

    # Save summary
    with open(
        output / "summary.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write("PROJECT 4: WHEEL AND UNDERBODY STUDY\n")
        file.write("=====================================\n")

        file.write(
            f"Inlet velocity: {cfg.inlet_velocity:.3f} m/s\n"
        )

        file.write(
            f"Wheel radius: {cfg.wheel_radius:.3f} m\n"
        )

        file.write(
            f"Ground clearance: {cfg.ground_clearance:.3f} m\n"
        )

        file.write(
            f"Diffuser exit height: "
            f"{cfg.diffuser_exit_height:.3f} m\n"
        )

        file.write(
            f"Ideal outlet velocity: "
            f"{performance['outlet_velocity']:.3f} m/s\n"
        )

        file.write(
            f"Ideal pressure rise: "
            f"{performance['pressure_rise']:.3f} Pa\n"
        )

        file.write(
            f"Ideal pressure recovery coefficient: "
            f"{performance['pressure_recovery_coefficient']:.4f}\n"
        )

        file.write(
            "\nThese are reduced-order analytical estimates, "
            "not validated CFD predictions.\n"
        )

    print(f"Results saved to: {output}")
