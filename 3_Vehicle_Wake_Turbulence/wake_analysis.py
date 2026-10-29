"""
VEHICLE WAKE ANALYSIS
=====================

Extracts wake characteristics from the computed velocity field.

Outputs:
- Streamwise velocity deficit
- Wake width
- Vorticity
- Wake profile data
"""

import numpy as np
import pandas as pd


def calculate_vorticity(u, v, dx, dy):

    dv_dx = np.gradient(v, dx, axis=1)
    du_dy = np.gradient(u, dy, axis=0)

    return dv_dx - du_dy


def calculate_velocity_deficit(u, solid, inlet_velocity):

    deficit = inlet_velocity - u

    # Ignore solid nodes
    deficit = np.where(solid, np.nan, deficit)

    return deficit


def calculate_wake_width(
    y,
    velocity_profile,
    inlet_velocity,
    threshold=0.95
):
    """
    Estimate the width of the region where streamwise
    velocity is below a chosen fraction of freestream velocity.

    This is a threshold-based wake-width indicator.
    """

    wake_mask = velocity_profile < threshold * inlet_velocity

    if not np.any(wake_mask):
        return 0.0

    wake_positions = y[wake_mask]

    return float(wake_positions.max() - wake_positions.min())


def analyse_wake(result, inlet_velocity, dx, dy):

    u = result["u"]
    v = result["v"]
    solid = result["solid"]

    x = result["x"]
    y = result["y"]

    deficit = calculate_velocity_deficit(
        u, solid, inlet_velocity
    )

    vorticity = calculate_vorticity(u, v, dx, dy)

    # Find the downstream edge of the vehicle.
    vehicle_columns = np.where(solid.any(axis=0))[0]

    if len(vehicle_columns) == 0:
        raise ValueError("Vehicle geometry was not found.")

    vehicle_end_x = vehicle_columns.max()

    # Choose several downstream measurement stations.
    stations = np.linspace(
        vehicle_end_x + 2,
        len(x) - 3,
        5,
        dtype=int
    )

    rows = []

    for station in stations:

        profile = u[:, station]

        valid = ~solid[:, station]

        wake_width = calculate_wake_width(
            y[valid],
            profile[valid],
            inlet_velocity
        )

        rows.append({
            "x_m": x[station],
            "wake_width_m": wake_width,
            "maximum_velocity_deficit_m_s": float(
                np.nanmax(deficit[:, station])
            )
        })

    return {
        "deficit": deficit,
        "vorticity": vorticity,
        "wake_stations": pd.DataFrame(rows)
    }
