from pydantic import BaseModel, Field, validator
from datetime import datetime

class TronAddressQueryCreate(BaseModel):
    address: str = Field(..., min_length=34, max_length=34)
    bandwidth: float
    energy: float
    balance: float

    @validator('address')
    def validate_tron_address(cls, address):
        if not (address.startswith('T') and len(address) == 34):
            raise ValueError('Invalid Tron address')
        return address

class TronAddressQueryRead(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True