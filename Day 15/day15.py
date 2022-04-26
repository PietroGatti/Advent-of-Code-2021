# Disclaimer: this is suboptimal. Made before knowing about Dijstrka
# algorithm or A*.

# Part 1

# Store the data as a list of lists of integers.
with open('input.txt') as f:
  lines = [line.strip() for line in f]

data = [[int(x) for x in line] for line in lines]

# Previous points.

def prev(point):
  # Given a point indeces in the matrix, returns the indeces of the points 
  # immediately on the left and immediately above.
  i, j = point
  previous = []
  if i > 0:
    previous.append((i-1, j))
  if j > 0:
    previous.append((i, j-1))
  return previous

# Store size of the (square) matrix data.
n = len(data)

# We will store the shortest paths into a dictionary:
# {point: length of the shortest path to point}.
dist_map = {}

# We read the matrix from the left to right, top to bottom following all the
# anti-diagonals, giving a first value in dist_map to the points belonging to
# the top-left half of the matrix.
# For now, the length of the shortest path to a given point is its risk value 
# plus the minimum of the length of the shortest paths to its predecessors.
for d in range(n):
  for k in range(d+1):
    dist_map[(k, d - k)] = min([dist_map[p] for p in prev((k, d - k))],
                               default=-data[0][0]) + data[k][d - k]

# We fill the second half of dist-map in the same way.
second_half = [(i, j) for i in range(n) for j in range(n) if i+j >= n]

for point in second_half:
  i, j = point
  dist_map[point] = min([dist_map[p] for p in prev(point)],
                        default=-1) + data[i][j]

# The dist_map at this stage is very likely to not be optimal.
# Update dist_map at each point considering the values in its neighbors and
# repeat the process until dist_map does not update anymore.


def ngbs(point, size):
  # returns the neighboring points of an entry
  n = size                                                    
  i, j = point  # row, col
  neighbors = []

  if i > 0:                                                                 
    neighbors.append((i-1,j))        # up
  if i < n - 1:
    neighbors.append((i+1,j))        # down
  if j > 0:
    neighbors.append((i,j-1))        # left
  if j < n - 1:
    neighbors.append((i,j+1))        # right
  return neighbors

# update the dist_map recursively, . These are precisely 

# Update a distance map.

def update(dist_map, to_check, matrix=data):
  # Recursive function. To avoid unuseful computations, to_check stores the
  # list of points that may change value at the next iteration. Those are
  # precisely the neighbors of points updated during the current iteration.
  # The recursion stops when there are no more points to update.
  
  new_dist_map = {k: v for k, v in dist_map.items()}
  new_to_check = []
  if not to_check:
    return new_dist_map
  for point in to_check:
    i, j = point
    new_value = matrix[i][j] + min([new_dist_map[p] for p in ngbs(point, n)])
    if new_value < new_dist_map[point]:
      new_dist_map[point] = new_value
      new_to_check += ngbs(point, n)

  # delete repetitions. Faster then filtering inside loop. 
  new_to_check = list(set(new_to_check))                                      
                                                                               
  return update(new_dist_map, new_to_check, matrix)

# Call the update function on the pre-filled dist_map. The answer is the value
# of the dist_map for the point (n-1, n-1).

keys = [key for key in dist_map]
new = update(dist_map, keys)
answer =  new[(n-1,n-1)]
print(f'Part 1: {answer}')

# Part 2

# ssum is a 'special sum'. When it exceeds 9 it starts over from 1.
def ssum(a,b):
  return a + b if a + b <= 9 else (a + b + 1) % 10

# The big matrix that is 5x5 times the original data and uses ssum.
big = [[0 for  j in range(5 * n)] for i in range(5 * n)]
for i in range(len(big)):
  for j in range(len(big[i])):
    big[i][j] = ssum(data[i%n][j%n], i // n + j // n)

    
# Repeat what done in Part 1 for the big matrix.
n = len(big)
dist_map = {}

for d in range(n):
  for k in range(d+1):
    dist_map[(k, d - k)] = min([dist_map[p] for p in prev((k, d - k))],
                               default=-big[0][0]) + big[k][d - k]

second_half = [(i, j) for i in range(n) for j in range(n) if i+j >= n]

for point in second_half:
  i, j = point
  dist_map[point] = min([dist_map[p] for p in prev(point)],
                        default=-big[0][0]) + big[i][j]

keys = [key for key in dist_map]
new = update(dist_map, keys, big)
answer =  new[(n-1,n-1)]
print(f'Part 2: {answer}')
