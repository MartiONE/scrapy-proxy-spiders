#! /usr/bin/env python3

import redis
import requests
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

'''
To-do list:
-Appropiate exception handling
-Logging
-Settings fixed, maybe from another file
-Maybe class inheritance
'''

DeclarativeBase = declarative_base()

# Settings for the postgres database
settings = {'drivername': 'postgres',
 'host': 'ec2-54-247-185-241.eu-west-1.compute.amazonaws.com',
 'port': '5432',
 'username': 'zsgfhmwkoflfsd',
 'password': 'kd3sPn7Sgj5ZhScCH2dbdPhCDC',
 'database': 'ddj0spavnrluds'}


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
r = redis.StrictRedis(host="redis-16451.c3.eu-west-1-1.ec2.cloud.redislabs.com", port=16451, password="javicp90")

# Iteration for the query results
for proxy in session.query(Proxies).filter(Proxies.ip != None).all():
    # Socks 4 and 5 not supported for now
    if proxy.con_type in ["http", "https"]:
        try:
            judge = requests.get("http://judge.live-proxy.net/index.php", 
                                 proxies = {"http" : proxy.full_address}, 
                                 timeout = 3)
            # Only store the item if the judge makes a correct answer
            if judge.status_code == 200:
                r.setex(proxy.full_address, 120, proxy.con_type)
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
