import os
from config import MAX_FILE_READ_CHARS

def get_file_content(working_directory, file_path):
    try:
        absolute_wd = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_wd, file_path))
        valid_target_dir = os.path.commonpath([absolute_wd, target_file]) == absolute_wd
    except Exception as e:
        return f"Error: {e}"

    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_file, "r") as f:
        file_content = f.read(MAX_FILE_READ_CHARS)
        check_limit = f.read(1)
    
    if check_limit:
        file_content += f'[...File "{file_path}" truncated at {MAX_FILE_READ_CHARS} characters]'
    
    return file_content
    
