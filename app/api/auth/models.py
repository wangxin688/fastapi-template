from enum import unique
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, expression

from app.db.db_base import Base
from app.db.db_mixin import TimestampMixin, PrimaryKeyMixin, NameMixin


class UserRole(Base):
    __tablename__ = "user_role"
    user_id = Column(Integer, ForeignKey("user.id", primary_key=True))
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True)

class User(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = 'user'
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    passwd = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=expression.true)
    role = relationship("Role", secondary="user_roles", overlaps="user", back_populates="user")


class Role(Base, PrimaryKeyMixin, NameMixin):
    __tablename__ = 'role'
    user = relationship(
        "User",
        secondary="user_role", overlaps="role", back_populates="role"
    )







