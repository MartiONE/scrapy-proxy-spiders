# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import requests
import time
import logging
import configparser

# Config parser
cfg = configparser.ConfigParser()
cfg.read("general.cfg")



class ProxyfetcherItem(scrapy.Item):
    # Build of the item
    ip = scrapy.Field()
    port = scrapy.Field()
    country = scrapy.Field()
    con_type = scrapy.Field()
    response_time = scrapy.Field()
    full_address = scrapy.Field()
    
    def status_check(self, item):
        # Save timestamp for later calculation of elapsed time
        timestamp = time.time()
        # Call the judge for the proxy
        try:
            judge = requests.get(cfg.get('judge', "url", fallback="http://www.bdsmpichunter.com/dde32.php"), 
                                 proxies = {"http" : "http://{}:{}".format(item["ip"], item["port"])}, 
                                 timeout = 5)          
            # Only store the item if the judge makes a correct answer
            if (judge.status_code == 200) and ("HTTP_HOST" in judge.text):
                item["response_time"] = round(time.time() - timestamp, 3)
                return item
        # Exception handling
        except requests.exceptions.Timeout as e:
            logging.info("Timeout: "+str(e))        
        except requests.exceptions.ProxyError as e:
            logging.info("Proxy error: "+str(e))
        except requests.exceptions.ConnectionError as e:
            logging.info("Connection Error: "+str(e))
        except requests.exceptions.ChunkedEncodingError as e:
            logging.info("Connection probably broken.")
        except Exception as e:
            logging.info("Uncaught exception: " +str(e))
