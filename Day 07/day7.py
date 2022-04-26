# Part 1

# Imports
import numpy as np

# Store the input as an array of integers representing each crab position
with open('input.txt') as f:
  data = next(f).strip().split(',')

crabs = np.array([int(datum) for datum in data])

# Array of all positions a crab can have
positions = np.arange(max(crabs))

# Distance matrix

def d_matrix(x, y, f=abs):
  # Given two vectors x, y, and a function f, returns the matrix
  # A_ij = f(x_i - y_j)
  m, = x.shape
  n, = y.shape
  x = x.reshape(m,1)
  x = np.pad(x, [(0, 0), (0,1)], mode='constant', constant_values=1)
  y = y.reshape(1,n)
  y = np.pad(y, [(1, 0), (0, 0)], mode='constant', constant_values=-1)
  matrix = f(np.matmul(x, y))
  return matrix

# Compute the distance matrix between all possible crab positions and the
# actual crab positions, with f = absolute value.
# The answer is the minimum of the sums along the rows in the distance matrix.

distance = d_matrix(positions, crabs, f=abs)
answer = np.min([np.sum(distance[i]) for i in range(len(distance))])

print(f'Part 1: {answer}')

# Part 2

def fuel(n):
  # Returns the fuel cost of moving n steps.
  n = np.abs(n)
  n = n * (n + 1) // 2
  return n

# Compute the distance matrix between all possible crab positions and the
# actual crab positions, with f = fuel.
# The answer is the minimum of the sums along the rows in the distance matrix.

distance = d_matrix(positions, crabs, fuel)
answer = np.min([np.sum(distance[i]) for i in range(len(distance))])

print(f'Part 2: {answer}')


