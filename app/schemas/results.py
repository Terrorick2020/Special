from pydantic import BaseModel

class ResultBase(BaseModel):
    domain: str
    subdomains_count: int
    pages_found: int
    description: str
    content_file_path: str

class ResultCreate(ResultBase):
    pass

class ResultResponse(ResultBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "domain": "example.com",
                "subdomains_count": 3,
                "pages_found": 15,
                "description": "Пример описания сайта",
                "content_file_path": "/results/example.com.txt"
            }
        }