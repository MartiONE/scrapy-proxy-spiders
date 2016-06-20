import scrapy
from ProxyFetcher.items import ProxyfetcherItem
import redis
import re
import configparser

# Config parser
cfg = configparser.ConfigParser()
cfg.read("general.cfg")


class FreeProxyListsSpider(scrapy.Spider):
        '''Spider for the forum of the website reeproxylists.net'''
        
        name = "freeproxylists"
        allowed_domains = ["freeproxylists.net"]
        
        def start_requests(self):
                req = scrapy.Request("http://www.freeproxylists.net/?c=&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=50", self.parse)
                r = redis.StrictRedis(host=cfg["remote_redis"]["host"], 
                                      port=cfg["remote_redis"]["port"], 
                                      password=cfg["remote_redis"]["password"])
                req.meta['proxy'] = "http://"+r.randomkey().decode("utf-8")
                yield req
                
        def parse(self, response):
                for row in response.xpath("//table[@class='DataGrid']/tr")[1:]:
                        item = ProxyfetcherItem()
                        # This website uses JavaScript for encryption of the IP with UTF-16
                        # Extract payload for the function
                        payload = row.xpath("td/script/text()")[0].re('"(.*)"')[0]
                        # Convert it from UTF-16
                        payload = "".join([chr(int(x, 16)) for x in payload.split("%")[1:]])
                        # Extract the IP clean, nice try website.
                        item["ip"] = re.search("(([0-9]{1,3}\.){3}[0-9]{1,3})", payload).group(0)
                        item["port"] = row.xpath("td[2]/text()").extract()[0].strip()
                        item["con_type"] = row.xpath("td[3]/text()").extract()[0].lower().strip()
                        item["country"] = row.xpath("td[5]/text()").extract()[0].strip()
                        item["full_address"] = "{}:{}".format(item["ip"], item["port"])
                        yield item.status_check(item)