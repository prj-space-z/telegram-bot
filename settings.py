from pydantic import BaseModel, Field, PostgresDsn, SecretStr

from services.yaml_reader import YAMLSettings, YAMLSettingsConfig


class Settings(YAMLSettings):
    api_token: SecretStr
    admin_id: int

    model_config = YAMLSettingsConfig(env_file_encoding="utf-8", yaml_file=("config.yml",))
