# Part 1

# Imports
import re
from itertools import product

# Store the input target as the coordinates of its corners.
with open('input.txt') as f:
  data = f.read()

corners = re.findall(r'-?\d+', data)
min_x, max_x, min_y, max_y = map(int, corners)

# Construct class for particles.
class Particle:
  
  def __init__(self, position, x_velocity, y_velocity):
    # initialize particle given position, and velocities                     
    self.x = position[0]
    self.y = position[1]
    self.x_velocity = x_velocity
    self.y_velocity = y_velocity

  @property
  def position(self):
    # Returns current position of a particle.
    return (self.x, self.y)

  def move(self): 
    # Method that moves the particle following the dynamics of the puzzle.                                                           
    self.x += self.x_velocity
    self.y += self.y_velocity
    # rhs is 1 when x_velocity>0, -1 when x_velocity<0 and 0 when x_velocity=0
    self.x_velocity -= (self.x_velocity > 0) - (self.x_velocity < 0)           
    self.y_velocity -= 1

  def in_target(self):
    # Returns True when particle is in target                                                    
    return (
        self.x >= min_x and
        self.x <= max_x and
        self.y >= min_y and
        self.y <= max_y
    )

  def out_of_target(self):
    # True when the particle is doomed to not hit the target.
    # We use a sufficient condition for this dynamics.                                             
    return (                                                                   
        (self.x > max_x and self.x_velocity >= 0) or
        (self.y < min_y and self.y_velocity <= 0)
    )

  def hit(self):
    # method to move a particle until either it hits the target: returning True
    # or the particle is never reaching the target: returning False.
    while not self.in_target():
      self.move()
      if self.out_of_target():
        return False
    return True
        
# We need to deal with all possible target relative positions to the start.
# We deduce for the possible initial velocities, necessary conditions to have
# solutions:
# - If min_x >= 0, then 0 <= initial_x_velocity <= max_x.
# - If min_x < 0, then min_x <= initial_x_velocity <= max(0, max_x).
# - If max_y > 0, then min_y <= initial_y_velocity <= abs(max_x) + max_y.
#   More precisely, there could be other solutions, but they would imply the
#   existence of infinitely many others, which we exclude.
# - If max_y <= 0, then min_y <= initial_y_velocity < -min_y is a sufficient
#   condition.

# Store the initial velocities bounds.
lower_x = min(0, min_x)
upper_x = max(0, max_x)
lower_y = min_y
if max_y > 0:
  upper_y = abs(max_x) + max_y
elif max_y <= 0:
  upper_y = -min_y

# List of all the possible initial velocities respecting the bounds.
initial_velocities = [(v_x, v_y) for v_x in range(lower_x, upper_x + 1)
                                 for v_y in range(lower_y, upper_y + 1)]


# Use the hit method for all the possibile initial velocities. Starting with
# the highest vertical velocity, the first time we hit the target we are
# guaranteed to hit the highest point.

for v_y in range(upper_y, lower_y - 1, -1):
  for v_x in range(lower_x, upper_x + 1):
    particle = Particle((0,0), v_x, v_y)
    if particle.hit():
      # highest point reached
      answer = int(v_y*(v_y+1)/2)                                               


print(f'Part 1: {answer}')

# Part 2

# Initialize points counter.
answer = 0

# Iterate over all the possible initial velocities respecting the bounds.
for (v_x, v_y) in initial_velocities:
  particle = Particle((0,0), v_x, v_y)
  if particle.hit():
    answer += 1

print(f'Part 2: {answer}')
  


  




  
