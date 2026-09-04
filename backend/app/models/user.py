from sqlalchemy import Table
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class UserRole(str, enum.Enum):
    PATIENT = "PATIENT"
    FAMILY_MEMBER = "FAMILY_MEMBER"
    CAREGIVER = "CAREGIVER"
    NURSE = "NURSE"
    PHYSIOTHERAPIST = "PHYSIOTHERAPIST"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Optional profiles based on role
    patient_profile = relationship("Patient", back_populates="user", uselist=False)
    caregiver_profile = relationship("Caregiver", back_populates="user", uselist=False)

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    date_of_birth = Column(String)
    gender = Column(String)
    phone = Column(String)
    address = Column(String)
    blood_group = Column(String)
    
    user = relationship("User", back_populates="patient_profile")

class Caregiver(Base):
    __tablename__ = "caregivers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    qualification = Column(String)
    specialization = Column(String)
    experience_years = Column(Integer)
    is_verified = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="caregiver_profile")


from sqlalchemy import Table

patient_family_link = Table(
    "patient_family_link",
    Base.metadata,
    Column("patient_id", Integer, ForeignKey("patients.id"), primary_key=True),
    Column("family_member_id", Integer, ForeignKey("family_members.id"), primary_key=True)
)

class FamilyMember(Base):
    __tablename__ = "family_members"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String)
    relation_type = Column(String)
    
    user = relationship("User", back_populates="family_member_profile")
    patients = relationship("Patient", secondary=patient_family_link, back_populates="family_members")

# We must dynamically add relationships back to Patient and User classes
Patient.family_members = relationship("FamilyMember", secondary=patient_family_link, back_populates="patients")
User.family_member_profile = relationship("FamilyMember", back_populates="user", uselist=False)

