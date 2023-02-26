#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main(void)
{
    long cardNumber = get_long("Enter card number:");
    bool result;
    // int lengthOfCardNumber = floor(log10(abs(cardNumber))) + 1;

    // convert long to string
    // char cardNumberStrTemp[16];
    char cardNumberStr[16];
    sprintf(cardNumberStr, "%ld", cardNumber);

    // reverse the card number

    printf("cardNumberStr %s\n", cardNumberStr);

    int lengthOfCardNumber = strlen(cardNumberStr);

    int modulus;

    // workaround for selecting number for luhn algorithm
    // if card length is even
    // modulus will be applied from first digit
    if (lengthOfCardNumber % 2 == 0)
        modulus = 0;
    else
        modulus = 1;

    int totalEvenNumbers = 0;
    int totalOddNumbers = 0;
    int totalCalculatedNumbers;
    for (int i = 0; i < lengthOfCardNumber; i++)
    {
        if ((i % 2) == modulus)
        {
            // workaround for multiplying the char
            // ###################################
            // to convert a 'char' to integer
            // we will subtract '0' from that 'char'
            // if we try converting directly string
            // we do not get the number itself
            // but we will get the ASCII value of char
            int tempEvenInt = cardNumberStr[i] - '0';

            // if any number multiplied by 2
            // result wont have more than two digits
            char tempEvenString[2];
            tempEvenInt = tempEvenInt * 2;

            // convert integer to string
            sprintf(tempEvenString, "%d", tempEvenInt);

            int lengthOfTempEvenNumber = strlen(tempEvenString);

            //calculate the total of elements from multiplied numbers
            for (int j = 0; j < lengthOfTempEvenNumber; j++)
            {
                // converting 'char' to 'int'
                totalEvenNumbers = totalEvenNumbers + tempEvenString[j] - '0';
            }
        }
        else
        {
            // converting 'char' to 'int'
            int tempOddInt = cardNumberStr[i] - '0';
            totalOddNumbers = totalOddNumbers + tempOddInt;
        }
    }

    totalCalculatedNumbers = totalOddNumbers + totalEvenNumbers;

    // check if modulus of total calculated number is 0
    // else return INVALID
    if ((totalCalculatedNumbers % 10) == 0)
    {
        result = true;
    }
    else
    {
        result = false;
        printf("INVALID\n");
        return 0;
    }

    // check for conditions for card types
    // else return INVALID
    if (result == true)
    {
        if (lengthOfCardNumber == 15 && cardNumberStr[0] == *"3" && (cardNumberStr[1] == *"4" || cardNumberStr[1] == *"7"))
        {
            printf("AMEX\n");
        }
        else if (lengthOfCardNumber == 16 && cardNumberStr[0] == *"5" && (cardNumberStr[1] == *"1" || cardNumberStr[1] == *"2" || cardNumberStr[1] == *"3" || cardNumberStr[1] == *"4" || cardNumberStr[1] == *"5"))
        {
            printf("MasterCard\n");
        }
        else if ((lengthOfCardNumber == 13 || lengthOfCardNumber == 16) && cardNumberStr[0] == *"4")
        {
            printf("Visa\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

    return 0;
}