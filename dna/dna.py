import csv
import sys


# object models

class Person:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes or {}


def main():
    n = len(sys.argv)

    # TODO: Check for command-line usage
    # HANDLE ARGV INPUTS
    if n != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return False

    people = []

    # Read database file into a variable
    # open database file
    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # get headers
        headers = reader.fieldnames

        # iterate through the rows
        # create a Person object
        # with name and attributes
        # and add it to people list
        for row in reader:
            person = Person("", [])
            for header in headers:
                if header == "name":
                    person.name = row[header]
                else:
                    person.attributes[header] = row[header]
            people.append(person)

    # Read DNA sequence file into a variable
    DNA = ''
    # open DNA sequence and set it to DNA string
    with open(sys.argv[2]) as f:
        DNA = f.readline().strip()

    # iterate through people
    # to check if they match the DNA
    for person in people:
        attributesLength = len(person.attributes.keys())
        matchCount = 1
        # iterate over attributes
        # if fails break the for loop
        # and start to lookup for a new person to match
        # else check if it is the last attribute to match
        for attr in person.attributes.keys():
            if longest_match(DNA, attr) != int(person.attributes[attr]):
                break
            else:
                # Check database for matching profiles
                # if all attributes match
                # without breaking the loop
                # return the person's name
                if attributesLength == matchCount:
                    print(person.name)
                    return True
                matchCount += 1
                continue

    # print if there is no match
    print("No Match")

    return False


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
