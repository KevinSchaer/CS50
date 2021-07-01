def main():
    # read user input
    text = input("Text: ")

    # calculate index of the text
    index = calculate_index(text)

    # determine and print final grade
    determine_grade(index)


def calculate_index(text):
    # count letters, words (words = whitespaces + 1) and sentences
    letters = sum(char.isalpha() for char in text)
    spaces = sum(space.isspace() for space in text)
    words = spaces + 1
    sentences = text.count(".") + text.count("!") + text.count("?")

    # determine index
    index = round(0.0588 * (100 * letters / words) - 0.296 * (100 * sentences / words) - 15.8)
    return index


def determine_grade(index):
    # print index
    if index < 1:
        print("Before Grade 1")
    elif index >= 1 and index < 16:
        print("Grade {0}".format(index))
    else:
        print("Grade 16+")


if __name__ == "__main__":
    main()