# Part 1

# Imports
import re
import numpy as np

# Cuboid class.

class Cuboid:

  def __init__(self, x1, x2, y1, y2, z1, z2):
    # A cuboid is determined by the a 6-tuple of it vertices coordinates
    # (xmin, xmax, ymin, ymax, zmin, zmax).
    self.xmin = x1
    self.xmax = x2
    self.ymin = y1
    self.ymax = y2
    self.zmin = z1
    self.zmax = z2
  
  # String representation. Not used.
  def __str__(self):
    return str(((self.xmin, self.xmax),
                (self.ymin, self.ymax),
                (self.zmin, self.zmax)))

# Valid cuboid.

def valid(cuboid):
  # Checks if a 6-uple of integers can represent a cuboid.
  return ((cuboid.xmin <= cuboid.xmax) and 
          (cuboid.ymin <= cuboid.ymax) and (cuboid.zmin <= cuboid.zmax))
  
# Cuboids intersection.

def c_intersect(c1, c2): 
  # Given two cuboids, if they intersect, returns their intersection (it is a
  # cuboid). If they don't, returns None.
  
  # First cuboid.                                                    
  c1x1 = c1.xmin
  c1x2 = c1.xmax
  c1y1 = c1.ymin
  c1y2 = c1.ymax
  c1z1 = c1.zmin
  c1z2 = c1.zmax

  # Second cuboid.
  c2x1 = c2.xmin
  c2x2 = c2.xmax
  c2y1 = c2.ymin
  c2y2 = c2.ymax
  c2z1 = c2.zmin
  c2z2 = c2.zmax

  # Interesction.
  c = Cuboid(max(c1x1, c2x1), min(c1x2, c2x2),
             max(c1y1, c2y1), min(c1y2, c2y2),
             max(c1z1, c2z1), min(c1z2, c2z2)
            )
  
  # Check if they actually intesrect before returning.
  if valid(c):
    return c
  else:
    return None

# Multicubioids and operations.
# A multicuboid is a list of mutually disjoint cuboids.

# Remove a sub-cuboid.
  
def c_remove(c1, c2):
  # Remove a subcuboid c2 from a cuboid c1.
  # Returns the resulting multicuboid.
                                                         
  if c2 == None:
    # Nothing to remove.                                                            
    return [c1]
  
  # First cuboid.       
  c1x1 = c1.xmin
  c1x2 = c1.xmax
  c1y1 = c1.ymin
  c1y2 = c1.ymax
  c1z1 = c1.zmin
  c1z2 = c1.zmax
  
  # Second cuboid.
  c2x1 = c2.xmin
  c2x2 = c2.xmax
  c2y1 = c2.ymin
  c2y2 = c2.ymax
  c2z1 = c2.zmin
  c2z2 = c2.zmax

  result = [Cuboid(c1x1, c2x1-1, c1y1, c1y2, c1z1, c1z2),
            Cuboid(c2x1, c2x2, c2y2+1, c1y2, c1z1, c1z2),
            Cuboid(c2x1, c2x2, c1y1, c2y1-1, c1z1, c1z2),
            Cuboid(c2x1, c2x2, c2y1, c2y2, c1z1, c2z1-1),
            Cuboid(c2x1, c2x2, c2y1, c2y2, c2z2+1, c1z2),
            Cuboid(c2x2+1, c1x2, c1y1, c1y2, c1z1, c1z2)
           ]
  
  # Filtering for valid, ensures that we are not listing 0-volume cuboids or
  # other degenerations.
  return [c for c in result if valid(c)]

# Difference.

def mc_diff(multicuboid, c2):
  # Returns the set theoretical difference between a multicuboid and a cuboid.
  # It is still a multicuboid.                                             
  if c2 == None:
    # Nothing to remove.
    return multicuboid

  result = []
  for c in multicuboid:
    ci = c_intersect(c, c2)
    result += (c_remove(c, ci))
  return result

# Union.

def mc_union(multicuboid, c2):
  # Returns the union between a multicuboid and a cuboid.
  # It is still a multicuboid.                                              
  return mc_diff(multicuboid, c2) + [c2]

# Volume.

def c_vol(c):
  # Returns the volume of a cuboid.
  # That is the number of points with integral coordinates it contains.                                                               
  return (c.xmax - c.xmin + 1) * (c.ymax - c.ymin + 1) * (c.zmax - c.zmin + 1)


def mc_vol(mc):
  # Returns the volume of a multicuboid.                                                              
  vol = 0
  for c in mc:
    vol += c_vol(c)
  return vol


# Store the data.
# Instructions will be a list of tuples (switch, cuboid) with switch = 1 for on,
# switch = 0 for off
with open('input.txt') as f:
  matches = [re.findall(r'on|off|-?\d+', line) for line in f]

instructions = []
for match in matches:
  if match[0] == 'on':
    switch = 1
  if match[0] == 'off':
    switch = 0
  cuboid = Cuboid(*map(int, match[1:]))
  instructions.append((switch, cuboid))

# Execute instructions.

def execute(instr):
  # Executes a list of instructions, switching on or off the cuboids.
  # Returns the multicuboid corresponding to the points that are on.
  # Initialize result as an empty multicuboid.
  result = []
  
  for switch, cuboid in instr:
    if switch == 1:                                                                
      result = mc_union(result, cuboid)                                          
    if switch == 0:                                                                
      result = mc_diff(result, cuboid)
  
  return result
    
# Region for Part 1.

region = Cuboid(*(-50, 50)*3)

# Restrict instructions to the region.

reduced_instructions = []

for switch, cuboid in instructions:
  intersection = c_intersect(cuboid, region)
  if intersection:
    reduced_instructions.append((switch, intersection))

# Execute the reduced instructions.

reduced_on = execute(reduced_instructions)

# The answer is the volume of the region that is on.

answer = mc_vol(reduced_on)
print(f'Part 1: {answer}')

# Part 2

# Execute the instructions.

on = execute(instructions)

# The answer is the volume of the region that is on.

answer = mc_vol(on)
print(f'Part 2: {answer}')
 
  

