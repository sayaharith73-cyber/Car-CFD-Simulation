"""
WHEEL AND UNDERBODY GEOMETRY
============================

Generates:
- Computational grid
- Circular wheel geometry
- Ground surface
- Simplified underbody profile
"""

import numpy as np


def create_geometry(cfg):

    x = np.linspace(0, cfg.domain_length, cfg.nx)
    y = np.linspace(0, cfg.domain_height, cfg.ny)

    X, Y = np.meshgrid(x, y)

    # Wheel geometry
    wheel_distance = np.sqrt(
        (X - cfg.wheel_center_x)**2
        + (Y - cfg.wheel_center_y)**2
    )

    wheel_solid = wheel_distance <= cfg.wheel_radius

    # Ground boundary
    ground_solid = Y <= 0.0

    # Underbody profile:
    # A simplified horizontal floor followed by a diffuser.
    diffuser_start = (
        cfg.domain_length - cfg.diffuser_length
    )

    diffuser_fraction = np.clip(
        (X - diffuser_start) / cfg.diffuser_length,
        0.0,
        1.0
    )

    underbody_height = (
        cfg.inlet_underbody_height
        + diffuser_fraction
        * (
            cfg.diffuser_exit_height
            - cfg.inlet_underbody_height
        )
    )

    underbody_solid = (
        (X >= 0.5)
        & (X <= cfg.domain_length)
        & (Y >= underbody_height)
        & (Y <= underbody_height + 0.04)
    )

    solid = wheel_solid | ground_solid | underbody_solid

    return {
        "x": x,
        "y": y,
        "X": X,
        "Y": Y,
        "wheel_solid": wheel_solid,
        "ground_solid": ground_solid,
        "underbody_solid": underbody_solid,
        "solid": solid,
        "underbody_height": underbody_height
    }
