import pandas as pd
from mlProject.utils.logging_utils import setup_logging
import logging
from mlProject.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_data(self) -> bool:
        try:
            data = pd.read_csv(self.config.unzip_data_dir)
            all_columns = list(data.columns)
            dtypes_list_str = data.dtypes.astype(str).tolist()

            schema_columns = list(self.config.all_schema.keys())
            schema_dtypes = list(self.config.all_schema.values())

            # Check for exact column match (order + length)
            column_name_match = all_columns == schema_columns
            # Check if all dtypes match exactly
            dtype_match = dtypes_list_str == schema_dtypes

            validation_status = column_name_match and dtype_match

            if not column_name_match:
                logging.info(f"Column mismatch:\nExpected: {schema_columns}\nFound: {all_columns}")
            if not dtype_match:
                logging.info(f"Dtype mismatch:\nExpected: {schema_dtypes}\nFound: {dtypes_list_str}")

            if validation_status:
                logging.info("All columns and dtypes match successfully.")

            # Write validation status once
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Validation status: {validation_status}")
                logging.info(f"Validation status written to {self.config.STATUS_FILE}")

            return validation_status

        except Exception as e:
            raise e
