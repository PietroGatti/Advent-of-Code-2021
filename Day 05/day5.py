# Imports
from collections import Counter
from math import gcd


# Part 1

# Store the input as a list of lines, where each line is determined by a list
# [(x1, y1), (x2, y2)] where (x1, y1) are the coordinates of the starting point
# and (x2, y2) are the coordinates of the ending point.

with open('input.txt') as f:
  data = [row for row in f]
                                     
data = [row.strip().split('->') for row in data]                               
data = [[point.split(',') for point in row] for row in data]                   
lines = [[(int(x), int(y)) for x, y in points] for points in data]

                                                                 
# The following functions return the vertical and horizontal spans of a given line, respectively

def ver(line):
  # given a line in the format above, returns the lenght of its projection to
  # the vertical axis.
  return line[1][1] - line[0][1]

def hor(line):
  # given a line in the format above, returns the lenght of its projection to
  # the horizontal axis.
  return line[1][0] - line[0][0]

def direction(line):
  # given a line in the format above, returns a list of discrete increments to
  # move from the first to the last point of the line in an integral lattice.
  x = hor(line)
  y = ver(line)
  d = gcd(x,y)
  x, y = x // d, y // d
  direction_range = [(i * x, i * y) for i in range(0, d + 1)]
  return direction_range

def draw(line, condition=lambda x: True):
  # if a line satisfy the condition specified in the parameters, returns a list
  # of points the line covers in an integral lattice.
  # Returns None otherwise
  if condition(line):
    (x1, y1) = (line[0][0], line[0][1])
    return [(x1 + i, y1 + j) for (i, j) in direction(line)]
  else:
    return []

def ver_or_hor(line):
  # Returns True if a line is vertical or horizontal, False otherwise.
  # This will the condition using draw.
  ver_bool = not bool(hor(line))	# A line is vertical when it has 0 horizontal span.
  hor_bool = not bool(ver(line))        # Horizontal if 0 vertical span.
  return ver_bool or hor_bool
  
# Draw all the lines in input that are vertical or horizontal.
# drawn_dict stores how many times each point has been drawned.

drawn = []
for line in lines:
  drawn += draw(line, ver_or_hor)

drawn_dict = Counter(drawn)

# Count how many points have been drawn at least twice.

answer = 0
for point in drawn_dict:
  if drawn_dict[point] >= 2:
    answer += 1


print(f'Part 1: {answer}')

# PART 2

# Remark: the only thing we need to change from part 1 is to extend the
# verification function to include also 45 degrees lines.

def ver_or_hor_or_diag45(line):
  ver_bool = not bool(hor(line))                                               
  hor_bool = not bool(ver(line))
  # A line is 45deg diagonal when horizontal and vertical spans are the same in
  # absolute value                                                
  diag45_bool = not bool(abs(hor(line)) - abs(ver(line)))                      
  return ver or hor or diag45

# Draw all the lines in input that are vertical, horizontal or diagonal of 45
# degrees. drawn_dict stores how many times each point has been drawned.

drawn = []
for line in lines:
  drawn += draw(line, ver_or_hor_or_diag45)

drawn_dict = Counter(drawn)

# We count and print how many points have been drawn at least twice

answer = 0
for point in drawn_dict:
  if drawn_dict[point] >= 2:
    answer += 1

print(f'Part 2: {answer}')

