from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.base_class import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    category = Column(String, index=True)
    duration_minutes = Column(Integer)
    base_price = Column(Float, nullable=False)
    required_qualification = Column(String)
    is_active = Column(Boolean, default=True)
