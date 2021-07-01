#include <stdio.h>
#include <cs50.h>

int get_input();

int main(void)
{
    // read height of pyramid from user
    int height = get_input();

    // plot the pyramid
    for (int row = 0; row < height; row++)
    {
        for (int col = 1; col <= height; col++)
        {
            // print empty space at the beginning
            if (col < height - row)
            {
                printf(" ");
            }
            else if (row == height - col)
            {
                // print # on the left hand side
                for (int i = 0; i <= row; i++)
                {
                    printf("#");
                }
                // print empty space in the middle
                printf("  ");

                // print # on the right hand side
                for (int i = row; i >= 0; i--)
                {
                    printf("#");
                }
                printf("\n");
            }
        }
    }
}

int get_input(void)
{
    int height;
    do
    {
        height = get_int("Enter the height of the pyramid: ");
    }
    while (height <= 0 || height > 8);

    return height;
}