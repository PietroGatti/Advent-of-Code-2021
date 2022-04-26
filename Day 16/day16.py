# Part 1

def to_bin(hex_string):
  # Convert a string representing an hexadecimal number into a binary string.
  # Padding with '1' and cutting the first three characters of the final result
  # has the effect of getting a binary number with leading zeros and exactly 4
  # bits for every hexadecimal digit. Example: '6' -> '0110'
  return bin(int('1' + hex_string, 16))[3:]


# Construct a class to deal with Packets.
class Packet:                                                                  
  
  def __init__(self, data, from_hex = True):
    # Packets are initialized recursively on their subpackets.
    # If the packed is coming from hexadecimal data, convert to binary first.                                
    if from_hex:
      data = to_bin(data)
    self.data = data
    self.version = int(data[:3], 2)
    self.type = int(data[3:6], 2)
    totalVersion = self.version
    if self.type == 4:
      value = ''
      i = 6
      while True:
        value += data[i+1:i+5]
        i += 5
        if data[i-5] == '0':
          break
      self.value = int(value, 2)
      self.length = i
      self.subPackets = []
    else:
      subPackets = []
      lenId = data[6]
      if lenId == '0':
        lenSub = int(data[7:22], 2)
        self.length = 22 + lenSub
        i = 0
        while i < lenSub:
          subPacket = Packet(data[22 + i:], False)
          subPackets.append(subPacket)
          totalVersion += subPacket.totalVersion
          i += subPacket.length
        self.subPackets = subPackets
      elif lenId == '1':
        nSub = int(data[7:18], 2)
        count = 0
        i = 0
        while count < nSub:
          subPacket = Packet(data[18 + i:], False)
          subPackets.append(subPacket)
          totalVersion += subPacket.totalVersion
          i += subPacket.length
          count += 1
        self.subPackets = subPackets
        self.length = 18 + i
    self.totalVersion = totalVersion    
    

    
    # The necessary functions to compute the value of a given type packet
    def type0(packet):
      return sum([p.value for p in packet.subPackets])
    
    def type1(packet):
      prod = 1
      for p in packet.subPackets:
        prod *= p.value
      return prod
    
    def type2(packet):
      return min([p.value for p in packet.subPackets])
    
    def type3(packet):
      return max([p.value for p in packet.subPackets])

    def type4(packet):
      return packet.value
    
    def type5(packet):
      return int(packet.subPackets[0].value > packet.subPackets[1].value)

    def type6(packet):
      return int(packet.subPackets[0].value < packet.subPackets[1].value)

    def type7(packet):
      return int(packet.subPackets[0].value == packet.subPackets[1].value)
    
    # Index the different functions in a dictionary.
    type_dict = {
              0: type0,
              1: type1,
              2: type2,
              3: type3,
              4: type4,
              5: type5,
              6: type6,
              7: type7
    }
    
    # Returns the value function given the type
    def get_value(t):
      return type_dict[t]
    
    # Initialize value of a packet
    self.value = get_value(self.type)(self)

    # Display a packet. Represents a packet as the minimum data required to
    # univocally determine it.
    self.display = data[:self.length]
    
  # Represents via display (not used)
  def __repr__(self):
    return self.display

# Store the input
with open('input.txt') as f:
  data = f.read()

# The answer is obtained getting the totalVersion attribute.

answer = Packet(data).totalVersion
print(f'Part 1: {answer}')

# Part 2

# The answer is obtained getting the value attribute.

answer = Packet(data).value
print(f'Part 2: {answer}')




