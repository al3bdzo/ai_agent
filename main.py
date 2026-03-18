import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_functions import available_functions, call_function

load_dotenv()

def generate_content(client, messages):
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = messages,
        config = types.GenerateContentConfig(
            system_instruction=system_prompt, 
            tools=[available_functions]
        ),
    )
    return response

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("No api key found!")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="AI Agent CLI tool!")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = generate_content(client, messages)

    if not response.usage_metadata:
        raise RuntimeError("Failed API Request!")

    function_results = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, args.verbose)
        if not function_call_result.parts:
            raise Exception("Function call didn't go as expected")
        if not function_call_result.parts[0].function_response:
            raise Exception("No result of the function call!")
        if not function_call_result.parts[0].function_response.response:
            raise Exception("No response from function!")
        function_results.append(function_call_result.parts[0])
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)

if __name__ == "__main__":
    main()
