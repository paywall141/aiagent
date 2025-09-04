import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from helpers.tools import available_functions

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
    # print(response.text)
    for call in response.function_calls:
        print(f"Calling function: {call.name}({call.args})")
    print_verbose(user_prompt, response)


def main():
    user_prompt = sys.argv[1]
    print(f"current prompt is: {user_prompt}")
    run_prompt(user_prompt)



if __name__ == "__main__":
    main()
