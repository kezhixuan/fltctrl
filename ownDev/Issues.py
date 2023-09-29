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

class Issues(Base):
    __tablename__ = "issues"
 #   issue_id_seq = Sequence("issue_id_seq", metadata=Base.metadata, start=1) 
 #   index: Mapped[int] = mapped_column(Integer, issue_id_seq,server_default=issue_id_seq.next_value(), primary_key=True)
    index: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer)
    issue_key: Mapped[str] = mapped_column(String(50)) 
    statuscategorychangedate: Mapped[str] = mapped_column(String(50)) 
    summary: Mapped[str] = mapped_column(String(50)) 
    components: Mapped[str] = mapped_column(String(50))
    creator: Mapped[str] = mapped_column(String(50)) 
    severity: Mapped[str] = mapped_column(String(50)) 
    created: Mapped[str] = mapped_column(String(50)) 
    bug_classification: Mapped[str] = mapped_column(String(50)) 
    project: Mapped[str] = mapped_column(String(50))
    defect_age: Mapped[str] = mapped_column(String(50)) 
    priority: Mapped[str] = mapped_column(String(50)) 
    release_phase: Mapped[str] = mapped_column(String(50)) 
    versions: Mapped[str] = mapped_column(String(50))
    duedate: Mapped[str] = mapped_column(String(50)) 
    updated: Mapped[str] = mapped_column(String(50)) 
    status: Mapped[str] = mapped_column(String(50)) 
    sims_demand_category: Mapped[str] = mapped_column(String(50)) 
    affected_version: Mapped[str] = mapped_column(String(50)) 
    affected_version_releasedate: Mapped[str] = mapped_column(String(50)) 
    affected_version_released: Mapped[str] = mapped_column(String(50)) 
    fixversions: Mapped[str] = mapped_column(String(50)) 
    labels: Mapped[str] = mapped_column(String(50))

    def __repr__(self) -> str:
        return f"Issues(index={self.index!r}, id={self.id!r},  issue_key={self.issue_key!r}, statuscategorychangedate={self.statuscategorychangedate!r}, summary={self.summary!r}, components={self.components!r}, creator={self.creator!r}, severity={self.severity!r}, created={self.created!r}, bug_classification={self.bug_classification!r}, project={self.project!r}, defect_age={self.defect_age!r}, priority={self.priority!r}, release_phase={self.release_phase!r}, versions={self.versions!r}, duedate={self.duedate!r}, updated={self.updated!r}, status={self.status!r}, sims_demand_category={self.sims_demand_category!r}, affected_version={self.affected_version!r}, affected_version_releasedate={self.affected_version_releasedate!r}, affected_version_released={self.affected_version_released!r}, fixversions={self.fixversions!r}, labels={self.labels!r})"