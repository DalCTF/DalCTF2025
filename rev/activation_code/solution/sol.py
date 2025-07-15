from pwn import *

# The encoded hex player suppose to extract
extract = b'\x62\x3d\x64\x60\x0a\x64\x60\x0a\x22\x3d\x66\x3b\x0a\x62\x3d\x66\x0a\x27\x66\x23\x66\x27\x60\x66\x0a\x32\x66\x62\x0a\x60\x66\x27\x64\x65\x20\x60\x0a\x3d\x66\x3d\x66'

# XOR with 0x55
flag = bytes([b ^ 0x55 for b in extract])

print(flag)


# Send the raw bytes to the binary
p = process('../activation_code')
p.recvuntil(b'Enter your activation code: ')
print("prepare")
p.send(original + b'\n')
print("sent")

