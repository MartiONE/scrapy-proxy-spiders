from sqlalchemy.orm import sessionmaker
from ProxyFetcher.models import Proxies, db_connect, create_table
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ProxyfetcherPipeline(object):
    def process_item(self, item, spider):
        return item
    
class ProxyfetcherHerokuPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        
    def process_item(self, item, spider):
        session = self.Session()
        proxy = Proxies(**item)
        
        try:
            # Not using add as sometimes will be duplicate key
            session.merge(proxy)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item
