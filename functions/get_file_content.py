import os

def get_file_content(working_directory, file_path):
    # If the file_path is outside the working_directory
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    # If the file_path is not a file
    return f'Error: File not found or is not a regular file: "{file_path}"'

    # Read the file and return its contents as a string
