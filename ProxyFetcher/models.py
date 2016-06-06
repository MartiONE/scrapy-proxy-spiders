from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import ProxyFetcher.settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**ProxyFetcher.settings.DATABASE))

def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)
    
class Proxies(DeclarativeBase):
    __tablename__ = "proxies"
    id = Column(Integer, primary_key=True)
    ip = Column("ip", String)
    port = Column("port", Integer)
    country = Column("country", String)
    con_type = Column("con_type",String)
    response_time = Column("response_time", Float)
    #availability = Column(100, Integer)
    #checks = Column(1, Integer)