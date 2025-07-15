import random

chat_log = [
    "[Player1] Guys, are you still there?",
    "[Player2] Yeah, I’m stuck in the basement.",
    "[Player3] Anyone found a way out yet?",
    "[Player4] I’m searching the north corridor.",
    "[Player2] Found a strange console, but it’s locked.",
    "[Player1] Check the logs on that console, maybe a clue.",
    "[Player3] It looks like encrypted data, nothing readable.",
    "[Player4] Wait, I see a pattern — some lines start with dalctf{",
    "[Player2] No way, could that be the flag?",
    "[Player1] Let’s keep looking, maybe more parts are hidden.", 
    "[Player3] Found another fragment near the exit door.",
    "[Player4] It reads: dalctf{exit_c0de_sh4red_in_log}",
    "[Player2] That must be it! We can escape now.",
    "[Player1] Hurry up, the door’s opening!",
]

def random_bytes(length=20):
    return bytes(random.getrandbits(8) for _ in range(length))

with open("system_dump_001.bin", "wb") as f:
    print("file created")
    for line in chat_log:
        f.write(random_bytes(random.randint(10, 40)))
        f.write(line.encode('ascii', errors='ignore') + b'\n')
    f.write(random_bytes(60))
