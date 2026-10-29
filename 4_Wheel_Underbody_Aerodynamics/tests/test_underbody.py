"""Automated tests for Project 4."""

import numpy as np
import pytest

from config import CFDConfig, validate_config

from geometry import create_geometry

from wheel_rotation import (
    calculate_angular_velocity,
    calculate_surface_velocity
)

from underbody import (
    calculate_underbody_flow,
    calculate_diffuser_performance
)


def test_configuration():

    cfg = CFDConfig()

    validate_config(cfg)


def test_geometry_dimensions():

    cfg = CFDConfig(
        nx=80,
        ny=40
    )

    geometry = create_geometry(cfg)

    assert geometry["solid"].shape == (cfg.ny, cfg.nx)


def test_wheel_rotation():

    omega = calculate_angular_velocity(
        vehicle_velocity=30.0,
        wheel_radius=0.3
    )

    assert omega == pytest.approx(100.0)


def test_wheel_surface_velocity():

    vx, vy = calculate_surface_velocity(
        x=np.array([1.0]),
        y=np.array([1.0]),
        center_x=0.0,
        center_y=0.0,
        angular_velocity=2.0
    )

    assert vx[0] == pytest.approx(-2.0)
    assert vy[0] == pytest.approx(2.0)


def test_underbody_velocity():

    cfg = CFDConfig()

    result = calculate_underbody_flow(cfg)

    assert np.isfinite(result["velocity"]).all()
    assert np.all(result["velocity"] > 0)


def test_diffuser_velocity_reduction():

    cfg = CFDConfig()

    result = calculate_diffuser_performance(cfg)

    assert result["outlet_velocity"] < cfg.inlet_velocity


def test_diffuser_pressure_recovery():

    cfg = CFDConfig()

    result = calculate_diffuser_performance(cfg)

    assert result["pressure_rise"] > 0
    assert result["pressure_recovery_coefficient"] > 0


def test_diffuser_with_equal_heights():

    cfg = CFDConfig(
        diffuser_exit_height=0.25
    )

    result = calculate_diffuser_performance(cfg)

    assert result["outlet_velocity"] == pytest.approx(
        cfg.inlet_velocity
    )

    assert result["pressure_rise"] == pytest.approx(0.0)
