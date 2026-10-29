"""
VEHICLE WAKE CFD
================

USER CONFIGURATION

All physical inputs use SI units:
- Length: metres
- Velocity: metres/second
- Density: kg/m^3
- Dynamic viscosity: Pa.s
- Time: seconds

The solver uses a simplified 2D incompressible
Navier-Stokes projection method.
"""

from dataclasses import dataclass


@dataclass
class CFDConfig:

    # -----------------------------------------
    # 1. COMPUTATIONAL DOMAIN
    # -----------------------------------------

    domain_length: float = 8.0
    domain_height: float = 3.0

    nx: int = 161
    ny: int = 61

    # -----------------------------------------
    # 2. VEHICLE GEOMETRY
    # -----------------------------------------

    vehicle_length: float = 1.2
    vehicle_height: float = 0.45

    vehicle_x: float = 1.5
    vehicle_y: float = 1.5

    # -----------------------------------------
    # 3. AIR PROPERTIES
    # -----------------------------------------

    density: float = 1.225
    dynamic_viscosity: float = 1.81e-5

    # -----------------------------------------
    # 4. FREESTREAM CONDITIONS
    # -----------------------------------------

    inlet_velocity: float = 10.0

    # -----------------------------------------
    # 5. TIME SETTINGS
    # -----------------------------------------

    time_step: float = 0.0005
    total_time: float = 0.5

    # Number of iterations for the pressure solver
    pressure_iterations: int = 80

    # -----------------------------------------
    # 6. OUTPUT SETTINGS
    # -----------------------------------------

    output_directory: str = "results"
    save_every: int = 200


def validate_config(cfg):

    if cfg.domain_length <= 0 or cfg.domain_height <= 0:
        raise ValueError("Domain dimensions must be positive.")

    if cfg.nx < 30 or cfg.ny < 20:
        raise ValueError("Increase the computational grid size.")

    if cfg.vehicle_length <= 0 or cfg.vehicle_height <= 0:
        raise ValueError("Vehicle dimensions must be positive.")

    if cfg.density <= 0 or cfg.dynamic_viscosity <= 0:
        raise ValueError("Air properties must be positive.")

    if cfg.inlet_velocity <= 0:
        raise ValueError("Inlet velocity must be positive.")

    if cfg.time_step <= 0 or cfg.total_time <= 0:
        raise ValueError("Time settings must be positive.")

    if cfg.pressure_iterations < 1 or cfg.save_every < 1:
        raise ValueError("Iteration settings must be positive.")

    if cfg.vehicle_x <= 0:
        raise ValueError("Vehicle must be downstream of the inlet.")

    if cfg.vehicle_x + cfg.vehicle_length >= cfg.domain_length:
        raise ValueError("Vehicle is too close to the outlet.")

    if (
        cfg.vehicle_y - cfg.vehicle_height / 2 <= 0
        or cfg.vehicle_y + cfg.vehicle_height / 2 >= cfg.domain_height
    ):
        raise ValueError("Vehicle must fit inside the domain.")

    print("Vehicle wake configuration validated.")
