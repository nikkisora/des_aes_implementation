import numpy as np
from tables import *

def m_p(polynomial1, polynomial2):  # multiply_polynomials
    result = 0
    for i in range(len(bin(polynomial2)) - 2):
        if polynomial2 & (1 << i):
            result ^= polynomial1 << i
    return result

def d_p(polynomial1, polynomial2):  # divide_polynomials
    quotient = 0
    reminder = polynomial1
    while len(bin(reminder)) >= len(bin(polynomial2)):
        shift = len(bin(reminder)) - len(bin(polynomial2))
        reminder ^= polynomial2 << shift
        quotient ^= 1 << shift
    return quotient, reminder

def g_m(polynomial1, polynomial2):  # galois_multiply
    mul_res = m_p(polynomial1, polynomial2)
    return d_p(mul_res, 0x11b)[1]

def split_hex(value):
    return divmod(value, 0x10)

def getBytes(value):
    high, low = split_hex(value)
    return sbox[high, low]

def getBytesInv(value):
    high, low = split_hex(value)
    return invSbox[high, low]

def subBytes(code):
    return np.array([getBytes(by) for by in code])

def subBytesInv(code):
    return np.array([getBytesInv(by) for by in code])

def keyExpansion(key, rounds):
    row, col = key.shape
    keyExp = np.zeros((row, col * (rounds + 1)), dtype=int)
    keyExp[:, :4] = key
    for i in range(1, rounds + 1):
        new_row = np.array([getBytes(by) for by in np.roll(keyExp[:, (i * 4) - 1], -1)])
        new_row = keyExp[:, (i - 1) * 4] ^ new_row ^ Rcon[:, i - 1]
        l = [new_row]
        for j in range(1, 4):
            new_row = keyExp[:, ((i - 1) * 4) + j] ^ new_row
            l.append(new_row)
        keyExp[:, (i * 4): (i * 4) + 4] = np.array(l).T
    return keyExp

def addRoundKey(code, key, i):
    # print('Key:', key[:, i * 4:(i * 4) + 4].flatten(), '\n')
    return code ^ key[:,i*4:(i*4)+4]

def shiftRows(code):
    code[1] = np.roll(code[1], -1)
    code[2] = np.roll(code[2], -2)
    code[3] = np.roll(code[3], -3)
    return code

def shiftRowsInv(code):
    code[1] = np.roll(code[1], 1)
    code[2] = np.roll(code[2], 2)
    code[3] = np.roll(code[3], 3)
    return code

def mixColumns(code):
    resList = []
    for rowcb in code.T:
        for rowcx in cx:
            res = 0
            for ccb, ccx in zip(rowcb, rowcx):
                res ^= g_m(ccb, ccx)
            resList.append(res)
    return np.array(resList).reshape((4, 4)).T

def mixColumnsInv(code):
    resList = []
    for rowcb in code.T:
        for rowicx in invCX:
            res = 0
            for ccb, cicx in zip(rowcb, rowicx):
                res ^= g_m(ccb, cicx)
            resList.append(res)
    return np.array(resList).reshape((4, 4)).T
