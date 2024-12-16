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
        files = request.files.getlist('files[]')
        file_count = len(files)

        if file_count <= 0:
            return 'No selected file'

        listFileName = []
        for file in files:
            # file.save(f"uploads/{file.filename}")
            # file = request.files['file']
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
                listFileName.append(new_filename)

        paramURI = ''
        if len(listFileName) > 1:
            paramURI = ','.join(listFileName)
        else:
            paramURI = listFileName[0]
        return redirect(url_for('proof', id=paramURI))
    else:
        return render_template('upload.html')


@app.route('/proof/<string:id>', methods=['GET', 'POST'])
def proof(id):
    if id != "":
        logid = id.split(',')
        if len(logid) > 1:
            chkFileInFolder = 0
            listFileName = []
            dataOverall = []
            for filename in logid:
                logFile = "logs/log_" + filename + ".json"
                if is_file_exists(logFile):
                    chkFileInFolder += 1
                    listFileName.append(filename)
                    data = read_json_file(logFile)
                    dataOverall.append(data)
            if chkFileInFolder == len(logid):
                print(dataOverall)
                return render_template('checklist.html', data={"id":listFileName, "results":dataOverall, "length": len(logid)})
            else:
                return redirect(url_for('upload'))
        else:
            logFile = "logs/log_" + id + ".json"
            if is_file_exists(logFile):
                data = read_json_file(logFile)
                return render_template('checklist.html', data={"id":id, "results":data, "length": 1})
            else:
                return redirect(url_for('upload'))
    else:
        return redirect(url_for('upload'))


@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        dataId = request.form.getlist('fileid[]')
        dataImage = {}
        dataRed = {}
        dataGreen = {}
        dataOverlap = {}
        resultOverall = []
        for l in range(len(dataId)):
            inxDataId = l
            dataImage[inxDataId] = request.form.getlist(f'imagepath[{inxDataId}][]')
            dataRed[inxDataId] = request.form.getlist(f'red[{inxDataId}][]')
            dataGreen[inxDataId] = request.form.getlist(f'green[{inxDataId}][]')
            dataOverlap[inxDataId] = request.form.getlist(f'overlap[{inxDataId}][]')
            create_date_folder(BASE_DIRECTORY_LRESULT_FOLDER + '/' + dataId[inxDataId])
            # save new image with text number dot
            result = []
            dictKey = ["red", "green", "overlapping", "original", "result"]
            length = len(dataImage[inxDataId])
            for i in range(length):
                newPathImage = dataImage[inxDataId][i].replace(BASE_DIRECTORY_RESULT_FOLDER, "")
                picResult = BASE_DIRECTORY_LRESULT_FOLDER + newPathImage
                write_text_on_image(dataImage[inxDataId][i], picResult, dataOverlap[inxDataId][i], dataGreen[inxDataId][i], dataRed[inxDataId][i])
                dots = [int(dataRed[inxDataId][i]), int(dataGreen[inxDataId][i]), int(dataOverlap[inxDataId][i]), dataImage[inxDataId][i], picResult]
                result.append(dict(zip(dictKey, dots)))
            tmpData = {"id": dataId[inxDataId], "data": result}
            resultOverall.append(tmpData)
            log_to_daily_file(dataId[inxDataId], result)
        return jsonify(resultOverall)
    else:
        return redirect(url_for('upload'))

@app.route('/result/<string:id>', methods=['GET'])
def result(id):
    logFile = "logs/log_" + id + ".json"
    if is_file_exists(logFile):
        data = read_file_last_line(logFile)
        if data is not None:
            return jsonify({"id": id, "data": data})
        else:
            return 'NOT FOUND'
    else:
        return redirect(url_for('upload'))


if __name__ == '__main__':
    app.run(debug=True)
