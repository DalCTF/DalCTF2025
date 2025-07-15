#include <stdio.h>
#include <string.h>
#include <stdlib.h> // For exit(), rand(), srand()
#include <time.h>   // For time()

void system_override_protocol() {
    FILE *flag_file;
    char flag[100] = {0}; // Buffer to store the flag content
    
    // Open the flag file
    flag_file = fopen("flag.txt", "r");
    
    if (flag_file == NULL) {
        printf("%s %s", "Please create 'flag.txt' in this directory with your",
                        "own debugging flag.\n");
        exit(0);
    }
    fgets(flag, sizeof(flag), flag_file); // Read the flag content from the file
    // Close the file
    fclose(flag_file);
    
    printf("\n********************************************************\n");
    printf("  ** PROTOCOL BYPASS INITIATED!                         **\n");
    printf("  ** You have found the Defense System Master Key!      **\n");
    printf("  ** The Master Access Key is: %s **\n", flag);
    printf("  ** SYSTEM RESTORATION COMPLETE.                       **\n");
    printf("********************************************************\n");
    exit(0); // Exit after successfully bypassing
}

void get_secret_word(char *secret_word) {
    // Generate a random 5-letter word
    int i;
    for (i = 0; i < 5; i++) {
        // Generate a random lowercase letter ('a' through 'z')
        secret_word[i] = 'a' + (rand() % 26);
    }
    secret_word[5] = '\0'; // Null-terminate the string
}

void mainframe_authentication_challenge() {
    char secret_word[6];    // Stores the random 5-letter secret word + null terminator
    char guess_buffer[16];  // The vulnerable buffer for user input (e.g., 16 bytes for buffer + other stack variables before RET)
    srand(time(NULL));
    int i;

    // Generate the secret word
    get_secret_word(secret_word);


    printf("\n--- Defense Authentication ---\n");
    printf("Provide all 5 digits accesses codes or be ready to be vaporized!\n");

    // FOR DEBUGGING/TESTING ONLY: In a real CTF, you would remove this hint!
    // printf("DEBUG HINT: Current Access Code: %s\n", secret_word);

    for (i = 0; i < 100; i++) {
        printf("\n[AUTHENTICATION ATTEMPT %d/%d]\n", i + 1, 100);
        printf("Enter 5-character access code: ");
        fflush(stdout); // Ensure prompt is displayed immediately

        // WARNING: Using gets() is inherently unsafe and leads to buffer overflows.
        // This is the intentional vulnerability for this CTF problem.
        gets(guess_buffer);

        // Check if the input is exactly 5 characters and matches the secret word
        if (strlen(guess_buffer) != 5 || strcmp(guess_buffer, secret_word) != 0) {
            printf("[ACCESS DENIED] Incorrect code or invalid format. Initiating System DESTRUCTION.\n");
            return;
        } else {
            printf("[ACCESS GRANTED] Code accepted. Proceeding to next authentication cycle...\n");
        }
    }

    printf("\n[AUTHENTICATION COMPLETE] IMPOSSIBLE! You've bypassed the mainframe's logic.\n");
    printf("However, the Master Access Key can only be found via the Bypass Protocol.\n");
    return;
}

// Main entry point for the program / game
int main() {
    // Disable buffering for standard output and input streams.
    // This ensures that printf statements are displayed immediately and
    // gets() waits for input without internal buffering delays.
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    printf("************************************************************************\n");
    printf("  ** Welcome, Player. You are now accessing the Defense Mechanisms. **\n");
    printf("  ** Identify yourself, or be ready to face the consequences.       **\n");
    printf("************************************************************************\n");

    // Initiate the mainframe authentication challenge, which contains the vulnerability.
    mainframe_authentication_challenge();

    printf("\n// Program terminated. End of line.\n");
    return 0;
}
