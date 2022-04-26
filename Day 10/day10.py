# Part 1

# Imports
import numpy as np

# Store the input as a list of strings.
with open('input.txt') as f:
  data = [row.strip() for row in f]

# Dictionary storing the score associated to each closing character.
closing = {')': 3, ']': 57, '}': 1197, '>': 25137}

# Dictionary storing for each opening character the one that closes it.
closes = {'(': ')', '[': ']', '{': '}', '<': '>'}
          
# Read each line character by character. 'read' stores the sequence of opened
# characters, when we close one correctly, we remove it from 'read'.
# The line is corrupted if we read a closing character that is not closing the 
# last opened character. We count its score and add it to the answer.

answer = 0

for line in data:
  read = []
  for char in line:
    if char in closing:
      if char == closes[read[-1]]:
        read.pop(-1)
      else:
        answer += closing[char]
        break
    else:
      read.append(char)

print(f'Part 1: {answer}')

# PART 2

# Dictionary storing the score associated to each closing character.
closing = {')': 1, ']': 2, '}': 3, '>': 4}


# Line completer

def complete(line):
  # given a string line, returns the empty string if it is corrupted and the
  # string that completes it if incomplete.

  # 'read' stores the sequence of opened characters, when we close one correctly,
  # we remove it from 'read'.
  # The line is corrupted if we read a closing character that is not closing the 
  # last opened character.
  read = []
  for char in line:
    if char in closing:
      if char == closes[read[-1]]:
        read.pop(-1)
      else:
        return
    else:
      read.append(char)

  # to complete the line look at 'read' backwards and match the open character
  # with their closing one.
  completion = ''.join([closes[char] for char in read[::-1]])
  return completion  

# Score

def score(string):
  # given a completion string returns its score s.
  s = 0
  for char in string:
    s *= 5
    s += closing[char]
  return s

# Array of the scores for each line in input.
line_scores = np.array([])

for line in data:
  if complete(line):
  # True only for non corrupted lines.                                  
    line_score = score(complete(line))
    line_scores = np.append(line_scores, line_score)

# The answer is the median of the array of scores.
answer = int(np.median(line_scores))
print(f'Part 2: {answer}')



      
    
    

