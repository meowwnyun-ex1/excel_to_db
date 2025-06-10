# ระบบ Import ข้อมูล Excel เข้า Supabase

🚀 **ระบบนำเข้าข้อมูลจาก Excel สู่ Supabase ประสิทธิภาพสูง**

ระบบที่พัฒนาด้วย Python สำหรับการนำเข้าข้อมูลจากไฟล์ Excel เข้าสู่ฐานข้อมูล Supabase (PostgreSQL) พร้อมฟีเจอร์ขั้นสูงอย่างการประมวลผลแบบ chunk, parallel insertion, การตรวจสอบข้อมูล และการปรับแต่งประสิทธิภาพ

## ✨ คุณสมบัติเด่น

- 📊 **ประมวลผลไฟล์ Excel**: รองรับไฟล์ .xlsx และ .xls พร้อมหลาย sheets
- ⚡ **ประสิทธิภาพสูง**: อ่านข้อมูลแบบ chunk และประมวลผลแบบ parallel สำหรับชุดข้อมูลขนาดใหญ่
- 🧹 **ตรวจสอบข้อมูล**: ทำความสะอาดข้อมูลและแปลงประเภทข้อมูลอัตโนมัติ
- 🔄 **ประมวลผลแบบ Batch**: การ insert แบบ bulk ที่ปรับแต่งแล้วพร้อมขนาด batch ที่กำหนดได้
- 📈 **ติดตามความคืบหน้า**: การติดตามความคืบหน้าแบบ real-time และเมตริกประสิทธิภาพ
- 🛠️ **การกำหนดค่าที่ยืดหยุ่น**: ตั้งค่าง่ายสำหรับสภาพแวดล้อมฐานข้อมูลที่แตกต่างกัน
- 🧪 **เครื่องมือทดสอบ**: เครื่องมือทดสอบและแก้ไขปัญหาที่ครอบคลุม
- 📋 **สร้างข้อมูลจำลอง**: ตัวสร้างข้อมูลในตัวสำหรับการทดสอบ

## 🏗️ โครงสร้างโปรเจค

```
excel-to-supabase/
├── .env                          # การกำหนดค่า Environment
├── requirements.txt              # Dependencies ของ Python
├── README.md                     # ไฟล์นี้
│
├── src/                          # โค้ดหลักของแอปพลิเคชัน
│   ├── config/                   # การจัดการการกำหนดค่า
│   │   ├── settings.py           # การตั้งค่าและ database URL
│   │   └── database.py           # ตัวจัดการการเชื่อมต่อฐานข้อมูล
│   │
│   ├── processors/               # โมดูลประมวลผลข้อมูล
│   │   ├── excel_reader.py       # ตัวอ่านไฟล์ Excel แบบ chunk
│   │   ├── data_validator.py     # การทำความสะอาดและตรวจสอบข้อมูล
│   │   └── database_writer.py    # การดำเนินการฐานข้อมูลและ parallel insertion
│   │
│   ├── utils/                    # โมดูลยูทิลิตี้
│   │   ├── logger.py             # ระบบ logging
│   │   └── progress.py           # ติดตามความคืบหน้า
│   │
│   └── main.py                   # โปรเซสเซอร์หลัก
│
├── logs/                         # ไฟล์ log
├── data/                         # ไดเรกทอรีข้อมูล
│   └── samples/                  # ไฟล์ตัวอย่าง
│
├── file_manager.py               # ระบบจัดการไฟล์ขั้นสูง
├── test_supabase.py              # ตัวทดสอบระบบแบบเร็ว
├── excel_generator.py            # ตัวสร้างข้อมูล mockup
├── setup_supabase.py             # สคริปต์ตั้งค่าเริ่มต้น
├── debug_connection.py           # เครื่องมือแก้ไขปัญหาการเชื่อมต่อ
└── force_supabase_test.py        # ทดสอบการเชื่อมต่อแบบบังคับ
```

## 🚀 การติดตั้งและเริ่มใช้งาน

