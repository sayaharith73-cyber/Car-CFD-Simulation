"""
VEHICLE WAKE POST-PROCESSING
============================

Produces:
1. Velocity magnitude contours
2. Streamline visualisation
3. Pressure distribution
4. Velocity deficit contours
5. Vorticity contours
6. Wake width CSV data
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from wake_analysis import analyse_wake


def save_results(cfg, result):

    output = Path(__file__).resolve().parent / "results"
    output.mkdir(parents=True, exist_ok=True)

    X = result["X"]
    Y = result["Y"]

    u = result["u"]
    v = result["v"]
    p = result["p"]
    solid = result["solid"]

    speed = np.sqrt(u**2 + v**2)

    speed_plot = np.ma.masked_where(solid, speed)
    pressure_plot = np.ma.masked_where(solid, p)

    analysis = analyse_wake(
        result,
        cfg.inlet_velocity,
        cfg.domain_length / (cfg.nx - 1),
        cfg.domain_height / (cfg.ny - 1)
    )

    # ---------------------------------------
    # 1. Velocity magnitude
    # ---------------------------------------

    fig, ax = plt.subplots(figsize=(12, 4))

    contour = ax.contourf(
        X, Y, speed_plot,
        levels=30,
        cmap="turbo"
    )

    ax.set_title("Vehicle Wake: Velocity Magnitude")
    ax.set_xlabel("Distance [m]")
    ax.set_ylabel("Height [m]")
    ax.set_aspect("equal")

    fig.colorbar(contour, ax=ax, label="Velocity [m/s]")

    fig.tight_layout()
    fig.savefig(output / "velocity_contour.png", dpi=200)
    plt.close(fig)

    # ---------------------------------------
    # 2. Streamlines
    # ---------------------------------------

    fig, ax = plt.subplots(figsize=(12, 4))

    u_plot = np.ma.masked_where(solid, u)
    v_plot = np.ma.masked_where(solid, v)

    ax.streamplot(
        result["x"],
        result["y"],
        u_plot,
        v_plot,
        density=1.5,
        color=speed_plot,
        cmap="turbo",
        linewidth=0.8
    )

    ax.set_title("Airflow Streamlines Behind Vehicle")
    ax.set_xlabel("Distance [m]")
    ax.set_ylabel("Height [m]")
    ax.set_aspect("equal")

    fig.tight_layout()
    fig.savefig(output / "streamlines.png", dpi=200)
    plt.close(fig)

    # ---------------------------------------
    # 3. Pressure contours
    # ---------------------------------------

    fig, ax = plt.subplots(figsize=(12, 4))

    contour = ax.contourf(
        X, Y, pressure_plot,
        levels=30,
        cmap="coolwarm"
    )

    ax.set_title("Computed Pressure Field")
    ax.set_xlabel("Distance [m]")
    ax.set_ylabel("Height [m]")
    ax.set_aspect("equal")

    fig.colorbar(contour, ax=ax, label="Pressure [Pa]")

    fig.tight_layout()
    fig.savefig(output / "pressure_contour.png", dpi=200)
    plt.close(fig)

    # ---------------------------------------
    # 4. Velocity deficit
    # ---------------------------------------

    fig, ax = plt.subplots(figsize=(12, 4))

    deficit_plot = np.ma.masked_invalid(
        analysis["deficit"]
    )

    contour = ax.contourf(
        X, Y, deficit_plot,
        levels=30,
        cmap="magma"
    )

    ax.set_title("Streamwise Velocity Deficit")
    ax.set_xlabel("Distance [m]")
    ax.set_ylabel("Height [m]")
    ax.set_aspect("equal")

    fig.colorbar(
        contour, ax=ax,
        label="Freestream velocity - local velocity [m/s]"
    )

    fig.tight_layout()
    fig.savefig(output / "velocity_deficit.png", dpi=200)
    plt.close(fig)

    # ---------------------------------------
    # 5. Vorticity
    # ---------------------------------------

    vorticity_plot = np.ma.masked_where(
        solid, analysis["vorticity"]
    )

    fig, ax = plt.subplots(figsize=(12, 4))

    limit = max(
        float(np.max(np.abs(analysis["vorticity"][~solid]))),
        1e-12
    )

    contour = ax.contourf(
        X, Y, vorticity_plot,
        levels=np.linspace(-limit, limit, 31),
        cmap="seismic",
        extend="both"
    )

    ax.set_title("Wake Vorticity Distribution")
    ax.set_xlabel("Distance [m]")
    ax.set_ylabel("Height [m]")
    ax.set_aspect("equal")

    fig.colorbar(
        contour, ax=ax,
        label="Vorticity [1/s]"
    )

    fig.tight_layout()
    fig.savefig(output / "vorticity.png", dpi=200)
    plt.close(fig)

    # ---------------------------------------
    # 6. Save numerical data
    # ---------------------------------------

    analysis["wake_stations"].to_csv(
        output / "wake_width.csv",
        index=False
    )

    np.savez_compressed(
        output / "wake_fields.npz",
        x=result["x"],
        y=result["y"],
        u=u,
        v=v,
        p=p,
        solid=solid,
        vorticity=analysis["vorticity"]
    )

    print(f"Results saved to: {output}")
