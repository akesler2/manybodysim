from mbsim.types import Mat2
from mbsim.state.universe import Universe

def boundary_mask(pos: Mat2, height: float, width: float) -> tuple[bool, bool, bool, bool]:
      # Create a mask for particles outside the boundaries
   # pos[:,0] is all x coordinates, pos[:,1] is all y coordinates
   out_left = pos[:,0] < 0
   out_right = pos[:,0] > width
   out_bottom = pos[:,1] < 0
   out_top = pos[:,1] > height

   return out_left, out_right, out_bottom, out_top


def reflective_boundary(pos: Mat2, vel, height: float, width: float) -> tuple[Mat2, Mat2]:
    # Reflects particles off the boundaries of the simulation
    # Returns the new positions and velocities

   out_left, out_right, out_bottom, out_top = boundary_mask(pos, height, width)

   # Outside left
   pos[out_left,0] = - pos[out_left, 0]
   vel[out_left,0] = - vel[out_left, 0]

   # Outside right
   pos[out_right,0] = 2*width - pos[out_right, 0]
   vel[out_right,0] = - vel[out_right, 0]

   # Outside bottom
   pos[out_bottom,1] = - pos[out_bottom, 1]
   vel[out_bottom,1] = - vel[out_bottom, 1]

   # Outside top
   pos[out_top,1] = 2*height - pos[out_top, 1]
   vel[out_top,1] = - vel[out_top, 1]

   return pos, vel
