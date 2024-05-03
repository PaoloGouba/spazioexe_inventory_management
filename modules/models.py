from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

## -- Accepted value list
class StatusEnum(str, Enum):
    nuovo = 'Nuovo'
    usato = 'Usato'
    ricondizionato = 'Ricondizionato'

class GradeEnum(str, Enum):
    a = 'A'
    b = 'B'
    c = 'C'
    d = 'D'
    p = 'Premium'

class AvaibilityEnum(str, Enum):
    available = 'Disponibile'
    sold = 'Venduto'
    not_sold = 'Non venduto'
    pending = 'In spospeso'
    warranty = 'In garanzia'
    reso = 'Reso'

class DeviceEnum(str, Enum):
    tv = 'TV'
    pc = 'PC'
    smartphone = 'Smartphone'
    tablet = 'Tablet'

class RepStatusEnum(str, Enum):
    consegnato = 'Consegnato'
    in_attesa = 'In attesa'
    chiamato = 'Chiamato'
    annullato = 'Annullato'
    in_sospeso = 'In sospeso'

## -- MODELS --
class Accessory(BaseModel):
    delivery_date: str
    first_name: str
    last_name: str
    price: float
    deposit: Optional[str] = None
    typology: str
    color: str
    customer_provider: Optional[str] = None
    status: StatusEnum

class Reparation(BaseModel) :
    request_date : str = datetime.now().strftime("%Y-%m-%d")
    first_name : str
    last_name : str   
    phone_number : str
    device : str
    brand : str
    model : str
    price : float = 0.0 # DEFAULT
    state : RepStatusEnum
    operator : str
    left_accessory : bool
    unlock_code : str
    color : str
    action : str 
    url : str
    muletto : bool


class Device(BaseModel) :
    device_type : DeviceEnum
    price : float
    sell_price : float
    imei_code : str
    battery_health : float
    brand : str
    model : str
    grade : GradeEnum 
    capacity : str
    status : StatusEnum
    manufacturer : str
    sold : bool
    customer_name : str
    customer_last_name : str
    selling_date : str
    article_type : str



