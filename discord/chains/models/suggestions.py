# app/models/suggestions.py

from typing import List
from pydantic import BaseModel, Field


class StyleSuggestion(BaseModel):
    user_clothes: str = Field(
        description="A description of user's clothes as a Stylist"
    )
    style: str = Field(description="A name of suggested style")
    description: str = Field(
        description="Explanation of the style and why the suggested clothes match"
    )
    target_cloth: str = Field(
        description="The description of the cloth provided by user."
    )
    clothes: List[str] = Field(
        description="List of short descriptions of the clothes to be used as queries"
    )


class ProductSuggestion(BaseModel):
    name: str = Field(description="The name of the product")
    url: str = Field(description="The URL of the product")
    description: str = Field(
        description="Short description explaining why this product is selected"
    )


class ProductSuggestions(BaseModel):
    products: List[ProductSuggestion] = Field(
        description="List of products suggested according to context and user's question"
    )
