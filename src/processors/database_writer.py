import pandas as pd
from sqlalchemy import (
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
from ..config.database import db_manager

logger = logging.getLogger(__name__)


class DatabaseWriter:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.engine = db_manager.engine
        self.metadata = MetaData()

    def create_table_from_dataframe(
        self, df_sample, primary_key="id", type_mapping=None
    ):
        columns = [Column(primary_key, Integer, primary_key=True, autoincrement=True)]

        for col_name, dtype in df_sample.dtypes.items():
            if col_name == primary_key:
                continue
            sql_type = String(255)  # Default type
            if type_mapping and col_name in type_mapping:
                type_map = {
                    "string": String(255),
                    "integer": Integer,
                    "float": Float,
                    "boolean": Boolean,
                    "datetime": DateTime,
                }
                sql_type = type_map.get(type_mapping[col_name], String(255))
            columns.append(Column(col_name, sql_type))

        self.table = Table(self.table_name, self.metadata, *columns)
        self.metadata.create_all(self.engine)
        logger.info(f"Table '{self.table_name}' created")

    def parallel_insert(self, dataframes):
        total = 0
        for df in dataframes:
            df.to_sql(
                self.table_name,
                self.engine,
                if_exists="append",
                index=False,
                chunksize=1000,
            )
            total += len(df)
        return total
