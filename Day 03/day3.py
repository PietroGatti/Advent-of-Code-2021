# Part 1

# Imports
import numpy as np


# REMARK: epsilon is just gamma with swapped bits, so it is enough to find one of the two.

# Idea: we replace all '0's with '-1's, so that when we sum bitwise
# if the result is negative, '0' is more frequent,
# if the result is positive, '1' is more frequent.

# Read each line of input in an array of integers where we convert 0 to -1.
# Sum the arrays componentwise and store the result in frequency.

frequency = np.array([0])
                                          
with open('input.txt') as f:
  for line in f:
    line_array = np.array(list(line.strip())).astype('int')             
    line_array = 2*line_array -1			                
    frequency = frequency + line_array                                  

# The sign of each component of frequency tells us the most (and least) common
# digit in each bit. Reconstruct gamma and epsilon as binary arrays. 

frequency = np.sign(frequency)                                          
gamma_array = 1/2 * (frequency + 1)                                     
epsilon_array = -1/2 * (frequency - 1)                                  

# Convert gamma and epsilon to integers and multiply them to get the answer.

powers_of_2 = 2 ** np.arange(len(gamma_array))[::-1] 
                     
gamma = gamma_array.dot(powers_of_2)                                    
epsilon = epsilon_array.dot(powers_of_2)
                                
answer = int(gamma * epsilon)
print(f'Part 1: {answer}')

# Part 2

# Store the data as a list of strings
with open('input.txt') as f:
  data = [line.strip() for line in f]                                      

# Bit criteria

def bit_criteria(nums, n, most=True):
  # Takes a list nums of binary strings and a bit position n.
  # If most is True, returns the sublist of numbers having the most common digit
  # in position n.
  # If most is False, it does the same with the least common digit.
  # In case of ties, 1 is considered to be the most common digit if most is True,
  # 0 otherwise.

  # initialize most/least common digit
  digit = int(most)

  # separate the strings into two sublists according to their n-th digit and
  # store them in a dictionary.                                                     
  nth_digit = {0:[], 1:[]}                                                     
  for num in nums:                                                             
    num_digit = int(num[n])
    nth_digit[num_digit].append(num)

  # change the most/least common digit according to the dictionary.
  if len(nth_digit[0]) > len(nums) / 2:                                        
    digit = -1 * digit + 1

  # return the desired sublist.                                               
  return nth_digit[digit]                                                     

# Function to get the rating.

def rating(nums, most=True):
  # Takes a list of binary strings. Iteratively filters the list of numbers
  # using bit_criteria for each digit from left to right. Returns the only
  # remaining string.

  N = len(nums[0])                                                                                        
  filtered = [x for x in nums]
  for n in range(N):
    filtered = bit_criteria(filtered, n, most)
    if len(filtered) == 1:
      break
  return filtered[0]

# Find oxygen and co2 ratings as binary strings using rating
oxygen_bin = rating(data, most=True)
co2_bin = rating(data, most=False)

# Convert oxygen and co2 to integers and multiply them to get the answer.
oxygen = int(oxygen_bin, base=2)
co2 = int(co2_bin, base=2)

answer = oxygen * co2
print(f'Part 2: {answer}')
  


