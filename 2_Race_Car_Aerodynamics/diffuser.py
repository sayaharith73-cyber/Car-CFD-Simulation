"""
SIMPLIFIED DIFFUSER MODEL
=========================

One-dimensional, incompressible, inviscid diffuser calculation.

This is NOT a three-dimensional underbody CFD solver.
It does not predict separation or diffuser stall.
"""

import numpy as np


def calculate_diffuser(
    inlet_area,
    outlet_area,
    inlet_velocity,
    density,
    inlet_pressure
):
    """
    Calculate idealised diffuser outlet conditions.

    Continuity:
        A1 * V1 = A2 * V2

    Bernoulli:
        P1 + 0.5*rho*V1^2
        = P2 + 0.5*rho*V2^2
    """

    if min(
        inlet_area,
        outlet_area,
        inlet_velocity,
        density
    ) <= 0:
        raise ValueError("Areas, velocity and density must be positive.")

    if outlet_area < inlet_area:
        raise ValueError(
            "This model expects an expanding diffuser."
        )

    outlet_velocity = (
        inlet_area * inlet_velocity / outlet_area
    )

    outlet_pressure = (
        inlet_pressure
        + 0.5 * density
        * (inlet_velocity**2 - outlet_velocity**2)
    )

    pressure_recovery = (
        outlet_pressure - inlet_pressure
    )

    return {
        "outlet_velocity": outlet_velocity,
        "outlet_pressure": outlet_pressure,
        "pressure_recovery": pressure_recovery,
        "area_ratio": outlet_area / inlet_area
    }
