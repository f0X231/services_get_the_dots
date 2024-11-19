from PIL import Image, ImageDraw, ImageFont
from flask import Flask, request, render_template_string
import os

# Create a Flask application
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return 'Invalid file or no selected file'
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return f'File uploaded successfully to {file_path}'
    return '''
    <!doctype html>
    <title>Upload an Image</title>
    <h1>Upload an Image (JPG or PNG)</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def allowed_file(filename):
    """
    Checks if the uploaded file has an allowed extension.
    """
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

if __name__ == '__main__':
    app.run(debug=True)

# Example function for adding text to an uploaded image
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
