"""
Application settings for ClaimAssistant.

This module centralizes configuration values for the application.

Current behavior:
- Loads app name, environment, debug mode, and database URL.
- Reads values from environment variables or a local .env file.

Future production behavior:
- Load PostgreSQL, Azure OpenAI, vector database, tracing, and security settings.
- Keep secrets out of source code.
- Support different values for local, staging, and production environments.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Typed application settings loaded from environment variables.

    BaseSettings allows ClaimAssist to read configuration from the
    environment while still validating expected types.

    Example:
        DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/dbname
    """

    app_name: str = Field(
        default="ClaimAssist",
        description="Human-readable application name.",
    )

    environment: str = Field(
        default="local",
        description="Current runtime environment such as local, staging, or production.",
    )

    debug: bool = Field(
        default=True,
        description="Whether debug behavior is enabled.",
    )

    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/claimassist",
        description="SQLAlchemy database connection URL.",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    
    test_database_url: str = Field(
    default="postgresql+psycopg2://postgres:postgres@localhost:5432/claimassist_test",
    description="SQLAlchemy database connection URL used for automated tests.",
)


settings = Settings()