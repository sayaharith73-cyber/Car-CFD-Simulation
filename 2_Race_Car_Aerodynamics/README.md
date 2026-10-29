
# Project 2 — Race-Car Aerodynamics

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![CFD](https://img.shields.io/badge/Field-Aerodynamics-orange)
![Status](https://img.shields.io/badge/Status-Development-yellow)

## Overview

This project investigates aerodynamic principles relevant to
race-car design.

The initial Python implementation focuses on airfoil geometry,
thin-airfoil lift theory, aerodynamic force calculations, and
idealised diffuser pressure recovery.

The long-term objective is to develop a more complete CFD workflow
for investigating racing wings, diffusers, and aerodynamic
performance.

**Important:** This initial version is an analytical and
educational aerodynamic model, not a validated 3D race-car CFD solver.

## Research Objectives

- Generate NACA four-digit airfoil geometries.
- Investigate lift coefficient as a function of angle of attack.
- Calculate dynamic pressure and idealised aerodynamic forces.
- Investigate diffuser area expansion.
- Produce reproducible engineering plots.
- Develop towards validated CFD simulations of race-car components.

## Numerical Methods

### Thin-Airfoil Theory

For a symmetric airfoil at small angles:

    CL = 2*pi*alpha

where alpha is measured in radians.

### Dynamic Pressure

    q = 0.5*rho*U^2

### Aerodynamic Forces

    Lift = q*A*CL

    Drag = q*A*CD

### Diffuser Continuity

    A1*V1 = A2*V2

### Bernoulli Equation

    P1 + 0.5*rho*V1^2
    = P2 + 0.5*rho*V2^2

## Model Limitations

The thin-airfoil model assumes inviscid, incompressible,
two-dimensional flow and attached-flow behaviour.

The diffuser model assumes ideal one-dimensional flow.

Neither model predicts realistic turbulent separation, stall,
viscous drag, ground effect, or three-dimensional wing interactions.

## Installation

From the Project 2 folder:

    python -m pip install -r requirements.txt

## Run

    python main.py

## User Inputs

Modify `config.py` to change:

| Parameter | Description |
|---|---|
| velocity | Incoming airflow velocity [m/s] |
| air_density | Air density [kg/m3] |
| chord | Wing chord [m] |
| angle_of_attack | Wing angle [degrees] |
| airfoil_code | NACA four-digit profile |
| number_of_panels | Reserved for future panel-method development |

## Output

The program generates:

- `airfoil_geometry.png`
- `lift_curve.png`
- `lift_curve.csv`
- `diffuser_pressure_recovery.png`
- `diffuser_results.csv`

## Testing

Run:

    python -m pytest tests -v

## Future Development

1. Implement a validated source/vortex panel method.
2. Introduce viscous aerodynamic analysis.
3. Investigate front and rear wing interactions.
4. Add ground-plane and moving-ground modelling.
5. Investigate diffuser separation and pressure recovery.
6. Develop a three-dimensional race-car CFD workflow.
7. Compare results against experimental or published data.

## Research Philosophy

All modelling assumptions should be documented.

Analytical estimates must be distinguished from CFD results.
Numerical predictions should be verified and validated before
being used for engineering conclusions.
