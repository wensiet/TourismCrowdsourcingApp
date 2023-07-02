import os
import sys

# Get the absolute path of the project directory
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project directory to the Python path
sys.path.insert(0, project_dir)


'''
To run all tests use command 'pytest'
To run one file with tests run 'pytest tests/file_name.py'
To run one single test run 'pytest tests/file_name.py::func_name'
'''
