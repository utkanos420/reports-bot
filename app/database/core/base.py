from sqlmodel import SQLModel, Field

class Base(SQLModel):
    __abstract__ = True
    id: int | None = Field(default=None, primary_key=True)
