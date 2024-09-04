from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from lib.delete import delete_all_in_folder, delete_specific_file
from lib.images import get_image_files
from lib.getDots import count_red_dots, count_green_dots, count_overlapping_green_red_dots
import os
import json

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Delete all files in the upload folder
        delete_all_in_folder(app.config['UPLOAD_FOLDER'])

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
            dictKey = ["red", "green", "overlapping"]
            for i in range(length):
                countRedDot = count_red_dots(os.path.join(app.config['UPLOAD_FOLDER'], image_files[i]))
                countGreenDot = count_green_dots(os.path.join(app.config['UPLOAD_FOLDER'], image_files[i]))
                countOverlapping = count_overlapping_green_red_dots(os.path.join(app.config['UPLOAD_FOLDER'], image_files[i]))
                dots = [countRedDot, countGreenDot, countOverlapping]
                result.append(dict(zip(dictKey, dots)))

            # return 'File uploaded successfully'
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



if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)