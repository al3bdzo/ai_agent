import os
# from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        absolute_wd = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_wd, directory))
        valid_target_dir = os.path.commonpath([absolute_wd, target_dir]) == absolute_wd
    except Exception as e:
        return f"Error: {e}"

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        listed_items_in_dir = []
        for listed in os.listdir(target_dir):
            listed_dir = os.path.normpath(os.path.join(target_dir, listed))
            file_size = os.path.getsize(listed_dir)
            is_dir = os.path.isdir(listed_dir)
            listed_items_in_dir.append(f"- {listed}: file_size={file_size}, is_dir={is_dir}")
        listed_items = '\n'.join(listed_items_in_dir)
    except Exception as e:
        return f"Error: {e}"
    
    return listed_items


schema_get_files_info = {
    "type" : "function",
    "name" : "get_files_info",
    "description" : "Lists files in a specified directory relative to the working directory, providing file size and directory status",
    "parameters" : {
        "type" : "object",
        "properties" : {
            "directory":{
                "type": "string",
                "description":"Directory path to list files from, relative to the working directory (default is the working directory itself)"
            }
        }
    }
}

# schema_get_files_info = types.FunctionDeclaration(
#     name="get_files_info",
#     description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
#     parameters=types.Schema(
#         type=types.Type.OBJECT,
#         properties={
#             "directory": types.Schema(
#                 type=types.Type.STRING,
#                 description="Directory path to list files from, relative to the working directory (default is the working directory itself)"
#             )
#         }
#     )
# )