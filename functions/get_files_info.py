import os
import argparse

def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs = os.path.abspath(working_directory)
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    return f'Success: "{directory}" is within the working directory'

# if __name__ == "__main__":
#     # parser = argparse.ArgumentParser(description="Working directory")
#     # parser.add_argument("working_dir", type=str, help="Choose your directory!")
#     # get_files_info(parser.parse_args().working_dir)
#     get_files_info('calculator')