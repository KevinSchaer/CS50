#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int check_key(string key, int argc);
char cypher(char text, string key);

int main(int argc, string argv[])
{
    // check if key is valid
    if (check_key(argv[1], argc) == 1)
    {
        return 1;
    }

    // extract key from user input
    string key = argv[1];

    string text = get_string("plaintext: ");

    char ciphertext[strlen(text)];

    // encrypt every character from the user input
    printf("ciphertext: ");
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        ciphertext[i] = cypher(text[i], key);
        printf("%c", ciphertext[i]);
    }
    printf("\n");

}

int check_key(string key, int argc)
{
    // check if user has entered a key
    if (argc != 2)
    {
        printf("You have not entered a key\n");
        return 1;
    }

    // length of key
    int length = strlen(key);

    // check the size of the key
    if (length != 26)
    {
        printf("Your key has not the correct size!\n");
        return 1;
    }

    for (int i = 0; i < length; i++)
    {
        if (isalpha(key[i]) == false) // check if the key contains non-alphabetic characters
        {
            printf("Your key contains non alphabetic characters!\n");
            return 1;
        }
        // check if a character appears more than once
        for (int j = i + 1; j < length; j++)
        {
            if (toupper(key[j]) == toupper(key[i]))
            {
                printf("Your key contains a letter more than once!\n");
                return 1;
            }
        }
    }
    return 0;
}

char cypher(char text, string key)
{
    // replace the original character with the encrypted one
    char cyphertext;

    if (isalpha(text)) // if input is alphabetical character
    {
        if (isupper(text)) // if input is uppercase
        {
            cyphertext = toupper(key[(text - 65)]);
            return cyphertext;
        }
        else // if input is lower case; key is always upper case
        {
            cyphertext = tolower(key[(text - 97)]);
            return cyphertext;
        }
    }
    else
    {
        return text;
    }
}