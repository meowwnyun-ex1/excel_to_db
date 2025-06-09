# fix_settings.py
content = """from typing import Optional

class Settings:
    DB_HOST: str = "db.ydmmxivfmfgbbphmitgy.supabase.co"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "jsCvOpw2RbFdpf5L"
    DB_TYPE: str = "postgresql"
    BATCH_SIZE: int = 1000
    MAX_WORKERS: int = 3
    CHUNK_SIZE: int = 5000
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/excel_to_db.log"

settings = Settings()"""

with open("src/config/settings.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Fixed settings.py")
