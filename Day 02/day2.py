# Part 1

# Create a dictionary of the total movement: {forward: x, up: y, down: z}

movement = {'forward': 0, 'up': 0, 'down': 0}

# Read the moves from input in lists [direction, magnitude].
# Increase the total movement in the given direction by the given magnitude.

with open('input.txt') as f:
  for line in f:
    move = line.split()                                                        
    movement[move[0]] += int(move[1])                                          

total_forward = movement['forward']
total_depth = movement['down'] - movement['up']

answer = total_forward * total_depth

print(f'Part 1: {answer}')


# Part 2

# Initialize global variables aim, depth and horizontal positions.

aim = 0
depth = 0
horizontal = 0

# Define functions for the possible movements.

def forward(x):
  global aim, depth, horizontal
  horizontal += x
  depth += aim * x

def up(x):
  global aim
  aim -= x

def down(x):
  global aim
  aim += x

# Label the functions in a dictionary to interpret the input.

movement = {'forward': forward, 'up': up, 'down': down}

# Read the moves from input in lists [direction, magnitude].
# Perform the moves according to the movement dict.

with open('input.txt') as f:
  for line in f:
    move = line.split()                                                        
    movement[move[0]](int(move[1]))                                           

answer = depth * horizontal
print(f'Part 2: {answer}')
  
