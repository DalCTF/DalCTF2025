#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define GRID_SIZE 3

void display_result_grid(int userX, int userY, int shipX, int shipY) {
    // Display result grid
    printf("\nResult:\n");
    printf("  ");
    for (int x = 1; x <= GRID_SIZE; x++) {
        printf("%d ", x);
    }
    printf("\n");
    
    for (int y = 1; y <= GRID_SIZE; y++) {
        printf("%d ", y);
        for (int x = 1; x <= GRID_SIZE; x++) {
            if (x == userX && y == userY) {
                if (x == shipX && y == shipY) {
                    printf("H "); // Hit
                } else {
                    printf("M "); // Miss
                }
            } else if (x == shipX && y == shipY) {
                printf("S "); // Ship position (revealed)
            } else {
                printf(". "); // Water
            }
        }
        printf("\n");
    }
    printf("H = Hit, M = Miss, S = Ship location, . = Water\n\n");
}

void display_grid(){
    // Display the grid with coordinates
    printf("\nGrid:\n");
    printf("  ");
    for (int x = 1; x <= GRID_SIZE; x++) {
        printf("%d ", x);
    }
    printf("(X)\n");
    
    for (int y = 1; y <= GRID_SIZE; y++) {
        printf("%d ", y);
        for (int x = 1; x <= GRID_SIZE; x++) {
            printf(". ");
        }
        printf("\n");
    }
    printf("(Y)\n");
}

int run_game() {
    char username[50];
    int userX, userY;
    int shipX, shipY;
    
    printf("=== DEBUG SYMBOLS (I need to remove this, don't think I needed it anymore) ===\n");
    printf("Username buffer address: %p\n", &username);
    printf("run_game function address: %p\n", (void*)run_game);
    printf("libc function (fgets) address: %p\n", (void*)fgets);
    printf("==============================\n\n");
    
    srand(time(NULL));
    
    printf("Please enter your username: ");
    gets(username);
    
    printf("\nHello, %s! Wanna play Battleship?\n", username);
    printf("The game is played on a %dx%d grid.\n", GRID_SIZE, GRID_SIZE);
    
    display_grid();
    
    shipX = (rand() % GRID_SIZE) + 1;
    shipY = (rand() % GRID_SIZE) + 1;
    
    // Get user's guess
    printf("\nEnter your guess:\n");
    printf("X coordinate (1-%d): ", GRID_SIZE);
    scanf("%d", &userX);
    printf("Y coordinate (1-%d): ", GRID_SIZE);
    scanf("%d", &userY);
    
    // Validate user input
    if (userX < 1 || userX > GRID_SIZE || userY < 1 || userY > GRID_SIZE) {
        printf("Invalid coordinates! Must be between 1 and %d.\n", GRID_SIZE);
        return 1;
    }
    
    display_result_grid(userX, userY, shipX, shipY);
    
    // Check if the user's guess matches the ship position
    if (userX == shipX && userY == shipY) {
        printf("Congratulations, %s! You found and sunk the battleship!\n", username);
        printf("What? You thought you would get a flag? No mate, try something else.\n");
    } else {
        printf("Sorry, %s. You missed the battleship!\n", username);
    }
    return 0;
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("Welcome to Armoury!\n");
    run_game();
    printf("Thank you for playing!\n");
    return 0;
}
