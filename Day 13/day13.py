# Part 1

# Reading and storing the input

with open('input.txt') as f:
  lines = [line.strip() for line in f]

# This list will contain the marked points as couples of coordinates.
paper = []

# This list will contain the axis guiding the folds, as couples of integers.
# For example the axis x=a is (a, 0), the axis y=b is (0,b).
instructions = []  
                    
# Read the non-spacing lines.
# We check wheter a line starts with 'f' to distinguish instructions and points.
for line in filter(lambda x: len(x) > 0, lines):
    if line[0] == 'f':
      direction, intercept = line.split('=')
      if direction[-1] == 'x':
        axis = (int(intercept), 0)
      elif direction[-1] == 'y':
        axis = (0, int(intercept))
      instructions.append(axis)
    else:
      point = tuple(int(z) for z in line.split(','))
      paper.append(point)


# Apply fold to a point.

def reflect(point, axis):
  # Given a point and a fold instruction (in the format above), returns the new
  # position of the point if it is affected by the fold, None otherwise.

  # As per the puzzle, the folds are right to left and bottom to top. So a point
  # is affected by a fold if the fold axis is vertical at its left or horizontal
  # above it.
  if all(a >= b for (a, b) in zip(point, axis)):
    # Condense horizontal and vertical cases.
    reflection = tuple(2 * b - a if b != 0 else a for (a,b) in zip(point, axis))
    return reflection
  else:
    return

# Apply fold to whole paper.

def fold(paper, axis):
  # Given a list of points and a fold instruction 
  # return the list of points after the fold. We pass through sets to avoid
  # repetitions.
  folded = set()
  for point in paper:
    reflection = reflect(point, axis)
    if reflection:
      folded.add(reflection)
    else:
      folded.add(point)
  return list(folded)
      
# The answer is the number of marked points after the first fold.

answer = len(fold(paper, instructions[0]))
print(f'Part 1: {answer}')


# Part 2

# Store the original in folded.
folded = [point for point in paper]

# Iteratively apply all the folding instructions to folded and update it.
for axis in instructions:
  folded = fold(folded, axis)

# Create a display to see the result of the folds.

# Sizes for the display
x = max([point[0] for point in folded])
y = max([point[1] for point in folded])

# Higlights with '#' the points appearing, prints '.' otherwise.
display =[['#' if (i, j) in folded else '.' for i in range(x + 1)]
          for j in range(y + 1)]

print('Part 2:')
for line in display:
  print(''.join(line))

      
  
