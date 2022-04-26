# Part 1

# Parse the data in a list of pairs [unique signal patterns, four digit output value]
with open('input.txt') as f:
  data = [[part.split() for part in line.split('|')] for line in f]            

# Lengths of patterns corresponding to unique numbers.          
unique_numbers = [2, 3, 4, 7] 

# The answer is obtained counting how many digits in output correspond have
# lengths corresponding to unique patterns.

answer = 0                                                 
for datum in data:
  output = datum[1]
  for digit in output:
    if len(digit) in unique_numbers:
      answer += 1

print(f'Part 1: {answer}')

# Part 2

# Dictionary that associates to length of pattern the corresponding digit
# for the univocal cases.
unique_n_seg = {2: '1', 3: '7', 4: '4', 7: '8'}


def decode(signal):
  # Given a signal, returns a decodification dictionary: {pattern: digit}.
  # Where the pattern is a sorted string.             
  # *Algorithm:
  #    - Decode the patterns corresponding to unique lenghts: 1, 4, 7 and 8.
  #    - Look at the patterns of length 6:
  #        - If it contains the pattern of 4, then it must codify 9.
  #        - Else if if contains the pattern of 1, then it must codify 0.
  #        - If none above, then it must codify 6.
  #    - Look at the patterns of length 5:
  #        - If the pattern is contained in the pattern of 6, then it must codify 5.
  #        - Else if the pattern contains the pattern of 1, then it must codify 3.
  #        - If none above, then it must codify 5.
  # In the algorithm we consider the patterns up to anagrams.
  # The output dictionary for decodification will accept keys in the form of
  # sorted strings.

  code = {}
  patterns = [set(x) for x in signal]
  for pattern in patterns:
    if len(pattern) in unique_n_seg:
      label = unique_n_seg[len(pattern)]
      code[label] = pattern
  six_seg = [x for x in patterns if len(x) == 6]
  for pattern in six_seg:
    if code['4'] < pattern:
      code['9'] = pattern
    elif code['1'] < pattern:
      code['0'] = pattern
    else:
      code['6'] = pattern
  five_seg = [x for x in patterns if len(x) == 5]
  for pattern in five_seg:
    if pattern < code['6']:
      code['5'] = pattern
    elif code['1'] < pattern:
      code['3'] = pattern
    else:
      code['2'] = pattern
  decoder = {''.join(sorted(code[digit])): digit for digit in code}
  return decoder

# Decode the data using the decode function, recall that we need to sort the
# pattern strings before passing them to decoder.

answer = 0
for signal, output in data:
  decoder = decode(signal)
  value = ''
  for pattern in output:
    pattern = ''.join(sorted(pattern))
    value += decoder[pattern]

  answer += int(value)

print(f'Part 2: {answer}')

