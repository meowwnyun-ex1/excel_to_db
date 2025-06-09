# src/processors/database_writer.py
import pandas as pd
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
)
from typing import Dict, Any, List, Optional
import logging
from ..config.settings import settings

logger = logging.getLogger(__name__)


class DatabaseWriter:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.engine = create_engine(
            f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )
        self.metadata = MetaData()

    def create_table_from_dataframe(
        self,
        df_sample: pd.DataFrame,
        primary_key: str = "id",
        type_mapping: Optional[Dict[str, str]] = None,
    ):
        """Create table from DataFrame structure"""
        columns = [Column(primary_key, Integer, primary_key=True, autoincrement=True)]

        for col_name, dtype in df_sample.dtypes.items():
            if col_name == primary_key:
                continue

            if type_mapping and col_name in type_mapping:
                sql_type = self._get_sqlalchemy_type(type_mapping[col_name])
            else:
                sql_type = String(255)

            columns.append(Column(col_name, sql_type))

        self.table = Table(self.table_name, self.metadata, *columns)
        self.metadata.create_all(self.engine)
        logger.info(f"Table '{self.table_name}' created")

    def _get_sqlalchemy_type(self, type_name: str):
        """Convert string type to SQLAlchemy type"""
        mapping = {
            "string": String(255),
            "integer": Integer,
            "float": Float,
            "boolean": Boolean,
            "datetime": DateTime,
        }
        return mapping.get(type_name, String(255))

    def parallel_insert(self, dataframes: List[pd.DataFrame]) -> int:
        """Insert dataframes to database"""
        total_inserted = 0

        for df in dataframes:
            df.to_sql(
                name=self.table_name,
                con=self.engine,
                if_exists="append",
                index=False,
                chunksize=settings.BATCH_SIZE,
            )
            total_inserted += len(df)

        return total_inserted
