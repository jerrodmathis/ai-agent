from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from config import WORK_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

function_map = {
    'get_files_info': get_files_info,
    'get_file_content': get_file_content,
    'run_python_file': run_python_file,
    'write_file': write_file,
}


def call_function(function_call_part: types.FunctionCall, verbose=False):
    name = function_call_part.name
    args = function_call_part.args
    if verbose:
        print(f' - Calling function: {name}({args})')
    else:
        print(f' - Calling function: {name}')

    if name in function_map:
        args = dict(args)
        args['working_directory'] = WORK_DIR
        result = function_map[name](**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"result": result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )
