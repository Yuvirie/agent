import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("prompt", type=str, help="User prompt to the model")
parser.add_argument("-v", "--verbose", action="store_true", default=False, help="turns on prompt and usage info")

args = parser.parse_args()

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists file content in string format with maximum limit of 10000 characters, otherwise it will truncute the response, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to get content from, relative to the working directory. If not provided, it will return the error",
            ),
        },
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs specified python file and returns the outputs and errors, constrained to the working directory. Timeouts after 30 seconds",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath of the python script to run. Required, if not present or if file is not a python script, it will result in error",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overrides the specified file with provided content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath of the file to override. If parent dir is not present it will create a one.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file in a string",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Always start with analyzing user question and try to find a proper file that the questions is refering too and then analyze it. Then go to the heart of the issue while you have proper context to do so.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

You should always assume that user asks the question related to function calls.
Also and it's critical, but when asked for a fix, fix the underlying issue after you analyse it, do not go for symptom fix.
"""



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

user_prompt = args.prompt


#context

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

#agent loop

iterations = 0

for iteriations in range(iterations, 20):
    
    test_response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            )
        )

    for candidate in test_response.candidates:
        messages.append(candidate.content)

    if test_response.function_calls:
        functions = test_response.function_calls
    else: 
        functions = None

    if args.verbose and test_response.usage_metadata:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {test_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {test_response.usage_metadata.candidates_token_count}")
        if functions:
            for func in functions:
                function_call_result = call_function(func)
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Error: No response from called function")
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
                messages.append(function_call_result)
    else:
        if functions:
            for func in functions:
                function_call_result = call_function(func)
                print(f"Calling function: {func.name}({func.args})")
                messages.append(function_call_result)
    
    
    if functions:
        iterations += 1
    else:
        print(test_response.text)
        break