"""
RACE-CAR AERODYNAMICS POST-PROCESSING
=====================================

Creates figures and CSV files for the GitHub project.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from airfoil import generate_naca4
from aerodynamics import calculate_coefficients


def save_airfoil_plot(cfg, output):
    """Plot the generated airfoil geometry."""

    xu, yu, xl, yl = generate_naca4(
        cfg.airfoil_code,
        cfg.chord
    )

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(xu, yu, label="Upper surface")
    ax.plot(xl, yl, label="Lower surface")

    ax.set_title(f"NACA {cfg.airfoil_code} Airfoil")
    ax.set_xlabel("Chordwise position [m]")
    ax.set_ylabel("Vertical position [m]")
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(output / "airfoil_geometry.png", dpi=200)
    plt.close(fig)


def save_lift_curve(output):
    """Generate a thin-airfoil lift curve."""

    angles = np.linspace(-10, 10, 81)

    coefficients = [
        calculate_coefficients(angle)[0]
        for angle in angles
    ]

    data = pd.DataFrame({
        "angle_of_attack_deg": angles,
        "lift_coefficient": coefficients
    })

    data.to_csv(output / "lift_curve.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(angles, coefficients, linewidth=2)

    ax.set_title("Idealised Lift Coefficient vs Angle of Attack")
    ax.set_xlabel("Angle of attack [degrees]")
    ax.set_ylabel("Lift coefficient, CL")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(output / "lift_curve.png", dpi=200)
    plt.close(fig)


def save_diffuser_plot(cfg, output):
    """Plot idealised diffuser pressure recovery."""

    area_ratios = np.linspace(1.0, 2.5, 50)

    inlet_area = 0.2
    inlet_velocity = cfg.velocity
    density = cfg.air_density
    inlet_pressure = cfg.static_pressure

    outlet_velocities = inlet_velocity / area_ratios

    outlet_pressures = (
        inlet_pressure
        + 0.5 * density
        * (inlet_velocity**2 - outlet_velocities**2)
    )

    pressure_rise = outlet_pressures - inlet_pressure

    data = pd.DataFrame({
        "area_ratio": area_ratios,
        "outlet_velocity_m_s": outlet_velocities,
        "ideal_pressure_recovery_pa": pressure_rise
    })

    data.to_csv(output / "diffuser_results.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(area_ratios, pressure_rise, linewidth=2)

    ax.set_title("Idealised Diffuser Pressure Recovery")
    ax.set_xlabel("Outlet / inlet area ratio")
    ax.set_ylabel("Static pressure rise [Pa]")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(output / "diffuser_pressure_recovery.png", dpi=200)
    plt.close(fig)


def save_all_plots(cfg):
    """Create the complete output directory and figures."""

    output = Path(__file__).resolve().parent / cfg.output_directory
    output.mkdir(parents=True, exist_ok=True)

    save_airfoil_plot(cfg, output)
    save_lift_curve(output)
    save_diffuser_plot(cfg, output)

    print(f"Figures and CSV files saved in: {output}")
