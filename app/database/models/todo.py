from datetime import datetime
from typing import Literal

from sqlalchemy import BIGINT, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

STATUS = Literal["active", "done"]

class Todo(Base):
    __tablename__ = "user_todos"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT)
    name: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=func.now())