import os
import argparse
import sys
import json

from dotenv import load_dotenv

# from google import genai
# from google.genai import types

from openai import OpenAI
import json

from prompts import system_prompt
from config import MAX_ITERATIONS
from call_functions import available_functions, call_function

load_dotenv()

def generate_content(client, messages):
    response = client.responses.create(
        model = "gpt-4.1-mini",
        input = messages,
        tools = available_functions,
        instructions = system_prompt
    )
    return response

def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("No api key found!")

    client = OpenAI(api_key=api_key)

    parser = argparse.ArgumentParser(description="AI Agent CLI tool!")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [{"role": "user", "content": args.user_prompt}]


    for _ in range(MAX_ITERATIONS):
        response = generate_content(client, messages)

        if hasattr(response, "output") and response.output:
            messages.extend(response.output)

        function_calls = [
            item for item in response.output 
            if hasattr(item, "type") and item.type == "function_call"
        ]

        for function_call in function_calls:
            function_response = call_function(function_call, verbose=args.verbose)

            if "content" not in function_response:
                raise Exception("Function call didn't return content")

            try:
                call_data = function_response["content"]
            except Exception:
                raise Exception("Function call returned invalid JSON")
            
            if not call_data:
                raise Exception("Functoin call returned empty data")
            
            call_id = function_call.call_id

            messages.append({"type" : "function_call_output" , "call_id" : call_id,"output" : call_data})

            if args.verbose:
                print(f"-> {call_data}")
            

        if not function_calls:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                if hasattr(response, "usage"):
                    print(f"Prompt tokens: {response.usage.input_tokens}")
                    print(f"Response tokens: {response.usage.output_tokens}")
            
            if hasattr(response, "output_text") and response.output_text:
                print(response.output_text)
            
            return 
    
    print("maximum iterations exceeded")
    sys.exit(1)


# def generate_content(client, messages):
#     response = client.models.generate_content(
#         model = "gemini-2.5-flash",
#         contents = messages,
#         config = types.GenerateContentConfig(
#             system_instruction=system_prompt, 
#             tools=[available_functions]
#         ),
#     )
#     return response

# def main():
#     api_key = os.environ.get("GEMINI_API_KEY")
#     if not api_key:
#         raise RuntimeError("No api key found!")

#     client = genai.Client(api_key=api_key)

#     parser = argparse.ArgumentParser(description="AI Agent CLI tool!")
#     parser.add_argument("user_prompt", type=str, help="User prompt")
#     parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
#     args = parser.parse_args()

#     messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

#     response = generate_content(client, messages)

#     if not response.usage_metadata:
#         raise RuntimeError("Failed API Request!")

#     function_results = []
#     for function_call in response.function_calls:
#         function_call_result = call_function(function_call, args.verbose)
#         if not function_call_result.parts:
#             raise Exception("Function call didn't go as expected")
#         if not function_call_result.parts[0].function_response:
#             raise Exception("No result of the function call!")
#         if not function_call_result.parts[0].function_response.response:
#             raise Exception("No response from function!")
#         function_results.append(function_call_result.parts[0])
#         if args.verbose:
#             print(f"-> {function_call_result.parts[0].function_response.response}")
        
#     if args.verbose:
#         print(f"User prompt: {args.user_prompt}")
#         print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
#         print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
#     print(response.text)

if __name__ == "__main__":
    main()
