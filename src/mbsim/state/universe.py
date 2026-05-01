from mbsim.types import Mat2, Masses


class Universe:
    def __init__(self, particles: tuple(Mat2, Mat2, Masses), width, height):
        self.positions, self.velocities, self.masses = particles
        self.width = width
        self.height = height

    def update(self, pos: Mat2, vel: Mat2):
        self.positions = pos
        self.velocities = vel

    def add_particle(self, particle):
        self.particles.append(particle)

    def remove_particle(self, particle):
        self.particles.remove(particle)

    def get_boundaries(self):
        return self.boundaries
