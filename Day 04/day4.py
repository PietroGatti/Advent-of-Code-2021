# Part 1

# Storing the input

with open('input.txt') as f:
  lines = [line for line in f]

# the pool of numbers to extract in order
pool = [int(val) for val in lines[0].split(',')]
                             
# Store the boards as a list of lists from the input
boards = []
i = -1
for line in lines[1:]:
  line = line.split()
  if len(line) > 0:
    boards[i].append([int(val) for val in line])
  else:
    boards.append([])
    i += 1

# When a number in a board is drawn from the pool, we replace that number in the board with a -1.

def pick(x, board):
  # replaces x with -1 if x appears in the board and return the new board

  board = [[-1 if element==x else element for element in line] for line in board]
  return board

# The value of a board is the sum of its element that have not been picked yet.
# That is, the sum of its elements that are not -1.


def value(board):
  # returns value of a board

  m = len(board)
  n = len(board[0])
  value = 0
  for i in range(m):
    for j in range(n):
      if board[i][j] > 0:
        value += board[i][j]
  return value


def win(board):
  # Checks if board has has won the bingo (all numbers in a row or column have been picked).
  # and returns its value.
  # returns None otherwise.
 
  N = len(board)
  for i in range(N):
    # starts checking following the diagonal first
    if board[i][i] < 0:
      # if entry in the diagonal has been picked, check the column
      # (there is one redundant comparison)
      for j in range(N):
        if board[i][j] >=0:
          break
        if j == N-1:
          return value(board)
      # if entry in the diagonal has been picked, check the row
      # (there is one redundant comparison)
      for j in range(N):
        if board[j][i] >=0:
          break  
        if j==N-1:
          return value(board)

# Play the bingo.
# Store a copy of the boards because we modify them by playing.

playing_boards = [board for board in boards]

# Initialize some global variables.

winner_found = False
winning_board_value = 0
last_drawn = 0

# Draw numbers from the pool in order. Mark the number in each board it appears.
# Check if there is a winner, if not update the boards and repeat.
# Store the winning board value and last number drawn.

for drawn in pool:  
  new_playing_boards = []
  for board in playing_boards:
    board = pick(drawn, board)
    new_playing_boards.append(board)
    if win(board):
      winning_board_value, last_drawn = (value(board), drawn)
      winner_found = True
      break
  playing_boards = new_playing_boards
  if winner_found:
    break

# compute the answer

answer = winning_board_value * last_drawn
print(f'Part 1: {answer}')

# Part 2

# Store a copy of the boards
playing_boards = [board for board in boards]


# Initialize some global variables

last_winning_board_value = 0
last_drawn = 0

# Draw numbers from the pool in order. Mark the number in each board it appears.
# If there is a winner remove it, unless it is the last board.
# Update the boards and repeat. When the last board wins store its value and
# the last number drawn.

for drawn in pool:
  new_playing_boards = []
  for board in playing_boards:
    board = pick(drawn, board)
    if not win(board):
      new_playing_boards.append(board)
    elif len(playing_boards) == 1:
      last_winning_board_value, last_drawn = (value(board), drawn)
      break
  playing_boards = new_playing_boards

# compute the answer
answer = last_winning_board_value * last_drawn
print(f'Part 2: {answer}')








  
  

