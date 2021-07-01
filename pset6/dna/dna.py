import pandas as pd
import sys
import numpy as np


def main():
    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py FILENAME")

    # extract database with people and their STR
    database = pd.read_csv(sys.argv[1])

    # read entire dna chain
    with open(sys.argv[2], "r") as raw_sequence:
        sequence = raw_sequence.read()

    # extract dna sequences
    dna = database.columns
    dna = dna.drop("name")

    # initialize empty list to store max STR
    max_STR = []
    # count the longest consecutive sequence for each dna pattern in the entire dna sequence
    for i in range(0, len(dna)):
        max_STR.append(determine_maxSTR(dna[i], sequence))

    # check for a match and print result
    check_Matching(database, max_STR)


def check_Matching(database, max_STR):
    # extract just the values from the database dataframe and check if a row is equal to the max_STR array
    # if that is the case print the name and leave the function
    data = database.loc[:, database.columns != 'name'].to_numpy()
    for row in range(0, len(data)):
        if np.array_equal(max_STR, data[row]):
            name = database.loc[row, "name"]
            print(name)
            return None  # leave function if match was found

    # if no match was found
    print("No match")


def determine_maxSTR(dna, sequence):
    # extract the index of each start of the searched sequence
    # find returns the index of the first occurences of a string pattern
    # therefore, we increase the start value to always find the next one
    indices = []
    start = 0
    for i in range(0, len(sequence)):
        idx = sequence.find(dna, start)
        if (idx == i):
            indices.append(idx)
            start = i + len(dna)

    # find the longest consecutive sequence
    # to do that count of how many elements the difference in their index is only 3
    # save it in a temporary counter, as soon as the temporary counter is larger than the final counter, overwrite it
    temp_counter = 0
    max_counter = 0
    for i in range(0, len(indices) - 1):
        if indices[i + 1] - indices[i] == len(dna):
            temp_counter += 1
        if temp_counter > max_counter:
            max_counter = temp_counter
        if indices[i + 1] - indices[i] != len(dna):
            temp_counter = 0

    # increase max_counter by 1 because it does not count the last element
    max_counter += 1

    return max_counter


if __name__ == "__main__":
    main()