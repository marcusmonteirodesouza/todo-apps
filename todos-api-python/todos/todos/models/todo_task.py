import datetime
import uuid
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from todos import db


class TodoTask(db.Model):
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    todo_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("todo.id"))
    todo: Mapped["Todo"] = relationship(back_populates="tasks")
    title: Mapped[str] = mapped_column(nullable=False)
    is_completed: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=now(), onupdate=now()
    )
