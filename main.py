import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

function_name_map = {
    'get_files_info': get_files_info,
    'get_file_content': get_file_content,
    'run_python_file': run_python_file,
    'write_file': write_file,
}


def call_function(function_call_part: types.FunctionCall, verbose=False):
    name = function_call_part.name
    args = function_call_part.args
    if verbose:
        print(f"Calling function: {name}({args})")
    else:
        print(f"Calling function: {name}")

    if name in function_name_map:
        result = function_name_map[name](
            working_directory='./calculator', **args)
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


def main():
    if len(sys.argv) <= 1:
        print("No prompt provided")
        print("Usage: python3 main.py <prompt>")
        sys.exit(1)

    prompt, *optionalArgs = sys.argv[1:]
    verbose = "--verbose" in optionalArgs

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if response.function_calls is not None:
        for function_call in response.function_calls:
            result = call_function(function_call, verbose)
            if result.parts[0].function_response.response:
                if verbose:
                    print(
                        f"-> {result.parts[0].function_response.response}")
            else:
                raise Exception('Fatal error: no response from function call')
    else:
        print(response.text)

    if (verbose):
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
