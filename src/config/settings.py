from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from .settings import settings

try:
    from supabase import create_client, Client

    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()
        self.supabase_client = None
        self._setup_engine()
        self._setup_supabase()

    def _setup_engine(self):
        """Create optimized database engine"""
        if settings.DB_TYPE == "postgresql":
            url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        elif settings.DB_TYPE == "mysql":
            url = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

        self.engine = create_engine(
            url,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=False,
        )

        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def _setup_supabase(self):
        """Setup Supabase client if available"""
        if SUPABASE_AVAILABLE and hasattr(settings, "SUPABASE_URL"):
            try:
                self.supabase_client = create_client(
                    settings.SUPABASE_URL, settings.SUPABASE_KEY
                )
            except Exception as e:
                print(f"Warning: Supabase setup failed: {e}")

    def get_session(self):
        """Get database session"""
        return self.SessionLocal()

    def create_tables(self):
        """Create all tables"""
        self.Base.metadata.create_all(bind=self.engine)

    def is_supabase_ready(self) -> bool:
        """Check if Supabase is configured and ready"""
        return self.supabase_client is not None


db_manager = DatabaseManager()
