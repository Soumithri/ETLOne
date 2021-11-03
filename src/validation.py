from pydantic import BaseModel, EmailStr
from typing import Literal


class UserValidation(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    gender: Literal['Genderfluid', 'Bigender', 'Male', 'Non-binary', 'Female',
                    'Agender', 'Genderqueer', 'Polygender']
    ip_address: str
