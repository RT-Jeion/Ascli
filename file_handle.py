from pathlib import Path
import os


def read_dir(param=None):
    """
    Get the Name of all the files in the dir
    """

    # Define the folder names you want to completely skip
    FOLDERS_TO_IGNORE = {'.git', 'venv', '__pycache__'}

    current_dir = Path('.')

    # Filter out files that belong to the ignored folders
    files = [
        str(p) for p in current_dir.rglob('*') 
        if p.is_file() and not any(ignored in p.parts for ignored in FOLDERS_TO_IGNORE)
    ]
    print(files)
    return files
    
    



def file_writer(file_name: str, file_ext: str, file_content: str) -> None:
    """
    Writes file by Given file content, and named the file by given file name and file extension.
    """
    full_file_name = file_name+"."+file_ext
    with open(full_file_name, 'w', encoding="utf-8") as f:
        f.write(file_content)

    print(f"Wrote to file: {full_file_name}")

def file_reader(file_name: str):
    """
    Reads a specific File
    """
    try:
        with open(file_name, 'r', encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Faced an error: {e}"

if __name__=="__main__":
    print(file_reader("test/yoo.py"))