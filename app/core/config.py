import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    database_name: str = os.getenv("DB_NAME", "proyecto_chatbot")
    database_user: str = os.getenv("DB_USER", "postgres")
    database_password: str = os.getenv("DB_PASSWORD", "12345")
    database_host: str = os.getenv("DB_HOST", "localhost")
    database_port: str = os.getenv("DB_PORT", "5432")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    form_cliente_url: str = os.getenv("FORM_CLIENTE_URL", "")
    form_reserva_url: str = os.getenv("FORM_RESERVA_URL", "")


    @property
    def database_url(self) -> str:
        return (
            f"dbname={self.database_name} "
            f"user={self.database_user} "
            f"password={self.database_password} "
            f"host={self.database_host} "
            f"port={self.database_port}"
        )


settings = Settings()
