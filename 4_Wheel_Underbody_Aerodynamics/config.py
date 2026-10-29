"""
PROJECT 4: WHEEL AND UNDERBODY AERODYNAMICS
===========================================

USER CONFIGURATION

SI units:
Length       : m
Velocity     : m/s
Density      : kg/m3
Viscosity    : Pa.s
Rotation     : rad/s
Pressure     : Pa
"""

from dataclasses import dataclass


@dataclass
class CFDConfig:

    # ------------------------------------
    # FREESTREAM CONDITIONS
    # ------------------------------------

    inlet_velocity: float = 30.0
    air_density: float = 1.225
    dynamic_viscosity: float = 1.81e-5
    atmospheric_pressure: float = 101325.0

    # ------------------------------------
    # WHEEL GEOMETRY
    # ------------------------------------

    wheel_radius: float = 0.33
    wheel_width: float = 0.22

    wheel_center_x: float = 1.0
    wheel_center_y: float = 0.40

    # 1.0 = rolling without longitudinal slip
    wheel_rotation_factor: float = 1.0

    # ------------------------------------
    # ROAD CONDITIONS
    # ------------------------------------

    ground_velocity: float = 30.0

    # ------------------------------------
    # UNDERBODY GEOMETRY
    # ------------------------------------

    vehicle_length: float = 4.5
    ground_clearance: float = 0.12

    inlet_underbody_height: float = 0.25
    diffuser_exit_height: float = 0.35

    diffuser_length: float = 0.80

    # ------------------------------------
    # COMPUTATIONAL DOMAIN
    # ------------------------------------

    domain_length: float = 6.0
    domain_height: float = 1.5

    nx: int = 200
    ny: int = 60

    # ------------------------------------
    # OUTPUT
    # ------------------------------------

    output_directory: str = "results"


def validate_config(cfg):

    positive_values = {
        "inlet_velocity": cfg.inlet_velocity,
        "air_density": cfg.air_density,
        "dynamic_viscosity": cfg.dynamic_viscosity,
        "wheel_radius": cfg.wheel_radius,
        "wheel_width": cfg.wheel_width,
        "ground_clearance": cfg.ground_clearance,
        "inlet_underbody_height": cfg.inlet_underbody_height,
        "diffuser_exit_height": cfg.diffuser_exit_height,
        "diffuser_length": cfg.diffuser_length,
        "domain_length": cfg.domain_length,
        "domain_height": cfg.domain_height,
    }

    for name, value in positive_values.items():
        if value <= 0:
            raise ValueError(f"{name} must be positive.")

    if cfg.nx < 20 or cfg.ny < 20:
        raise ValueError("Grid resolution is too small.")

    if cfg.wheel_rotation_factor < 0:
        raise ValueError("Wheel rotation factor cannot be negative.")

    if cfg.ground_velocity < 0:
        raise ValueError("Ground velocity cannot be negative.")

    if cfg.diffuser_exit_height < cfg.inlet_underbody_height:
        raise ValueError(
            "This model requires an expanding diffuser."
        )

    if cfg.wheel_center_y < cfg.wheel_radius:
        raise ValueError("Wheel intersects the ground.")

    if cfg.wheel_center_x <= 0:
        raise ValueError("Wheel must be inside the domain.")

    if cfg.diffuser_length >= cfg.domain_length:
        raise ValueError("Diffuser is too long for the domain.")

    print("Project 4 configuration validated.")
