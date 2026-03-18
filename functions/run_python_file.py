import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_wd = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_wd, file_path))
        valid_target_dir = os.path.commonpath([absolute_wd, target_file]) == absolute_wd
    except Exception as e:
        return f"Error: {e}"
    
    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file]
    if args:
        command.extend(args)
    
    try:
        completed_process = subprocess.run(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            timeout=30
        )
    except Exception as e:
        return f"Error: {e}"

    result = []
    if completed_process.returncode:
        result.append(f"Process exited with code {completed_process.returncode}")
    
    if not completed_process.stdout and not completed_process.stderr:
        result.append("No output produced")
    
    if completed_process.stdout:
        result.append(f"STDOUT: {completed_process.stdout}")
    
    if completed_process.stderr:
        result.append(f"STDERR: {completed_process.stderr}")

    return '\n'.join(result)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file given its path relative to the working directory and Return its Stdout or Stderr as a string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command line arguments to pass to the python script",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single command line argument"
                )
            ),
        },
        required=["file_path"]
    )
)