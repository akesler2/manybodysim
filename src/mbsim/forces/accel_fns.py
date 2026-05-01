# defines acceleration functions resulting from different force fields

import numpy as np
from mbsim.types import FloatArray, Mat2, Masses, AccelerationFn

def no_accel(pos: Mat2, vel: Mat2, m: Masses, t: float) -> Mat2:
    n = pos.shape[0]
    return np.zeros((n, 2))

#def constant_accel(pos: Mat2, vel: Mat2, m: Masses, t: float) -> Mat2:
 #   return np.array([0, g])

