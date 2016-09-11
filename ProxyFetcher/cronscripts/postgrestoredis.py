#! /usr/bin/env python3

import redis
import requests
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.orm.exc import ObjectDeletedError
import configparser

# Config parser
cfg = configparser.ConfigParser()
cfg.read("general.cfg")

'''
To-do list:
-Appropiate exception handling
-Logging
-Settings fixed, maybe from another file
-Maybe class inheritance
'''

DeclarativeBase = declarative_base()

# Settings for the postgres database
settings = {'drivername': cfg['postgres']['drivername'],
 'host': cfg['postgres']['host'],
 'port': cfg['postgres']['port'],
 'username': cfg['postgres']['username'],
 'password': cfg['postgres']['password'],
 'database': cfg['postgres']['database']}


class Proxies(DeclarativeBase):
    '''Class for the database'''
    __tablename__ = "proxies"
    full_address = Column("full_address",String, primary_key=True)
    ip = Column("ip", String)
    port = Column("port", Integer)
    country = Column("country", String)
    con_type = Column("con_type",String)
    response_time = Column("response_time", Float)

# Engine and session creation
engine = create_engine(URL(**settings))
Session = sessionmaker(bind=engine)
session = Session()

# Redis session opener
r = redis.StrictRedis(host=cfg['remote_redis']['host'], port=int(cfg['remote_redis']['port']), password=cfg['remote_redis']['password'])

# Iteration for the query results
for proxy in session.query(Proxies).filter(Proxies.ip != None).all():
    # Socks 4 and 5 not supported for now
    try:
        if proxy.con_type in ["http", "https"]:
            try:
                judge = requests.get(cfg.get('judge', "url", fallback="http://www.bdsmpichunter.com/dde32.php"), 
                                     proxies = {"http" : "http://"+proxy.full_address}, 
                                     timeout = 3)
                # Only store the item if the judge makes a correct answer
                if (judge.status_code == 200) and ("HTTP_HOST" in judge.text):
                    r.setex(proxy.full_address, 120, proxy.con_type)
                # Catch the ones that even answering correctly are not what we expect
                else:
                    try:
                        session.delete(proxy)
                        session.commit()
                        print("Bad response, deleted "+proxy.full_address)
                    except sqlalchemy.orm.exc.ObjectDeletedError as e:
                        print("Duplicated key")                   
            # Exception handling
            except Exception as e:
                # Deletion from the database
                try:
                    session.delete(proxy)
                    session.commit()
                    print("Bad proxy, deleted "+proxy.full_address)
                except sqlalchemy.orm.exc.ObjectDeletedError as e:
                    print("Duplicated key")
        else:
            print("Not http/https, deleted"+proxy.con_type)
            session.delete(proxy)
            session.commit()
    except ObjectDeletedError as e:
        print("Object deleted error")
