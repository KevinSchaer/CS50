import sys


def main():
    # get user input
    while True:  # repeat while input is negative
        input_number = input("Enter a card number: ")
        length = len(input_number)
        if length >= 13 and length <= 16:  # if input has a valid length break
            break
        elif length < 13:  # length is too short exit
            print("INVALID")
            sys.exit(0)

    # convert input_number from string to an array of integer numbers
    number = [int(digit) for digit in input_number]

    validate_card(number)


def validate_card(number):
    num2 = []
    num = []
    for idx, digit in enumerate(reversed(number)):
        if idx % 2 != 0:
            digit = 2 * digit
            if digit > 9:
                num2.append(get_digit(digit, 0))
                num2.append(get_digit(digit, 1))
            else:
                num2.append(digit)
        else:
            num.append(digit)

    # calculate sum of numbers which have to be multiplied by two
    sum2_number = sum(num2)
    # calculate sum of the rest of numbers
    sum_number = sum(num)
    # calculate checksum
    check_sum = sum_number + sum2_number

    check_manufacturer(check_sum, number)


def check_manufacturer(check_sum, number):
    # check if checksum is valid
    if get_digit(check_sum, 0) != 0:
        print("INVALID")
    # check which card company it is
    else:
        if number[0] == 3 and (number[1] == 4 or number[1] == 7):
            print("AMEX")
        elif number[0] == 4:
            print("VISA")
        elif number[0] == 5 and (number[1] == 1 or number[1] == 2 or number[1] == 3 or number[1] == 4 or number[1] == 5):
            print("MASTERCARD")
        else:
            print("INVALID")


def get_digit(number, n):
    return number // 10**n % 10


if __name__ == "__main__":
    main()