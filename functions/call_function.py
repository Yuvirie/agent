from functions.run_python import run_python_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from google.genai import types
import subprocess

function_map = {
    "run_python_file": run_python_file,
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file
}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(print(f"Calling function: {function_call_part.name}({function_call_part.args})"))
    else:
        print(f" - Calling function: {function_call_part.name}")

    func_name = function_call_part.name
    args = function_call_part.args
    args["working_directory"] = "./calculator"
    
    if func_name in function_map:
        result = function_map[func_name](**args)
    else:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"error": f"Unknown function: {func_name}"},
            )
        ],
    )


    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=func_name,
            response={"result": result},
        )
    ],
)