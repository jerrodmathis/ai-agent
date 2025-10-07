import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function, available_functions
from config import MAX_ITERS
from prompts import system_prompt


def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
        ):
            raise Exception('Fatal error: no response from function call')
        if verbose:
            print(
                f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])

    if not function_responses:
        raise Exception('Fatal error: no responses generated, exiting.')

    messages.append(types.Content(role="user", parts=function_responses))


def main():
    load_dotenv()

    if len(sys.argv) <= 1:
        print("AI Code Assistant")
        print("\nUsage: python3 main.py <prompt> [--verbose]")
        print("Example: python3 main.py 'How do I fix the calculator?'")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt, *optionalArgs = sys.argv[1:]
    verbose = "--verbose" in optionalArgs

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            response = generate_content(client, messages, verbose)
            if response:
                print("Final response:")
                print(response)
                break
        except Exception as err:
            print(f"Error in generate_content: {err}")


if __name__ == "__main__":
    main()
