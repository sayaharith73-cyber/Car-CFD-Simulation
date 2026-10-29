"""
ROTATING WHEEL KINEMATICS
=========================

Calculates wheel angular velocity and surface velocity.

This module calculates boundary kinematics.
It does not independently solve the airflow around the wheel.
"""

import numpy as np


def calculate_angular_velocity(
    vehicle_velocity,
    wheel_radius,
    rotation_factor=1.0
):

    if wheel_radius <= 0:
        raise ValueError("Wheel radius must be positive.")

    return (
        rotation_factor
        * vehicle_velocity
        / wheel_radius
    )


def calculate_surface_velocity(
    x,
    y,
    center_x,
    center_y,
    angular_velocity
):
    """
    Calculate velocity at points on a rotating wheel.

    Positive angular velocity follows the counter-clockwise
    mathematical convention.

    vx = -omega * (y - cy)
    vy =  omega * (x - cx)
    """

    rx = x - center_x
    ry = y - center_y

    vx = -angular_velocity * ry
    vy = angular_velocity * rx

    return vx, vy


def calculate_wheel_parameters(cfg):

    omega = calculate_angular_velocity(
        cfg.inlet_velocity,
        cfg.wheel_radius,
        cfg.wheel_rotation_factor
    )

    revolutions_per_minute = (
        omega * 60 / (2 * np.pi)
    )

    return {
        "angular_velocity_rad_s": omega,
        "rotation_rpm": revolutions_per_minute,
        "peripheral_speed_m_s": omega * cfg.wheel_radius
    }
