# Part 1

# Imports
from collections import Counter

# Store the input for starting polymer and insertion rules.
with open('input.txt') as f:
  lines = [line.strip() for line in f if len(line.strip()) > 0]

starting_polymer = lines[0]
rules_list = [line.split(' -> ') for line in lines[1:]]

# For this puzzle, we think of strings as dictionaries counting how many times
# each pair of characters appears in them.
# Example: 'ABABC' becomes {'AB': 2, 'BA': 1, 'BC': 1}

def counting_pairs(string):
  # Takes a string, returns the dictionary that counts it pairs of characthers.
  pairs = [string[i:i+2] for i in range(len(string)-1)]
  return Counter(pairs)

# Rephrase the insertion rules in these terms. We make the rules into a
# dictionary {key: val} where keys are pairs of characters and the value is the
# list of the two pairs obtained from the key after instertion.
# Example 'AB' -> 'C' corresponds to the key {'AB': ['AC', 'CB']}

rules = {pair: [pair[0] + inserted, inserted + pair[1]]
         for pair, inserted in rules_list}

# Insertion function.

def insertion(pairs_dict, ins_rules=rules):
  # Takes a pairs counting dictionary, returns a new pairs counting dictionary
  # after applying the insertion rules (in the format specified above).
  new_pairs = {key: 0 for key in rules}
  for pair in pairs_dict:
    new_pairs[ins_rules[pair][0]] += pairs_dict[pair]                              
    new_pairs[ins_rules[pair][1]] += pairs_dict[pair]                              
  return new_pairs

# Evolution of the polymer

def evolution(polymer, steps, ins_rules=rules):
  # Given a polymer (in the form of a string) applies the insertion rules for
  # the required amount of steps. Returns a pairs counting dictionary of the
  # result.
  pairs_dict = counting_pairs(polymer)
  for step in range(steps):
    pairs_dict = insertion(pairs_dict, ins_rules)
  return pairs_dict

# Characters counting

def counting_chars(pairs_dict):
  # Returns a character counting dictionary from a pair counting dictionary.
  dict_0 = {pair[0] : 0 for pair in pairs_dict}
  # Need to count the second chars too because we lost information on what is
  # the original string's last character.
  dict_1 = {pair[1] : 0 for pair in pairs_dict}                                
  for pair in pairs_dict:
    dict_0[pair[0]] += pairs_dict[pair]
    dict_1[pair[1]] += pairs_dict[pair] 
  return {char : max(dict_0[char], dict_1[char]) for char in dict_0}           

# Evolve the starting polymer in input (according to the insertion rules) for
# the required number of steps. Count the most and least common characters. The
# answer is their difference.

polymer = starting_polymer
steps = 10
pairs_dict = evolution(polymer, steps)
chars_dict = counting_chars(pairs_dict)
answer = max(chars_dict.values()) - min(chars_dict.values())
print(f'Part 1: {answer}')

# Part 2

# Same as Part 1, more steps.

polymer = starting_polymer
steps = 40
pairs_dict = evolution(polymer, steps)
chars_dict = counting_chars(pairs_dict)
answer = max(chars_dict.values()) - min(chars_dict.values())
print(f'Part 2: {answer}')                                 
