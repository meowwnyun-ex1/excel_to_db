#!/usr/bin/env python3
"""
Entry point สำหรับรันกับ Supabase
ใช้ไฟล์นี้แทน main.py เดิม
"""

import sys
import os
from pathlib import Path

# เพิ่ม project root ใน Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.main import ExcelToDatabaseProcessor
from src.config.settings import settings
from src.config.database import db_manager
from src.utils.logger import setup_logger

logger = setup_logger()


def validate_supabase_config():
    """ตรวจสอบการตั้งค่า Supabase"""
    required_vars = ["SUPABASE_URL", "SUPABASE_KEY", "SUPABASE_DB_PASSWORD"]
    missing_vars = []

    for var in required_vars:
        if not getattr(settings, var, None):
            missing_vars.append(var)

    if missing_vars:
        logger.error(f"❌ Missing Supabase configuration: {', '.join(missing_vars)}")
        logger.error("Please set in .env file:")
        for var in missing_vars:
            logger.error(f"  {var}=your-value")
        return False

    return True


def main():
    """Main entry point สำหรับ Supabase"""

    if len(sys.argv) < 3:
        print(
            """
🚀 Excel to Supabase Integration

Usage: python run_supabase.py <excel_file> <table_name> [sheet_name]

Examples:
  python run_supabase.py data/sales.xlsx sales_data
  python run_supabase.py data/users.xlsx users "Sheet1"

Configuration required in .env:
  SUPABASE_URL=https://your-project.supabase.co
  SUPABASE_KEY=your-anon-key
  SUPABASE_DB_PASSWORD=your-db-password
  DB_HOST=db.your-project.supabase.co
        """
        )
        sys.exit(1)

    excel_file = sys.argv[1]
    table_name = sys.argv[2]
    sheet_name = sys.argv[3] if len(sys.argv) > 3 else None

    # Validate file
    if not os.path.exists(excel_file):
        logger.error(f"❌ File not found: {excel_file}")
        sys.exit(1)

    # Validate Supabase configuration
    if not validate_supabase_config():
        sys.exit(1)

    # Check Supabase connection
    if not db_manager.is_supabase_ready():
        logger.warning(
            "⚠️ Supabase client not available, using direct PostgreSQL connection"
        )

    logger.info(f"🚀 Starting Excel to Supabase processing")
    logger.info(f"📁 File: {excel_file}")
    logger.info(f"📊 Target table: {table_name}")

    try:
        # Type mapping สำหรับข้อมูลทั่วไป
        type_mapping = {
            "id": "integer",
            "name": "string",
            "email": "string",
            "phone": "string",
            "age": "integer",
            "amount": "float",
            "price": "float",
            "quantity": "integer",
            "date": "datetime",
            "created_at": "datetime",
            "updated_at": "datetime",
            "is_active": "boolean",
            "status": "string",
        }

        processor = ExcelToDatabaseProcessor(
            excel_file=excel_file,
            table_name=table_name,
            sheet_name=sheet_name,
            type_mapping=type_mapping,
        )

        # Process with table creation
        results = processor.process(create_table=True)

        # Success summary
        logger.info("✅ Processing completed successfully!")
        logger.info(f"📊 Results:")
        logger.info(f"   • Total rows: {results['total_rows']:,}")
        logger.info(f"   • Processed: {results['processed_rows']:,}")
        logger.info(f"   • Inserted: {results['inserted_rows']:,}")
        logger.info(f"   • Time: {results['processing_time']:.2f} seconds")

        if hasattr(settings, "SUPABASE_URL"):
            logger.info(
                f"🔗 View in Supabase: {settings.SUPABASE_URL}/project/default/editor"
            )

        print(f"\n🎉 SUCCESS!")
        print(
            f"📈 Processed {results['inserted_rows']:,} rows in {results['processing_time']:.1f}s"
        )
        print(f"📊 Table: {table_name}")

        return results

    except Exception as e:
        logger.error(f"❌ Processing failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
