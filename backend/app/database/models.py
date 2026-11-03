import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.session import Base


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    preferred_language = Column(String(10), default="en")  # 'en' or 'hi'
    location = Column(String(200), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    crop_profiles = relationship("CropProfile", back_populates="farmer", cascade="all, delete-orphan")
    risk_reports = relationship("RiskReport", back_populates="farmer", cascade="all, delete-orphan")
    advisories = relationship("Advisory", back_populates="farmer", cascade="all, delete-orphan")


class CropProfile(Base):
    __tablename__ = "crop_profiles"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String(50), nullable=False)
    growth_stage = Column(String(50), nullable=False)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=True)

    farmer = relationship("Farmer", back_populates="crop_profiles")


class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(200), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    forecast_timestamp = Column(String(50), nullable=True)
    retrieved_at = Column(DateTime, default=utc_now)


class RiskReport(Base):
    __tablename__ = "risk_reports"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=True)
    crop = Column(String(50), nullable=False)
    growth_stage = Column(String(50), nullable=True)
    risk_type = Column(String(50), nullable=False)
    risk_level = Column(String(20), nullable=False)  # LOW, MODERATE, HIGH
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    farmer = relationship("Farmer", back_populates="risk_reports")


class Advisory(Base):
    __tablename__ = "advisories"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=True)
    crop = Column(String(50), nullable=True)
    recommendation = Column(Text, nullable=False)
    language = Column(String(10), default="en")
    created_at = Column(DateTime, default=utc_now)

    farmer = relationship("Farmer", back_populates="advisories")
