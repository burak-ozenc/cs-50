def main():
    # get input
    cardNumber = input("Enter card number:")

    # check input is valid
    if checkInput(cardNumber) == False:
        main() 

    length = len(cardNumber)

    # modulus regulates the card number length for the luhn algorithm
    modulus = int(length) % 2

    totalEvenNumbers = 0
    totalOddNumbers = 0
    totalCalculatedNumbers = 0

    counter = 0
    # iterate through the card number
    # calculates number according to luhn algoritm
    for i in cardNumber:
        if counter % 2 == modulus:
            tempEvenInt = int(i) * 2
            for j in str(tempEvenInt):
                totalEvenNumbers = totalEvenNumbers + int(j)
        else:
            totalOddNumbers += int(i)
        counter += 1

    totalCalculatedNumbers = totalOddNumbers + totalEvenNumbers

    if totalCalculatedNumbers % 10 == 0:
        checkCardType(cardNumber)
    else:
        print("INVALID")

# check input type


def checkInput(text):
    return text.strip().isdigit()

# check the card type according to card number and its length


def checkCardType(cardNumber):
    length = len(cardNumber)
    if length == 15 and cardNumber[0] == "3" and (cardNumber[1] == "4" or cardNumber[1] == "7"):
        print("AMEX")
    elif length == 16 and cardNumber[0] == "5" and (cardNumber[1] == "1" or cardNumber[1] == "2" or cardNumber[1] == "3" or cardNumber[1] == "4" or cardNumber[1] == "5"):
        print("MASTERCARD")
    elif (length == 13 or length == 16) and cardNumber[0] == "4":
        print("VISA")
    else:
        print("INVALID")


main()
