def to_pow(num):
    superscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    return str(num).translate(superscript)

def cryp():

    m = 83
    print('Input M = {}\n'.format(m))
    p, g, x = 97, 2, 8
    y = pow(g, x, p)
    print('y = {}{} mod {} = {}'.format(g, to_pow(x), p, y))
    print('p = {}, g = {}, y = {}'.format(p, g, y))

    k = 95
    print('k = {}'.format(k))
    a = g ** k % p
    b = (y ** k) * m % p
    print('a = {}{} mod {} = {}'.format(g, to_pow(k), p, a))
    print('b = {}{} * {} mod {} = {}'.format(y, to_pow(k), m, p, b))

    new_m = (b * (pow(a, p-1-x))) % p
    # print(new_m)

    print('\nOutput M = {}*({}{})⁻{} mod {} = {}'.format(b, a, to_pow(x), to_pow(1), p, new_m))

def main():
    cryp()

if __name__ == '__main__':
    main()