import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

When a user asks to "run" a Python file, you should use the run_python_file function to execute it. For example:
- "run tests.py" -> call run_python_file with file_path="tests.py"
- "run main.py with arguments 1 2 3" -> call run_python_file with file_path="main.py" and args=["1", "2", "3"]
"""

model_name = "gemini-2.0-flash-001"


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

# Dictionary mapping function names to actual functions
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    
    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Check if function name is valid
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Get the function and prepare arguments
    function = function_map[function_name]
    args = dict(function_call_part.args)
    
    # Add working_directory to the arguments
    args["working_directory"] = "./calculator"
    
    # Call the function
    function_result = function(**args)
    
    # Return the result as types.Content
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("No input provided")
        exit(1)

    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    max_iterations = 20
    
    for iteration in range(max_iterations):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=config,
            )

            # Add the response candidates to the conversation
            for candidate in response.candidates:
                messages.append(candidate.content)

            # Handle function calls first (before checking for text)
            if response.function_calls:
                function_responses = []
                
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose)
                    
                    # Check if the function call result has the expected structure
                    if not hasattr(function_call_result, 'parts') or len(function_call_result.parts) == 0:
                        raise Exception("Function call result does not have expected structure")
                    
                    if not hasattr(function_call_result.parts[0], 'function_response'):
                        raise Exception("Function call result does not contain function_response")
                    
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    
                    function_responses.append(function_call_result)
                
                # Add all function responses to the conversation
                for function_response in function_responses:
                    messages.append(function_response)

            # Check if we have a final text response (no function calls)
            elif response.text:
                print(response.text)
                break
            
            else:
                # No function calls and no text - something went wrong
                print("No response text or function calls received")
                break

        except Exception as e:
            print(f"Error during generation: {e}")
            break

    else:
        # Loop completed without breaking (max iterations reached)
        print(f"Maximum iterations ({max_iterations}) reached without completion")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
