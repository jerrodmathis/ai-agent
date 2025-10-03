import os

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    try:
        abs_wd = os.path.abspath(working_directory)
        rel_path = os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(rel_path)
        if not abs_path.startswith(abs_wd):
            raise Exception(
                f'Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(abs_path):
            raise Exception(
                f'File not found or is not a regular file: "{file_path}"')
    except OSError as oserr:
        return f'Error: {oserr}'
    except Exception as err:
        return f'Error: {err}'
    else:
        try:
            f = open(abs_path, 'r')
        except OSError as oserr:
            return f'Error: {oserr}'
        else:
            content = f.read(MAX_CHARS)
            if len(content) == MAX_CHARS:
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters].'
            f.close()
            return content
