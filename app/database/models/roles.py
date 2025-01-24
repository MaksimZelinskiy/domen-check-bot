from datetime import datetime
from typing import Literal

from sqlalchemy import BIGINT, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

STATUS = Literal["active", "block"]


class Role(Base):
    __tablename__ = "roles"
    role_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)

    name: Mapped[str] = mapped_column()
    status: Mapped[STATUS] = mapped_column(default="active")    
