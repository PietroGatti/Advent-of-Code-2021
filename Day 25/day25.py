# Imports
from math import ceil

# Store the data. Represent the ocean floor configuration as a list of lists of
# strings.

with open('input.txt') as f:
  input_floor = [list(line.strip()) for line in f]

# Directions and shifts.
directions = {'>' : (1, 0), 'v' : (0, 1)}

def shift(floor, direction):
  # Returns a shifted copy of the ocean floor shifted by the direction
  # specified. Directions are '>': right, 'v', down.
  if direction == '>':
    return [line[1:] + [line[0]] for line in floor]
  if direction == 'v':
    return floor[1:] + [floor[0]]

# One step.

def get_moves(floor, direction):
  # Given a floor configuration and a direction, returns the list of possible
  # that the cucumber facing that direction can perform.
  # Moves will be in the form (direction, starting_position)

  moves = []
  shifted = shift(floor, direction)

  # We compare the floor wiht its shifted version to see which cucumber can
  # move.
  for i, (line_f, line_s) in enumerate(zip(floor, shifted)):
    for j, (element_f, element_s) in enumerate(zip(floor[i], shifted[i])):
      if element_f == direction and element_s == '.':
        moves.append((direction, (i, j)))
  return moves

def move(floor, moves, height, width):
  # Apllies a list of moves to floor and returns the result.
  new_floor = floor[:]
  for d, (i, j) in moves:
    a, b = directions[d]
    new_floor[i][j] = '.'
    new_floor[(i + b) % height][(j + a) % width] = d
  return new_floor

# Evolution of the floor.

def get_directions():
  # Iterator that yields the directions alternating.
  while True:
    for d in ['>', 'v']:
      yield d

def evolve(floor):
  # Evolves the floor configuration and returns the number of steps when there
  # are no other possible moves.

  height, width = len(floor), len(floor[0])
  steps = 0
  directions_iter = get_directions()

  for direction in directions_iter:
    steps += .5
    moves = get_moves(floor, direction)
    if moves:
      floor = move(floor, moves, height, width)
      changed = True
    elif not changed:
      break
    else:
      changed = False
    
  return ceil(steps)

# To get the answer, apply evolve to the input floor configuration.

answer = evolve(input_floor)

print(f'Answer: {answer}')

