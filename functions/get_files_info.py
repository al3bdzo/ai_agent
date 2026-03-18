import os

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
    
    listed_items_in_dir = []

    try:
        for listed in os.listdir(target_dir):
            listed_dir = os.path.normpath(os.path.join(target_dir, listed))
            file_size = os.path.getsize(listed_dir)
            is_dir = not os.path.isfile(listed_dir)
            listed_items_in_dir.append(f"- {listed}: file_size={file_size}, is_dir={is_dir}")
    except Exception as e:
        return f"Error: {e}"
    
    listed_items = '\n'.join(listed_items_in_dir)
    return listed_items
        