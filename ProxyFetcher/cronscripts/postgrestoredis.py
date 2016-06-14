#! /usr/bin/env python3

import redis
import requests
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

DeclarativeBase = declarative_base()

settings = {'drivername': 'postgres',
 'host': 'ec2-54-247-185-241.eu-west-1.compute.amazonaws.com',
 'port': '5432',
 'username': 'zsgfhmwkoflfsd',
 'password': 'kd3sPn7Sgj5ZhScCH2dbdPhCDC',
 'database': 'ddj0spavnrluds'}


class Proxies(DeclarativeBase):
    __tablename__ = "proxies"
    full_address = Column("full_address",String, primary_key=True)
    ip = Column("ip", String)
    port = Column("port", Integer)
    country = Column("country", String)
    con_type = Column("con_type",String)
    response_time = Column("response_time", Float)

engine = create_engine(URL(**settings))
Session = sessionmaker(bind=engine)
session = Session()

r = redis.StrictRedis(host="redis-16451.c3.eu-west-1-1.ec2.cloud.redislabs.com", port=16451, password="javicp90")

for proxy in session.query(Proxies).filter(Proxies.ip != None).all():
    try:
        judge = requests.get("http://judge.live-proxy.net/index.php", 
                             proxies = {str(proxy.con_type) : proxy.full_address}, 
                             timeout = 3)
        # Only store the item if the judge makes a correct answer
        if judge.status_code == 200:
            r.setex(proxy.full_address, 120, proxy.con_type)
    # Exception handling
    except Exception as e:
        print("Bad proxy"+proxy.full_address)
    
