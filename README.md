# Automotive Aerodynamics CFD

### Python-Based Computational Fluid Dynamics for Vehicle Aerodynamics

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![CFD](https://img.shields.io/badge/Engineering-CFD-orange)
![Status](https://img.shields.io/badge/Status-Development-yellow)

## About This Project

This repository explores computational fluid dynamics (CFD) and
automotive aerodynamics using Python-based numerical methods.

The aim is to develop a structured, reproducible research portfolio
covering vehicle drag, race-car aerodynamics, turbulent wakes, and
wheel and underbody flow.

The repository is organised into four independent projects.

## Projects

### 01 — External Flow Around a Car

Study flow around a simplified vehicle-like body, including velocity
fields, streamlines, and numerical methods for external aerodynamics.

[Open Project 1](01_external_car_flow/README.md)

### 02 — Race-Car Aerodynamics

Planned investigation of wings, diffusers, downforce, and aerodynamic
design parameters.

[Open Project 2](02_race_car_aerodynamics/README.md)

### 03 — Vehicle Wake and Turbulence

Planned investigation of wake structures, flow separation, and
turbulence behind vehicles.

[Open Project 3](03_vehicle_wake_turbulence/README.md)

### 04 — Wheel and Underbody Aerodynamics

Planned investigation of ground clearance, wheel rotation, and
underbody airflow.

[Open Project 4](04_wheel_underbody_aerodynamics/README.md)

## Technology

- Python
- NumPy
- Matplotlib
- Pytest
- Git and GitHub

## Installation

Install Python 3.10 or later.

Clone the repository:

    git clone <YOUR_REPOSITORY_URL>
    cd automotive-aerodynamics-cfd

Install dependencies:

    python -m pip install -r requirements.txt

Run the first project:

    cd 01_external_car_flow
    python main.py

## Research Principles

- Document the governing equations and assumptions.
- Verify numerical implementations against known solutions.
- Investigate grid and domain sensitivity.
- Distinguish educational models from validated engineering CFD.
- Record simulation conditions and reproducible results.

## Current Status

Project 1 provides an educational two-dimensional Lattice Boltzmann
flow model. It is a starting point for numerical experimentation,
not a validated predictor of real-car aerodynamic performance.

The remaining projects are planned development areas.

## Future Direction

The long-term objective is to develop reliable workflows for
automotive aerodynamic analysis, validation, and design exploration.

## Author

Independent CFD and automotive aerodynamics study.

**Note:** Numerical results will be treated as engineering evidence
only after appropriate verification and validation.
