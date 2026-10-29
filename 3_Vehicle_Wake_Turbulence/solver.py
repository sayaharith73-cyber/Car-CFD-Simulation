"""
2D INCOMPRESSIBLE NAVIER-STOKES SOLVER
======================================

Educational fractional-step projection method.

Numerical assumptions:
- Constant-density incompressible flow
- Explicit convection and diffusion
- First-order pressure projection
- No-slip vehicle surface
- Prescribed inlet velocity
- Approximate zero-gradient outlet

This is a basic research-learning solver. Its pressure,
boundary conditions and stability require further verification
before interpreting its results as physical predictions.
"""

import numpy as np


def apply_velocity_boundaries(u, v, solid):

    # Inlet: uniform horizontal velocity
    u[:, 0] = 10.0
    v[:, 0] = 0.0

    # Outlet: approximate zero-gradient condition
    u[:, -1] = u[:, -2]
    v[:, -1] = v[:, -2]

    # Stationary top and bottom walls
    u[0, :] = 0.0
    u[-1, :] = 0.0
    v[0, :] = 0.0
    v[-1, :] = 0.0

    # No-slip vehicle surface
    u[solid] = 0.0
    v[solid] = 0.0

    return u, v


def apply_pressure_boundaries(p, solid):

    # Approximate zero normal pressure gradient at inlet
    p[:, 0] = p[:, 1]

    # Reference pressure at outlet
    p[:, -1] = 0.0

    # Neumann conditions at channel walls
    p[0, :] = p[1, :]
    p[-1, :] = p[-2, :]

    # Pressure inside solid cells is not physically solved.
    p[solid] = 0.0

    return p


def pressure_poisson(p, rhs, dx, dy, solid, iterations):

    dx2 = dx**2
    dy2 = dy**2

    for _ in range(iterations):

        old = p.copy()

        p[1:-1, 1:-1] = (
            (
                old[1:-1, 2:]
                + old[1:-1, :-2]
            ) * dy2
            + (
                old[2:, 1:-1]
                + old[:-2, 1:-1]
            ) * dx2
            - rhs[1:-1, 1:-1] * dx2 * dy2
        ) / (2 * (dx2 + dy2))

        p = apply_pressure_boundaries(p, solid)

    return p


def run_simulation(cfg, geometry):

    X, Y, x, y, dx, dy, solid = geometry

    rho = cfg.density
    nu = cfg.dynamic_viscosity / rho
    dt = cfg.time_step

    u = np.zeros_like(X)
    v = np.zeros_like(Y)
    p = np.zeros_like(X)

    u, v = apply_velocity_boundaries(u, v, solid)

    steps = int(cfg.total_time / dt)

    # Keep velocity snapshots for wake analysis
    snapshots = []

    for step in range(1, steps + 1):

        un = u.copy()
        vn = v.copy()

        # First derivatives: central differences
        du_dx = (un[1:-1, 2:] - un[1:-1, :-2]) / (2 * dx)
        du_dy = (un[2:, 1:-1] - un[:-2, 1:-1]) / (2 * dy)

        dv_dx = (vn[1:-1, 2:] - vn[1:-1, :-2]) / (2 * dx)
        dv_dy = (vn[2:, 1:-1] - vn[:-2, 1:-1]) / (2 * dy)

        # Second derivatives: diffusion
        lap_u = (
            (un[1:-1, 2:] - 2 * un[1:-1, 1:-1]
             + un[1:-1, :-2]) / dx**2
            +
            (un[2:, 1:-1] - 2 * un[1:-1, 1:-1]
             + un[:-2, 1:-1]) / dy**2
        )

        lap_v = (
            (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1]
             + vn[1:-1, :-2]) / dx**2
            +
            (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1]
             + vn[:-2, 1:-1]) / dy**2
        )

        # Convective acceleration
        convection_u = (
            un[1:-1, 1:-1] * du_dx
            + vn[1:-1, 1:-1] * du_dy
        )

        convection_v = (
            un[1:-1, 1:-1] * dv_dx
            + vn[1:-1, 1:-1] * dv_dy
        )

        # Intermediate velocity
        u_star = un.copy()
        v_star = vn.copy()

        u_star[1:-1, 1:-1] = (
            un[1:-1, 1:-1]
            + dt * (
                -convection_u + nu * lap_u
            )
        )

        v_star[1:-1, 1:-1] = (
            vn[1:-1, 1:-1]
            + dt * (
                -convection_v + nu * lap_v
            )
        )

        u_star, v_star = apply_velocity_boundaries(
            u_star, v_star, solid
        )

        # Divergence of intermediate velocity
        divergence = (
            (u_star[1:-1, 2:] - u_star[1:-1, :-2])
            / (2 * dx)
            +
            (v_star[2:, 1:-1] - v_star[:-2, 1:-1])
            / (2 * dy)
        )

        rhs = np.zeros_like(p)
        rhs[1:-1, 1:-1] = rho / dt * divergence

        p = pressure_poisson(
            p,
            rhs,
            dx,
            dy,
            solid,
            cfg.pressure_iterations
        )

        # Velocity correction
        u = u_star.copy()
        v = v_star.copy()

        u[1:-1, 1:-1] = (
            u_star[1:-1, 1:-1]
            - dt / rho
            * (
                p[1:-1, 2:] - p[1:-1, :-2]
            ) / (2 * dx)
        )

        v[1:-1, 1:-1] = (
            v_star[1:-1, 1:-1]
            - dt / rho
            * (
                p[2:, 1:-1] - p[:-2, 1:-1]
            ) / (2 * dy)
        )

        u, v = apply_velocity_boundaries(u, v, solid)

        # Store results periodically
        if step % cfg.save_every == 0 or step == steps:

            speed = np.sqrt(u**2 + v**2)

            if not np.isfinite(speed).all():
                raise FloatingPointError(
                    "Numerical instability detected. "
                    "Reduce time_step or refine the numerical method."
                )

            snapshots.append({
                "time": step * dt,
                "u": u.copy(),
                "v": v.copy(),
                "p": p.copy()
            })

            print(
                f"Step {step}/{steps} | "
                f"Time: {step * dt:.4f} s | "
                f"Maximum velocity: {speed.max():.4f} m/s"
            )

    return {
        "x": x,
        "y": y,
        "X": X,
        "Y": Y,
        "u": u,
        "v": v,
        "p": p,
        "solid": solid,
        "snapshots": snapshots,
        "nu": nu
    }
