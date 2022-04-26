# Part 1

# Store the data as a list of integers

with open('input.txt') as f:
  data = next(f).strip().split(',')

fishes = [int(datum) for datum in data]

# Global dictionary {age: number of fishes that age} to store the situation
# at each generation. In the terms of the puzzle, 'age' here stands for 'days
# before creating a new lanternfish'.
value = 0
generation = dict.fromkeys(range(9), value)

# Store the initial state in the generation dictionary.
for fish in fishes:
  generation[fish] += 1                                                        


# Remark: since the position of fishes is not important, we can assume that each
# fish cycles its age from 8, 7, ..., 1, 0 and that newborn fishes start at age 6.

def evolve(days):
  # Updates the generation dictionary according to the evolution of the system
  # after the specified amount of days. Returns the total number of fishes.
  global generation
  for day in range(days):
    # store the number of fishes that are born this genereation
    new_borns = generation[0]
    # update the generation dictionary: reduce age by 1 modulo 9 of each fish.
    generation = {((age - 1) % 9): generation[age] for age in generation}
    # add the newborn fishes as having age 6.
    generation[6] += new_borns
  # return total amount of fishes
  return sum([generation[age] for age in generation])

# The result of evolve with 80 days gives us the answer for part 1.
days = 80
answer = evolve(days)

print(f'Part 1: {answer}')

# Part 2

# Reinitialize generation dictionary.
value = 0
generation = dict.fromkeys(range(9), value)

for fish in fishes:
  generation[fish] += 1

# The result of evolve with 256 days gives us the answer for part 2.
days = 256
answer = evolve(days)

print(f'Part 2: {answer}')
