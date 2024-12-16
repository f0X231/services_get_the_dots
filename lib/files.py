import os
import json

"""
Reads a JSON file and returns its content as a dictionary.
Args:
    file_path: Path to the JSON file
Return: 
    json: Dictionary containing the JSON data
"""
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file at '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


"""
Descriptions: Appends JSON data to a daily log file.
Args:
    data (dict): The data to log, must be JSON-serializable.
    log_dir (str): Directory where the log files will be stored. Default is 'logs'.
Returns:
    str: Path to the log file.
"""
def log_to_daily_file(filename, data, log_dir="services_get_the_dots/logs"):
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create the log file name based on the current date
    # current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"log_{filename}.json")

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


"""Reads and parses the last line of a JSON Lines file."""
def read_file_last_line(file_path):
    try:
        with open(file_path, "rb") as file:
            # Move to the end of the file
            file.seek(0, 2)
            if file.tell() == 0:  # Check if the file is empty
                return None
            # Move backward to find the last newline
            file.seek(-2, 2)
            while file.tell() > 0:
                char = file.read(1)
                if char == b'\n':
                    break
                file.seek(-2, 1)
            # Read and decode the last line
            last_line = file.readline().decode().strip()
            return json.loads(last_line)  # Parse the JSON line
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Last line is not valid JSON.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


"""
Gets the file extension from a filename.
Args:
filename: The filename to process.
Returns:
The file extension (without the dot), or None if no extension is found.
"""
def get_file_extension(filename):
  _, ext = os.path.splitext(filename)
  return ext[1:] if ext else None