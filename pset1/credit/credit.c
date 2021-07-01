#include <stdio.h>
#include <cs50.h>

long get_input_number(void);
void check_card(long number, int checksum, int counter, int start_digit);

int main(void)
{
    // read input number
    long number = get_input_number();
    // store number in a new variable that we can keep the original number
    long result = number;
    // define some helper variables and a counter for the length of the number
    int mult_2 = 0, other = 0, counter = 0, checksum = 0;
    int modulo, modulo2, start_digit;

    // determine different components for checksum and the length of the creditcard number
    do
    {
        // save the first 2 digits of the credicard number
        if (result < 100 && result >= 10)
        {
            start_digit = result;
        }

        modulo = result % 10;
        // handle the digits which have to be multiplid by 2
        if (counter % 2 != 0)
        {
            modulo2 = 2 * modulo;
            // handle the special case of a modulo*2 with more than one digit
            if (modulo2 > 9)
            {
                for (int i = 0; i < 2; i++)
                {
                    mult_2 = mult_2 + (modulo2 % 10);
                    modulo2 = modulo2 / 10;
                }
            }
            // add the digits which have to be multiplid by two
            else
            {
                mult_2 = mult_2 + modulo2;
            }
        }
        // handle the digits which doesn't have to be multiplid by 2
        else
        {
            other = other + modulo;
        }
        // remove the last digit of the creditcard number and raise the counter by 1
        result = result / 10;
        counter += 1;
    }
    while (result > 0);

    // calculate the checksum of the creditcard
    checksum = mult_2 + other;

    // check if card is valid
    check_card(number, checksum, counter, start_digit);
}

// %%%%%%%%%%%%%%Functions%%%%%%%%%%%%%%%%%%%%%%%

long get_input_number(void)
{
    long number;
    do
    {
        number = get_long("Enter your creditcard number: \n");
    }
    while (number < 0);

    return number;
}


void check_card(long number, int checksum, int counter, int start_digit)
{
    // if checksum is valid
    if (checksum % 10 == 0 && counter >= 13 && counter <= 16)
    {
        // distinguish between different start digits
        switch (start_digit)
        {
            // would also be possible to put on one line
            // if the first case is fulfilled it performes the next possible task although this task is described in another case
            case 34:
            case 37:
                printf("Number: %li\n", number);
                printf("AMEX\n");
                break;
            case 40:
            case 41:
            case 42:
            case 43:
            case 44:
            case 45:
            case 46:
            case 47:
            case 48:
            case 49:
                printf("Number: %li\n", number);
                printf("VISA\n");
                break;
            case 51:
            case 52:
            case 53:
            case 54:
            case 55:
                printf("Number: %li\n", number);
                printf("MASTERCARD\n");
                break;
            default:
                printf("Number: %li\n", number);
                printf("INVALID\n");
                break;
        }
    }
    else
    {
        printf("Number: %li\n", number);
        printf("INVALID\n");
    }
}