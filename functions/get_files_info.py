import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        abs_dir = os.path.abspath(working_directory)
    else:
        abs_dir = os.path.abspath(os.path.join(working_directory, directory))
    abs_working = os.path.abspath(working_directory)

    # Check if abs_dir is inside abs_working
    if not os.path.commonpath([abs_working, abs_dir]) == abs_working:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.exists(abs_dir):
        return f'Error: Directory "{directory}" does not exist'
    if not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'

    entries = []
    with os.scandir(abs_dir) as it:
        for entry in it:
            info = entry.stat()
            entries.append({
                'name': entry.name,
                'size': info.st_size,
                'is_directory': entry.is_dir()
            })

    # Build the formatted string
    result_lines = []
    for entry in entries:
        result_lines.append(
            f"- {entry['name']}: file_size={entry['size']} bytes, is_dir={entry['is_directory']}"
        )
    return "\n".join(result_lines)

if __name__ == "__main__":
    working_directory = os.getcwd()
    directory = None  # Change this to a specific directory if needed
    files_info = get_files_info(working_directory, directory)
    if isinstance(files_info, str):
        print(files_info)
    else:
        for info in files_info:
            print(info)