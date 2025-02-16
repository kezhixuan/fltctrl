from typing import List
from typing import Optional
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Sequence


class Base(DeclarativeBase):
    pass


class refresh_hist(Base):
    __tablename__ = "refresh_hist"
    refresh_hist_id = Sequence("refresh_hist_id_seq", metadata=Base.metadata, start=1)
    index: Mapped[int] = mapped_column(
        Integer,
        refrsh_hist_id_seq,
        server_default=refrsh_hist_id_seq.next_value(),
        primary_key=True,
    )
    index: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer)
    refresh_date: Mapped[str] = mapped_column(String(50))

    def __repr__(self) -> str:
        return f"Issues(index={self.index!r}, id={self.id!r},  issue_key={self.refresh_date!r})"
