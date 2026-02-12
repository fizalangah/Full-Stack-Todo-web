# from typing import List
# import json

# from pydantic import validator
# from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     PROJECT_NAME: str = "Full Stack Todo API"
#     DATABASE_URL: str
#     SECRET_KEY: str
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

#     BACKEND_CORS_ORIGINS: List[str] = []
#     GEMINI_API_KEY: str | None = None

#     @validator("BACKEND_CORS_ORIGINS", pre=True)
#     def assemble_cors_origins(cls, v):
#         if isinstance(v, str):
#             try:
#                 return json.loads(v)
#             except json.JSONDecodeError:
#                 return [i.strip() for i in v.split(",")]
#         return v

#     class Config:
#         env_file = ".env"
#         case_sensitive = True
#         extra = "ignore"


# settings = Settings()


import json
from typing import Any, List, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Allow any type to prevent pydantic from crashing on empty env var
    BACKEND_CORS_ORIGINS: Any = []
    GEMINI_API_KEY: Optional[str] = None

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str) and v:
            if v.startswith("["):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    # Handle case where string starts with '[' but is not valid JSON
                    return [i.strip() for i in v.split(",")]
            else:
                return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        # Handle case where v is None or empty string
        return []

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
