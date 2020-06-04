import bitarray
import numpy as np
from tables import *

def lrotate(l, x):
    return l[x:]+l[:x]

def f(r, k):
    r = r[E-1]
    B = r^k
    Sbits = bitarray.bitarray()
    for s in range(8):
        i = int(''.join(map(str, [B[6*s]*1, B[6*s+5]*1])), 2)
        j = int(''.join(map(str, B[6*s+1:6*s+5]*1)), 2)
        Sbits.extend(format(S_BOX[s, i, j], '04b'))
    return np.array(Sbits.tolist())[P-1]


def das(msg, key, decrypt=0):
    # generate sub keys
    if type(key) is str:
        keyBits = bitarray.bitarray()
        keyBits.frombytes(key.encode('utf-8'))
    else:
        keyBits=key

    keyBits_pc1 = bitarray.bitarray()
    keyBits_pc1.extend(np.array(keyBits.tolist())[PC_1-1])

    #subkeys
    C, D = [], []
    C.append(keyBits_pc1[:28])
    D.append(keyBits_pc1[28:])

    for i, shf in enumerate(SHIFT):
        C.append(lrotate(C[i], shf))
        D.append(lrotate(D[i], shf))

    K = []
    for i in range(1, 17):
        K.append(np.array((C[i]+D[i]).tolist())[PC_2-1])

    #acctually encode
    if type(msg) is str:
        msgBits = bitarray.bitarray()
        msgBits.frombytes(msg.encode('utf-8'))
    else:
        msgBits = msg

    # append to 64-bit
    if(len(msgBits)%64):
        msgBits.extend((64-len(msgBits)%64)*'0')
    
    #break on 64-bit blocks
    blocks = []
    for i in range(int(len(msgBits)/64)):
        blocks.append(msgBits[64*i:64*(i+1)])

    if decrypt:
        K.reverse()
    # encode blocks
    encodedMsg = bitarray.bitarray()
    for block in blocks:
        block_IP = np.array(block.tolist())[IP-1]

        left = block_IP[:32]
        right = block_IP[32:]

        for subKey in K:
            newRight = left^f(right, subKey)
            left=right
            right=newRight

        encodedMsg.extend(np.concatenate((right, left), axis=0)[IP_1-1])

    return encodedMsg


msg = 'this is my declaration of encryption'
key = 'secret!!'

encodedB = das(msg, key)
print(encodedB)
decoded = das(encodedB, key, 1)
print(decoded.tobytes().decode('utf-8'))