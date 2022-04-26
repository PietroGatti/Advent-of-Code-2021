# Part 1

# Imports
from itertools import cycle
from collections import Counter

# Store the initial position of the two players.
with open('input.txt') as f:
  position_0, position_1 = tuple(int(line[-2]) for line in f)

# In contrast with the puzzle description, we call the board positions
# 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, insead of
# 10, 1, 2, 3, 4, 5, 6, 7, 8, 9 to simplify the scores calculations.


# Part 1

# Keep track of players positions on the board and scores.
board = [position_0 - 1, position_1 -1]                                 
score = [0, 0]                                                           

# The deterministic die.
die = cycle(range(1, 101))    

# Keep track of how many times the die has been rolled.                                                 
rolls = 0

# Play the game.

# Repeat until someone wins.                                                               
while True:

  # player 0 plays
  player_0_die = 0
  for _ in range(3):
    rolls += 1
    player_0_die += next(die)
  
  # update board and score accordingly
  board[0] = (board[0] + player_0_die) % 10
  score[0] += board[0] + 1

  # if player 0 won, stop the game
  if score[0] >= 1000:
    break

  # player 1 plays
  player_1_die = 0
  for _ in range(3):
    rolls += 1
    player_1_die += next(die)
  
  # if player 1 won, stop the game
  board[1] = (board[1] + player_1_die) % 10
  score[1] += board[1] + 1
  if score[1] >= 1000:
    break

# Compute and print the answer.
answer =  min(score[0], score[1]) * rolls
print(f'Part 1: {answer}')

# Part 2

# Store all the possible outcomes of the sum of 3 three-sided dice in a die.

die = []

for i in range(1, 4):
  for j in range(1, 4):
    for k in range(1, 4):
      die.append(i + j + k)

# Dictionary counting how many times each sum appears.
die_rate = dict(Counter(die))

# Remove repetitions from die.                                             
die = list(set(die))

# The main idea is that each time some number is rolled in die, there are
# rate = die_rate[number] universes with that outcome. So, instead of counting
# all the games with that outcome, we consider it to be just one game that and
# multiply its value by rate when counting how many games each player won.

# Store how many games each player has won.
games = [0, 0]

# Store the players id in a list.
players = [0, 1]
                            
# Switch player.
def other(player):
  # Returns 0 on 1 and viceversa.                                                          
  return -1 * player + 1

# Starting positions.                                                               
start_board = [position_0 - 1, position_1 - 1]                                                   


def play(player=0, board=start_board, score=[0, 0], rate=1):
  # Recursive function that plays a game.
  # Tracks the who has to play, board state and score for the current game.
  # As explained above, rate counts how many universes have that precise
  # sequence of die rolls. The current game will be worth as many universes as
  # its rate, the list games gets updated accordingly.
    
  if score[0] >= 21:
    # End the current game if player 0 has won. This happened in 'rate' universes
    # so it accounts for a quantity of 'rate' games won.                                                        
    games[0] += rate                                                           
    return     
                                                                 
  if score[1] >= 21:
    # End the current game if player 1 has won. Accord him 'rate' games won.                                                    
    games[1] += rate                                                                                             
    return

  for roll in die:
    # For each possible die roll:
    
    # - Update boards, scores and rate according to the die roll.
    new_board = [(board[p] + roll) % 10 if p == player else board[p]
                 for p in players]
    new_score = [score[p] + new_board[p] + 1 if p == player else score[p]
                 for p in players]
    new_rate = rate * die_rate[roll]

    # - Determine who is the next player                                                                           
    new_player = other(player)
   
    # - Keep playing the game with the new values.
    play(new_player, new_board, new_score, new_rate)

# Play the game
play()

# The answer is the number of most games won.
answer = max(games)
print(f'Part 2: {answer}') 

