import os
import yaml
from src.NetworkSecurity.logging.logger import logger
from src.NetworkSecurity.exception.exception import NetworkSecurityException
from pydantic import validate_call
from box import Box
from pathlib import Path
from typing import Any
import sys

@validate_call
def read_yaml(path_to_yaml: Path) -> Box:
    """reads yaml file and returns data

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """

    try:
        content = yaml.safe_load(open(path_to_yaml))
        logger.info(f"Yaml File: {path_to_yaml} loaded successfully")
        return Box(content)
    # throws error when file is empty
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@validate_call
def create_directories(path_to_directories: list):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        logger.info(f"created directory at: {path}")