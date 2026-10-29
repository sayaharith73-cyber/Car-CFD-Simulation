"""
UNDERBODY FLOW ANALYSIS
=======================

Reduced-order one-dimensional model.

Calculates:
- Underbody flow velocity
- Static pressure
- Pressure coefficient
- Diffuser pressure recovery

Assumptions:
- Steady flow
- Constant density
- Incompressible flow
- No viscous losses
- Uniform velocity across each section

This is NOT a CFD solution.
"""

import numpy as np


def calculate_underbody_flow(
    cfg,
    number_of_points=150
):

    x = np.linspace(
        0.0,
        cfg.domain_length,
        number_of_points
    )

    diffuser_start = (
        cfg.domain_length - cfg.diffuser_length
    )

    fraction = np.clip(
        (x - diffuser_start) / cfg.diffuser_length,
        0.0,
        1.0
    )

    height = (
        cfg.inlet_underbody_height
        + fraction
        * (
            cfg.diffuser_exit_height
            - cfg.inlet_underbody_height
        )
    )

    # Unit span: area is equal to passage height.
    inlet_area = cfg.inlet_underbody_height
    local_area = height

    velocity = (
        cfg.inlet_velocity
        * inlet_area / local_area
    )

    dynamic_pressure = (
        0.5 * cfg.air_density * cfg.inlet_velocity**2
    )

    pressure = (
        cfg.atmospheric_pressure
        + 0.5 * cfg.air_density
        * (
            cfg.inlet_velocity**2
            - velocity**2
        )
    )

    pressure_coefficient = (
        pressure - cfg.atmospheric_pressure
    ) / dynamic_pressure

    return {
        "x": x,
        "height": height,
        "velocity": velocity,
        "pressure": pressure,
        "pressure_coefficient": pressure_coefficient
    }


def calculate_diffuser_performance(cfg):

    inlet_height = cfg.inlet_underbody_height
    outlet_height = cfg.diffuser_exit_height

    outlet_velocity = (
        cfg.inlet_velocity
        * inlet_height / outlet_height
    )

    pressure_rise = (
        0.5 * cfg.air_density
        * (
            cfg.inlet_velocity**2
            - outlet_velocity**2
        )
    )

    dynamic_pressure = (
        0.5 * cfg.air_density
        * cfg.inlet_velocity**2
    )

    pressure_recovery_coefficient = (
        pressure_rise / dynamic_pressure
    )

    return {
        "outlet_velocity": outlet_velocity,
        "pressure_rise": pressure_rise,
        "pressure_recovery_coefficient":
            pressure_recovery_coefficient
    }
