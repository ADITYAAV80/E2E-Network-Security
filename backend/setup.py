"""
setup.py is a Python script used to define a package’s 
metadata, dependencies, and installation instructions. 
It is part of Setuptools, which helps in packaging and 
distributing Python projects.
You can then install package via pip install -e .
"""

from setuptools import find_packages,setup
from typing import List

def get_requirements() ->List[str]:
    """
    Returns list of requirements
    """
    requirement_list = []
    try:
        with open("requirements.txt","r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                ##ignore empy lines and "-e ."
                if requirement and requirement!="-e .":
                    requirement_list.append(requirement)
    except Exception as e:
        print(e)
    
    return requirement_list

setup(
    name="Network Security",
    version="0.0.1",
    author="Aditya",
    author_email="adityaav80@gmail.com",
    packages=find_packages(),
    install_requires= get_requirements()
)