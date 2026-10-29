"""
POST-PROCESSING AND VISUALISATION
=================================

Creates:
- Velocity magnitude contour
- Velocity streamlines
- Density variation contour
- Convergence history
- Compressed numerical output

Density variation is shown in lattice units. It is not a
calibrated pressure distribution in pascals.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def save_results(cfg, result):
    """Save the flow plots and numerical fields."""

    output = Path(__file__).resolve().parent / cfg.output_directory
    output.mkdir(parents=True, exist_ok=True)

    rho = result["rho"]
    ux = result["ux"]
    uy = result["uy"]
    solid = result["solid"]

    nx = cfg.nx
    ny = cfg.ny

    x = np.arange(nx)
    y = np.arange(ny)
    X, Y = np.meshgrid(x, y)

    speed = np.sqrt(ux**2 + uy**2)

    # Mask solid nodes so contours are not plotted inside the body.
    speed_plot = np.ma.masked_where(solid, speed)

    # ------------------------------------------
    # Figure 1: velocity magnitude
    # ------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 4))

    levels = np.linspace(0, max(float(speed.max()), 1e-12), 30)

    contour = ax.contourf(
        X, Y, speed_plot,
        levels=levels,
        cmap="turbo"
    )

    ax.set_title("Velocity Magnitude Around a Simplified Body")
    ax.set_xlabel("x [lattice nodes]")
    ax.set_ylabel("y [lattice nodes]")
    ax.set_aspect("equal")

    fig.colorbar(
        contour, ax=ax,
        label="Velocity magnitude [lattice units]"
    )

    fig.tight_layout()
    fig.savefig(output / "velocity_contour.png", dpi=200)

    # ------------------------------------------
    # Figure 2: streamlines
    # ------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 4))

    ux_plot = np.ma.masked_where(solid, ux)
    uy_plot = np.ma.masked_where(solid, uy)

    ax.streamplot(
        x, y, ux_plot, uy_plot,
        density=1.4,
        color=speed_plot,
        cmap="turbo",
        linewidth=0.8,
        arrowsize=0.7
    )

    ax.set_title("Flow Streamlines Around a Simplified Body")
    ax.set_xlabel("x [lattice nodes]")
    ax.set_ylabel("y [lattice nodes]")
    ax.set_aspect("equal")

    fig.tight_layout()
    fig.savefig(output / "streamlines.png", dpi=200)

    # ------------------------------------------
    # Figure 3: density variation
    # ------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 4))

    fluid = ~solid
    rho_reference = float(np.mean(rho[fluid]))
    density_variation = rho - rho_reference

    density_plot = np.ma.masked_where(
        solid, density_variation
    )

    limit = max(
        float(np.max(np.abs(density_variation[fluid]))),
        1e-12
    )

    contour = ax.contourf(
        X, Y, density_plot,
        levels=np.linspace(-limit, limit, 31),
        cmap="coolwarm",
        extend="both"
    )

    ax.set_title("Density Variation Relative to the Fluid Mean")
    ax.set_xlabel("x [lattice nodes]")
    ax.set_ylabel("y [lattice nodes]")
    ax.set_aspect("equal")

    fig.colorbar(
        contour, ax=ax,
        label="Density variation [lattice units]"
    )

    fig.tight_layout()
    fig.savefig(output / "density_variation.png", dpi=200)

    # ------------------------------------------
    # Figure 4: mean-velocity convergence history
    # ------------------------------------------
    history = result["history"]

    if len(history) > 0:
        fig, ax = plt.subplots(figsize=(7, 4))

        ax.plot(
            history[:, 0],
            history[:, 1],
            marker="o",
            markersize=3
        )

        ax.set_title("Mean Velocity Convergence History")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Mean streamwise velocity [lattice units]")
        ax.grid(True, alpha=0.3)

        fig.tight_layout()
        fig.savefig(output / "convergence.png", dpi=200)

    # ------------------------------------------
    # Save numerical fields
    # ------------------------------------------
    np.savez_compressed(
        output / "flow_fields.npz",
        rho=rho,
        ux=ux,
        uy=uy,
        solid=solid
    )

    # Save a plain-text simulation report
    with open(
        output / "summary.txt", "w", encoding="utf-8"
    ) as file:

        file.write("EXTERNAL FLOW SIMULATION REPORT\n")
        file.write("===============================\n")
        file.write("Method: D2Q9 Lattice Boltzmann, BGK\n")
        file.write("Units: lattice units\n")
        file.write("Domain: periodic in x, solid walls in y\n")
        file.write("Body: simplified rounded rectangle\n")
        file.write(f"Grid: {nx} x {ny}\n")
        file.write(f"Iterations: {result['iterations']}\n")
        file.write(f"Mean-velocity target met: {result['converged']}\n")
        file.write(
            f"Mean fluid density: {rho[fluid].mean():.8e}\n"
        )
        file.write(
            f"Maximum fluid speed: {speed[fluid].max():.8e}\n"
        )
        file.write(
            "Physical drag coefficient: NOT CALCULATED\n"
        )

    plt.close("all")

    print(f"\nResults saved to: {output}")
    print("Generated velocity, streamline and density plots.")
