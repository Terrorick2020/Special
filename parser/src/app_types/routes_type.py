from pydantic import BaseModel


class InnerHello(BaseModel):
    preview: str

class Hello(BaseModel):
    glob:  str
    inner: InnerHello

class InnerParse(BaseModel):
    parse_info: str

class Parse(BaseModel):
    glob:  str
    inner: InnerParse

class ApiRoutes(BaseModel):
    prefix: str
    hello:  Hello
    parser: Parse
