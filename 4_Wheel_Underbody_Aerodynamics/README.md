
# Project 4 — Wheel and Underbody Aerodynamics CFD

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Engineering](https://img.shields.io/badge/Field-Automotive%20Aerodynamics-orange)
![Status](https://img.shields.io/badge/Status-Development-yellow)

## Overview

This project investigates wheel and underbody aerodynamics using
Python-based numerical and analytical methods.

The objective is to explore how wheel rotation, road conditions,
ground clearance and diffuser geometry influence automotive
aerodynamic performance.

The project currently contains:

- Wheel rotational kinematics.
- Simplified wheel geometry.
- Underbody geometry generation.
- Idealised one-dimensional underbody flow analysis.
- Diffuser pressure recovery calculations.
- Automated tests and engineering visualisations.

**Important:** The current version is a reduced-order educational
model. It is not a coupled CFD simulation of rotating wheels and
underbody airflow.

## Research Objectives

1. Investigate wheel rotational speed.
2. Study the influence of ground clearance.
3. Investigate underbody velocity changes.
4. Examine diffuser expansion.
5. Investigate pressure recovery.
6. Develop towards realistic wheel and underbody CFD.

## Physical Principles

### Wheel Rotation

For pure rolling:

    omega = U/R

### Reynolds Number

    Re = rho*U*D/mu

### Continuity Equation

    A1*U1 = A2*U2

### Bernoulli Equation

    P1 + 0.5*rho*U1^2
    = P2 + 0.5*rho*U2^2

### Pressure Coefficient

    Cp = (P - P_infinity)/(0.5*rho*U_infinity^2)

## Numerical Approach

The initial implementation uses:

- Python and NumPy.
- Cartesian geometry generation.
- Analytical wheel rotation.
- One-dimensional incompressible flow calculations.
- Matplotlib for visualisation.

A coupled Navier-Stokes solver is planned for future development.

## Installation

From the Project 4 directory:

    python -m pip install -r requirements.txt

## Running the Project

    python main.py

## User Inputs

Edit `config.py`.

| Parameter | Description |
|---|---|
| inlet_velocity | Incoming air velocity |
| wheel_radius | Wheel radius |
| wheel_width | Wheel width |
| wheel_rotation_factor | Wheel rotation factor |
| ground_velocity | Road velocity |
| ground_clearance | Ground clearance |
| inlet_underbody_height | Underbody inlet height |
| diffuser_exit_height | Diffuser outlet height |
| diffuser_length | Diffuser length |

All physical dimensions use SI units.

## Generated Results

The results directory contains:

- geometry.png
- wheel_rotation.png
- underbody_velocity.png
- underbody_pressure.png
- pressure_coefficient.png
- underbody_results.csv
- summary.txt

## Testing

Run:

    python -m pytest tests -v

## Limitations

The current implementation does not calculate:

- Coupled airflow around a rotating wheel.
- Turbulent wheel wakes.
- Three-dimensional underbody flow.
- Viscous diffuser separation.
- Ground-effect downforce.
- Validated aerodynamic drag or lift coefficients.

The simplified model should not be used to make quantitative
predictions about real racing vehicles.

## Future Development

1. Introduce a moving-wall boundary condition for rotating wheels.
2. Implement a moving-ground boundary condition.
3. Develop a two-dimensional incompressible Navier-Stokes solver.
4. Investigate diffuser separation.
5. Introduce realistic wheel-arch geometry.
6. Develop three-dimensional underbody simulations.
7. Compare against experimental measurements.

## Research Reproducibility

Document the geometry, boundary conditions, wheel speed, road speed,
ground clearance, numerical assumptions and validation evidence
for every simulation.

A visualisation alone is not evidence of numerical accuracy.
