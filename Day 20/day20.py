# Part 1

# Store the data.

# Convert '.' into '0' and '#' into '1'.
# The enhance algorithm will be stored as a dictionary {position: bit_value}.
# The input image is stored as a list of lists of '0's and '1's.
with open('input.txt') as f:
  data = [line for line in f if not line.isspace()]

enhance_algo = {i: ('0' if char == '.' else '1')
                for i, char in enumerate(data[0])}

input_image = [''.join(['0' if char == '.' else '1'
               for char in line.strip()])
               for line in data[1:]]

# Enhance a pixel.

def enhance_pixel(i, j, image):
  # Function to enhance the pixel in position (i, j) in an image: list of '0's 
  # and '1's. Returns the new value for the pixel.
  s = ''
  for k in range(-1,2):
    s += image[i+k][j-1:j+2]
  return enhance_algo[int(s, 2)]

# Padding.
# Preprocess images by padding so that the enhance algorithm works as if the
# image were infinite.

def preprocess(image, padding = '0'):
  # Pads the image with widht-two frame of the specified character. Returns the
  # new image.                                   
  n = len(image) + 4
  new_image = [padding*n]*2                                                    
  for line in image:
    new_image += [padding*2 + line + padding*2]
  new_image += [padding*n]*2
  return(new_image)

# Function to enhance an image following the given algorithm.
# We assume the image is 'preprocessed', meaning that it has two rows and columns
# of padding with a single character. The result will be a padded image,
# to ease reiteration. The first and last columns and rows will not contribute to the
# enhanced image, except for the kind of padding we need to apply at the end.

# Enhance

def enhance_image(preprocessed_image):
  # Takes an image that has been preprocessed (padded). Applies the enhance
  # algorithm to all its pixels and returns the new image.
  # Remark that the result is also a padded image, to emulate the infinite
  # extension. The padding character depends on the value of the enhance
  # algorithm on the previous padding.                                     
  new_image = []                                                               
  for i in range(1, len(preprocessed_image) - 1):                              
    new_line = ''.join([                                                       
          enhance_pixel(i, j, preprocessed_image)                              
          for j in range(1, len(preprocessed_image[i]) -1)
          ])
    new_image.append(new_line)

  # Determine the new padding
  s = 9 * preprocessed_image[0][0]                                             
  padding = enhance_algo[int(s, 2)] 
  new_image = preprocess(new_image, padding)
  return new_image

# Preprocess and enhance twice the image in input.

enhanced = enhance_image(preprocess(input_image))                         
enhanced = enhance_image((enhanced))

# Count the lit pixels, i.e. the '1's to obtain the answer.
answer = 0                                                                      
for line in enhanced:
  for char in line:
    if char == '1':
      answer += 1
print(f'Part 1: {answer}')

# Part 2

# Preprocess the input image.
image = preprocess(input_image)

# Enhance 50 times.
for _ in range(50):                                                            
  image = enhance_image(image)

# The anwer is the number of lit pixels.
answer = 0                                                                      
for line in image:
  for char in line:
    if char == '1':
      answer += 1
print(f'Part 2: {answer}')  
                                                                # count lit pixels
