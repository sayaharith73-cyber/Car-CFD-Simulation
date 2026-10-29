
"""
RACE-CAR AERODYNAMICS
=====================

USER INPUT CONFIGURATION

All geometry dimensions are in metres.
Velocity is in m/s.
Angles are in degrees.
Pressure is in Pa.

The initial aerodynamic model is an inviscid,
two-dimensional airfoil panel method.
"""

from dataclasses import dataclass


@dataclass
class WingConfig:

    # ------------------------------------
    # FREESTREAM CONDITIONS
    # ------------------------------------

    velocity: float = 40.0
    air_density: float = 1.225
    static_pressure: float = 101325.0

    # ------------------------------------
    # WING GEOMETRY
    # ------------------------------------

    chord: float = 1.0
    angle_of_attack: float = 5.0

    # ------------------------------------
    # AIRFOIL GEOMETRY
    # ------------------------------------

    # NACA 4-digit airfoil designation
    # Example: 0012 = symmetric, 12% thick
    airfoil_code: str = "0012"

    number_of_panels: int = 80

    # ------------------------------------
    # NUMERICAL SETTINGS
    # ------------------------------------

    linear_solver_tolerance: float = 1e-10

    # ------------------------------------
    # OUTPUT
    # ------------------------------------

    output_directory: str = "results"


def validate_config(cfg):

    if cfg.velocity <= 0:
        raise ValueError("Velocity must be positive.")

    if cfg.air_density <= 0:
        raise ValueError("Air density must be positive.")

    if cfg.static_pressure <= 0:
        raise ValueError("Static pressure must be positive.")

    if cfg.chord <= 0:
        raise ValueError("Chord must be positive.")

    if not -15 <= cfg.angle_of_attack <= 15:
        raise ValueError(
            "Use an angle of attack between -15 and 15 degrees "
            "for this initial model."
        )

    if len(cfg.airfoil_code) != 4 or not cfg.airfoil_code.isdigit():
        raise ValueError(
            "Airfoil code must contain four digits, e.g. 0012."
        )

    if cfg.number_of_panels < 20:
        raise ValueError("Use at least 20 panels.")

    if cfg.number_of_panels % 2 != 0:
        raise ValueError("Use an even number of panels.")

    print("Wing configuration validated.")
