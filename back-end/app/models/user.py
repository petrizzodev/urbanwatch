from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from core.db import Base


class UserInDB(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, index=True, nullable=False)
    type_document = Column(String, nullable=False)
    id_document = Column(String, index=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    disable_notifications = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    creation_date  = Column(DateTime, default=datetime.now)
    password = Column(String, nullable=False)

    incidents = relationship('Incident', back_populates='user')