import pandas as pd
from typing import Dict, List, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)


class DataValidator:
    def __init__(self, validation_rules: Optional[Dict[str, Any]] = None):
        self.validation_rules = validation_rules or {}
        self.errors = []

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize dataframe"""
        # Create copy to avoid modifying original
        df_clean = df.copy()

        # Clean column names
        df_clean.columns = [self._clean_column_name(col) for col in df_clean.columns]

        # Remove completely empty rows
        df_clean = df_clean.dropna(how="all")

        # Clean string columns
        for col in df_clean.select_dtypes(include=["object"]).columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace("nan", "")

        return df_clean

    def _clean_column_name(self, col_name: str) -> str:
        """Clean column name for database compatibility"""
        # Convert to lowercase and replace spaces/special chars with underscore
        clean_name = re.sub(r"[^a-zA-Z0-9_]", "_", str(col_name).lower())
        clean_name = re.sub(r"_+", "_", clean_name)  # Remove multiple underscores
        clean_name = clean_name.strip("_")  # Remove leading/trailing underscores

        return clean_name

    def validate_data_types(
        self, df: pd.DataFrame, type_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """Validate and convert data types"""
        df_typed = df.copy()

        for column, target_type in type_mapping.items():
            if column not in df_typed.columns:
                continue

            try:
                if target_type == "integer":
                    df_typed[column] = (
                        pd.to_numeric(df_typed[column], errors="coerce")
                        .fillna(0)
                        .astype(int)
                    )
                elif target_type == "float":
                    df_typed[column] = pd.to_numeric(
                        df_typed[column], errors="coerce"
                    ).fillna(0.0)
                elif target_type == "datetime":
                    df_typed[column] = pd.to_datetime(df_typed[column], errors="coerce")
                elif target_type == "boolean":
                    df_typed[column] = (
                        df_typed[column]
                        .astype(str)
                        .str.lower()
                        .isin(["true", "1", "yes", "y"])
                    )

            except Exception as e:
                logger.warning(f"Type conversion failed for column {column}: {e}")

        return df_typed

    def validate_required_fields(
        self, df: pd.DataFrame, required_fields: List[str]
    ) -> List[int]:
        """Validate required fields and return invalid row indices"""
        invalid_rows = []

        for field in required_fields:
            if field in df.columns:
                null_mask = (
                    df[field].isnull() | (df[field] == "") | (df[field] == "nan")
                )
                invalid_rows.extend(df[null_mask].index.tolist())

        return list(set(invalid_rows))  # Remove duplicates
