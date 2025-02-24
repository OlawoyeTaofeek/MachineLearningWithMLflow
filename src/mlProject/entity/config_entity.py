from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Configuration class for data ingestion settings.

    Attributes:
        root_dir (Path): Root directory where data ingestion artifacts will be stored.
        source_url (str): URL from which the dataset will be downloaded.
        local_data_dir (Path): Path where the downloaded data file will be saved locally.
        unzip_dir (Path): Directory path where the downloaded dataset will be extracted.
    
    Notes:
        - The class is marked as frozen, making instances immutable after creation.
        - Ensures consistency and safety when passing configuration details across components.
    """
    root_dir: Path
    source_url: str
    local_data_dir: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    """
    Configuration class for data validation settings.

    Attributes:
        root_dir (Path): Root directory for storing data validation artifacts.
        STATUS_FILE (str): Path to the file where the validation status will be recorded.
        unzip_data_dir (Path): Directory containing the extracted data for validation.
        all_schema (dict): Dictionary defining the expected schema (column names and data types).

    Notes:
        - The class is frozen, ensuring immutability after instantiation.
        - The schema dictionary plays a critical role in ensuring data integrity before further processing.
    """
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict
