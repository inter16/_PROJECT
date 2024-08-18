from pydantic import BaseModel


class VisionResult(BaseModel):
    SN:str
    num:int