import os
import requests
from PIL import Image, ImageDraw, ImageFont

def get_image_files(directory):
    # List of image file extensions to look for
    # image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg']
    image_extensions = ['.jpg', '.jpeg', '.png']

    # Get all files in the directory
    files = os.listdir(directory)

    # Filter the list to only include image files
    image_files = [file for file in files if os.path.splitext(file)[1].lower() in image_extensions]
    
    # Sort the list of image files alphabetically
    image_files.sort()

    return image_files

# Example usage
# directory_path = '/path/to/your/directory'
# image_files = get_image_files(directory_path)
# print(image_files)


"""
Splits an image into six equal parts and saves them as separate files.
Args:
    image_path (str): The file path to the image to be split.
Returns:
    str: The full path to the created folder.
"""
def split_image(image_path, save_path, split_num=6):
    try:
        print('processing image split')
        # Load the image
        image = Image.open(image_path)

        # Get image dimensions
        width, height = image.size

        # Calculate the size of each split image
        split_width = width / split_num
        split_height = height / split_num

        # Splitting the image into 6 parts
        list_of_images = []
        for i in range(split_num):  # Two rows
            for j in range(split_num):  # Three columns
                # Calculate the box for cropping
                left = j * split_width
                upper = i * split_height
                right = (j + 1) * split_width
                lower = (i + 1) * split_height

                # Crop the image
                new_split_image = image.crop((left, upper, right, lower))

                # Save the split image
                dot_image_name_and_path = os.path.join(save_path, f'dot_{i+1}_{j+1}.jpg')
                new_split_image.save(dot_image_name_and_path)
                list_of_images.append(dot_image_name_and_path)

        # print("Image split into six parts successfully!")
        return list_of_images
    except Exception as e:
        # print(f"An error occurred: {e}")
        return False


"""
Writes text on an image and saves it to a specified output path.
Parameters:
- image_path (str): Path to the input image.
- text (str): Text to write on the image.
- output_path (str): Path to save the output image.
- position (tuple): (x, y) position of the text on the image.
- font_path (str): Path to a .ttf font file. If None, a default font is used.
- font_size (int): Size of the font.
- text_color (tuple): Color of the text in RGB format.
"""
def write_text_on_image(image_path, output_path, text2, text3, text4, font_path=None, font_size=5):
    # Open the image
    image = Image.open(image_path)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Load the font
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    # Add text to the image
    position2 = (140, 5)
    text_color2 = (255, 255, 255) # white
    draw.text(position2, text2, font=font, fill=text_color2)

    position3 = (5, 130)
    text_color3 = (0, 102, 0) # green
    draw.text(position3, text3, font=font, fill=text_color3)

    position4 = (140, 130)
    text_color4 = (255, 0, 0) # red
    draw.text(position4, text4, font=font, fill=text_color4)

    # Save the modified image
    image.save(output_path)

    print(f"Image saved to {output_path}")

"""
Downloads an image from the specified URL and saves it to the given path.

:param url: str, the URL of the image to download
:param save_path: str, the local file path to save the image
:return: None
"""
def download_image(url, save_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        # Check if the request was successful
        if response.status_code == 200:
            # Write the content to a file in binary mode
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image successfully downloaded and saved to {save_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")