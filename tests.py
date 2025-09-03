from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
import os

def test():
    print("========TEST 1========")
    print( run_python_file("calculator", "main.py") )
    print("========TEST 2========")
    print( run_python_file("calculator", "main.py", ["3 + 5"]) )
    print("========TEST 3========")
    print( run_python_file("calculator", "tests.py") )
    print("========TEST 4========")
    print( run_python_file("calculator", "../main.py") )
    print("========TEST 4========")
    print( run_python_file("calculator", "nonexistent.py") )


if __name__ == "__main__":
    wd = os.getcwd()
    test()
    
