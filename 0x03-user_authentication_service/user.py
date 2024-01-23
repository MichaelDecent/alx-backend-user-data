#!/usr/bin/env python3
"""This module cover User Model
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    """User Model
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    hashed_paswword = Column(String(250))
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

