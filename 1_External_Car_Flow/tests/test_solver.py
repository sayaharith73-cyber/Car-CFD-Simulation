"""Basic tests for geometry and solver stability."""

import numpy as np

from config import CFDConfig
from geometry import create_solid_mask
from solver import run_simulation


def test_geometry_contains_solid_body():
    cfg = CFDConfig(
        nx=80,
        ny=40,
        body_length=15,
        body_height=8,
        body_corner_radius=2,
        max_iterations=20,
    )

    solid = create_solid_mask(cfg)

    assert solid.shape == (cfg.ny, cfg.nx)
    assert solid[0, :].all()
    assert solid[-1, :].all()
    assert solid.sum() > 2 * cfg.nx


def test_solver_returns_finite_fields():
    cfg = CFDConfig(
        nx=80,
        ny=40,
        body_length=15,
        body_height=8,
        body_corner_radius=2,
        max_iterations=20,
        check_every=10,
    )

    solid = create_solid_mask(cfg)
    result = run_simulation(cfg, solid)

    assert result["rho"].shape == (cfg.ny, cfg.nx)
    assert np.isfinite(result["rho"]).all()
    assert np.isfinite(result["ux"]).all()
    assert np.isfinite(result["uy"]).all()


def test_velocity_is_zero_at_stationary_walls():
    cfg = CFDConfig(
        nx=80,
        ny=40,
        body_length=15,
        body_height=8,
        body_corner_radius=2,
        max_iterations=20,
        check_every=10,
    )

    solid = create_solid_mask(cfg)
    result = run_simulation(cfg, solid)

    assert np.allclose(result["ux"][0, :], 0.0)
    assert np.allclose(result["ux"][-1, :], 0.0)
    assert np.allclose(result["uy"][0, :], 0.0)
    assert np.allclose(result["uy"][-1, :], 0.0)
