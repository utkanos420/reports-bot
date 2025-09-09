from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Report(SQLModel, table=True):
    __tablename__ = "reports"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id", nullable=False)
    user_username: str = Field(nullable=False)
    report_floor: int = Field(nullable=False)
    report_cabinet: int = Field(nullable=False)
    report_reason: str = Field(nullable=False)
    report_fio: str = Field(nullable=False)
    report_description: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: Optional["User"] = Relationship(back_populates="reports")
