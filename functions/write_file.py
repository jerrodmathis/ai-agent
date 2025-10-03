import os


def write_file(working_directory, file_path, content):
    try:
        abs_wd = os.path.abspath(working_directory)
        rel_path = os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(rel_path)
        if not abs_path.startswith(abs_wd):
            raise Exception(f'Cannot write to "{
                            file_path}" as it is outside the permitted working directory')
    except OSError as oserr:
        return f'Error: {oserr}'
    except Exception as err:
        return f'Error: {err}'
    else:
        try:
            if not os.path.exists(os.path.dirname(abs_path)):
                os.makedirs(os.path.dirname(abs_path))
            with open(abs_path, 'w') as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except OSError as oserr:
            return f'Error: {oserr}'
