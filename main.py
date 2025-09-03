import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)
if len(sys.argv) < 2 :
    print("No prompt provided. Exiting with code 1")
    sys.exit(1)

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
    )
    print(response.text)
    print_verbose(user_prompt, response)


def main():
    user_prompt = sys.argv[1]
    print(f"current prompt is: {user_prompt}")
    run_prompt(user_prompt)



if __name__ == "__main__":
    main()
