#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>


// Compilation: gcc main.c -o lets-test-your-memory -g
void readFlag() {
	FILE* in;
	int flagSize = 64;
	char flag[flagSize];

	in = fopen("flag.txt", "rt");
	if(in == NULL) {
		puts("Failed to read in flag");
	}
	fgets(flag, flagSize, in);
	fclose(in);
}


void guessFlag() {
	int guessLength;
	char* guess;

	puts("Let's test your memory. Try to guess the flag!");
	puts ("Enter the length of your guess:");
	scanf("%d", &guessLength);
	getchar();
	guess = malloc(guessLength);
	puts("Enter your guess:");
	fgets(guess, guessLength, stdin);

	sleep(1);
	puts("Look's like you forgot... Or did you?");

	free(guess);
}


int main() {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	readFlag();

	puts("\n=== Game Menu ===");
	puts("1. Run Program");
	puts("2. Run Game in Debug Mode (Wut?)");
	puts("Enter your choice:");

	int choice;
	scanf("%d", &choice);
	switch(choice) {
		case 1: 
			guessFlag();
			break;
		case 2:
			pid_t pid = getpid();

			char pid_str[32];
			snprintf(pid_str, sizeof(pid_str), "%d", pid);

			puts("Launching GDB...");
			char* args[] = {
				"gdb",
			       	"-q", 
				"--pid", pid_str, 
				"-ex", "file ./lets-test-your-memory",
				"-ex", "b guessFlag",
				"-ex", "r",
				NULL};
			execvp("gdb", args);
			break;
		default:
			puts("Please enter a valid choice");
	}

	return 0;
}
