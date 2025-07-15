from Crypto.Util.number import getPrime, bytes_to_long


def RatScrew(flag):
    p = getPrime(24)
    q = getPrime(1024)

    n = p * q
    e = 65537


    m = bytes_to_long(flag)
    c = pow(m, e, n)
    return n, e, c



def main():

    flag = "dalctf{1n_Th3_Ph4ra0hs_t0mb_or_Wh4t3vEr}"
    n, e, c = RatScrew(flag.encode())
    

    print(r"""

                              .sSSSSSSSs
                              sSS=""^^^"s
                  /\       , /  \_\_\|_/_)
                 /';;     /| \\\/.-. .-./
                / \;|    /. \,S'  -   - |
               / -.;|    | '.SS     _|  ;
              ; '-.;\,   |'-.SS\   __  /S
              | _  ';\\.  \' SSS\_____/SS
              |  '- ';\\.  \_SSS[_____]SS
              \ '--.-';;-. __SSS/\    SSS
               \  .--' ';;'.=SSS`\\_\_SSS
                `._ .-'` _';;..=.=.=.\.=\
                   ;-._-'  _.;\.=.=.=.|.=|
         ,     _.-'    `"=._  ;\=.=__/__/
         )\ .'`   __        ".;|.=.=.=./
         (_\   .-`  '.   |    \/=.=.=/`
          /\\         \-,|     |.--'|
         /  \`,       //  \    | |  |
        ( (__) )  _.-'--,  \   | |  '--,
         ;----' -'--,__}}}  \  '--, __}}}
  jgs    \_________}}}       \___}}}
    """)
    print("I am the mighty Sphinx, guardian of the secrets of the Rat Screw Tomb. You will not pass until you answer my riddles three. But be warned, for if you answer incorrectly, you will be cursed to wander the tomb forever.")
    print("\nOn top of that, even if I tell you the secrets, the Rat Screw Algorithm is super secure and you'll never break it anyway. Basically you shouldn't even try.")
    print("Are you ready for the first riddle? y/n")
    input_answer = input().strip().lower()
    if input_answer != 'y':
        print("You have chosen wisely. Farewell, mortal.")
        return
    else:
        print("Very well, here is your first riddle:")
        print("\n----------------------")
        print("\nWhat is it that walks on four legs in the morning, two legs at noon, and three in the evening?")
        answer = input().strip().lower()
        if answer in ["man", "human", "human being", "person", "a man", "a human", "a person"]:
            print("Correct! You have answered the first riddle. But do not celebrate yet, for there are two more to come.")
            print("Here is your second riddle:")
            print("\n----------------------")
            print("\nWhat can travel around the world while staying in a corner?")
            answer = input().strip().lower()
            if answer in ["stamp", "a stamp", "postage stamp"]:
                print("Uhh okay, no one has ever got that one before. Congratulations I guess.")
                print("Alright. Here is your final riddle:")
                print("\n----------------------")
                print("\nThe man who makes it doesn't want it, the man who buys it doesn't need it, and the man who needs it doesn't know it yet. What is it?")
                answer = input().strip().lower()
                if answer in ["coffin", "a coffin", "coffin box"]:
                    print("Noooooooooooo!!! You have answered all my riddles correctly! You may pass and take the secrets of the Rat Screw Algorithm with you. But remember, even if you know the secrets, the algorithm is so secure that it is practically unbreakable.")
                    print(f"\n\nHere are the secrets:\nn = {n}\ne = {e}\nc = {c}")
                    print("Good luck, mortal. You will need it.")
                else:
                    print("Incorrect! You have failed the third riddle. You are cursed to always plug in your USB upside down. Don't come back! The Rat Screw Algorithm is too secure for you to break anyway.")
                    return
            else:
                print("Incorrect! You have failed the second riddle. You are cursed to trip on your shoelaces once a day forever.")
                return
        else:
            print("Incorrect! You have failed the first riddle. I place a curse on your bloodline.")
            return

if __name__ == "__main__":
    main()