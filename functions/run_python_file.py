import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_wd = os.path.abspath(working_directory)
        rel_path = os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(rel_path)
        if not abs_path.startswith(abs_wd):
            raise Exception(f'Cannot execute "{
                            file_path}" as it is outside the permitted working directory')
        if not os.path.exists(abs_path):
            raise Exception(f'File "{file_path}" not found.')
        if not abs_path.endswith('.py'):
            raise Exception(f'"{file_path}" is not a Python file.')
    except OSError as oserr:
        return f'Error: {oserr}'
    except Exception as err:
        return f'Error: {err}'
    else:
        try:
            completed_process = subprocess.run(
                ['python3', abs_path, *args],
                timeout=30,
                capture_output=True,
                cwd=abs_wd
            )
        except Exception as err:
            return f'Error: executing Python file: {err}'
        else:
            output = f'STDOUT: {completed_process.stdout}\n'
            output += f'STDERR: {completed_process.stderr}\n'

            if completed_process.returncode != 0:
                output += f'Process exited with code {
                    completed_process.returncode}'

            if len(output) > 0:
                return output
            else:
                return 'No output produced.'
