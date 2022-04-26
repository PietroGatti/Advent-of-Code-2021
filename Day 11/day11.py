# Part 1

# Imports
from itertools import product
import numpy as np

# Store the input as a matrix of integers
with open('input.txt') as f:
  lines = [line.strip() for line in f]

data = np.array([[int(num) for num in line] for line in lines])

# Find the neighbors

increments = {-1, 0, 1}
directions = [(x, y) for x, y in product(increments, increments) if (x, y) != (0,0)]

def ngbs(point, matrix):
  # Given a couple (i, j) of indeces in a matrix, returns the list of its 
  # (at most 8) neighboring couples of indeces.
  m, n = matrix.shape
  i, j = point
  neighbors = [(i + x, j + y) for x, y in directions if (0 <= i + x < m and 0 <= j + y < n)]
  return neighbors

# Construct a function that determines if at some step a  point (octopus) has
# flashed and carries over, recursively, the effects of flashing on the
# neighboring points.

def flash(start, matrix, flashed=set()):
  # Recursive function that takes a point, a matrix and the points 
  # that have already flashed.
  # Checks if a point have flashed and carries the effect of flashing to its
  # neighbors, modifying the matrix and keeping track of the points that have
  # flashed.
  # It calls itself recursively on the neighbors of the starting point.

  # If the entry is not 0 there is nothing to do.
  if matrix[start] != 0 or start in flashed:
    return
  else:
    # If the entry is 0 add the point to flashed.
    flashed.add(start)
    neighbors = ngbs(start, matrix)
    # Take the neighboring points that are not flashing right now or have not
    # flashed and increase them by 1.
    neighbors_not_zero = [n for n in neighbors if matrix[n] != 0]
    for point in neighbors_not_zero:
      matrix[point] = (matrix[point] + 1) % 10
    # Reiterate for the neighbors.
    for point in neighbors:
      flash(point, matrix, flashed)  
  

# Copy of the input data.
generation = np.copy(data)

# List all points in the matrix.                                                    
points = [(i, j) for i in range(generation.shape[0])                           
          for j in range(generation.shape[1])]

# For the required number of steps, we iterate the following process.
# All entries are increased by 1 modulo 10, the function flash is called to
# carry over the effect of any point flashing in this step. The set flashed
# keeps track of the points that have flashed during each step. Summing their
# cardinality we get the answer.
steps = 100
answer = 0

for step in range(steps):
  flashed = set()
  generation = (generation + np.ones(generation.shape)) % 10
  for point in points:
    flash(point, generation, flashed)
  answer += len(flashed)

print(f'Part 1: {answer}')

# Part 2

# Copy of the input data.
generation = np.copy(data)

# Iterate as in Part 1, until all entries are 0. The answer is the number of
# steps required.
answer = 1
while True:
  flashed = set()
  generation = (generation + np.ones(generation.shape)) % 10
  for point in points:
    flash(point, generation, flashed)
  if (generation == np.zeros(generation.shape)).all():
    break
  else:
    answer += 1

print(f'Part 2: {answer}')





