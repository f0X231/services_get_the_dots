from PIL import Image, ImageDraw, ImageFont

def write_text_on_image(image_path, text, output_path, position=(10, 10), font_path=None, font_size=30, text_color=(255, 255, 255)):
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
    draw.text(position, text, font=font, fill=text_color)

    # Save the modified image
    image.save(output_path)

    print(f"Image saved to {output_path}")

# Example usage
# write_text_on_image('input.jpg', 'Hello, World!', 'output.jpg', position=(50, 50), font_size=40)