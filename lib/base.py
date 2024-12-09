import os
import json
import shutil
from datetime import datetime

"""
Checks if the file extension is allowed.
Args:
    filename (str): filename and extension to be checked.
Returns:
    boolean: True if the extension is allowed, False otherwise.
"""
def allowed_image_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
Creates a folder structure in the format of 'year/month/day' within the specified base path.
Args:
    base_path (str): The base path where the folder structure will be created.
Returns:
    str: The full path to the created folder.
"""
def create_date_folder(base_path):
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    folder_path = os.path.join(base_path, year, month, day)
    os.makedirs(folder_path, exist_ok=True)

    return folder_path

"""
Deletes folder include all files and subdirectories in a folder.
Args:
    folder_path (str): path to the folder to be deleted.
Returns:
    boolean: delete successfully or not.
"""
def delete_all_in_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Delete all files and subdirectories in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Delete file or link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Delete directory
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        # print(f"All files and subdirectories in {folder_path} have been deleted.")
        return True
    else:
        # print(f"The folder {folder_path} does not exist.")
        return False

"""
Delete specific file.
Args:
    file_path (str): path file for delete it.
Returns:
    boolean: delete successfully or not.
"""
def delete_specific_file(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        try:
            os.remove(file_path)  # Delete the file
            return True
        except Exception as e:
            # print(f"Failed to delete {file_path}. Reason: {e}")
            return False
    else:
        # print(f"The file {file_path} does not exist.")
        return False


"""
Checks if a parameter is set (not None) and not empty.

:param param: The parameter to check
:return: True if the parameter is set and not empty, False otherwise
"""
def is_set_and_not_empty(param):
    # Check if the parameter is None
    if param is None:
        return False
    
    # Check for emptiness for strings, lists, dictionaries, etc.
    if isinstance(param, (str, list, tuple, dict, set)) and len(param) == 0:
        return False

    # For other types (e.g., numbers), return True since they can't be "empty"
    return True