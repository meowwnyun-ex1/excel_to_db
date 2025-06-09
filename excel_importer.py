import pandas as pd
from sqlalchemy import create_engine
import os

# Direct Supabase connection
engine = create_engine(
    "postgresql://postgres:jsCvOpw2RbFdpf5L@db.ydmmxivfmfgbbphmitgy.supabase.co:5432/postgres"
)

# Read Excel & Import
df = pd.read_excel("employees_1000.xlsx")
df.to_sql("employees_test", engine, if_exists="replace", index=False)
print(f"✅ Import: {len(df)} rows")
