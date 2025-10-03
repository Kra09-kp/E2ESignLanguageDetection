import yaml
import sys,os
from sign_language_detection.exceptions import AppException
from sign_language_detection.logger import logger
from pathlib import Path

def read_yaml(file_path: str) -> dict:
    """
    Read a YAML file and return its contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise AppException(e) from e 