from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from lib.base import delete_all_in_folder, delete_specific_file
from lib.images import get_image_files
from lib.getDots import count_red_dots, count_green_dots, count_overlapping_green_red_dots
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Delete all files in the upload folder
        # delete_all_in_folder(app.config['UPLOAD_FOLDER'])
        today = datetime.datetime.now().strftime('%Y%m%d')

        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            split_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # delete original file
            delete_specific_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_files = get_image_files(app.config['UPLOAD_FOLDER'])
            # getting length of list
            result = []
            length = len(image_files)
            dictKey = ["red", "green", "overlapping", "image_original", "image_result"]
            for i in range(length):
                countRedDot = count_red_dots(os.path.join(app.config['UPLOAD_FOLDER'], image_files[i]))
                countGreenDot = count_green_dots(os.path.join(app.config['UPLOAD_FOLDER'], image_files[i]))
                countOverlapping = count_overlapping_green_red_dots(os.path.join(app.config['UPLOAD_FOLDER'], image_files[i]))
                write_text_on_image(os.path.join(app.config['UPLOAD_FOLDER'], image_files[i]), os.path.join(app.config['RESULT_FOLDER'], image_files[i]), str(countOverlapping), str(countGreenDot), str(countRedDot))
                picOriginal = os.path.join(app.config['UPLOAD_FOLDER'], image_files[i])
                picResult = os.path.join(app.config['RESULT_FOLDER'], image_files[i])
                dots = [countRedDot, countGreenDot, countOverlapping, picOriginal, picResult]
                result.append(dict(zip(dictKey, dots)))

            # return 'File uploaded successfully'
            log_to_daily_file(result)
            json_string = json.dumps(result, indent=4)
            return json_string
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def split_image(image_path):
    """
    Splits an image into six equal parts and saves them as separate files.
    :param image_path: The file path to the image to be split.
    """
    try:
        # Load the image
        image = Image.open(image_path)

        # Get image dimensions
        width, height = image.size

        # Calculate the size of each split image
        split_width = width / 6
        split_height = height / 6

        # Splitting the image into 6 parts
        for i in range(6):  # Two rows
            for j in range(6):  # Three columns
                # Calculate the box for cropping
                left = j * split_width
                upper = i * split_height
                right = (j + 1) * split_width
                lower = (i + 1) * split_height

                # Crop the image
                split_image = image.crop((left, upper, right, lower))

                # Save the split image
                # split_image.save(f'split_image_{i+1}_{j+1}.jpg')
                split_image.save(os.path.join(app.config['UPLOAD_FOLDER'], f'split_image_{i+1}_{j+1}.jpg'))

        print("Image split into six parts successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function for generating a unique identifier
def generate_uid():
    """
    Generates a unique identifier using UUID.
    Returns:
    - str: A unique identifier as a string.
    """
    return str(uuid.uuid4())

def write_text_on_image(image_path, output_path, text2, text3, text4, font_path=None, font_size=5):
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
Descriptions: Appends JSON data to a daily log file.
Args:
    data (dict): The data to log, must be JSON-serializable.
    log_dir (str): Directory where the log files will be stored. Default is 'logs'.
Returns:
    str: Path to the log file.
"""
def log_to_daily_file(data, log_dir="logs"):
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create the log file name based on the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"log_{current_date}.json")

    # Append the data as a new JSON object to the log file
    with open(log_file, "a") as f:
        json_entry = json.dumps(data, ensure_ascii=False)
        f.write(json_entry + "\n")
    
    return log_file

"""
Descriptions: Check if a file exists.
Args: 
    file_path (str): The path to the file to check.
Returns: 
    bool: True if the file exists, False otherwise.
"""
def is_file_exists(file_path):
    return os.path.isfile(file_path)


if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)