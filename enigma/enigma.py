class Machine:

    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, rotors, reflector):
        self.rotors = rotors
        self.reflector = reflector

    def encipher(self, text):
        """
        Encipher the given input

        Args: text (string) plain text to encode

        Returns: string
        """
        return "".join((self.encipher_character(x) for x in text.upper()))

    def decipher(self, text):

        for rotor in self.rotors:
            rotor.reset()

        return self.encipher(text)

    def encipher_character(self, x):

        if x not in Machine.ALPHABET:
            return x
        contact_index = Machine.ALPHABET.index(x)

        for rotor in self.rotors:
            contact_letter = rotor.alphabet[contact_index]
            x = rotor.encipher(contact_letter)
            contact_index = rotor.alphabet.index(x)

        contact_letter = Machine.ALPHABET[contact_index]
        x = self.reflector.reflect(contact_letter)
        try:
            contact_index = Machine.ALPHABET.index(x)
        except ValueError:
            return x

        for rotor in reversed(self.rotors):
            contact_letter = rotor.alphabet[contact_index]
            x = rotor.decipher(contact_letter)
            contact_index = rotor.alphabet.index(x)

        self.rotors[0].rotate()
        for index in range(1, len(self.rotors)):
            rotor = self.rotors[index]
            turn_frequency = len(Machine.ALPHABET)*index
            if self.rotors[index-1].rotations % turn_frequency == 0:
                rotor.rotate()

        return Machine.ALPHABET[contact_index]


class Rotor:

    def __init__(self, mappings, offset=0):
        self.initial_offset = offset
        self.reset()
        self.forward_mappings = dict(zip(self.alphabet, mappings))
        self.reverse_mappings = dict(zip(mappings, self.alphabet))

    def reset(self):

        self.alphabet = Machine.ALPHABET
        self.rotate(self.initial_offset)
        self.rotations = 1

    def rotate(self, offset=1):
        self.rotations = offset
        self.alphabet = self.alphabet[offset:] + self.alphabet[:offset]

    def encipher(self, character):
        return self.forward_mappings[character]

    def decipher(self, character):

        return self.reverse_mappings[character]
    

class Reflector:

    def __init__(self, mappings):
        self.mappings = dict(zip(Machine.ALPHABET, mappings))

        for x in self.mappings:
            y = self.mappings[x]
            if x != self.mappings[y]:
                raise ValueError("Mapping for {0} and {1} is invalid".format(x, y))

    def reflect(self, character):

        return self.mappings[character]
