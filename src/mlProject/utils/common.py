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
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logging.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)
    
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
