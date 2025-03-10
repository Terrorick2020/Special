from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Int, ForeignKey, DateTime, func


class Base(DeclarativeBase):
    pass

class GateWay(Base):
    __tablename__ = "gateway"

    id: Mapped[int] = mapped_column(primary_key=True)
    domain: Mapped[str] = mapped_column(String())
    info_id: Mapped[int] = mapped_column(Int())

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Info(Base):
    __tablename__ = "info"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String())
    raw_text: Mapped[str] = mapped_column(String())
    accommodation_text: Mapped[str] = mapped_column(String())
    raw_info_id: Mapped[int] = mapped_column(ForeignKey("gateway.info_id"))

class SubDomains(Base):
    __tablename__ = "sub_domains"

    id: Mapped[int] = mapped_column(primary_key=True)
    sub_domain: Mapped[str] = mapped_column(String())
    domain_id: Mapped[int] = mapped_column(ForeignKey("gateway.id"))
