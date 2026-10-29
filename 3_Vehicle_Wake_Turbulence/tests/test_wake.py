"""Automated tests for Project 3."""

import numpy as np
import pytest

from config import CFDConfig, validate_config
from geometry import create_geometry
from wake_analysis import (
    calculate_vorticity,
    calculate_velocity_deficit,
    calculate_wake_width
)


def small_config():

    return CFDConfig(
        domain_length=4.0,
        domain_height=2.0,
        nx=61,
        ny=31,
        vehicle_length=0.6,
        vehicle_height=0.3,
        vehicle_x=0.8,
        vehicle_y=1.0,
        total_time=0.001,
        time_step=0.0005,
        pressure_iterations=10
    )


def test_configuration():

    cfg = small_config()

    validate_config(cfg)


def test_geometry():

    cfg = small_config()

    X, Y, x, y, dx, dy, solid = create_geometry(cfg)

    assert solid.shape == (cfg.ny, cfg.nx)
    assert solid.any()
    assert dx > 0
    assert dy > 0


def test_velocity_deficit():

    u = np.array([
        [10.0, 8.0, 6.0],
        [10.0, 9.0, 7.0]
    ])

    solid = np.zeros_like(u, dtype=bool)

    deficit = calculate_velocity_deficit(
        u, solid, 10.0
    )

    assert deficit[0, 0] == pytest.approx(0.0)
    assert deficit[0, 1] == pytest.approx(2.0)


def test_wake_width():

    y = np.array([0.0, 0.5, 1.0, 1.5, 2.0])

    velocity = np.array([
        10.0, 8.0, 5.0, 8.0, 10.0
    ])

    width = calculate_wake_width(
        y, velocity, 10.0
    )

    assert width == pytest.approx(1.0)


def test_vorticity_of_uniform_flow():

    u = np.ones((10, 10)) * 10.0
    v = np.zeros((10, 10))

    omega = calculate_vorticity(
        u, v, 0.1, 0.1
    )

    assert np.allclose(omega, 0.0)


def test_velocity_deficit_masks_solid():

    u = np.ones((3, 3)) * 10
    solid = np.zeros((3, 3), dtype=bool)
    solid[1, 1] = True

    deficit = calculate_velocity_deficit(
        u, solid, 10.0
    )

    assert np.isnan(deficit[1, 1])
