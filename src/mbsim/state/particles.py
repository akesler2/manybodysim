import numpy as np


def random_particle_gen(n, particle_init):
    # Generates particles with a uniform distribution of positions within the simulation boundaries
    # and a normal distribution of velocities 

    rng = np.random.default_rng(particle_init.seed)

    # Generate positions uniformly within the simulation boundaries
    pos = rng.random((n, 2)) * np.array([particle_init.width, particle_init.height])
    
    # Generate velocities with a normal distribution around the mean velocity
    theta = rng.uniform(0, 2*np.pi, size=n)
    unit_vec = np.column_stack([np.cos(theta), np.sin(theta)])
    speed = rng.normal(loc=particle_init.v_mean, scale=particle_init.v_std, size=n)
    vel = speed[:, np.newaxis] * unit_vec
    
    # Generate masses
    masses = particle_init.mass * np.ones(n,)
    return pos, vel, masses


