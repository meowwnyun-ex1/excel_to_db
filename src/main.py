from pathlib import Path
import sys
from typing import Dict, Any, Optional
import pandas as pd

from .processors.excel_reader import ExcelReader
from .processors.data_validator import DataValidator
from .processors.database_writer import DatabaseWriter
from .utils.logger import setup_logger
from .utils.progress import track_progress
from .config.settings import settings

logger = setup_logger()


class ExcelToDatabaseProcessor:
    def __init__(
        self,
        excel_file: str,
        table_name: str,
        sheet_name: Optional[str] = None,
        validation_rules: Optional[Dict[str, Any]] = None,
        type_mapping: Optional[Dict[str, str]] = None,
    ):

        self.excel_reader = ExcelReader(excel_file, sheet_name)
        self.data_validator = DataValidator(validation_rules)
        self.database_writer = DatabaseWriter(table_name)
        self.type_mapping = type_mapping or {}

        # Statistics
        self.stats = {
            "total_rows": 0,
            "processed_rows": 0,
            "inserted_rows": 0,
            "error_rows": 0,
            "processing_time": 0,
        }

    def process(self, create_table: bool = True) -> Dict[str, Any]:
        """Main processing method"""
        import time

        start_time = time.time()

        try:
            # Step 1: Validate and analyze Excel file
            logger.info("🔍 Analyzing Excel file...")
            file_info = self.excel_reader.get_sheet_info()
            self.stats["total_rows"] = file_info["total_rows"]

            logger.info(
                f"📋 File Info: {file_info['total_rows']} rows, {len(file_info['columns'])} columns"
            )

            # Step 2: Create table if requested
            if create_table:
                logger.info("🏗️ Creating database table...")
                # Read small sample to infer structure
                sample_chunk = next(self.excel_reader.read_chunks(chunk_size=100))
                sample_clean = self.data_validator.clean_dataframe(sample_chunk)

                self.database_writer.create_table_from_dataframe(
                    sample_clean, type_mapping=self.type_mapping
                )

            # Step 3: Process data in chunks
            logger.info("🚀 Starting data processing...")

            chunks_to_process = []
            for chunk in track_progress(
                self.excel_reader.read_chunks(settings.CHUNK_SIZE),
                total=self.stats["total_rows"],
                description="Reading Excel",
            ):
                # Clean and validate data
                chunk_clean = self.data_validator.clean_dataframe(chunk)

                if self.type_mapping:
                    chunk_clean = self.data_validator.validate_data_types(
                        chunk_clean, self.type_mapping
                    )

                # Add to batch for processing
                chunks_to_process.append(chunk_clean)
                self.stats["processed_rows"] += len(chunk_clean)

                # Process in batches to manage memory
                if len(chunks_to_process) >= settings.MAX_WORKERS:
                    inserted = self.database_writer.parallel_insert(chunks_to_process)
                    self.stats["inserted_rows"] += inserted
                    chunks_to_process = []

            # Process remaining chunks
            if chunks_to_process:
                inserted = self.database_writer.parallel_insert(chunks_to_process)
                self.stats["inserted_rows"] += inserted

            # Calculate final statistics
            self.stats["processing_time"] = time.time() - start_time

            logger.info("✅ Processing completed successfully!")
            self._log_summary()

            return self.stats

        except Exception as e:
            logger.error(f"❌ Processing failed: {e}")
            raise

    def _log_summary(self):
        """Log processing summary"""
        logger.info("📊 Processing Summary:")
        logger.info(f"   Total rows: {self.stats['total_rows']:,}")
        logger.info(f"   Processed rows: {self.stats['processed_rows']:,}")
        logger.info(f"   Inserted rows: {self.stats['inserted_rows']:,}")
        logger.info(f"   Error rows: {self.stats['error_rows']:,}")
        logger.info(f"   Processing time: {self.stats['processing_time']:.2f} seconds")
        logger.info(
            f"   Speed: {self.stats['processed_rows']/self.stats['processing_time']:.2f} rows/second"
        )


# CLI Usage Example
def main():
    """CLI entry point"""
    if len(sys.argv) < 3:
        print("Usage: python -m src.main <excel_file> <table_name>")
        sys.exit(1)

    excel_file = sys.argv[1]
    table_name = sys.argv[2]

    # Example type mapping
    type_mapping = {
        "id": "integer",
        "name": "string",
        "email": "string",
        "age": "integer",
        "salary": "float",
        "created_at": "datetime",
        "is_active": "boolean",
    }

    processor = ExcelToDatabaseProcessor(
        excel_file=excel_file, table_name=table_name, type_mapping=type_mapping
    )

    try:
        results = processor.process(create_table=True)
        print(f"🎉 Successfully processed {results['inserted_rows']} rows!")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
