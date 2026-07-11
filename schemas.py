from pydantic import BaseModel, Field, EmailStr

class ContactForm(BaseModel):
    name: str=Field(min_length=2, max_length=300, description="Type your name")
    email: EmailStr=Field(description="Sender's email address")
    subject: str=Field(min_length=5, max_length=300, description="Sender's subject")
    message: str=Field(min_length=10, max_length=1000, description="Message here")