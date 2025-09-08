from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .report import Report


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    is_muted: bool = Field(default=False, nullable=False, sa_column_kwargs={"server_default": "0"})
    user_id: int = Field(unique=True, nullable=False)
    user_username: str = Field(nullable=False)
    users_reports_count: Optional[int] = Field(default=None, nullable=True)

    reports: List["Report"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
