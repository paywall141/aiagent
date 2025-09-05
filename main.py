import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from helpers.tools import available_functions
from functions.call_function import call_function
from config import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
if len(sys.argv) < 2 :
    print("No prompt provided. Exiting with code 1")
    sys.exit(1)

system_prompt = system_prompt
total_prompt = 0
total_response = 0

def verbose_flag():
    return "--verbose" in sys.argv[2:]

def print_verbose(prompt, res):
    if verbose_flag():
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
        print(f"Totals burned: Prompt={total_prompt} Response={total_response}")


def run_prompt(user_prompt):
    # messages is a list of genai.types.Content
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    global total_prompt, total_response
    seen_texts = set()  

    def extract_text(resp):
        texts = []
        for cand in resp.candidates:
            for part in cand.content.parts:
                if part.text:
                    texts.append(part.text)
        return "".join(texts).strip()

    def extract_text_from_candidate(candidate):
        return "".join(p.text for p in candidate.content.parts if p.text).strip()

    for i in range(20):
        # generate_content loop
        try:
            print(f"Generating new content for loop iter: {i+1}")
            response = client.models.generate_content(
                model ='gemini-2.0-flash-001', 
                contents = messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
        except Exception as e:
            print(f"Error generating content/initial response: {e}")
            response = None

        # check for response as exit condition
        if not response:
            print( "no response found, exiting")
            return
        # Safely grab text (instead of response.text, which triggers warnings)
        text_out = extract_text(response)
        if text_out and not response.function_calls:
            print(f"Final response: {text_out}")
            break
        # optional: break if no further actions
        if not response.function_calls:
            print("No more function calls. Exiting loop.")
            return       

        # add candidates to messages list for NEXT conversation (call to generate_content)
        #  genai.types.Candidate
        for candidate in response.candidates:
            text_parts = extract_text_from_candidate(candidate)
            print("\n *** Adding Candidate text to messages:", {text_parts})
            messages.append(candidate.content)
            seen_texts.add(text_parts)


        # A model response may request multiple tool/function calls in one turn.  
        # This is where the ai executes function calls of type  genai.types.FunctionCall
        for call in response.function_calls or []:

            # each call returns of type genai.types.GenerateContentResponse 
            result_content = call_function( call, verbose = verbose_flag() )

            try:
                # Extract the function output
                func_response = result_content.parts[0].function_response.response

                # append output to messages to build context
                messages.append( types.Content(
                    role="user",
                    parts=[types.Part.from_function_response(
                        name = call.name,
                        response = func_response)]
                    ))
            except AttributeError:
                raise RuntimeError(f"Fatal: call_function did not return a valid types.Content for {call.name}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

            # this is most of the print noise
            # print(f"Function {call.name} returned: {func_response}")   
        total_prompt += response.usage_metadata.prompt_token_count
        total_response += response.usage_metadata.candidates_token_count
        print_verbose(user_prompt, response)


def main():
    user_prompt = sys.argv[1]
    run_prompt(user_prompt)



if __name__ == "__main__":
    main()
