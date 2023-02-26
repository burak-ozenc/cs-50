// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// to count the number of words
int counter = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;


// TODO: Choose number of buckets in hash table
const unsigned int N = LENGTH;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // hash the word
    // case insensitivity handled inside of hash fuction
    int hashed = hash(word);

    // get the linked list from hash table
    node *LL = table[hashed];

    // when next cursor is NULL
    // finish search and return false
    while (LL != NULL)
    {
        // if a value found
        // return true
        if (strcasecmp(word, LL->word) == 0)
            return true;

        LL = LL->next;
    }

    return false;
}

// Hashes word to a number
// ref => https://www.youtube.com/watch?v=AeyiX6S3NgE
//     => https://www.digitalocean.com/community/tutorials/hash-table-in-c-plus-plus
unsigned int hash(const char *word)
{
    // create a simple hash
    int hashed = 0;
    for (int i = 0; i < strlen(word); i = i + 1)
        hashed += (tolower(word[i])) * (toupper(word[i]));

    return hashed % LENGTH;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // read file
    FILE *file = fopen(dictionary, "r");
    // if null return false
    if (file == NULL)
        return false;

    // storage space for word
    char word[LENGTH + 1];

    // iterate over file until EOF reached
    while (fscanf(file, "%s", word) != EOF)
    {
        // allocate memory for new node
        node *n = malloc(sizeof(node));

        // null check for malloc func
        if (n == NULL)
        {
            return false;
        }

        // set pointer of the node to new word
        strcpy(n->word, word);

        // create a hash for the word
        int hash_val = hash(word);

        // set current node's pointer to the next node
        n->next = table[hash_val];

        // place node to the hash table
        table[hash_val] = n;

        // raise word counter
        counter++;
    }
    // close file
    fclose(file);

    // if loaded successfully return true
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // calculates the size on load
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // iterate over hash table
    for (int i = 0; i < N ; i++)
    {
        // current node
        node *n = table[i];

        // iterate over linke list until it is null
        while (n)
        {
            // set temp node to current node
            node *tmp = n;
            // set current node to next node
            n = n->next;
            // free temp node
            free(tmp);
        }
        // loop ends here
        if (i == N - 1)
            return true;
    }

    return false;
}