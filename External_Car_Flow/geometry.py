"""
GEOMETRY GENERATION
===================

Creates a two-dimensional domain containing a rounded,
car-like obstacle.

This is a simplified geometric test body, not a realistic
automotive CAD model.
"""

import numpy as np


def create_solid_mask(cfg):
    """
    Return a Boolean array of shape (ny, nx).

    True  = solid wall or body
    False = fluid

    The domain is periodic in the x direction.
    The top and bottom rows are stationary walls.
    """

    x = np.arange(cfg.nx)
    y = np.arange(cfg.ny)

    X, Y = np.meshgrid(x, y)

    # Stationary channel walls
    solid = np.zeros((cfg.ny, cfg.nx), dtype=bool)
    solid[0, :] = True
    solid[-1, :] = True

    # Body centre
    centre_x = cfg.body_x_fraction * (cfg.nx - 1)
    centre_y = (cfg.ny - 1) / 2.0

    # Distance from the body centre
    dx = np.abs(X - centre_x)
    dy = np.abs(Y - centre_y)

    half_length = cfg.body_length / 2.0
    half_height = cfg.body_height / 2.0
    radius = cfg.body_corner_radius

    # Rounded-rectangle signed-distance calculation
    qx = dx - (half_length - radius)
    qy = dy - (half_height - radius)

    outside_x = np.maximum(qx, 0.0)
    outside_y = np.maximum(qy, 0.0)

    outside_distance = np.sqrt(
        outside_x**2 + outside_y**2
    )

    inside_distance = np.minimum(
        np.maximum(qx, qy), 0.0
    )

    signed_distance = (
        outside_distance + inside_distance - radius
    )

    body = signed_distance <= 0.0

    # Prevent the body from occupying the stationary walls.
    # The geometry should have fluid clearance above and below.
    if np.any(body[0, :]) or np.any(body[-1, :]):
        raise ValueError(
            "The body intersects a domain wall. "
            "Reduce body_height or increase ny."
        )

    solid |= body

    # Check that the body is completely inside the domain
    body_nodes = np.where(body)

    if len(body_nodes[1]) == 0:
        raise ValueError(
            "No body nodes were created. Check geometry settings."
        )

    if body_nodes[1].min() <= 1 or body_nodes[1].max() >= cfg.nx - 2:
        raise ValueError(
            "The body is too close to the periodic domain boundary."
        )

    return solid
