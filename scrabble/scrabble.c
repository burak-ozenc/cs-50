#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // convert to lowercase
    for (int i = 0; word1[i]; i++)
    {
        word1[i] = tolower(word1[i]);
    }
    for (int i = 0; word2[i]; i++)
    {
        word2[i] = tolower(word2[i]);
    }

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // compare scores
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    int length = strlen(word);
    int initialValue = 0;
    for (int i = 0; i < length; i = i + 1)
    {
        if (word[i] >= 'a' && word[i] <= 'z')
        {
            // a has value of 97
            // z has value of 122 on ASCII table
            // we subtract 97 from ASCII value and find the index on POINTS array
            int value = (int)word[i] - 97;
            initialValue = initialValue + POINTS[value];
        }
    }
    return initialValue;
}
