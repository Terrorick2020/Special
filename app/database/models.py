from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, index=True, nullable=False)
    subdomains_count = Column(Integer, nullable=False)
    pages_found = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    content_file_path = Column(String, nullable=False)