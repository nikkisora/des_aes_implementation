import numpy as np
from supFunc import *

np.set_printoptions(formatter={'int': '{:02x}'.format})

def AES(text, key):
    rounds = keyRound[len(key)*8]
    text = text.reshape((4, 4)).T
    key = key.reshape((4, 4)).T
    eKey = keyExpansion(key, rounds)
    text = addRoundKey(text, eKey, 0)
    for i in range(1, rounds + 1):
        text = subBytes(text)
        text = shiftRows(text)
        if i != rounds:
            text = mixColumns(text)
        text = addRoundKey(text, eKey, i)
    return text

def invAES(text, key):
    rounds = keyRound[len(key)*8]
    text = text.reshape((4, 4))
    key = key.reshape((4, 4)).T
    
    eKey = keyExpansion(key, rounds)
    for i in range(rounds, 0, -1):
        text = addRoundKey(text, eKey, i)
        if i != rounds:
            text = mixColumnsInv(text)
        text = shiftRowsInv(text)
        text = subBytesInv(text)
        
    text = addRoundKey(text, eKey, 0)
    return text


text = np.frombuffer('water is wet, no'.encode('utf-8'), dtype=np.uint8).reshape((4,4)).T.flatten()
key  = np.array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])


print('text bytes:', text)
print('key bytes: ', key)
code = AES(text, key)
print('ciphertext:', code.flatten())
text2 = invAES(code, key)
print('plain text:', text2.T.flatten())