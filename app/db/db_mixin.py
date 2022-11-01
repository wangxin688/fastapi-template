from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PrimaryKeyMixin:
    id = Column(Integer, primary_key=True)


class NameMixin:
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
