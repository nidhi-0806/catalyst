from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(64), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())

    csv_records = relationship("CSVRecord", back_populates="user")
    file_uploads = relationship("FileUpload", back_populates="user")
    jwt_tokens = relationship("JWTToken", back_populates="user")


class CSVRecord(Base):
    __tablename__ = "csv_records"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="csv_records")


class FileUpload(Base):
    __tablename__ = "file_uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(64), nullable=False)
    file_path = Column(String(256), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="file_uploads")


class JWTToken(Base):
    __tablename__ = "jwt_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="jwt_tokens")
