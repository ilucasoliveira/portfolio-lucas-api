from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactForm(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(min_length=1, max_length=150)
    message: str = Field(min_length=10, max_length=5000)
    website: str = Field(default="", max_length=200)