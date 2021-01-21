from pydantic import EmailStr, BaseModel, validator


class Email(BaseModel):
    email: EmailStr


class ActivateEmail(Email):
    code: str

    @validator('code')
    def validate_code_length(cls, v):
        if len(v.strip()) != 4:
            raise ValueError({'error': 'Code mush have 4 digits'})

        return v
