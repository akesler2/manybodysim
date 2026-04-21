import numpy as np


def inertial_frame()
    return np.array([0, 0, 0])

def constant_force(force):
    return force

def gravitational_force(mass1, mass2, distance):
    return mass1 * mass2 / distance**2
