# Part 1

depths = []

with open('input.txt') as f:
  for line in f:
    depths.append(int(line))

prev = depths[0]
count = 0
for d in depths[1:]:
  if d >= prev:
    count += 1
  prev = d

print(f'Part1: {count}')

# Part 2

prev_window = sum(depths[0:3])
count = 0

for i in range(1, len(depths)):
  window = sum(depths[i:i+3])
  if window > prev_window:
    count += 1
  prev_window = window

print(f'Part2: {count}')
