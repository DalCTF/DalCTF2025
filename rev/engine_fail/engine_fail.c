#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "flag.h"

#define PATCH_LEN 1

int flag_numb = 0;

extern uint8_t je_opcode;

// Always returns 0 -> unpatched binary will hit engine_fail
int engine_ready(void) {
    return 0;
}

// Called on JE failure
void engine_fail_handler(void) {
    puts("Engine failed to start!");
    exit(1);
}

// Whitelist checker: must be run before check_region()
void enforce_whitelist(void) {
    uint8_t b = je_opcode;
    if (!( b == 0x90            /* NOP */
        || (b >= 0x40 && b <= 0x4F) /* INC/DEC */
        || b == 0xEB            /* JMP short */ // this is the intended instruction the player suppose to use
        || b == 0xE9            /* JMP near */
        || b == 0x74            /* JE */
        || b == 0x75 )) {       /* JNZ */
        
        puts("Cheater detected!");
        exit(1);
    }
}

// Declare asm block
extern void check_region(void);

__asm__ (
    ".intel_syntax noprefix        \n"
    ".text                         \n"
    ".globl check_region           \n"
    ".globl je_opcode              \n"
    "check_region:                 \n"
    "    call engine_ready         \n"
    "    test eax, eax             \n"
    "je_opcode:                    \n"
    "    je    engine_fail         \n"
    "    ret                       \n"
    "engine_fail:                  \n"
    "    jmp   engine_fail_handler \n"
    ".att_syntax prefix            \n"
);

static void print_flag(void) {
    // derive key from the opcode change, the key is only correct if je_opcode = 0xEB, cause that's what the flag was encoded with, which is (0xEB ^ 0x74)
    uint8_t key = je_opcode ^ 0x74;
    if (key == 0) {
        // still JE, unpatched
        puts("Engine failed to start!");
        exit(1);
    }
    // now decode with the single-byte key
    char buf[FLAG_LEN+1];
    for (size_t i = 0; i < FLAG_LEN; i++) {
        buf[i] = enc_flag[i] ^ key;
    }
    buf[FLAG_LEN] = '\0';
    puts(buf);
}

int main(void) {
    enforce_whitelist();
    check_region();
    puts("You’re airborne!");
    flag_numb = 1337;
    print_flag();
    return 0;
}

