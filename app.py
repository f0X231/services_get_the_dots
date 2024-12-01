import os
import json
import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from urllib.parse import urlparse, parse_qs
from lib.images import split_image, write_text_on_image, download_image
from lib.base import allowed_image_file, create_date_folder
from lib.files import log_to_daily_file, read_json_file, is_file_exists, read_file_last_line, get_file_extension
from lib.getDots import count_red_dots, count_green_dots, count_overlapping_green_red_dots

app = Flask(__name__, template_folder='templates', static_url_path='/static')
BASE_DIRECTORY_UPLOAD_FOLDER = 'uploads/'
BASE_DIRECTORY_RESULT_FOLDER = 'static/images/origin'
BASE_DIRECTORY_LRESULT_FOLDER = 'static/images/results'


@app.route('/get', methods=['GET', 'POST'])
def get():
    current_url = request.url
    parsed_url = urlparse(current_url)
    query_params = parse_qs(parsed_url.query)
    urlImage = query_params['id'][0]
    # download image from url for save to sys.
    folder_path = create_date_folder(BASE_DIRECTORY_UPLOAD_FOLDER)
    getExt = get_file_extension(urlImage)
    new_filename = str(uuid.uuid4())
    unique_filename = new_filename + "." + getExt
    file_path = os.path.join(folder_path, unique_filename)
    download_image(urlImage, file_path)
    # Split the image into six parts
    split_folder_path = os.path.join(BASE_DIRECTORY_RESULT_FOLDER, new_filename)
    os.makedirs(split_folder_path, exist_ok=True)
    list_of_split_image = split_image(file_path, split_folder_path)
    # Count the number of red, green, and overlapping dots in each split image
    result = []
    dictKey = ["red", "green", "overlapping", "image"]
    length = len(list_of_split_image)
    for i in range(length):
        countRedDot = count_red_dots(list_of_split_image[i])
        countGreenDot = count_green_dots(list_of_split_image[i])
        countOverlapping = count_overlapping_green_red_dots(list_of_split_image[i])
        dots = [countRedDot, countGreenDot, countOverlapping, list_of_split_image[i]]
        result.append(dict(zip(dictKey, dots)))  

    log_to_daily_file(new_filename, result)
    return redirect(url_for('proof', id=new_filename))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Check if the post request has the file part
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return 'No selected file'
        
        if file and allowed_image_file(file.filename):
            folder_path = create_date_folder(BASE_DIRECTORY_UPLOAD_FOLDER)
            new_filename = str(uuid.uuid4())
            unique_filename = new_filename + os.path.splitext(secure_filename(file.filename))[1]
            file_path = os.path.join(folder_path, unique_filename)
            file.save(file_path)

            # Split the image into six parts
            split_folder_path = os.path.join(BASE_DIRECTORY_RESULT_FOLDER, new_filename)
            os.makedirs(split_folder_path, exist_ok=True)
            list_of_split_image = split_image(file_path, split_folder_path)

            # Count the number of red, green, and overlapping dots in each split image
            result = []
            dictKey = ["red", "green", "overlapping", "image"]
            length = len(list_of_split_image)
            for i in range(length):
                countRedDot = count_red_dots(list_of_split_image[i])
                countGreenDot = count_green_dots(list_of_split_image[i])
                countOverlapping = count_overlapping_green_red_dots(list_of_split_image[i])
                dots = [countRedDot, countGreenDot, countOverlapping, list_of_split_image[i]]
                result.append(dict(zip(dictKey, dots)))  

            log_to_daily_file(new_filename, result)
            return redirect(url_for('proof', id=new_filename))
    else:
        return render_template('upload.html')


@app.route('/proof/<string:id>', methods=['GET', 'POST'])
def proof(id):
    logFile = "logs/log_" + id + ".json"
    if is_file_exists(logFile):
        data = read_json_file(logFile)
        return render_template('checklist.html', data={"id":id, "results":data})
    else:
        return redirect(url_for('upload'))


@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        dataId = request.form.get('fileid')
        dataImage = request.form.getlist('imagepath[]')
        dataRed = request.form.getlist('red[]')
        dataGreen = request.form.getlist('green[]')
        dataOverlap = request.form.getlist('overlap[]')

        create_date_folder(BASE_DIRECTORY_LRESULT_FOLDER + '/' + dataId)
        # save new image with text number dot
        result = []
        dictKey = ["red", "green", "overlapping", "original", "result"]
        length = len(dataImage)
        for i in range(length):
            newPathImage = dataImage[i].replace(BASE_DIRECTORY_RESULT_FOLDER, "")
            picResult = BASE_DIRECTORY_LRESULT_FOLDER + newPathImage
            write_text_on_image(dataImage[i], picResult, dataOverlap[i], dataGreen[i], dataRed[i])
            dots = [int(dataRed[i]), int(dataGreen[i]), int(dataOverlap[i]), dataImage[i], picResult]
            result.append(dict(zip(dictKey, dots)))

        log_to_daily_file(dataId, result)
        return jsonify(result)
    else:
        return redirect(url_for('upload'))

@app.route('/result/<string:id>', methods=['GET'])
def result(id):
    logFile = "logs/log_" + id + ".json"
    if is_file_exists(logFile):
        data = read_file_last_line(logFile)
        if data is not None:
            return jsonify(data)
        else:
            return 'NOT FOUND'
    else:
        return redirect(url_for('upload'))


if __name__ == '__main__':
    app.run(debug=True)
