import os
import sys
import yaml
import json
import joblib
from typing import List, Dict, Any, Union
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from box.exceptions import BoxValueError, BoxKeyError
from src.mlProject.utils.logging_utils import setup_logging
import logging
from jsonschema import validate, ValidationError

## Building Utilities  
log_file_path = setup_logging('Utils_common.log')

@ensure_annotations
def load_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Load a YAML file into a ConfigBox object.

    Args:
        path_to_yaml (Path): The path to the YAML file.

    Raises:
        ValueError: If the YAML file is not found, empty, or has an invalid structure.

    Returns:
        ConfigBox: The loaded YAML data as a ConfigBox object.
    """
    try:
        with open(path_to_yaml, "r", encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)
            if yaml_data is None:
                logging.error(f"YAML file {path_to_yaml} is empty.")
                raise ValueError(f"YAML file {path_to_yaml} is empty.")
            logging.info(f"YAML file {path_to_yaml} loaded successfully.")
        return ConfigBox(yaml_data)
    
    except yaml.YAMLError as e:
        logging.exception(f"Error parsing YAML: {e}")

    except FileNotFoundError:
        logging.exception(f"YAML file {path_to_yaml} not found.")
        raise ValueError(f"YAML file {path_to_yaml} not found.")

    except BoxKeyError as e:
        logging.exception(f"Invalid YAML structure: {e}")
        raise ValueError(f"Invalid YAML structure: {e}")

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        raise ValueError(f"An unexpected error occurred: {e}")
    
    
@ensure_annotations
def save_json(path: Path, data: dict):
    """Save JSON data after ensuring the directory exists.

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logging.info(f"JSON file saved at: {path}")
    
# validate Json schema before loading it
def validate_json_schema(data: dict, schema: dict):
    try:
        validate(instance=data, schema=schema)
        logging.info("JSON schema validation successful.")
    except ValidationError as e:
        logging.error(f"JSON schema validation failed: {e}")
        raise

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load JSON file data.

    Args:
        path (Path): Path to the JSON file.

    Raises:
        FileNotFoundError: If the JSON file does not exist.
        ValueError: If the JSON file is empty or invalid.

    Returns:
        ConfigBox: Data as class attributes instead of a dict.
    """
    try:
        if not path.exists():
            logging.error(f"JSON file {path} not found.")
            raise FileNotFoundError(f"JSON file {path} not found.")

        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)

        if not content:
            logging.error(f"JSON file {path} is empty.")
            raise ValueError(f"JSON file {path} is empty.")

        logging.info(f"JSON file loaded successfully from: {path}")
        return ConfigBox(content)

    except json.JSONDecodeError as jde:
        logging.exception(f"Error decoding JSON from {path}: {jde}")
        raise ValueError(f"Error decoding JSON from {path}: {jde}")

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        raise ValueError(f"An unexpected error occurred: {e}")
    
@ensure_annotations
def save_joblib(path: Path, data: Any):
    """Save data using joblib
    
    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logging.info(f"Binary file saved at: {path}")

@ensure_annotations
def load_joblib(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logging.info(f"binary file loaded from: {path}")
    return data

@ensure_annotations
def create_directories(paths: list, verbose: bool = True):
    """Create directories from a list of paths.

    Args:
        paths (list): List of directory paths to create.
        verbose (bool, optional): Whether to log directory creation. Defaults to True.
    """
    for path in paths:
        os.makedirs(path, exist_ok=True)
        verbose and logging.info(f"Created directory at: {path}")


@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"