# very messy, don't want to rewrite nor comment

# Part 1

# Imports
import numpy as np
from numpy.linalg import norm
from scipy.spatial.distance import cdist
from collections import Counter



# Scanner class

class Scanner:
  
  def __init__(self, beacons):
    # A Scanner is initialized by the list of coordinates of the beacons it
    # sees.
    self.beacons = beacons

    # Distances dictionary. For each beacon, its index in scanner is a key. The
    # corresponding value is a dictionary counting all the euclidean distances
    # between the point at index and all other points in the scanner.
    # Example: scanner = [(0, 0, 0), (1, 0, 0), (0, 1, 0)],
    #          scanner.dist = {0: {0: 1, 1: 2}, 1: {0: 1, 1: 1, sqrt(2): 1},
    #                          2: {0: 1, 1: 1, sqrt(2): 1}}
    # Comparing this attribute between scanners provides a necessary condition
    # for their alignment. 
    self.dist = {i: Counter([norm(beacon - point) for point in self.beacons])
                 for i, beacon in enumerate(self.beacons)}
  
  # Move a scanner
  def move(self, point):
    # Moves a scanner to the specified point by translating all its beacons.
    self.beacons += point
  
  # Representation method, not used.
  def __repr__(self):
    return str(self.beacons)

  



# Common points

def common_points(scanner_1, scanner_2):
  # Given two scanners tests if their dist attribute allow for them to see the
  # at least 12 common beacons.
  # Returns an iterator of pair of points (in their
  # respective local coordinates) at which the two scanners could be aligned.
  # If no such points are found returns False.
 
  dist_1 = scanner_1.dist
  dist_2 = scanner_2.dist
  for i, _ in enumerate(scanner_1.beacons):
    for j, _ in enumerate(scanner_2.beacons):
      if sum((dist_1[i] & dist_2[j]).values()) >= 12:
        # Found two points, one in each scanner, that have at least 12 common
        # dist values. This is a necessary condition for the scanners to be
        # aligned.
        yield scanner_1.beacons[i], scanner_2.beacons[j]
  return False

# Global variable that will store the scanners absolute positions with respect
# to the first scanner, assumed at (0, 0, 0).
scanners_absolute_positions = []                             

# Aligning two scanners.

def aligned(beacons_1, beacons_2):
  # Two scanners are aligned if they share at least 12 beacons in absolute
  # coordinates.
  number_same_points = np.sum((beacons_1[:, None]==beacons_2).all(-1).any(1))
  if number_same_points >= 12:
    return True
  return False

# Create an iterator for the possible rotations.

R = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]])
T = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])

def rotations():
  # Yields all the possible 24 rotations as matrices to apply on the left.
  # The sequence is: R, T, T, T, three times (12 actions)
  #                  Multiply by RTR
  #                  repeat R, T, T, T, three times (remaining 12 actions).                            
  M = np.identity(3)
  for cycle in range(2):
    for step in range(3):
      M = np.einsum('ij,jk->ik', R, M)
      yield M
      for turn in range(3):
        M = np.einsum('ij,jk->ik', T, M)
        yield M
    M = np.einsum('ij,jk,kl,lm->im', R, T, R, M)

def align(scanner_1, scanner_2, point_1, point_2):
  # Given two scanners and a point for each of them, tries to align them, by
  # translating one point to the other and applying all the possible rotations.
  # When succesful, moves the second scanner in the coordinate system of the
  # first, stores the new absolute coordinates of the second scanner and returns
  # True.
  # In use, the first scanner will alsways be considered in the absolute system
  # of reference.
  beacons_1 = np.copy(scanner_1.beacons)
  for M in rotations():
    beacons_2 = np.copy(scanner_2.beacons)
    beacons_2 -= point_2
    beacons_2 = np.einsum('ij,kj->ki', M, beacons_2)
    beacons_2 += point_1
    if aligned(beacons_1, beacons_2): 
      scanners_absolute_positions.append(point_1 - np.einsum('ij,j->i' ,M, point_2))
      scanner_2.beacons[:] = beacons_2                                         
      return True

# Align the scanners in input.

# Store the input as list of scanners.

with open('input.txt') as f:
  data = [line.strip() for line in f if not line.isspace()]

data.append(data.pop(0))
scanners_data = []
scanner = []

for line in data:
  if line[-1] == '-':
    scanners_data.append(Scanner(np.array(scanner)))
    scanner = []
  else:
    scanner.append(np.array(line.split(','), int))

scanners = scanners_data[:]

# The absolute system of reference is the one where the first scanner is at
# (0, 0, 0), so it will be considered as already moved.
# All the other scanners are 'to move', until transformed in absolute coordinates.

moved = [scanners[0]]
to_move = list(scanners[1:])

while to_move:
  for scanner_2 in to_move:
    for scanner_1 in moved:
      common = common_points(scanner_1, scanner_2)
      alignment = False
      if common:
        for point_1, point_2 in common:
          alignment = align(scanner_1, scanner_2, point_1, point_2)
          if alignment:
            moved.append(scanner_2)
            to_move.remove(scanner_2)
            break
      if alignment:
        break

# The scanners are all in the same frame of reference. The answer is the number
# of unique beacons.
         
beacons = [scanner.beacons for scanner in scanners]
beacons = np.unique(np.concatenate(beacons), axis = 0)
answer = len(beacons)

print(f'Part 1: {answer}')

# Part 2

# Take the vector of all scanners absolute positions.  
p = np.array(scanners_absolute_positions)

# Construct the matrix of all manhattan distances. Its maxim entry is the answer.
out = cdist(p, p, metric='cityblock')
answer = int(np.amax(out))

print(f'Part 2: {answer}')





      
      




