import os
from pathlib import Path
import logging

project_name="NetworkSecurity"

# %()s ->string format specifier asctime->current time message->any input to logging
logging.basicConfig(level=logging.INFO,format="%(asctime)s: %(message)s")

list_of_files = [
    # GitHub Actions Workflow (CI/CD)
    ".github/workflows/main.yaml",  # Ensures the workflows folder exists for GitHub Actions

    f"{project_name}Data/.gitkeep",

    # Core Project Package
    f"src/{project_name}/__init__.py",  # Marks this directory as a Python package

    # Components - Functional Parts of the Project
    f"src/{project_name}/components/__init__.py",  # Initializes the components module

    # Utilities - Helper Functions
    f"src/{project_name}/utils/__init__.py",  # Initializes the utils module
    f"src/{project_name}/utils/common.py",  # Contains reusable utility functions

    # Configuration - Settings & Configurations
    f"src/{project_name}/config/__init__.py",  # Initializes the config module
    f"src/{project_name}/config/configuration.py",  # Manages configurations for the project

    # Pipeline - Data/Model Workflow
    f"src/{project_name}/pipeline/__init__.py",  # Initializes the pipeline module

    # Entity - Data Classes & Structured Configurations
    f"src/{project_name}/entity/__init__.py",  # Initializes the entity module
    f"src/{project_name}/entity/config_entity.py",  # Defines configuration entities using classes

    # Constants - Global Project-Wide Constants
    f"src/{project_name}/constants/__init__.py",  # Stores project constants (paths, API keys, etc.)
    f"src/{project_name}/exception/__init__.py",
    f"src/{project_name}/logging/__init__.py",
    f"src/{project_name}/cloud/__init__.py",




    # Configuration & Parameter Files
    "config/config.yaml",  # Stores general project configuration settings
    "params.yaml",  # Contains hyperparameters or runtime-specific parameters
    "schema.yaml",  # Contains schema

    # Main Application Files
    "main.py",  # Entry point for the application
    "Dockerfile",  # Defines how to containerize the project with Docker
    "setup.py",  # Used to package and install the project as a Python package
    "requirements.txt",
    ".gitignore",


    # Research & Experimentation
    "notebooks/research.ipynb",  # Jupyter Notebook for experimentation and prototyping
    # Web Application (if applicable)
    "templates/index.html"  # HTML template for web-based UI (used in Flask/Django apps)
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)

    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating directory {filedir} for the file: {filename}")

    # file does not exist or is 0 bytes
    if (not os.path.exists(filepath) or (os.path.getsize(filepath)==0)):
        with open(filepath,"w") as f:
            pass
        logging.info(f"Creating empty file :{filepath}")
        
    else:
        logging.info(f"{filename} already exists")