import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        absolute_wd = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_wd, file_path))
        valid_target_dir = os.path.commonpath([absolute_wd, target_file]) == absolute_wd
    except Exception as e:
        return f"Error: {e}"

    if not valid_target_dir:
        return f'Error: Cannot Write "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        dir_name = os.path.dirname(target_file)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file given its path relative to the working directory and the desired content to be written",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to file"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file"
            )
        },
        required=["file_path", "content"]
    )
)