### ข้อกำหนดเบื้องต้น
- Python 3.8+
- บัญชี Supabase
- ไฟล์ Excel ที่ต้องการ import

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 2. ตั้งค่าเริ่มต้น
```bash
python setup_supabase.py
```

### 3. ทดสอบการเชื่อมต่อ
```bash
python test_supabase.py
```

### 4. สร้างข้อมูลทดสอบ (ถ้าต้องการ)
```bash
python excel_generator.py test
```

## ⚙️ การกำหนดค่า

### ไฟล์ .env
```env
# การกำหนดค่าฐานข้อมูล Supabase
DB_HOST=your-project.supabase.co
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.your-project-ref
DB_PASSWORD=your-password
DB_TYPE=postgresql

# การกำหนดค่าการประมวลผล
BATCH_SIZE=2000
MAX_WORKERS=6
CHUNK_SIZE=10000

# การ Logging
LOG_LEVEL=INFO
LOG_FILE=logs/excel_to_db.log
```

## 📖 วิธีการใช้งาน

### การใช้งานพื้นฐาน

#### 1. ทดสอบเร็ว
```bash
python test_supabase.py
```

#### 2. Import ไฟล์ Excel ที่กำหนดเอง
```bash
python test_supabase.py data.xlsx table_name
```

#### 3. Import พร้อมระบุ sheet
```bash
python test_supabase.py data.xlsx table_name sheet_name
```

### การใช้งานขั้นสูง

#### 1. สร้างและทดสอบไฟล์ขนาดต่างๆ
```bash
# ไฟล์ขนาดเล็ก (100 แถว)
python file_manager.py small

# ไฟล์ขนาดกลาง (5,000 แถว)
python file_manager.py medium

# ไฟล์ขนาดใหญ่ (10,000 แถว)
python file_manager.py large

# ไฟล์ขนาดใหญ่มาก (50,000 แถว)
python file_manager.py xlarge
```

#### 2. ทดสอบประสิทธิภาพ
```bash
python file_manager.py benchmark
```

#### 3. สร้างข้อมูลตัวอย่าง
```bash
# สร้างข้อมูลทุกประเภท
python excel_generator.py all

# สร้างข้อมูลยอดขาย
python excel_generator.py sales 10000

# สร้างข้อมูลพนักงาน
python excel_generator.py employee 1000
```

### การใช้งานในโค้ด Python

```python
from src.main import ExcelToDatabaseProcessor

# กำหนด type mapping
type_mapping = {
    "name": "string",
    "age": "integer",
    "salary": "float",
    "hire_date": "datetime",
    "is_active": "boolean"
}

# สร้าง processor
processor = ExcelToDatabaseProcessor(
    excel_file="data.xlsx",
    table_name="employees",
    type_mapping=type_mapping
)

# ประมวลผล
results = processor.process(create_table=True)
print(f"Import สำเร็จ: {results['inserted_rows']} แถว")
```

## 🔧 คำอธิบายสคริปต์

### สคริปต์หลัก

#### `file_manager.py` - ระบบจัดการไฟล์ขั้นสูง
- สร้างไฟล์ทดสอบขนาดต่างๆ
- รัน pipeline แบบสมบูรณ์พร้อมการติดตามประสิทธิภาพ
- ทดสอบ benchmark ประสิทธิภาพ
- ตั้งค่าระบบและไฟล์ configuration

#### `test_supabase.py` - ตัวทดสอบแบบเร็ว
- ทดสอบระบบด้วยข้อมูลง่ายๆ
- รองรับการทดสอบไฟล์ที่กำหนดเอง
- ตรวจจับประเภท column อัตโนมัติ

#### `excel_generator.py` - ตัวสร้างข้อมูลจำลอง
- สร้างข้อมูลจำลองหลากหลายประเภท
- รองรับการสร้างข้อมูลขนาดต่างๆ
- สร้างไฟล์ Excel หลาย sheets

### สคริปต์ Debug และ Setup

#### `debug_connection.py` - วินิจฉัยปัญหาการเชื่อมต่อ
- ทดสอบการโหลด .env file
- ทดสอบการเชื่อมต่อ Supabase โดยตรง
- ทดสอบ project settings

