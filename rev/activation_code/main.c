#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

/*
62 3d 64 60 0a 64 60 0a 
22 3d 66 3b 0a 62 3d 66 
0a 27 66 23 66 27 60 
66 0a 32 66 62 0a 60 
66 27 64 65 20 60 0a 
3d 66 3d 66
*/

// “7h15_15_wh3n_7h3_r3v3r53_g37_53r10u5_h3h3” in hex, each byte followed by random hex numb
static const char key[] = {
    0x62,0x01, 0x3d,0x10, 0x64,0x20, 0x60,0x22,
    0x0a,0x0F, 0x64,0x02, 0x60,0x12, 0x0a,0x21,
    0x22,0x0E, 0x3d,0x1F, 0x66,0x03, 0x3b,0x13,
    0x0a,0x1E, 0x62,0x0D, 0x3d,0x14, 0x66,0x04,
    0x0a,0x1D, 0x27,0x15, 0x66,0x0C, 0x23,0x05,
    0x66,0x16, 0x27,0x1C, 0x60,0x06, 0x66,0x23,
    0x0a,0x17, 0x32,0x07, 0x66,0x1B, 0x62,0x0B,
    0x0a,0x08, 0x60,0x18, 0x66,0x0A, 0x27,0x1A,
    0x64,0x24, 0x65,0x09, 0x20,0x19, 0x60,0x25,
    0x0a,0x99, 0x3d,0x26, 0x66,0x21, 0x3d,0x12, 
    0x66,0x13
};
static const size_t key_len = sizeof(key) / 2;

int checkLength(const char *input) {
    return strlen(input) == key_len;
}

int checkFlag(const char *input) {
    // Fake flag function
    if (strcmp(input, "password") == 0 || strcmp(input, "activate") == 0 || strcmp(input, "admin") == 0) {
        printf("You thought you were smart huh? Not that easy bud, try again ;')'\n");
        return 1;
    }
    return 0;
}

int checkXOR(const char *input) {
    size_t len = key_len;
    // Check each char in the player input if it's match the encoded flag
    for (size_t i = 0; i < len; i++) {
        unsigned char expected = key[2*i];
        if (( (unsigned char)input[i] ^ 0x55 ) != expected) {
            return 0;
        }
    }
    return 1;
}

int validate(const char *input) {
    checkFlag(input);
    if (!checkLength(input)) return 0;
    if (!checkXOR(input))    return 0;
    return 1;
}

int main(void) {
    char input[64];
    ssize_t  n;

    printf("Enter your activation code: ");
    fflush(stdout);

    // Read raw bytes
    n = read(STDIN_FILENO, input, sizeof(input));
    if (n <= 0) {
        perror("read");
        return 1;
    }

    // Strip trailing newline, if present
    if (input[n-1] == '\n') {
        n--;
    }

    // Null‐terminate so strlen() inside validate() works
    if (n >= (ssize_t)sizeof(input)) {
        n = sizeof(input) - 1;
    }
    input[n] = '\0';

    if (validate(input)) {
        printf("What you just enter is the answer :]");
    } else {
        puts("Invalid code.");
    }

    return 0;
}

