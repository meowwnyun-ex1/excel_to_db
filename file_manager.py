# สร้างไฟล์ setup_and_test.py เพื่อรันทุกอย่างในไฟล์เดียว

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.main import ExcelToDatabaseProcessor  # Import main processor


def setup_env():
    """สร้าง .env file"""
    env_content = """# Database Configuration สำหรับ Supabase
DB_HOST=db.ydmmxivfmfgbbphmitgy.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=jsCvOpw2RbFdpf5L
DB_TYPE=postgresql

# Processing Configuration
BATCH_SIZE=1000
MAX_WORKERS=3
CHUNK_SIZE=5000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/excel_to_db.log
"""

    with open(".env", "w") as f:
        f.write(env_content)
    print("✅ สร้าง .env")


def setup_dirs():
    """สร้าง directories"""
    dirs = ["logs", "data", "data/samples"]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    print("✅ สร้าง directories")


def create_test_excel():
    """สร้างไฟล์ Excel ทดสอบ"""

    # Test data
    test_data = {
        "Name": ["สมชาย ใจดี", "สมหญิง รักดี", "ประชา เจริญ", "มานะ สุขดี"],
        "Age": [25, 30, 35, 28],
        "Email": [
            "somchai@test.com",
            "somying@test.com",
            "pracha@test.com",
            "mana@test.com",
        ],
        "Salary": [45000.0, 55000.0, 75000.0, 50000.0],
        "Department": ["IT", "Sales", "Marketing", "HR"],
        "Active": [True, True, False, True],
        "Join Date": ["2023-01-15", "2023-02-20", "2023-03-10", "2024-01-05"],
    }

    df = pd.DataFrame(test_data)
    test_file = "test_employees.xlsx"
    df.to_excel(test_file, index=False)
    print(f"✅ สร้าง {test_file}")
    return test_file


def quick_test():
    """ทดสอบ import ด้วยไฟล์ที่สร้าง"""

    print("🚀 ทดสอบ Excel → Supabase")
    print("=" * 40)

    # Import processor
    try:
        from src.main import ExcelToDatabaseProcessor
    except ImportError:
        print("❌ ไม่พบ src module - ตรวจสอบ project structure")
        return False

    # Type mapping
    type_mapping = {
        "name": "string",
        "age": "integer",
        "email": "string",
        "salary": "float",
        "department": "string",
        "active": "boolean",
        "join_date": "datetime",
    }

    test_file = create_test_excel()

    processor = ExcelToDatabaseProcessor(
        excel_file=test_file, table_name="test_employees", type_mapping=type_mapping
    )

    try:
        results = processor.process(create_table=True)

        print("\n" + "=" * 40)
        print("🎉 SUCCESS!")
        print("=" * 40)
        print(f"📊 Import: {results['inserted_rows']} แถว")
        print(f"⏱️  เวลา: {results['processing_time']:.2f} วินาที")
        print(f"\n🔗 ตรวจสอบใน Supabase:")
        print(f"   → Table Editor → test_employees")

        # ลบไฟล์ทดสอบ
        os.remove(test_file)
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def create_larger_dataset():
    """สร้างข้อมูลขนาดใหญ่กว่า"""

    print("📊 สร้างข้อมูลขนาด 1,000 rows...")

    departments = ["IT", "Sales", "Marketing", "HR", "Finance", "Operations"]
    provinces = ["กรุงเทพฯ", "เชียงใหม่", "ขอนแก่น", "สงขลา", "ระยอง"]

    data = []
    for i in range(1000):
        record = {
            "Employee_ID": f"EMP{i+1:04d}",
            "Name": f"พนักงาน {i+1}",
            "Department": random.choice(departments),
            "Salary": random.randint(25000, 100000),
            "Age": random.randint(22, 60),
            "Province": random.choice(provinces),
            "Active": random.choice([True, True, False]),  # 66% active
            "Join_Date": f"202{random.randint(1,4)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        }
        data.append(record)

    df = pd.DataFrame(data)
    filename = "employees_1000.xlsx"
    df.to_excel(filename, index=False)
    print(f"✅ สร้าง {filename}")
    return filename


def test_large_file():
    """ทดสอบไฟล์ขนาดใหญ่"""

    large_file = create_larger_dataset()

    from src.main import ExcelToDatabaseProcessor

    type_mapping = {
        "employee_id": "string",
        "name": "string",
        "department": "string",
        "salary": "integer",
        "age": "integer",
        "province": "string",
        "active": "boolean",
        "join_date": "datetime",
    }

    processor = ExcelToDatabaseProcessor(
        excel_file=large_file, table_name="employees_1000", type_mapping=type_mapping
    )

    try:
        results = processor.process(create_table=True)

        print("\n" + "=" * 50)
        print("🎉 LARGE FILE SUCCESS!")
        print("=" * 50)
        print(f"📋 Total: {results['total_rows']:,} แถว")
        print(f"✅ Import: {results['inserted_rows']:,} แถว")
        print(f"⏱️  เวลา: {results['processing_time']:.2f} วินาที")
        print(
            f"🚀 ความเร็ว: {results['inserted_rows']/results['processing_time']:.0f} แถว/วินาที"
        )

        # ลบไฟล์
        os.remove(large_file)
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main function"""

    print("🔧 Excel to Supabase Setup & Test")
    print("=" * 50)

    # Setup
    setup_env()
    setup_dirs()

    if len(sys.argv) > 1:
        if sys.argv[1] == "large":
            test_large_file()
        elif sys.argv[1] == "create":
            create_larger_dataset()
        else:
            quick_test()
    else:
        # Default: quick test
        quick_test()


if __name__ == "__main__":
    main()