#### `setup_supabase.py` - การตั้งค่าเริ่มต้น
- สร้างไฟล์ .env
- สร้างโครงสร้างไดเรกทอรี
- สร้างสคริปต์ทดสอบ

## 📊 การปรับแต่งประสิทธิภาพ

### พารามิเตอร์ที่สำคัญ

- **BATCH_SIZE** (2000): ขนาด batch สำหรับ database operations
- **MAX_WORKERS** (6): จำนวน threads สำหรับ parallel processing
- **CHUNK_SIZE** (10000): ขนาด chunk สำหรับอ่านไฟล์ Excel

### คำแนะนำการปรับแต่ง

#### สำหรับไฟล์ขนาดใหญ่:
```env
BATCH_SIZE=5000
MAX_WORKERS=8
CHUNK_SIZE=20000
```

#### สำหรับเครื่องที่มี RAM จำกัด:
```env
BATCH_SIZE=1000
MAX_WORKERS=4
CHUNK_SIZE=5000
```

## 🧪 การทดสอบ

### ทดสอบการเชื่อมต่อ
```bash
python debug_connection.py
```

### ทดสอบแบบบังคับ (หากมีปัญหา)
```bash
python force_supabase_test.py
```

### แก้ไขปัญหาอัตโนมัติ
```bash
python force_supabase_test.py fix
```

## 📈 ตัวอย่างผลลัพธ์

```
🎉 กระบวนการเสร็จสิ้น!
============================================================
📊 Performance Summary:
    File: employees_50000.xlsx (15.2 MB)
    Total rows: 50,000
    Processed: 50,000
    Inserted: 50,000
    Success rate: 100.0%
    Total time: 45.67 seconds
    Speed: 1,095 rows/sec
    Throughput: 0.33 MB/sec

⏱️ Stage Breakdown:
    excel_reading: 8.34s (18.3%)
    validation_setup: 0.12s (0.3%)
    database_setup: 2.45s (5.4%)
    data_processing: 34.76s (76.1%)

🗄️ Database: Table 'employees' contains 50,000 rows
```

## 🎯 Use Cases

1. **การ Migrate ข้อมูล**: ย้ายข้อมูลจาก Excel เข้า Supabase
2. **Bulk Import**: นำเข้าข้อมูลขนาดใหญ่อย่างมีประสิทธิภาพ
3. **การประมวลผลข้อมูล**: ทำความสะอาดและแปลงข้อมูลก่อน import
4. **การทดสอบประสิทธิภาพ**: ทดสอบประสิทธิภาพการ import ขนาดต่างๆ
5. **การพัฒนาระบบ**: สร้างข้อมูลจำลองสำหรับพัฒนาระบบ

## 🔍 การแก้ไขปัญหาที่พบบ่อย

### ปัญหาการเชื่อมต่อ
```bash
# ตรวจสอบการเชื่อมต่อ
python debug_connection.py

# แก้ไขอัตโนมัติ
python force_supabase_test.py fix
```

### ปัญหา Memory
- ลด CHUNK_SIZE และ BATCH_SIZE
- ลด MAX_WORKERS

### ปัญหาความเร็ว
- เพิ่ม MAX_WORKERS (แต่ไม่เกิน CPU cores)
- เพิ่ม BATCH_SIZE
- ใช้ SSD สำหรับไฟล์ชั่วคราว

## 📞 การสนับสนุน

หากพบปัญหาหรือต้องการความช่วยเหลือ:

1. ตรวจสอบ logs ใน `logs/excel_to_db.log`
2. รัน `python debug_connection.py` เพื่อวินิจฉัยปัญหา
3. ตรวจสอบการตั้งค่าในไฟล์ `.env`

## 📄 ลิขสิทธิ์

โปรเจคนี้เผยแพร่ภายใต้ MIT License

---

🚀 **พร้อมใช้งาน? เริ่มต้นด้วย:** `python setup_supabase.py`