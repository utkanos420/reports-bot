from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_api_key: str
    bot_admin_id: str


class DatabaseSettings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./db.sqlite3"
    db_echo: bool = True


settings = BotSettings()
db_settings = DatabaseSettings()

admin_ids = []
admin_ids.append(int(settings.bot_admin_id))
print(admin_ids)