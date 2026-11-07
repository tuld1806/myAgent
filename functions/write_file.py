import os
def write_file(working_directory: str, file_path: str, content: str) -> str:    
    try: 
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        target_dir = os.path.dirname(target_file_path)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)
        with open(f"{target_file_path}", 'w', encoding='utf-8') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"