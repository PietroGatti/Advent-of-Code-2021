# Note: This solution is not fully programmatic, it relies on pattern found in
# the puzzle input.

# Part 1

from time import perf_counter as pfc



# The puzzle input is composed of 14 subroutines. Each subroutines differs from
# another by the value of three variables that we denote u, a, and b.
# These can be found, respectively at lines 4, 5 and 15 of each subroutine.
# For example, consider the subroutine
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1	->	u = 1
# add x 14	->	a = 14
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 8	->	b = 8
# mul y x
# add z y

# Store each subroutine parameter from the puzzle input.
with open('input.txt') as f:
  data = [line.strip().split(' ') for line in f]

subs = []
parameters = []

for i, line in enumerate(data + ['*']):
  if i % 18 in {4, 5, 15}:
    parameters.append(int(line[-1]))
  if i % 18 == 0 and i != 0:
    subs.append(parameters)
    parameters = []

# Applying a subroutine with a given input digit, only changes the value of the
# variable z.

# If i is the input digit, applying a subroutine with parameters u, a, b to z
# gives the following result.
# If z % 26 == i - a: z // u		(*)
# Else: 26 * (z // u) + i + b		(**)
#
# Observe that half of the subroutines have u=1 and the other half u=26. With
# our input, the subroutines with u=1 are all of the kind (**).
# This implies that for z=0 to be sent to 0, each subroutine with u=26 must be
# of kind (*) and undo the most recent subroutine (**) that we have applied.

# This forces each digit of the input number to be coupled with another and
# satisfy a condition of the form:
#		
#		digit_j = digit_i + increment_ij.
#
# We store these conditions in a dictionary.

queue = []
conditions = {}
for j, sub in enumerate(subs):
  if sub[0] == 1:
    queue.append((j, sub))
  else:
    i, (_, a_i, b_i) = queue.pop(-1)
    j, (_, a_j, b_j) = j, sub
    conditions[(i, j)] = b_i + a_j

# Now we build the biggest input satisfying the conditions.

max_input = [0] * 14
for (i, j), increment in conditions.items():
  max_input[i] = min(9, 9 - increment)
  max_input[j] = max_input[i] + increment

answer = ''.join(str(e) for e in max_input)
print(f'Part 1: {answer}')

# Part 2

# This is the lowest input satisfying the conditions.

min_input = [0] * 14
for (i, j), increment in conditions.items():
  min_input[i] = max(1, 1 - increment)
  min_input[j] = min_input[i] + increment

answer = ''.join(str(e) for e in min_input)
print(f'Part 2: {answer}')

  
