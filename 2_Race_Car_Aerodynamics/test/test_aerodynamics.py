"""Automated tests for Project 2."""

import numpy as np
import pytest

from airfoil import generate_naca4
from aerodynamics import (
    calculate_coefficients,
    calculate_dynamic_pressure,
    calculate_forces,
)
from diffuser import calculate_diffuser


def test_naca_airfoil_geometry():
    xu, yu, xl, yl = generate_naca4("0012", 1.0)

    assert len(xu) == len(yu)
    assert len(xl) == len(yl)

    assert np.isfinite(xu).all()
    assert np.isfinite(yu).all()

    # Symmetric airfoil should have approximately
    # mirrored upper and lower surfaces.
    assert np.allclose(yu, -yl)


def test_symmetric_airfoil_zero_angle():
    cl, cd = calculate_coefficients(0.0)

    assert cl == pytest.approx(0.0)
    assert cd == pytest.approx(0.0)


def test_lift_increases_with_angle():
    cl_5, _ = calculate_coefficients(5.0)
    cl_10, _ = calculate_coefficients(10.0)

    assert cl_10 > cl_5 > 0


def test_dynamic_pressure():
    q = calculate_dynamic_pressure(1.225, 40.0)

    assert q == pytest.approx(980.0)


def test_force_calculation():
    lift, drag = calculate_forces(
        density=1.225,
        velocity=40.0,
        chord=1.0,
        span=1.5,
        lift_coefficient=0.5,
        drag_coefficient=0.02
    )

    assert lift > 0
    assert drag > 0


def test_diffuser_reduces_velocity():
    result = calculate_diffuser(
        inlet_area=0.2,
        outlet_area=0.4,
        inlet_velocity=40.0,
        density=1.225,
        inlet_pressure=101325.0
    )

    assert result["outlet_velocity"] == pytest.approx(20.0)
    assert result["outlet_pressure"] > 101325.0


def test_diffuser_rejects_contraction():
    with pytest.raises(ValueError):
        calculate_diffuser(
            inlet_area=0.4,
            outlet_area=0.2,
            inlet_velocity=40.0,
            density=1.225,
            inlet_pressure=101325.0
        )
