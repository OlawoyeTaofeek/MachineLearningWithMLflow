import pandas as pd
from mlProject.utils.logging_utils import setup_logging
import logging
from mlProject.entity.config_entity import DataValidationConfig


class DataValidation:
    """
    A class to handle data validation by checking:
    1. If the dataset's column names exactly match the defined schema (including order).
    2. If the dataset's data types match the expected data types defined in the schema.

    Attributes:
        config (DataValidationConfig): Configuration object containing schema definitions, 
                                       file paths, and validation status file location.
    """

    def __init__(self, config: DataValidationConfig):
        """
        Initializes the DataValidation object with the given configuration.

        Args:
            config (DataValidationConfig): An object containing:
                - all_schema (dict): Expected column names and their corresponding data types.
                - unzip_data_dir (str): Path to the extracted CSV file.
                - STATUS_FILE (str): Path to write the validation status.
        """
        self.config = config

    def validate_data(self) -> bool:
        """
        Validates the ingested dataset by:
        - Comparing column names and their order with the expected schema.
        - Ensuring data types of each column match the schema exactly.

        Process:
            1. Reads the CSV file from the specified path.
            2. Extracts columns and their data types.
            3. Compares them with the provided schema.
            4. Logs detailed mismatches if any.
            5. Writes the overall validation status (True/False) to a status file.

        Returns:
            bool: True if both columns and data types match the schema exactly, False otherwise.

        Raises:
            Exception: If any error occurs during file reading, validation, or status writing.

        Logging Details:
            - Logs mismatched columns and data types with expected vs. actual results.
            - Logs successful validation when all checks pass.
        """
        try:
            # Load the dataset
            data = pd.read_csv(self.config.unzip_data_dir)
            all_columns = list(data.columns)
            dtypes_list_str = data.dtypes.astype(str).tolist()

            # Schema details
            schema_columns = list(self.config.all_schema.keys())
            schema_dtypes = list(self.config.all_schema.values())

            # Check for exact column and dtype match
            column_name_match = all_columns == schema_columns
            dtype_match = dtypes_list_str == schema_dtypes

            validation_status = column_name_match and dtype_match

            # Detailed logging for mismatches
            if not column_name_match:
                logging.info(f"Column mismatch:\nExpected: {schema_columns}\nFound: {all_columns}")
            if not dtype_match:
                logging.info(f"Dtype mismatch:\nExpected: {schema_dtypes}\nFound: {dtypes_list_str}")

            if validation_status:
                logging.info("All columns and data types match the expected schema successfully.")

            # Write the validation status
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Validation status: {validation_status}")
                logging.info(f"Validation status written to {self.config.STATUS_FILE}")

            return validation_status

        except Exception as e:
            logging.error(f"Error during data validation: {e}")
            raise e
