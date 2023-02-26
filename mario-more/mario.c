#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // get user input for height
    int spaces = get_int("Height: ");
    int hashes = 1;
    // for desired output, user should enter a number between 1 and 8(both included)
    // check if conditions match
    if (spaces > 0 && spaces < 9)
    {
        // print until reaching to desired length of lines
        do
        {
            // for readability curly parentheses has been deleted
            // for one line to use of curly parentheses are unnecessary
            int i;
            for (i = 0; i < (spaces - 1); ++i)
                putchar(' ');

            for (i = 0; i < (hashes); ++i)
                putchar('#');

            for (i = 0; i < 2; ++i)
                putchar(' ');

            for (i = 0; i < (hashes); ++i)
                putchar('#');

            printf("\n");
            spaces = spaces - 1;
            hashes = hashes + 1;
        }
        while (spaces > 0);
    }
    else if (spaces >= 9)
    {
        //if number is bigger than desired input
        //show message and call the itself
        printf("Please enter a number lower than 9.\n");
        main();
    }
    else
    {
        //if number is negative
        //show message and call itself
        printf("Please enter positive number.\n");
        main();
    }
    return 0;
}