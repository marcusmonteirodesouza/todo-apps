import datetime
import uuid
from typing import Set
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from todos import db


class Todo(db.Model):
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    owner_id: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[Set["TodoTask"]] = relationship(back_populates="todo")
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=now(), onupdate=now()
    )
