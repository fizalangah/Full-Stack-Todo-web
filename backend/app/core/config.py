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
from typing import List, Optional

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    BACKEND_CORS_ORIGINS: List[str] = []
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str):
            if v.startswith("["):
                return json.loads(v)
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, List):
            return v
        raise ValueError("BACKEND_CORS_ORIGINS must be a string or a list of strings")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()

