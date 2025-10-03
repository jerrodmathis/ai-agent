import os


def get_files_info(working_directory, directory="."):
    abs_wd = os.path.abspath(working_directory)
    rel_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(rel_path)
    if not abs_path.startswith(abs_wd):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'

    contents = os.listdir(abs_path)
    file_info = []
    for file in contents:
        file_size = os.path.getsize(os.path.join(abs_path, file))
        is_dir = os.path.isdir(os.path.join(abs_path, file))
        file_info.append(f'- {file}: file_size={
                         file_size} bytes, is_dir={is_dir}')
    return '\n'.join(file_info)
