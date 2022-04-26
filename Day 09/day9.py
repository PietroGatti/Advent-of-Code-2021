# Part 1

# Imports
import numpy as np

# Store the data in a numpy matrix
with open('input.txt') as f:
  matrix = np.array([[int(x) for x in row.strip()] for row in f])

# Neighbors

def ngbs(point, matrix, condition=lambda *args: True):
  # Takes a matrix array, the point coordinates of one of its entries and a
  # condition they have to satisfy.
  # Returns the set of point coordinates of the entry's neighbors up, down,
  # left, right, provided they exist and they satisfy the specified condition.

  m, n = matrix.shape                                                       
  i, j = point                                                            
  if not condition(point, matrix):
    return None
  neighbors = set()

  if i > 0:                                                                 
    neighbors.add((i-1,j))				# up
  if i < m - 1:
    neighbors.add((i+1,j))                           # down
  if j > 0:
    neighbors.add((i,j-1))                           # left
  if j < n - 1:
    neighbors.add((i,j+1))                           # right
  
  # filter the result for condition
  neighbors = set(nb for nb in neighbors if condition(nb, matrix))
  return neighbors

# A low point is an entry in the matrix that its strictly lower than all its
# four neighbors. We read the matrix and identify the low points. Each low point
# contributes to the answer with its value + 1.

answer = 0
for i in range(len(matrix)):
  for j in range(len(matrix[i])):
    if matrix[i][j] < min([matrix[nb] for nb in ngbs((i,j), matrix)]):
      answer += matrix[i][j] + 1

print(f'Part 1: {answer}')




# Part 2

def not_nine(point, matrix):
  # function to determine if the entry at specified point coordinates is not 9
  # in the given matrix.
  i, j = point
  return matrix[i][j] != 9

def get_basin(point, matrix, condition):
  # Takes a matrix, the point coordinates of one of its entries and a condition
  # they have to satisfy.
  # Returns the basin of that point (as in the puzzle description).
  # Think of the matrix as having holes at entries not satisfying the condition,
  # this function then returns the connected component of the given point as a
  # set of point coordinates.

  if not condition(point, matrix):
    return set()
  basin = {point}
  boundary = ngbs(point, matrix, condition)

  # We construct the basin following this iteration:
  # 0. Start with the basin as the set containing only the given point.
  # 1. Take the basin boundary, that is the set of all its neighboring points
  #    that are not already in basin.
  # 2. If there is no boundary we completed the basin.
  # 3. Add the boundary to the basin. Go to step 1.
  
  while boundary:
    new_boundary = set()
    for point in boundary:
      neighbors = ngbs(point, matrix, condition).difference(basin)
      basin = basin.union(neighbors)
      new_boundary = new_boundary.union(neighbors)
    boundary = new_boundary
  return basin

# Construct all the basins for the given matrix.

# Keep track of the points to see, that is, not already included in some basin.
to_see = set((i, j) for i in range(len(matrix))
             for j in range(len(matrix[i])) if not_nine((i,j), matrix))

basins = []

# Iterate over the points not already included in some basin. Construct their
# basin. Update the set of points to see accordingly.
while to_see:
  point = next(iter(to_see))
  basin = get_basin(point, matrix, not_nine)
  basins.append(basin)
  to_see = to_see.difference(basin)

# List of the basins' sizes.
basins_sizes = [len(basin) for basin in basins]

# The answer is the product of the 3 biggest basins.
answer = 1 
for i in range(3):
  biggest = basins_sizes.pop(basins_sizes.index(max(basins_sizes)))
  answer *= biggest
print(f'Part 2: {answer}')
    
    
   












