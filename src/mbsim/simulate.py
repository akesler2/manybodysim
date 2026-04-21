import numpy as np
from objects import Universe, Particle
from forces import inertial_frame, constant_force, gravitational_force

# Set universe parameters
size  = (1000, 1000)
time_duration = 100
time_step = 0.01
force_field = inertial_frame()
particle_num = 10
particle_mass = 1

# Seed particles with ramdom positions and velocities
particles = []
for i in range(particle_num):
    position = np.random.rand(2) * size
    velocity = np.random.rand(2) * 100
    particles.append(Particle(mass, position, velocity))

# Create universe
universe = Universe(particles, size)

# Simulate universe
for i in range(time_duration):
    universe.update()

    return universe