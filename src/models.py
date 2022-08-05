from sqlalchemy import Column, Integer, String
from .database import Base


class Credentials(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    fullname = Column(String, unique=True, index=True)
    password = Column(String, unique=True, index=True)
