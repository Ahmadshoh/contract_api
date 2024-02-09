from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime, timedelta


class Contact(BaseModel):
    email: str = Field(description="The email of the company this contracts was signed", default="Not found")
    phone: str = Field(description="The phone number of the company this contracts was signed", default="Not found")


class Address(BaseModel):
    country: str = Field(description="The country of the company this contracts was signed", default="Not found")
    city: str = Field(description="The city of the company this contracts was signed", default="Not found")
    zipcode: str = Field(description="The zip code of the company this contracts was signed", default="Not found")
    street: str = Field(description="The street of the company this contracts was signed", default="Not found")
    number: str = Field(description="The street number of the company this contracts was signed", default="Not found")


class Company(BaseModel):
    name: str = Field(description="The company this contracts was signed", default="Not found")
    address: Address
    contact: Contact


class Contract(BaseModel):
    title: str = Field(description="Title of the contracts. Here you can choose some title if exist, or tarif name, or other options that could be used as title. If this is not in the contracts, come up with it yourself based on the data.", default="Not found")
    contract_number: str = Field(description="Number of contracts", default="Not found")
    client_number: str = Field(description="Number of client", default="Not found")
    company: Optional[Company] = None
    effective_date: str = Field(description="Effective date of the contracts. If not provided, then take current date.", default=datetime.now())
    expiration_date: str = Field(description="Expiration date of the contracts. If not provided, search for 'Minimum contracts term' and add it to effective date", default=datetime.now() + timedelta(days=365))
    payment_details: dict[str, Any] = Field(
        description="Payment details mentioned in the contracts. This can include payment terms, amounts, and due dates.",
        default={}
    )
