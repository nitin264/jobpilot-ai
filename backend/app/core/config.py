from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="JOBPILOT_",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "JobPilot AI"
    app_version: str = "0.1.0"
    environment: str = "local"
    debug: bool = False
    log_level: str = "INFO"

    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "jobpilot"
    database_user: str = "jobpilot"
    database_password: str = Field(default="jobpilot", repr=False)

    @property
    def database_dsn(self) -> str:
        return (
            f"postgresql://{self.database_user}:***@"
            f"{self.database_host}:{self.database_port}/{self.database_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
