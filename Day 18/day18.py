# Part 1

# Imports
import re

# We think a snail (number) as a list of complex numbers.

# String to snail

def make_snail(myString):
  # Returns a list of complext numbers representing a snail number.
  # Real numbers will denote the actual numeric values in the snail number.
  # 1j denotes open parenthesis, -1j closed parenthesis.

  data = re.findall(r'(\[|\]|\d+)', myString)                                 
  snail = []
  for substring in data:
    if substring == '[':
      snail.append(1j)
    elif substring == ']':
      snail.append(-1j)
    elif substring.isnumeric():
      snail.append(int(substring))
  return snail

                                          


# Explode a snail.

def explode(snail):
  # Method to explode a snail number. It is changed in place.
  # Returns True if it changed, False otherwise.

  # index of the last numeric value found, initialized None
  last_num_i = None
  
  # keep count of the number of parenthesis we open and close.                                                    
  open_ = 0                                                                    
  for i in range(len(snail)):
    if snail[i].imag != 0:
      open_ += snail[i].imag
    if (open_ >= 5 and                                                         
        snail[i+1].imag == 0 and
        snail[i+2].imag == 0):
    # exploding pair found
      
      # replace first parenthesis with 0, this will replace the whole pair
      snail[i] = 0

      # add first element of exploding pair to previous number (if present)                                                             
      if last_num_i:                                                          
        snail[last_num_i] += snail[i+1]
      
      # remove all elements relative to the exploding pair
      # (including closing parenthesis), storing the second value
      snail.pop(i+3)                                                           
      to_add = snail.pop(i+2)                                                  
      snail.pop(i+1)
      
      # search for numbers after the pair and add the stored value if there is
      # a number.                                                      
      for j in range(i + 1, len(snail)):                                       
        if snail[j].imag == 0:
          snail[j] += to_add
          # The snail has been modified, so we return True before completing
          # the loop.
          return True 
      
      # The snail has been modified, so we return True.
      return True

    if snail[i].imag == 0:
    # last numeric value in position i, store the index                                                    
      last_num_i = i

  return False


# Split a snail.

def split(snail):
  # Method to split a numeric value inside a snail number. The snail is changed
  # in place, return True if changed, False otherwise

  for i in range(len(snail)):
    if snail[i].real >= 10:
      left = snail[i] // 2
      right = (snail[i] + 1) // 2
      pair_to_insert = [1j, left, right, -1j]
      snail[:] = snail[:i] + pair_to_insert + snail[i+1:]                      
      return True
  return False

# Add

def add(snail1, snail2):
  # Method to add to snail numbers.
  # Returns the result snail simplified.
  
  # We consider the empty string as the neutral element for addition.
  if snail1 == '':
    return snail2
  elif snail2 == '':
    return snail1

  else:
    snail = [1j] + snail1 + snail2 + [-1j]
    to_do = True
    while to_do:
    # to_do is True until we have simplified something.
      to_do = explode(snail) or split(snail)
    return snail

# Snail magnitude

def magnitude(snail):
  # Recursive method to get the value of a snail from its subsnails.

  # base case
  if len(snail) == 1:
    return snail[0]

  else:
    # keep track of how many parenthesis we open and close after the first one
    open_ = 0

    # we will consider two sub-snails.
    # Build the first.
    sub_snail1 = []

    # first element is always a parenthesis so we skip it
    for i, val in enumerate(snail[1:]):                                        
      sub_snail1.append(val)
      if val.imag != 0:
        open_ += val.imag
      if open_ == 0:
      # closed all the open paranthesis: done reading the first subsnail.
        break

    # the rest of the snail is the second subsnail.
    sub_snail2 = snail[i+2:-1]                                                 
    return 3 * magnitude(sub_snail1) + 2 * magnitude(sub_snail2)               


# Store the input as a list of snails numbers.

with open('input.txt') as f:
  data = [line for line in f]

snails = [make_snail(datum) for datum in data]

# Sum all the snails in input as snails numbers. The magnitude of the result
# is the answer.

# the empty string acts as 0 for snail addition
sum_snail = ''

for snail in snails:
  sum_snail = add(sum_snail, snail)

answer = magnitude(sum_snail)
print(f'Part 1: {answer}')

# Part 2

# Sum all the possible pairs of snails in input. The maximum magnitude of the
# results is the answer.

# We are doing redundant operations.
answer = 0
for i, snail_i in enumerate(snails):
  for j, snail_j in enumerate(snails):
    if i != j:
      value_sum = magnitude(add(snail_i, snail_j))
      if value_sum > answer:
        answer = value_sum


print(f'Part 2: {answer}')
  



      
    
  
  


