#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
from datetime import datetime
import logging


class ExcelFileManager:
    """จัดการไฟล์ Excel และ folder structure"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.setup_directories()
        self.logger = self.setup_logger()

    def setup_directories(self):
        """สร้าง folder structure"""
        directories = [
            "data/input",
            "data/processed",
            "data/backup",
            "data/samples",
            "logs",
            "exports",
        ]

        for directory in directories:
            (self.base_path / directory).mkdir(parents=True, exist_ok=True)

    def setup_logger(self):
        """Setup logger สำหรับ file operations"""
        logger = logging.getLogger("file_manager")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.FileHandler(self.base_path / "logs" / "file_manager.log")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def add_file(self, file_path: str, category: str = "input") -> str:
        """เพิ่มไฟล์ Excel เข้าระบบ"""
        source_path = Path(file_path)

        if not source_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Validate Excel file
        if source_path.suffix.lower() not in [".xlsx", ".xls"]:
            raise ValueError("File must be Excel format (.xlsx or .xls)")

        # Create backup first
        backup_path = self.backup_file(source_path)

        # Move to appropriate folder
        target_folder = self.base_path / "data" / category
        target_path = target_folder / source_path.name

        # Handle duplicate names
        if target_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name_stem = source_path.stem
            suffix = source_path.suffix
            target_path = target_folder / f"{name_stem}_{timestamp}{suffix}"

        shutil.copy2(source_path, target_path)
        self.logger.info(f"File added: {target_path}")

        return str(target_path)

    def backup_file(self, file_path: Path) -> str:
        """สำรองไฟล์ก่อนประมวลผล"""
        backup_folder = self.base_path / "data" / "backup"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = backup_folder / backup_name

        shutil.copy2(file_path, backup_path)
        self.logger.info(f"Backup created: {backup_path}")

        return str(backup_path)

    def move_to_processed(self, file_path: str) -> str:
        """ย้ายไฟล์ไป processed folder หลังประมวลผลเสร็จ"""
        source_path = Path(file_path)
        processed_folder = self.base_path / "data" / "processed"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        processed_name = f"{source_path.stem}_processed_{timestamp}{source_path.suffix}"
        processed_path = processed_folder / processed_name

        shutil.move(source_path, processed_path)
        self.logger.info(f"Moved to processed: {processed_path}")

        return str(processed_path)

    def list_files(self, category: str = "input") -> list:
        """แสดงรายชื่อไฟล์ในแต่ละ category"""
        folder_path = self.base_path / "data" / category

        if not folder_path.exists():
            return []

        excel_files = []
        for file_path in folder_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in [".xlsx", ".xls"]:
                excel_files.append(
                    {
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime),
                    }
                )

        return sorted(excel_files, key=lambda x: x["modified"], reverse=True)

    def clean_old_files(self, days: int = 30):
        """ลบไฟล์เก่าที่เกิน X วัน"""
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)

        folders_to_clean = ["processed", "backup"]
        removed_count = 0

        for folder_name in folders_to_clean:
            folder_path = self.base_path / "data" / folder_name

            if not folder_path.exists():
                continue

            for file_path in folder_path.iterdir():
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    removed_count += 1
                    self.logger.info(f"Removed old file: {file_path}")

        return removed_count

    def get_storage_info(self) -> dict:
        """แสดงข้อมูลการใช้พื้นที่"""
        info = {}

        folders = ["input", "processed", "backup", "samples"]

        for folder_name in folders:
            folder_path = self.base_path / "data" / folder_name

            if not folder_path.exists():
                info[folder_name] = {"files": 0, "size": 0}
                continue

            files = list(folder_path.glob("*.xls*"))
            total_size = sum(f.stat().st_size for f in files)

            info[folder_name] = {
                "files": len(files),
                "size": total_size,
                "size_mb": round(total_size / 1024 / 1024, 2),
            }

        return info


# ==========================================
# CLI Interface สำหรับ File Management
# ==========================================


def main():
    """CLI สำหรับจัดการไฟล์"""
    import sys

    if len(sys.argv) < 2:
        print(
            """
📁 Excel File Manager

Commands:
  setup                           - สร้าง folder structure
  add <file_path>                - เพิ่มไฟล์ Excel
  list [category]                - แสดงรายชื่อไฟล์ (input/processed/backup)
  clean [days]                   - ลบไฟล์เก่า (default: 30 วัน)
  info                           - แสดงข้อมูลการใช้พื้นที่
  process <file_path> <table>    - ประมวลผลไฟล์ Excel → Supabase

Examples:
  python file_manager.py setup
  python file_manager.py add ~/Downloads/sales.xlsx
  python file_manager.py list input
  python file_manager.py process data/input/sales.xlsx sales_table
        """
        )
        sys.exit(1)

    command = sys.argv[1]
    manager = ExcelFileManager()

    if command == "setup":
        manager.setup_directories()
        print("✅ Folder structure created")

    elif command == "add":
        if len(sys.argv) < 3:
            print("❌ Usage: add <file_path>")
            sys.exit(1)

        try:
            result_path = manager.add_file(sys.argv[2])
            print(f"✅ File added: {result_path}")
        except Exception as e:
            print(f"❌ Error: {e}")

    elif command == "list":
        category = sys.argv[2] if len(sys.argv) > 2 else "input"
        files = manager.list_files(category)

        if not files:
            print(f"📁 No files in {category} folder")
        else:
            print(f"📁 Files in {category} folder:")
            for file_info in files:
                size_mb = round(file_info["size"] / 1024 / 1024, 2)
                print(
                    f"  • {file_info['name']} ({size_mb}MB) - {file_info['modified'].strftime('%Y-%m-%d %H:%M')}"
                )

    elif command == "clean":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        removed = manager.clean_old_files(days)
        print(f"✅ Removed {removed} old files (>{days} days)")

    elif command == "info":
        info = manager.get_storage_info()
        print("📊 Storage Information:")

        total_size = 0
        for folder, data in info.items():
            print(f"  • {folder}: {data['files']} files, {data['size_mb']}MB")
            total_size += data["size"]

        print(f"  • Total: {round(total_size / 1024 / 1024, 2)}MB")

    elif command == "process":
        if len(sys.argv) < 4:
            print("❌ Usage: process <file_path> <table_name>")
            sys.exit(1)

        file_path = sys.argv[2]
        table_name = sys.argv[3]

        # Import and run Supabase processor
        try:
            import sys

            sys.path.append(".")
            from run_supabase import main as run_supabase

            # Temporarily modify sys.argv for run_supabase
            original_argv = sys.argv.copy()
            sys.argv = ["run_supabase.py", file_path, table_name]

            run_supabase()

            # Move to processed folder
            manager.move_to_processed(file_path)
            print(f"✅ File moved to processed folder")

            sys.argv = original_argv

        except Exception as e:
            print(f"❌ Processing error: {e}")

    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()
