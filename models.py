from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, json_schema_extra={"example": "Home office as a driver for VR Applications"})
    prompt: Optional[str] = Field(default="Virtual Realms", json_schema_extra={"example": "Virtual Realms"})
    short_description: str = Field(..., json_schema_extra={"example": "Remote work has become the norm post-pandemic..."})
    content: str = Field(..., json_schema_extra={"example": "Virtual reality (VR) creates computer-generated immersive environments..."})
    image_url: Optional[str] = Field(
        default=None,
        json_schema_extra={"example": "https://storage.googleapis.com/stylefixtailoringnextjsassets/testimages/2024-04-19_10-40-08_5991.webp"}
    )


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int = Field(..., json_schema_extra={"example": 4})
    created_at: str = Field(..., json_schema_extra={"example": "2025-03-27T03:55:47.044655Z"})


class ErrorDetail(BaseModel):
    code: str = Field(..., json_schema_extra={"example": "NOT_FOUND"})
    message: str = Field(..., json_schema_extra={"example": "Article with ID 999 not found"})
    details: Optional[dict] = Field(default=None)


class ApiResponse(BaseModel, Generic[DataT]):
    success: bool = Field(..., json_schema_extra={"example": True})
    data: Optional[DataT] = None
    error: Optional[ErrorDetail] = None
    meta: Optional[dict] = None
