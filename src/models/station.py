from pydantic import BaseModel


class StationOut(BaseModel):
    id: int
    line_name: int
    line_hex_color: int
    station_name: int

    class Config:
        orm_mode = True


class StationCreate(BaseModel):
    line_name: int
    line_hex_color: int
    station_name: int
