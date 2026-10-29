"""
AIRFOIL GEOMETRY GENERATOR
==========================

Generates NACA four-digit airfoil coordinates.

Output:
    x_upper, y_upper
    x_lower, y_lower

Coordinates are in metres.
"""

import numpy as np


def generate_naca4(code, chord=1.0, points=150):
    """Generate upper and lower surfaces of a NACA 4-digit airfoil."""

    if len(code) != 4 or not code.isdigit():
        raise ValueError("Use a four-digit NACA code.")

    if chord <= 0 or points < 20:
        raise ValueError("Chord must be positive and points >= 20.")

    m = int(code[0]) / 100.0
    p = int(code[1]) / 10.0
    thickness = int(code[2:]) / 100.0

    # Cosine spacing provides more points near the leading edge.
    beta = np.linspace(0.0, np.pi, points)
    x = chord * (1.0 - np.cos(beta)) / 2.0

    xc = x / chord

    # NACA thickness distribution.
    yt = 5.0 * thickness * chord * (
        0.2969 * np.sqrt(xc)
        - 0.1260 * xc
        - 0.3516 * xc**2
        + 0.2843 * xc**3
        - 0.1015 * xc**4
    )

    yc = np.zeros_like(x)
    dyc_dx = np.zeros_like(x)

    if m > 0 and p > 0:
        front = xc < p
        rear = ~front

        yc[front] = (
            m / p**2
            * (2 * p * xc[front] - xc[front]**2)
            * chord
        )

        yc[rear] = (
            m / (1 - p)**2
            * (
                1 - 2 * p
                + 2 * p * xc[rear]
                - xc[rear]**2
            )
            * chord
        )

        dyc_dx[front] = (
            2 * m / p**2 * (p - xc[front])
        )

        dyc_dx[rear] = (
            2 * m / (1 - p)**2 * (p - xc[rear])
        )

    theta = np.arctan(dyc_dx)

    x_upper = x - yt * np.sin(theta)
    y_upper = yc + yt * np.cos(theta)

    x_lower = x + yt * np.sin(theta)
    y_lower = yc - yt * np.cos(theta)

    return x_upper, y_upper, x_lower, y_lower
