# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime
import os

DB_URL = os.environ["VIDEOS_DB_CONNECTION"]

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

