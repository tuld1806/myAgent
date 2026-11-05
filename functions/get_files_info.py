import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try: 
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):#check for exist dir
            return f'Error: "{directory}" is not a directory'

        contents = ''
        for item in os.listdir(target_dir):
            item_dir = os.path.join(target_dir, item)
            file_name = os.path.basename(item_dir)
            file_size = os.path.getsize(item_dir)
            is_dir = os.path.isdir(item_dir)
            contents += f'  - {file_name}: file_size={file_size} bytes, is_dir={is_dir}\n'
        return contents
        
    except Exception as e:
        return f"Error: {e}"
    
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Working directory")
    # parser.add_argument("working_dir", type=str, help="Choose your directory!")
    # get_files_info(parser.parse_args().working_dir)
    get_files_info('functions')