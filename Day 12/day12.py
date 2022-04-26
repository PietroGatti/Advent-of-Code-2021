# Part 1

# Store the input as a list of lists of lenght two [a, b]
with open('input.txt') as f:
  lines = [line.strip() for line in f]

data = [line.split('-') for line in lines]


# Organize the graph into a dictonary {key: value}
# value is the set of edges at distance 1 from key.
# Assume that edges can only leave start but not come to it, while all the other
# edges are bidirected.

keys = set(vertex for edge in data for vertex in edge)
dist_1 = {key: set() for key in keys}
for edge in data:
  (dist_1[edge[0]]).add(edge[1])
  if edge[0] != 'start':
    (dist_1[edge[1]]).add(edge[0])

dist_1 = {key: list(value) for key, value in dist_1.items()}

# Generate the paths.

def create_paths(begin='start', path=tuple()):
  # Recursive function that generates paths.
  # Continues the path in input with the given begin point (it is always called
  # with a valid continuation) and calls itself recursively.
  
  # Extend the path with begin.
  path += (begin,)
  
  # Iterate through the vertices at distance 1 from begin.
  for vertex in dist_1[begin]:
    # If the vertex is a small cave already visited by this path, ignore it.
    if vertex.islower() and vertex in path:
      continue
    # If the vertex is the 'end' vertex, then we extend the path with 'end' and
    # add it to paths and continue the iteration.
    if vertex == 'end':
      paths.add(path+('end',))
      continue  
    # Extend the path calling the function with this new vertex    
    create_paths(vertex, path)

# Fill the set of paths, its cardinality is the answer.

paths = set()
create_paths()
answer = len(paths)
print(f'Part 1: {answer}')

# Part 2

# Generate the paths with an extra condition.

def create_paths2(begin='start', path=tuple(), small_cave=False):
  # As create_paths except that we keep track of a boolean variable small_cave
  # that is True if we already visited a small cave twice.
  path += (begin,)
  if begin.islower() and path.count(begin) == 2:
    small_cave = True
  for vertex in dist_1[begin]:
    if vertex.islower() and vertex in path and small_cave:
      continue   
    if vertex == 'end':
      paths.add(path+('end',))
      continue 
    create_paths2(vertex, path, small_cave)

# Fill the set of paths, its cardinality is the answer.

paths = set()
create_paths2()
answer = len(paths)
print(f'Part 2: {answer}')
    
  


