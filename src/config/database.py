import pandas as pd
import logging

logger = logging.getLogger(__name__)


class DatabaseWriter:
    def __init__(self, table_name: str):
        self.table_name = table_name
        # Late import to avoid circular dependency
        from ..config.database import db_manager

        self.engine = db_manager.engine

    def create_table_from_dataframe(self, df_sample, **kwargs):
        """Simple table creation using pandas"""
        try:
            df_sample.head(0).to_sql(
                self.table_name, self.engine, if_exists="replace", index=False
            )
            logger.info(f"Table '{self.table_name}' created")
        except Exception as e:
            logger.error(f"Table creation failed: {e}")
            raise

    def parallel_insert(self, dataframes):
        """Batch insert using pandas"""
        total = 0
        try:
            for df in dataframes:
                df.to_sql(
                    self.table_name,
                    self.engine,
                    if_exists="append",
                    index=False,
                    method="multi",
                )
                total += len(df)
                logger.info(f"Inserted {len(df)} rows")
            return total
        except Exception as e:
            logger.error(f"Insert failed: {e}")
            raise
