import os
import subprocess
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try: 
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        
        if not valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python3", target_file_path]
        if args != None:
            command.extend(args)

        completed_process = subprocess.run(
            command, 
            cwd=working_dir_abs, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        output = []
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if not (completed_process.stderr or completed_process.stdout):
            output.append("No output produced")
        else:
            if completed_process.stderr:
                output.append(f"STDERR: {completed_process.stderr}")
            if completed_process.stdout:
                output.append(f"STDOUT: {completed_process.stdout}")
        return '\n'.join(output)    
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a python file by command",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory",
                },
                "args": {
                    "type": "string",
                    "description": "Arguments list to pass subprocess.run()"
                }
            },
        },
    },
}