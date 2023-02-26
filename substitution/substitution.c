#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

string enryptString(string encryptionArray, string text);
bool checkEncryptionArray(string encryptionArray);
string errorMessage;

int main(int argc, string argv[])
{
    // for the validation of argument key has length of 26
    // and corrent amount of argument
    bool validateInput = false;

    if(argc == 2 && strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else if (argc == 2 && strlen(argv[1]) == 26)
    {
        // input validated
        // check if array is unique and alphabetic
        validateInput = checkEncryptionArray(argv[1]);
        if(validateInput == false)
        {
            printf("%s",errorMessage);
            return 1;
        }
    }
    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }


    // if necessary conditions are provided
    // get input from user to encrypt
    if(validateInput == true)
    {
        string text_to_encrypt = get_string("plaintext: ");
        string encrypted_text = enryptString(argv[1],text_to_encrypt);
        printf("ciphertext: %s\n",encrypted_text);
    }

    return 0;
}

// check for uniqueness
// or key is alphabetic
bool checkEncryptionArray(string encryptionArray)
{
    for (int i = 0; i < strlen(encryptionArray); i++)
    {
        if (isalpha(encryptionArray[i]))
        {
            int count = 0;
            for (int j = 0; j < strlen(encryptionArray); j++)
            {
                if (encryptionArray[j] == encryptionArray[i])
                {
                    count += 1;
                }
                if (count > 1)
                {
                    // error message handled globally
                    errorMessage = "Key must not contain repeated characters.\n";
                    return false;
                }
            }
        }
        else
        {
            // error message handled globally
            errorMessage = "Key must only contain alphabetic characters.\n";
            return false;
        }
    }
    return true;
}

// only encrypt the letters
// check their ASCII values
// and set if they are uppercase or lowercase
string enryptString(string encryptionArray, string text)
{
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            text[i] = tolower(encryptionArray[(int)text[i] - 97]);
        }
        else if (text[i] >= 'A' && text[i] <= 'Z')
        {
            text[i] = toupper(encryptionArray[(int)text[i] - 65]);
        }
    }

    return text;
}