def apply_velocity_boundaries(u, v, solid, inlet_velocity):

    u[:, 0] = inlet_velocity
    v[:, 0] = 0.0

    u[:, -1] = u[:, -2]
    v[:, -1] = v[:, -2]

    u[0, :] = 0.0
    u[-1, :] = 0.0
    v[0, :] = 0.0
    v[-1, :] = 0.0

    u[solid] = 0.0
    v[solid] = 0.0

    return u, v
