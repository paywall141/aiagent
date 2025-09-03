from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
import os

if __name__ == "__main__":
    wd = os.getcwd()
print("========TEST 1========")
print( get_file_content("calculator", "main.py") )
print("========TEST 2========")
print( get_file_content("calculator", "pkg/calculator.py") )
print("========TEST 3========")
print( get_file_content("calculator", "/bin/cat") )
print("========TEST 4========")
print( get_file_content("calculator", "pkg/does_not_exist.py") )