#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // calculate average RGB Color
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            int average = round((red + green + blue) / 3.0);
            // set new BW Color
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // extract original RGB Values
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            // calculate Sepia Colors
            int sepiaRed = round(0.393 * red + 0.769 * green + 0.189 * blue);
            int sepiaGreen = round(0.349 * red + 0.686 * green + 0.168 * blue);
            int sepiaBlue = round(0.272 * red + 0.534 * green + 0.131 * blue);

            // apply sepia color to image
            // it can happen that a sepia color is larger than 255
            if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepiaRed;
            }

            if (sepiaGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }

            if (sepiaBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            // store value in a temporary variable and change place with the mirrored value
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // create a temporary copy of the entire image
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // iterate through the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // initalize variables for storing sum of the RGB Colors and a counter to count the number of neighbour pixels
            int sum_red = 0, sum_green = 0, sum_blue = 0, counter = 0;

            // now it gets a little ugly because we have to distinguish between corner, edge and inner pixels
            // each of them have a different number of neighbour pixels. Therefore, we have to treat them differently

            // a solution for this problem is to check if a pixel has a neighbour pixel
            // To do that we need two additional for loops
            for (int h = -1; h < 2; h++)
            {
                for (int w = -1; w < 2; w++)
                {
                    if ((i + h < 0) || (i + h > (height - 1)))
                    {
                        continue;
                    }
                    else if ((j + w < 0) || (j + w > (width - 1)))
                    {
                        continue;
                    }
                    else
                    {
                        sum_red += temp[i + h][j + w].rgbtRed;
                        sum_green += temp[i + h][j + w].rgbtGreen;
                        sum_blue += temp[i + h][j + w].rgbtBlue;
                        counter += 1;
                    }
                }
            }
            // After adding all the surrounding pixel values calculate the average value
            // However, we store them for the moment in the temporary copy of the image
            image[i][j].rgbtRed = round(sum_red / (float) counter);
            image[i][j].rgbtGreen = round(sum_green / (float) counter);
            image[i][j].rgbtBlue = round(sum_blue / (float) counter);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // create a temporary copy of the entire image
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // initialize the two different sobel filters
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    // iterate through the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // initalize variables for storing sum of the RGB Colors
            int Gx_red = 0, Gx_green = 0, Gx_blue = 0, Gy_red = 0, Gy_green = 0, Gy_blue = 0;

            // now we calculate the sobel values for each pixel. However, the corner and edge pixel have less neighbour pixel
            // and therefore we have to treat them differently. We imagine imaginary 0 values for these non-existing pixels
            // This means, we can simply ignore them, because if we multiply the sobel matrix with 0 we get 0 as a result
            // Thus, we can do the same as in the blur filter.

            for (int h = -1; h < 2; h++)
            {
                for (int w = -1; w < 2; w++)
                {
                    if ((i + h < 0) || (i + h > (height - 1)))
                    {
                        continue;
                    }
                    else if ((j + w < 0) || (j + w > (width - 1)))
                    {
                        continue;
                    }
                    else
                    {
                        Gx_red += temp[i + h][j + w].rgbtRed * Gx[h + 1][w + 1];
                        Gx_green += temp[i + h][j + w].rgbtGreen * Gx[h + 1][w + 1];
                        Gx_blue += temp[i + h][j + w].rgbtBlue * Gx[h + 1][w + 1];
                        Gy_red += temp[i + h][j + w].rgbtRed * Gy[h + 1][w + 1];
                        Gy_green += temp[i + h][j + w].rgbtGreen * Gy[h + 1][w + 1];
                        Gy_blue += temp[i + h][j + w].rgbtBlue * Gy[h + 1][w + 1];
                    }
                }
            }
            // calculate the final red, green and blue value for each pixel
            int red = round(sqrt(pow(Gx_red, 2) + pow(Gy_red, 2)));
            int green = round(sqrt(pow(Gx_green, 2) + pow(Gy_green, 2)));
            int blue = round(sqrt(pow(Gx_blue, 2) + pow(Gy_blue, 2)));

            // It can happen that a value is larger than 255, if that is the case reduce it to 255
            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }

            // assign new value to the original image
            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }
    }
    return;
}























