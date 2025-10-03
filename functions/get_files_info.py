import os


def get_files_info(working_directory, directory="."):
    try:
        abs_wd = os.path.abspath(working_directory)
        rel_path = os.path.join(working_directory, directory)
        abs_path = os.path.abspath(rel_path)
        if not abs_path.startswith(abs_wd):
            raise Exception(
                f'Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(abs_path):
            raise Exception(f'"{directory}" is not a directory')
    except OSError as oserr:
        return f'Error: {oserr}'
    except Exception as err:
        return f'Error: {err}'
    else:
        try:
            file_info = list(map(lambda f: (
                f,
                os.path.getsize(os.path.join(abs_path, f)),
                os.path.isdir(os.path.join(abs_path, f))
            ), os.listdir(abs_path)))
        except OSError as oserr:
            return f'Error: {oserr}'
        else:
            file_info_strings = list(map(
                lambda info: f'- {info[0]}: file_size={info[1]}, is_dir={info[2]}', file_info))
            return '\n'.join(file_info_strings)
