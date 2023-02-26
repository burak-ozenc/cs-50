#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BUFFER_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // check arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // open file
    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        return 1;
    }

    // set output image to null
    FILE *img = NULL;

    // an array for storing 512 bytes
    BYTE buffer[BUFFER_SIZE];

    char fileName[8];
    int counter = 0;
    while (fread(buffer, sizeof(BYTE), BUFFER_SIZE, file) == BUFFER_SIZE)
    {
        // check if an image file is starting, if not continue to write
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && buffer[3] >= 0xe0 && buffer[3] <= 0xef)
        {
            // close existing file if it is not the first file
            if (counter > 0)
            {
                fclose(img);
            }

            sprintf(fileName, "%03i.jpg", counter);
            img = fopen(fileName, "w");
            fwrite(&buffer, sizeof(BYTE), BUFFER_SIZE, img);
            counter += 1;
        }
        else if (counter > 0)
        {
            fwrite(&buffer, sizeof(BYTE), BUFFER_SIZE, img);
        }

    }

    // close file and image
    fclose(file);
    fclose(img);

    return 0;
}