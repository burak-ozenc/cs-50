from cs50 import get_int


def main():
    # get input
    length = get_int("Height: ")
    # check the height conditions
    if length > 0 and length < 9:
        # iterate over length
        for x in range(1, length+1):
            # newLine is the half of the new line
            newLine = (" " * (length - x))
            newLine = newLine + ("#" * x)
            # reverse newLine, remove whitespace, add to newLine and print
            print(newLine + "  " + newLine[::-1].replace(" ", ""))
    else:
        main()


main()
