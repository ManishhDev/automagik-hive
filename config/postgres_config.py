"""PostgreSQL configuration using Agno's built-in abstractions"""
import os
from typing import Optional
from agno.storage.postgres import PostgresStorage


def get_postgres_storage(
    table_name: str = "pagbank_sessions",
    mode: str = "team"
) -> Optional[PostgresStorage]:
    """
    Get PostgreSQL storage using Agno's built-in PostgresStorage.
    Falls back to None if DATABASE_URL is not set (will use SQLite).
    """
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        return None
    
    # Agno handles everything - table creation, schema management, etc.
    return PostgresStorage(
        table_name=table_name,
        db_url=db_url,
        mode=mode,
        auto_upgrade_schema=True
    )