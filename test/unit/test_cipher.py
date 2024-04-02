import pytest

from enigma_bombe.cipher import cipher_text, inverse_rotor, rotate_rotor, RotorA, RotorB, RotorC, RotorD
import random 


def test_inverse_rotor():
    #given 
    rotor = [0,1,2]

    #when 
    inv_rotor = inverse_rotor(rotor)

    #Then 
    assert inv_rotor == [0,1,2]

    #given 
    rotor = [0,1,2]

    #when 
    inv_rotor = inverse_rotor(rotor)

    #Then 
    assert inv_rotor == [0,1,2]


    #given 
    rotor = [5,3,11,15,20,22,19,4,7,23,0,24,16,12,8,6,25,21,13,2,18,10,1,17,9,14];

    #when 
    inv_rotor = inverse_rotor(rotor)

    #Then 
    assert inv_rotor == [10,22,19,1,7,0,15,8,14,24,21,2,13,18,25,3,12,23,20,6,4,17,5,9,11,16]

def test_rotate():
    #given 
    rotor = [0,1,2]

    #when 
    inv_rotor = rotate_rotor(rotor)

    #Then (rotation of identity is identity)
    assert inv_rotor == [0,1,2]

    #given (basically adding one to each vector)
    rotor = [1,2,0]

    #when 
    inv_rotor = rotate_rotor(rotor)

    #Then (rotation of a constant rotor is a constant)
    assert inv_rotor == [1,2,0]

    #given (add one, subtract one, identity)
    rotor = [1,0,2]

    #when 
    inv_rotor = rotate_rotor(rotor)

    #Then (rotation = identity, add one, subtract one)
    assert inv_rotor == [0,2,1]

    #given 
    rotor = [5,3,11,15,20,22,19,4,7,23,0,24,16,12,8,6,25,21,13,2,18,10,1,17,9,14];

    #when 
    inv_rotor = rotate_rotor(rotor)
    print(inv_rotor)
    #Then 
    assert inv_rotor == [15, 6, 4, 12, 16, 21, 23, 20, 5, 8, 24, 1, 25, 17, 13, 9, 7, 0, 22, 14, 3, 19, 11, 2, 18, 10]

def test_cipher():

    ##### TEST A SIMPLE CIPHERING

    #given 
    identity = [x for x in range(26)]
    AtoBandBtoA = [1,0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    text = "at"

    #when
    cipher = cipher_text(text, [AtoBandBtoA,identity,identity], [0,0,0])

    #then
    #what should this be? 
    #a=>b, reflector makes b into a 
    #t goes through reflector to be s
    assert cipher == "bs"

    ##### TEST THAT CIPHER IS REVERSABLE
    #given
    text = "matthewwashere"

    #when
    cipher = cipher_text(text, [identity,identity,identity], [0,0,0])

    #then
    assert cipher == "nbssgfxxbtgfqf"

    #given
    text = "nbssgfxxbtgfqf"

    #when
    cipher = cipher_text(text, [identity,identity,identity], [0,0,0])

    #then
    assert cipher == "matthewwashere"

    ######### TEST MATCHES WITH REACTJS CODE
    #given
    text = "matthewwashere"

    #when 
    cipher = cipher_text(text, [RotorD, RotorB, RotorC], [0,0,0])

    #then
    assert cipher=="ljffizqqidizpz"

def test_long_cipher():
    identify = [x for x in range(26)]
    all_rotors = [RotorA, RotorB, RotorC, RotorD,identify]

    with open("data/messages.txt", "r", encoding="utf-8") as f: 
        text = f.readline().strip()
        while len(text) > 0:

            #Given 
            
            #pick a random set of rotors
            rotors = random.choices(all_rotors, k=3)
            #pick some random offsets (also called the ring)
            offsets = [random.randint(0, 25) for i in range(1,4) ]

            #When 

            #cipher the text
            cipher = cipher_text(text, rotors, offsets)
            #decipher the cipher 
            decipher = cipher_text(cipher, rotors, offsets) 
            #recipher the decipher text (could be different than original text because of non-alphanumeric characters)
            recipher = cipher_text(decipher, rotors, offsets)

            #Then
            assert cipher == recipher 

            #get next text 
            text = f.readline().strip()


