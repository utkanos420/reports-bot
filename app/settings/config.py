from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_api_key: str
    bot_admin_id: str


settings = BotSettings()
