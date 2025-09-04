import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from helpers.tools import available_functions
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
if len(sys.argv) < 2 :
    print("No prompt provided. Exiting with code 1")
    sys.exit(1)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
def verbose_flag():
    return "--verbose" in sys.argv[2:]

def print_verbose(prompt, res):
    if verbose_flag():
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")


def run_prompt(user_prompt):
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model ='gemini-2.0-flash-001', 
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    # this is where the ai executes function calls
    for call in response.function_calls or []:
        result_content = call_function( call, verbose = verbose_flag() )
        try:
            func_response = result_content.parts[0].function_response.response
        except AttributeError:
            raise RuntimeError(f"Fatal: call_function did not return a valid types.Content for {call.name}")
        print(f"Function {call.name} returned: {func_response}")

    print_verbose(user_prompt, response)


def main():
    user_prompt = sys.argv[1]
    print(f"current prompt is: {user_prompt}")
    run_prompt(user_prompt)



if __name__ == "__main__":
    main()
