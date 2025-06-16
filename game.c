#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    // Seed the random number generator with current time
    srand(time(0));
    
    int randomNumber = (rand() % 100) + 1; // Random number between 1 and 100
    int no_of_guesses = 0;
    int guessed_number;

    // Loop until the user guesses the correct number
    do {
        printf("Guess the number: ");
        
        // Correct scanf syntax (no comma inside format string, pass variable address)
        scanf("%d", &guessed_number);

        // Compare numbers directly (no quotes)
        if (guessed_number > randomNumber) {
            printf("Lower number please!\n");
        }
        else if (guessed_number < randomNumber) {
            printf("Higher number please!\n");
        }
        else {
            printf("Congrats!! You guessed it right.\n");
        }

        no_of_guesses++;  // Increment the number of guesses

    } while (guessed_number != randomNumber);

    // Final message
    printf("You guessed the number in %d guesses.\n", no_of_guesses);

    return 0;
}
