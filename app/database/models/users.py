from datetime import datetime
from typing import Literal

from sqlalchemy import BIGINT, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

STATUS = Literal["active", "block"]

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)

    name: Mapped[str] = mapped_column()
    username: Mapped[str | None] = mapped_column(default=None)

    status: Mapped[STATUS] = mapped_column(default=None)    

    lang: Mapped[str | None] = mapped_column(default=None)
    utm: Mapped[str | None] = mapped_column(default="search")

    role_id: Mapped[int | None] = mapped_column(default=None)

    date_reg: Mapped[datetime] = mapped_column(default=func.now())
