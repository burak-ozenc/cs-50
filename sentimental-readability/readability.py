import re


def main():
    # get input
    text = input("Text:")

    # only word count should start from 1
    # word count = white spaces + 1
    wordCount = 1
    letterCount = 0
    sentenceCount = 0

    # iterate through all characters on input
    for letter in text:
        if letter == '!' or letter == '?' or letter == '.':
            sentenceCount += 1

        if letter == " ":
            wordCount += 1

        isSymbol = re.sub(r'[^\w]', '', letter)
        if (isSymbol):
            letterCount += 1

    result = compute_grade(letterCount, wordCount, sentenceCount)

    # print final result
    if (result < 1):
        print("Before Grade 1\n")
    elif (result > 16):
        print("Grade 16+\n")
    else:
        print("Grade \n", result)

# apply Coleman-Liau formula


def compute_grade(letters, words, sentences):
    l = 100 * float(letters) / float(words)
    s = 100 * float(sentences) / float(words)
    index = 0.0588 * l - 0.296 * s - 15.8

    return round(index)


main()
