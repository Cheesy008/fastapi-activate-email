from pydantic import EmailStr, BaseModel, validator
from fastapi import HTTPException


class ActivateEmail(BaseModel):
    email: EmailStr
    code: str

    @validator('code')
    def validate_code_length(cls, v):
        if len(v.strip()) != 4:
            raise ValueError({'error': 'Code must have 4 digits'})

        return v


class Login(BaseModel):
    username: str
    password: str


def check_activated_email(email):
    with open('emails.txt', 'r') as f:
        for stored_email in f:
            if email == stored_email.strip():
                raise HTTPException(status_code=400, detail={'error': 'Email already activated'})
