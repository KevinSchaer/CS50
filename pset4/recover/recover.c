#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// define the datatype byte
typedef uint8_t byte;

int main(int argc, char *argv[])
{
    // potential error handling
    if (argc != 2)
    {
        printf("Usage: recover forensicfilename.raw\n");
        return 1;
    }

    // Open files
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // declare temporary buffer for the 512 byte blocks
    byte buffer[512];
    // declare a counter to count number of jpgs found
    int jpg_counter = 0;

    // initialize output file
    FILE *image;

    // go through card.raw until there are no blocks left
    // read in each step a 512 byte block
    // if we haven't already found a jpg go through the loop until we find one
    // as soon as we find a jpg header check if we have already found one
    // if that is the case close the old file
    // than open a new file with the increasing number as file name
    // if we have already found a jpg or found the very first jpg we can write each 512 byte block to the output file
    // if we find a new jpg header close the old file and open a new one
    while (fread(buffer, sizeof(buffer), 1, file)) // read 512 bytes once from file and save them in buffer
    {
        // check if header corresponds to the beginning of a jpg file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) // bitwise addition
        {
            // if this is true we can write but first we have to close the old file
            if (jpg_counter >= 1)
            {
                fclose(image);
            }

            // create naming and open a new file
            char filename[8];
            sprintf(filename, "%03i.jpg", jpg_counter);
            image = fopen(filename, "w");
            jpg_counter += 1;
        }

        if (jpg_counter >= 1)
        {
            // write content in file
            fwrite(buffer, sizeof(buffer), 1, image);
        }
    }

    // close all files
    fclose(file);
    fclose(image);
}





