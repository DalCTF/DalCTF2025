from sympy import nextprime
from Crypto.Util.number import long_to_bytes, inverse

# Replace these with actual challenge values
n = input("Enter n: ")
e = input("Enter e: ")
c = input("Enter c: ")
n = int(n)
e = int(e)
c = int(c)
p = 2
found = False
while True:
    if n % p == 0:
        print(f"Found prime factor: p = {p}")
        found = True
        break
    p = nextprime(p)

if not found:
    print("Failed to factor n")
    exit(1)

# Step 2: Compute q and phi(n)
q = n // p
phi = (p - 1) * (q - 1)

# Step 3: Compute private exponent d
d = inverse(e, phi)

# Step 4: Decrypt ciphertext
m = pow(c, d, n)
flag = long_to_bytes(m)

print(f"Decrypted message: {flag}")
