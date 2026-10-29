"""
USER CONFIGURATION
==================

Project 1: External flow around a simplified car-like body.

The current model uses lattice units, not SI units.
It is a two-dimensional, periodic Lattice Boltzmann simulation.

Change the values below to experiment with:
- Computational domain size
- Body dimensions
- Numerical resolution
- Flow-driving acceleration
- Number of iterations

Instructions for changing the values : 

- nx, ny: increase the grid size for a finer numerical representation. This increases computational cost.
- body_length, body_height: change the size of the simplified obstacle in lattice nodes.
- body_corner_radius: change how rounded the body corners are.
- body_x_fraction: move the obstacle along the domain.
- acceleration_x: controls how strongly the fluid is driven through the periodic domain.
- relaxation_time: controls the lattice viscosity. Values too close to 0.5 can cause numerical instability.
- max_iterations: maximum number of iterations before the simulation stops.
- convergence_tolerance: a target for the change in mean velocity, not proof that every aspect of the flow has converged.

"""

from dataclasses import dataclass

@dataclass
class CFDConfig:

    # ------------------------------------------------
    # 1. COMPUTATIONAL DOMAIN
    # ------------------------------------------------
    nx: int = 320
    ny: int = 120

    # ------------------------------------------------
    # 2. SIMPLIFIED BODY GEOMETRY
    # ------------------------------------------------
    body_length: int = 60
    body_height: int = 18
    body_corner_radius: int = 5

    # Body centre as a fraction of domain length.
    # 0.30 means 30% of the way across the domain.
    body_x_fraction: float = 0.30

    # ------------------------------------------------
    # 3. FLOW CONDITIONS
    # ------------------------------------------------
    # Uniform body-force acceleration in lattice units.
    # Increase cautiously; large forcing can destabilise
    # the numerical solution.
    acceleration_x: float = 1.0e-6
    acceleration_y: float = 0.0

    # ------------------------------------------------
    # 4. LATTICE BOLTZMANN SETTINGS
    # ------------------------------------------------
    # Single-relaxation-time BGK collision model.
    # Must be greater than 0.5 for positive viscosity.
    relaxation_time: float = 0.80

    # ------------------------------------------------
    # 5. ITERATION SETTINGS
    # ------------------------------------------------
    max_iterations: int = 6000
    check_every: int = 200
    convergence_tolerance: float = 1.0e-6

    # ------------------------------------------------
    # 6. OUTPUT
    # ------------------------------------------------
    output_directory: str = "results"


def validate_config(cfg: CFDConfig) -> None:
    """Check the input settings before starting the solver."""

    if cfg.nx < 50 or cfg.ny < 30:
        raise ValueError(
            "Use at least 50 x 30 lattice nodes."
        )

    if cfg.body_length < 5 or cfg.body_height < 5:
        raise ValueError(
            "Body length and height must be at least 5 nodes."
        )

    if cfg.body_length >= cfg.nx / 2:
        raise ValueError(
            "Body length must be less than half the domain length."
        )

    if cfg.body_height >= cfg.ny - 4:
        raise ValueError(
            "Body is too tall for the computational domain."
        )

    if not 0.0 < cfg.body_x_fraction < 1.0:
        raise ValueError(
            "body_x_fraction must be between 0 and 1."
        )

    if not 0.5 < cfg.relaxation_time < 2.0:
        raise ValueError(
            "For this BGK implementation, relaxation_time "
            "must be greater than 0.5 and less than 2.0."
        )

    if cfg.body_corner_radius < 0:
        raise ValueError(
            "Body corner radius cannot be negative."
        )

    if cfg.body_corner_radius > min(
        cfg.body_length, cfg.body_height
    ) / 2:
        raise ValueError(
            "Body corner radius is too large."
        )

    if cfg.acceleration_x < 0:
        raise ValueError(
            "This example expects non-negative x acceleration."
        )

    if cfg.max_iterations < 1 or cfg.check_every < 1:
        raise ValueError(
            "Iteration counts must be positive."
        )

    if cfg.convergence_tolerance <= 0:
        raise ValueError(
            "Convergence tolerance must be positive."
        )

    print("Configuration validation passed.")
