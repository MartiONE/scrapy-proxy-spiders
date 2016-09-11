import scrapy
from ProxyFetcher.items import ProxyfetcherItem
import redis
import re
import configparser

# Config parser
cfg = configparser.ConfigParser()
cfg.read("general.cfg")


class FreeProxyListsSpider(scrapy.Spider):
        '''
        Spider for the forum of the website reeproxylists.net
        
        WARNING - Not working properly right now, catpcha support has to be added.
        
        '''
        
        name = "freeproxylists"
        allowed_domains = ["freeproxylists.net"]
        
        def start_requests(self):
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.8,es;q=0.6', 'Accept-Encoding': 'gzip, deflate, sdch', 'Connection': 'keep-alive', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Cache-Control': 'max-age=0', 'Host': 'www.freeproxylists.net', 'Upgrade-Insecure-Requests': '1', 'Cookie': 'visited=2016%2F09%2F11+21%3A12%3A31; hl=en; pv=7; userno=20160911-010067; from=direct'} 
                req = scrapy.Request("http://www.freeproxylists.net/?c=&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=50", self.parse, headers=headers)
                # Gather a random proxy from our redis server
                #r = redis.StrictRedis(host=cfg["remote_redis"]["host"], 
                #                     port=cfg["remote_redis"]["port"], 
                #                      password=cfg["remote_redis"]["password"])
                #req.meta['proxy'] = "http://"+r.randomkey().decode("utf-8")
                yield req
                
        def parse(self, response):
                for row in response.xpath("//table[@class='DataGrid']/tr")[1:]:
                        # There are empty rows for publicity purposes, ignore them
                        if len(row.xpath("td")) > 1:
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
