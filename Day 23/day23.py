# Part 1

# Imports
from collections import defaultdict
from queue import PriorityQueue
from time import perf_counter as pfc



# Store the input as a string.

with open('input.txt') as f:
  input_string = ''.join([char for char in f.read()])

# The burrows states are stored as strings with characters in '.ABCD'.
# For example the input state.
input_state = ''.join(char for char in input_string if char in '.ABCD') 

# Index the positions in the hallway from 0 to 10.
# spots are the positions at which an amphipod can stop.
spots = [0, 1, 3, 5, 7, 9, 10]

# burrows contains the entrance positions of each room as keys and the respective
# amphipod type as value.
# names is its reverse.
burrows = {2: 'A', 4: 'B', 6: 'C', 8: 'D'}
names = {v: k for k, v in burrows.items()}

# Energy cost associated to each type of amphipod.
energy = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


# A move is a pair of indeces indicating which two entries of the state string
# have to be switched to represent it.

# Blocked paths.

def blocked(start, end, state):
  # Given a start and end position in the hallway, returns True it the path
  # between the two if blocked, False otherwise.
  if start < end:
    direction = 1
  else:
    direction = -1
  for i in range(start + direction, end + direction, direction):
    if state[i] != '.':
      return True 

# Possible moves.

def move_out(burrow, spot, state):
  # Takes a state, a burrow index and a spot index in the hallway.
  # If we can move an amphipod out of the burrow to the given spot, returns
  # the move in the form of start and end index in the state string and its
  # cost in energy.

  # If the path is blocked returns None
  if blocked(burrow, spot, state):
    return
  
  # Keep track of the distance to exit the burrow.
  distance = abs(burrow - spot) + 1

  found = False

  for i in range(10 + (burrow // 2), len(state), 4):
    if state[i] == '.':
      distance += 1
    else:
      if not found:
        amphipod = state[i]
        start = i
        end = spot
        cost = distance * energy[amphipod]
        found = True

      if state[i] != burrows[burrow]:
        # Only in this case the amphipod found can move out.
        return ((start, end), cost)


def move_in(spot, burrow, state):
  # Takes a state, a burrow index and a spot index in the hallway.
  # If we can move an amphipod from the given spot into the specified burrow,
  # returns the move in the form of start and end index in the state string and
  # its cost in energy.

  amphipod = state[spot]

  # If the amphipod is not compatible with the burrow return None.
  if burrows[burrow] != amphipod:
    return

  # If the path is blocked return None
  if blocked(spot, burrow, state):
    return 
  
  # Keep track of the distance to enter the burrow.
  distance = abs(burrow - spot)
  for i in range(10 + (burrow // 2), len(state), 4):
    if state[i] == '.':
      distance += 1
      end = i
    elif state[i] != amphipod:
      return

  start = spot
  cost = distance * energy[amphipod]
  return ((start, end), cost)
    
def make(move, state):
  # Apply a move to a state, returns the new state.
  start, end = move
  new_state = list(state)
  new_state[start], new_state[end] = new_state[end], new_state[start]
  return ''.join(new_state)
  
def possible_moves(state):
  # Given a states, returns the possbile moves and their costs as an iterator.
  for spot in spots:
    amphipod = state[spot]
    if amphipod != '.':
      burrow = names[amphipod]
      x = move_in(spot, burrow, state)
      if x:
        move, cost = x
        yield move, cost
  for burrow in burrows:
    for spot in spots:
      if state[spot] == '.':
        x = move_out(burrow, spot, state)
        if x:
          move, cost = x
          yield move, cost

# To solve the puzzle, we apply Dijkstra aglorithm to the states.

def dijkstra(initial_state, final_state):
  costs = defaultdict((lambda : float('inf')))
  costs[initial_state] = 0
 
  pq = PriorityQueue()
  pq.put((0, initial_state))
  
  while not pq.empty():
    (cost, current_state) = pq.get()
    if current_state == final_state:
      return cost
    
    for move, cost in possible_moves(current_state):
      next_state = make(move, current_state)
      
      old_cost = costs[next_state]
      new_cost = costs[current_state] + cost
      if new_cost < old_cost:
        pq.put((new_cost, next_state))
        costs[next_state] = new_cost

# Store the value of the final state, depends on the puzzle input.
depth = (len(input_state) - 11) // 4
final_state = 11 * '.' + 'ABCD' * depth

# Apply the Dijkstra algorithm to get the answer.
answer = dijkstra(input_state, final_state)
print(f'Part 1: {answer}')

# Part 2

# Modify the input.
to_add = '''  #D#C#B#A#  \n  #D#B#A#C#  \n'''
input_string = input_string[:42] + to_add + input_string[42:]

# Get input and final states.

input_state = ''.join(char for char in input_string if char in '.ABCD') 
depth = (len(input_state) - 11) // 4
final_state = 11 * '.' + 'ABCD' * depth

# Apply the Dijkstra algorithm to get the answer.
answer = dijkstra(input_state, final_state)
print(f'Part 2: {answer}')

