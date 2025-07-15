from Crypto.Util.number import getPrime, bytes_to_long


def RatScrew(flag):
    p = getPrime(24)
    q = getPrime(1024)

    n = p * q
    e = 65537


    m = bytes_to_long(flag)
    c = pow(m, e, n)
    return n, e, c


