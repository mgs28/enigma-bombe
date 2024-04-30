import string

# Pre configured rotors
RotorA = [
    5,
    3,
    11,
    15,
    20,
    22,
    19,
    4,
    7,
    23,
    0,
    24,
    16,
    12,
    8,
    6,
    25,
    21,
    13,
    2,
    18,
    10,
    1,
    17,
    9,
    14,
]
RotorB = [
    12,
    11,
    19,
    7,
    8,
    13,
    4,
    6,
    14,
    16,
    0,
    25,
    17,
    10,
    1,
    23,
    3,
    18,
    9,
    5,
    20,
    22,
    24,
    21,
    15,
    2,
]
RotorC = [
    0,
    16,
    18,
    6,
    11,
    25,
    14,
    2,
    19,
    3,
    10,
    13,
    8,
    24,
    15,
    4,
    9,
    20,
    23,
    12,
    1,
    5,
    17,
    22,
    7,
    21,
]
RotorD = [
    1,
    0,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
]
RotorReflector = [x - 1 if x % 2 == 1 else x + 1 for x in range(26)]
identify = [x for x in range(26)]
ALL_ROTORS = [RotorA, RotorB, RotorC]
# wider set of rotors 
# ALL_ROTORS = [RotorA, RotorB, RotorC, RotorD, identify]



def inverse_rotor(rotor):
    """
    return an inverse lookup for a given rotor
    """
    temp_r = [-1] * len(rotor)
    for i in rotor:
        temp_r[rotor[i]] = i

    return temp_r


def rotate_rotor(rotor):
    """
    Rotate the rotor with a mechanical representation where the mapping between letters shifts
    to the next letter (e.g. A->B then B->C after a rotation).
    """

    # create transformation vector (e.g. position i adds or subtracts a number 
    # of characters from a given character)
    temp_r = [rotor[i] - i for i in range(len(rotor))]

    # rotate the transformations
    temp_r = [temp_r[-1]] + temp_r[0:-1]

    return [(i + temp_r[i]) % len(temp_r) for i in range(len(temp_r))]


def cipher_text(text, rotors_in, offsets_in):
    """
    cipher the text with the given set of rotors and offsets
    ex) cipher ("matthewwashere", [RotorD, RotorB, RotorC], [0,0,0])
    """
    ######################
    # TODO: Add error checks (e.g. len(rotors)=len(offsets)), 
    #       all characters in text are ascii.lower()
    ######################
    text = text.lower()
    #create copies so we don't mess with original rotors, etc
    rotors = rotors_in.copy()
    offsets = offsets_in.copy()


    #print(f"Ciphering with rotors = {rotors}, offset={offsets} and text = {text}")

    # calculate the inverse rotors
    inverse_rotors = []
    for r in rotors:
        inverse_rotors.append(inverse_rotor(r))

    output = ""
    for c in text:
        # print("ciphering {}".format(c))
        if c in string.ascii_lowercase:
            cipher_character = ord(c) - 97

            # first way through
            for i in range(len(rotors)):
                cipher_character = rotors[i][cipher_character]
                # print("... using cipher {} => {}".format(rotors[i],chr(input+97)))

            # print("... goes into reflector as {}".format( chr(input+97)))

            # reflector
            cipher_character = RotorReflector[cipher_character]

            # go backwards!
            for i in range(len(rotors) - 1, -1, -1):
                cipher_character = inverse_rotors[i][cipher_character]
                # print("... using inv_cipher_{} {} => {}".format(i,inverse_rotors[i],chr(input+97)))

            # print("... comes out as {}".format( chr(input+97)))

        output += chr(cipher_character + 97)

        # rotate rotors
        carry = 1
        for i in range(len(rotors)):

            # rotate a rotor
            if carry == 1:
                rotors[i] = rotate_rotor(rotors[i])
                inverse_rotors[i] = rotate_rotor(inverse_rotors[i])
                carry = 0
                # check to see if it rotated a full cycle
                if offsets[i] > len(rotors[0]):
                    # if full rotation of this rotor then rotate the next one too (otherwise don't)
                    offsets[i] = (offsets[i] + carry) % len(rotors[0])
                    carry = 1

    return output
