from pydantic import BaseModel


class InnerHello(BaseModel):
    preview: str

class InnerParser(BaseModel):
    get_info: str

class Hello(BaseModel):
    glob: str
    inner: InnerHello

class Parser(BaseModel):
    glob: str
    inner: InnerParser

class ApiRoutes(BaseModel):
    prefix: str
    hello: Hello
    parser: Parser
