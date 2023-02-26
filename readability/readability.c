#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int compute_grade(int letters, int words, int sentences);

int main(void)
{
    // get input
    string word1 = get_string("Text: ");

    // only word count should start from 1
    // word count = white spaces + 1
    int wordCount = 1;
    int letterCount = 0;
    int sentenceCount = 0;
    // loop over text
    for (int i = 0; i < strlen(word1); i++) {
        // check word ending punctuations
        if (word1[i] == '!' || word1[i] == '?' || word1[i] == '.')
            sentenceCount++;
        // check word counts with white spaces
        if (word1[i] == ' ')
            wordCount++;

        //check if it is a alphabetical character
        if (isalpha(word1[i]))
            letterCount++;
    }

    // compute result
    int result = compute_grade(letterCount, wordCount, sentenceCount);

    // print final result
    if (result < 1)
        printf("Before Grade 1\n");
    else if (result > 16)
        printf("Grade 16+\n");
    else
        printf("Grade %d\n", result);


    return 0;
}

// calculate result with Coleman-Liau formula
int compute_grade(int letters, int words, int sentences)
{
    double l = 100 * (double) letters / (double) words;
    double s = 100 * (double) sentences / (double) words;
    double index = 0.0588 * (double) l - 0.296 * (double) s - 15.8;

    return round(index);
}