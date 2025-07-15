#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define FLAGSIZE 64
#define BUFFER_SIZE 16

int main(int argc, char **argv)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  char secret_code[4] = "LOCK";
  char buffer[BUFFER_SIZE];

  // Welcome message print
  printf("╔═══════════════════════════════════════════════════════════╗\n");
  printf("║                DEVELOPER DEFENSE MAP                      ║\n");
  printf("║                                                           ║\n");
  printf("║ This map reveals the developer defense mechanisms         ║\n");
  printf("║ that hide an incredible secret. To gain access,           ║\n");
  printf("║ you must demonstrate your understanding of                ║\n");
  printf("║ the game mechanism.                                       ║\n");
  printf("╚═══════════════════════════════════════════════════════════╝\n\n");

  printf("Input: ");
  gets(buffer);

  if (!strncmp(secret_code, "1337", 4))
  {
    // Message congratulating user
    printf("\n╔═══════════════════════════════════════════════════════════╗\n");
    printf("║             CONGRATULATIONS, 1337 Player!                 ║\n");
    printf("║                                                           ║\n");
    printf("║ You've successfully broken through our defenses!          ║\n");
    printf("║ Your next destination: Find the blue neon facility.       ║\n");
    printf("║ Be warned - more tests await you on your journey.         ║\n");
    printf("╚═══════════════════════════════════════════════════════════╝\n\n");

    for (int i = 0; i < 3; i++) {
      printf(".");
      fflush(stdout);  // Ensure the dot is displayed immediately
      sleep(1);
    }
    printf("\n");
    printf("Oh yeah, I almost forgot, here is your flag: ");

    char buf[FLAGSIZE];
    FILE *f = fopen("flag.txt","r");
    if (f == NULL) {
        printf("%s %s", "Please create 'flag.txt' in this directory with your",
                        "own debugging flag.\n");
        exit(0);
    }

    fgets(buf,FLAGSIZE,f);
    printf("%s", buf);

    return 0;
  }

  printf("You are not allowed to look at the map!\n");
  return 1;
}
