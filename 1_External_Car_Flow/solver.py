"""
LATTICE BOLTZMANN SOLVER
========================

D2Q9 lattice, BGK collision, Guo forcing and bounce-back
at stationary solid nodes.

All variables use lattice units.

This implementation is intended for learning and testing
at modest Reynolds numbers. It is not a validated vehicle CFD
solver and does not include a physical drag-force calculation.
"""

import numpy as np


# Nine discrete velocity directions
# Order: rest, east, north, west, south, NE, NW, SW, SE
CX = np.array([0, 1, 0, -1, 0, 1, -1, -1, 1])
CY = np.array([0, 0, 1, 0, -1, 1, 1, -1, -1])

WEIGHTS = np.array([
    4 / 9,
    1 / 9, 1 / 9, 1 / 9, 1 / 9,
    1 / 36, 1 / 36, 1 / 36, 1 / 36
])

OPPOSITE = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6])


def equilibrium(rho, ux, uy):
    """
    Calculate the D2Q9 equilibrium distribution.

    rho: density array
    ux, uy: velocity arrays
    """

    feq = np.empty((9, *rho.shape), dtype=float)

    speed_squared = ux**2 + uy**2

    for i in range(9):
        cu = CX[i] * ux + CY[i] * uy

        feq[i] = WEIGHTS[i] * rho * (
            1.0
            + 3.0 * cu
            + 4.5 * cu**2
            - 1.5 * speed_squared
        )

    return feq


def macroscopic_fields(f, cfg, solid):
    """Calculate density and velocity from distributions."""

    rho = np.sum(f, axis=0)

    # Prevent division by zero in an invalid numerical state.
    rho_safe = np.maximum(rho, 1.0e-12)

    jx = np.sum(f * CX[:, None, None], axis=0)
    jy = np.sum(f * CY[:, None, None], axis=0)

    # Body force per unit volume in lattice units.
    fx = rho * cfg.acceleration_x
    fy = rho * cfg.acceleration_y

    fx[solid] = 0.0
    fy[solid] = 0.0

    # Guo forcing uses a half-force velocity correction.
    ux = (jx + 0.5 * fx) / rho_safe
    uy = (jy + 0.5 * fy) / rho_safe

    ux[solid] = 0.0
    uy[solid] = 0.0

    return rho, ux, uy, fx, fy


def collide(f, rho, ux, uy, fx, fy, cfg):
    """Apply BGK collision and the Guo forcing source."""

    tau = cfg.relaxation_time
    feq = equilibrium(rho, ux, uy)

    f_post = np.empty_like(f)

    force_prefactor = 1.0 - 0.5 / tau
    cu_velocity = np.zeros_like(rho)
    speed_squared = ux**2 + uy**2

    for i in range(9):
        cu = CX[i] * ux + CY[i] * uy
        c_force = CX[i] * fx + CY[i] * fy
        velocity_force = ux * fx + uy * fy

        # Discrete forcing term
        forcing = WEIGHTS[i] * force_prefactor * (
            3.0 * (
                (CX[i] - ux) * fx
                + (CY[i] - uy) * fy
            )
            + 9.0 * cu * c_force
        )

        f_post[i] = (
            f[i]
            - (f[i] - feq[i]) / tau
            + forcing
        )

    return f_post


def stream_and_bounce_back(f_post, solid):
    """
    Stream distributions to neighbouring nodes.

    Apply on-node bounce-back at solid nodes to approximate
    stationary no-slip walls and the body surface.
    """

    f_streamed = np.empty_like(f_post)

    for i in range(9):
        f_streamed[i] = np.roll(
            f_post[i],
            shift=(CY[i], CX[i]),
            axis=(0, 1)
        )

    # Reflect distributions at solid nodes.
    # Periodicity in x is supplied by np.roll.
    for i in range(1, 9):
        f_streamed[i, solid] = f_post[OPPOSITE[i], solid]

    return f_streamed


def run_simulation(cfg, solid):
    """
    Run the lattice Boltzmann simulation.

    Returns density, velocity components, iteration count
    and a basic mean-velocity convergence history.
    """

    rho = np.ones((cfg.ny, cfg.nx), dtype=float)
    ux = np.zeros_like(rho)
    uy = np.zeros_like(rho)

    # Initialise all populations at equilibrium.
    f = equilibrium(rho, ux, uy)

    fluid = ~solid
    previous_mean_velocity = None
    history = []
    converged = False
    iterations_completed = 0

    for iteration in range(1, cfg.max_iterations + 1):

        rho, ux, uy, fx, fy = macroscopic_fields(
            f, cfg, solid
        )

        f_post = collide(
            f, rho, ux, uy, fx, fy, cfg
        )

        f = stream_and_bounce_back(f_post, solid)

        iterations_completed = iteration

        # Check convergence periodically.
        if iteration % cfg.check_every == 0:
            rho, ux, uy, _, _ = macroscopic_fields(
                f, cfg, solid
            )

            mean_velocity = float(np.mean(ux[fluid]))
            history.append((iteration, mean_velocity))

            print(
                f"Iteration {iteration:6d} | "
                f"mean streamwise velocity = "
                f"{mean_velocity:.8e}"
            )

            if previous_mean_velocity is not None:
                relative_change = abs(
                    mean_velocity - previous_mean_velocity
                ) / max(abs(mean_velocity), 1.0e-12)

                if (
                    iteration >= 2 * cfg.check_every
                    and relative_change < cfg.convergence_tolerance
                ):
                    converged = True
                    print("Mean-velocity convergence target reached.")
                    break

            previous_mean_velocity = mean_velocity

    rho, ux, uy, _, _ = macroscopic_fields(f, cfg, solid)

    if not converged:
        print(
            "Maximum iterations reached or convergence target "
            "not met. Inspect the results and convergence history."
        )

    return {
        "rho": rho,
        "ux": ux,
        "uy": uy,
        "solid": solid,
        "iterations": iterations_completed,
        "converged": converged,
        "history": np.asarray(history, dtype=float).reshape(-1, 2),
    }
