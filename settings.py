from pydantic import BaseModel, Field, PostgresDsn, SecretStr

from services.yaml_reader import YAMLSettings, YAMLSettingsConfig


class Settings(YAMLSettings):
    api_token: SecretStr
    admin_id: int
    mongodb_url: SecretStr
    celery_broker: SecretStr

    max_images_pattern: int

    minio_endpoint: str
    minio_access_key: SecretStr
    minio_secret_key: SecretStr
    minio_secure: bool

    redis_host: str
    redis_port: int
    redis_db: int

    model_config = YAMLSettingsConfig(env_file_encoding="utf-8", yaml_file=("config.yml",))
