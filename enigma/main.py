from enigma import *


r1 = Rotor("VEADTQRWUFZNLHYPXOGKJIMCSB", 1)
r2 = Rotor("WNYPVJXTOAMQIZKSRFUHGCEDBL", 2)
r3 = Rotor("DJYPKQNOZLMGIHFETRVCBXSWAU", 3)
reflector = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
machine = Machine([r1, r2, r3], reflector)
x = machine.encipher("Hello Mr.AhmadZade!")
print(x)
print(machine.decipher(x))