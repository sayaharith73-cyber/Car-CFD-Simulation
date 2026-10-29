"""
VEHICLE GEOMETRY GENERATOR
==========================

Creates a 2D computational grid and simplified
rounded-rectangle vehicle geometry.

True  = vehicle solid
False = fluid
"""

import numpy as np


def create_geometry(cfg):

    x = np.linspace(0, cfg.domain_length, cfg.nx)
    y = np.linspace(0, cfg.domain_height, cfg.ny)

    dx = x[1] - x[0]
    dy = y[1] - y[0]

    X, Y = np.meshgrid(x, y)

    # Vehicle position
    cx = cfg.vehicle_x + cfg.vehicle_length / 2
    cy = cfg.vehicle_y

    half_length = cfg.vehicle_length / 2
    half_height = cfg.vehicle_height / 2

    # Rounded rectangle approximation
    radius = min(0.12 * cfg.vehicle_height, half_height)

    qx = np.abs(X - cx) - (half_length - radius)
    qy = np.abs(Y - cy) - (half_height - radius)

    outside = np.sqrt(
        np.maximum(qx, 0)**2
        + np.maximum(qy, 0)**2
    )

    inside = np.minimum(np.maximum(qx, qy), 0)

    distance = outside + inside - radius

    solid = distance <= 0

    return X, Y, x, y, dx, dy, solid


def save_geometry(cfg, solid):

    import matplotlib.pyplot as plt
    from pathlib import Path

    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)

    plt.figure(figsize=(12, 4))

    plt.imshow(
        solid,
        origin="lower",
        extent=[
            0, cfg.domain_length,
            0, cfg.domain_height
        ],
        aspect="auto",
        cmap="gray_r"
    )

    plt.xlabel("Streamwise distance [m]")
    plt.ylabel("Vertical distance [m]")
    plt.title("Vehicle Geometry and Computational Domain")

    plt.tight_layout()
    plt.savefig(output / "vehicle_geometry.png", dpi=200)
    plt.close()
