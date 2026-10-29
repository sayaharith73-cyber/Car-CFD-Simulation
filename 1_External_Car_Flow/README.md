# Project 1 — External Flow Around a Simplified Car Body

## Overview

This project explores external aerodynamics using Python and the
Lattice Boltzmann Method (LBM).

The current model represents a simplified, rounded body inside a
two-dimensional periodic computational domain.

It is designed to introduce numerical flow simulation, geometry
generation, velocity-field visualisation, and basic software testing.

**This is a learning model, not a validated real-car CFD simulation.**

## Objectives

- Generate a computational domain and solid-body mask.
- Implement a D2Q9 Lattice Boltzmann solver.
- Visualise velocity magnitude and flow streamlines.
- Explore how body geometry and numerical settings affect the flow.
- Create a reproducible and documented Python workflow.

## Governing Method

The solver uses a single-relaxation-time BGK collision operator
with a Guo forcing term and bounce-back solid boundaries.

The kinematic lattice viscosity is

    nu = (tau - 0.5) / 3

where `tau` is the relaxation time.

The method is intended for low-speed, approximately incompressible
flow in lattice units.

## Model Assumptions

- Two-dimensional flow.
- Periodic boundary conditions in the streamwise direction.
- Stationary solid walls at the top and bottom.
- A simplified rounded-rectangle body.
- Constant body-force acceleration.
- No turbulence model.
- No moving ground or rotating wheels.
- No physical drag coefficient calculation.

Because the streamwise domain is periodic, this is not an isolated
vehicle in an open wind tunnel. The wake can interact with the
periodic domain and the body again.

## Installation

From the repository root:

    python -m pip install -r requirements.txt

## Run the Simulation

Enter this folder:

    cd 01_external_car_flow

Run:

    python main.py

## User Inputs

Edit `config.py`.

| Parameter | Meaning |
|---|---|
| `nx`, `ny` | Domain size in lattice nodes |
| `body_length` | Body length in lattice nodes |
| `body_height` | Body height in lattice nodes |
| `body_corner_radius` | Rounded-corner radius |
| `body_x_fraction` | Streamwise body position |
| `acceleration_x` | Streamwise forcing |
| `relaxation_time` | BGK relaxation parameter |
| `max_iterations` | Maximum solver iterations |

These inputs use lattice units and must not be interpreted directly
as metres, metres per second, or pascals.

## Results

The solver saves:

- `results/velocity_contour.png`
- `results/streamlines.png`
- `results/density_variation.png`
- `results/convergence.png`
- `results/flow_fields.npz`
- `results/summary.txt`

Plots and output files are generated when the code runs.

## Run the Tests

From this folder:

    python -m pytest tests -v

## Limitations and Future Work

The current implementation does not calculate physical vehicle drag
or lift. It does not model three-dimensional geometry, turbulent
boundary layers, realistic inlet/outlet conditions, moving ground,
or rotating wheels.

Future development should include:

1. Verification against established LBM benchmark cases.
2. Grid and domain-size sensitivity studies.
3. An isolated-body inlet/outlet formulation.
4. Physical-unit scaling and force validation.
5. A realistic vehicle geometry and suitable turbulence treatment.
6. Comparison with published aerodynamic measurements.

## Scientific Reproducibility

Record the input parameters, numerical method, mesh resolution,
iteration history, and validation evidence for each simulation.

A visually plausible contour is not sufficient evidence of accuracy.
