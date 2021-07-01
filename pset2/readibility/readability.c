#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int calculate_index(string text);
void determine_grade(int index);

int main(void)
{
    string text = get_string("Enter your text: \n"); // get user input

    int index = calculate_index(text);

    determine_grade(index); // print the grade of the input
}

int calculate_index(string text)
{
    int letters = 0;
    int words = 1; // because we count whitespaces -> number of words == number of whitespaces + 1
    int sentences = 0;

    for (int i = 0, length = strlen(text); i < length; i++) // go through every character in the text
    {
        if (isalpha(text[i]) != false) // check if character is a letter like a, b, c, etc.
        {
            letters += 1;
        }

        if (isspace(text[i]) != false) // count whitespaces
        {
            words += 1;
        }
        switch (text[i]) // check for symbols which indicate the end of a sentence
        {
            case '.':
            case '?':
            case '!':
                sentences += 1;
                break;
            default:
                break;
        }
    }

    printf("letters: %i\n", letters);
    printf("words: %i\n", words);
    printf("sentences: %i\n", sentences);

    // letters per 100 words and sentences per 100 words, we use the 100.0 to be sure that we get a float result
    // round the result to the next integer value
    int index = round(0.0588 * (100.0 * letters / words) - 0.296 * (100.0 * sentences / words) - 15.8);

    return index;
}

void determine_grade(int index)
{
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 1 && index < 16)
    {
        printf("Grade %i\n", index);
    }
    else
    {
        printf("Grade 16+\n");
    }
}














