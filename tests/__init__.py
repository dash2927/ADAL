# Import os, sys for path operations
import os
import sys

# Set main project path as the current directory
PROJECT_PATH = os.getcwd()
# Set source path as project path + project name
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "recipeezy"
)
# Append source path to current sys path
sys.path.append(SOURCE_PATH)
