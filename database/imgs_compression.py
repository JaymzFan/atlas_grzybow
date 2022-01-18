# run this in any directory
# add -v for verbose
# get Pillow (fork of PIL) from
# pip before running -->
# pip install Pillow

# import required libraries
import os
import sys
import time
from PIL import Image



# Define a main function
def main():
    verbose = False

    formats = ('.png')

    # looping through all the files
    # in a current directory
    for file in os.listdir('database/intermediate/Grzyby_Razem_zdjecia'):

        # If the file format is JPG or JPEG
        if os.path.splitext(file)[1].lower() in formats:

            if file == 'compressed':
                continue
            print(file)
            folder_input_path = 'database/intermediate/Grzyby_Razem_zdjecia/'
            folder_output_path = 'database/intermediate/Grzyby_Razem_zdjecia/compressed/'
            filepath = os.path.join(folder_input_path,
                                    file)

            # open the image
            picture = Image.open(filepath)
            picture = picture.convert("RGB")

            # Save the picture with desired quality
            # To change the quality of image,
            # set the quality variable at
            # your desired level, The more
            # the value of quality variable
            # and lesser the compression

            picture.save(folder_output_path + file.replace("png", 'JPEG'),
                         "JPEG",
                         optimize=True,
                         quality=100)
    print("Done")


# Driver code
if __name__ == "__main__":
    main()