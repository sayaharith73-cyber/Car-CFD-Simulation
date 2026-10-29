# Project 3 — Vehicle Wake and Turbulence CFD

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![CFD](https://img.shields.io/badge/Field-Automotive%20Aerodynamics-orange)
![Status](https://img.shields.io/badge/Status-Development-yellow)

## Overview

This project investigates the aerodynamic wake behind a simplified
vehicle geometry using Python-based numerical methods.

The objective is to understand how airflow behaves downstream of
a vehicle and how body geometry and flow conditions influence
velocity deficit, recirculation and vorticity.

The initial implementation uses a simplified two-dimensional
incompressible Navier-Stokes projection method.

**This is an educational numerical model, not a validated
turbulent automotive CFD simulation.**

## Research Objectives

- Investigate flow around a simplified vehicle body.
- Visualise downstream velocity distributions.
- Calculate streamwise velocity deficit.
- Investigate vorticity distributions.
- Estimate wake width at downstream locations.
- Explore Reynolds number and grid sensitivity.
- Develop towards validated turbulent-flow simulations.

## Governing Equations

### Conservation of Mass

    div(u) = 0

### Conservation of Momentum

    du/dt + (u.grad)u
    = -grad(p)/rho + nu*laplacian(u)

### Kinematic Viscosity

    nu = mu/rho

### Reynolds Number

    Re = rho*U*L/mu

### Velocity Deficit

    Delta U = U_infinity - u

### Vorticity

    omega_z = dv/dx - du/dy

## Numerical Method

The solver uses a fractional-step pressure projection approach:

1. Calculate intermediate velocity.
2. Construct the pressure Poisson equation.
3. Solve for pressure.
4. Correct the velocity field.
5. Apply boundary conditions.
6. Repeat over time.

The present implementation uses a Cartesian grid and simplified
vehicle geometry.

## Installation

From this project folder:

    python -m pip install -r requirements.txt

## Running the Simulation

    python main.py

## User Configuration

Edit `config.py` to modify:

| Parameter | Description |
|---|---|
| domain_length | Computational domain length |
| domain_height | Computational domain height |
| nx, ny | Grid resolution |
| vehicle_length | Body length |
| vehicle_height | Body height |
| inlet_velocity | Freestream velocity |
| density | Air density |
| dynamic_viscosity | Dynamic viscosity |
| time_step | Numerical time increment |
| total_time | Simulation duration |

All inputs use SI units.

## Generated Results

The program generates:

- vehicle_geometry.png
- velocity_contour.png
- streamlines.png
- pressure_contour.png
- velocity_deficit.png
- vorticity.png
- wake_width.csv
- wake_fields.npz

## Testing

Run:

    python -m pytest tests -v

## Model Limitations

The current model does not include:

- A turbulence closure model.
- Three-dimensional vehicle geometry.
- Moving ground.
- Rotating wheels.
- Experimentally validated pressure drag.
- A fully validated immersed-boundary treatment.
- A demonstrated mesh-independent wake solution.

The wake should not be interpreted as a prediction of a real
vehicle's turbulent aerodynamic performance.

## Future Research

1. Improve pressure boundary conditions.
2. Verify the projection solver using established benchmarks.
3. Perform grid and time-step sensitivity studies.
4. Investigate turbulent flow using an appropriate turbulence model.
5. Introduce realistic vehicle geometries.
6. Compare wake profiles with published experimental data.
7. Investigate drag reduction through rear-end geometry changes.

## Scientific Reproducibility

Every simulation should record its geometry, fluid properties,
boundary conditions, grid resolution, time step, convergence
behaviour, and validation evidence.

Visualisation alone is not proof of numerical accuracy.
