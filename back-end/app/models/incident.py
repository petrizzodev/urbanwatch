from datetime import datetime
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class Incident(Base):
    __tablename__ = "incident"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)
    description = Column(String(255), nullable=False)
    detail = Column(String(255), nullable=False)
    address = Column(String, nullable=False)
    evidence = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.now)
    state = Column(String, nullable=False)

    user_username = Column(String, ForeignKey('users.username'))
    user = relationship("UserInDB", back_populates="incidents")