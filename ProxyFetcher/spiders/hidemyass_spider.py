import scrapy
from ProxyFetcher.items import ProxyfetcherItem
import re

# Spider for the forum of the website hidemyass.com

class HideMyAssProxySpider(scrapy.Spider):
    
        name = "hidemyass"
        allowed_domains = ["proxylist.hidemyass.com"]
        start_urls = [
            "http://proxylist.hidemyass.com/search-1304566"
        ]    
        
        def parse(self, response):
                for j in response.xpath("//tbody/tr"):
                        # Getting the styles, filtering and displaying
                        style = j.xpath("td[2]/span/style/text()").re("\.([^\{]+){display:none}")
                        result = ""
                        for i in j.xpath("td[2]/span/*|span/text()")[2:]:
                                # First chech for the style 'display: inline' and the abscense of any
                                if ("display: inline" in i.extract()) | ("<" not in i.extract()):
                                        result += i.xpath("text()").extract()[0] if i.xpath("text()").extract() else i.extract().strip()
                                # Check for the class, as sometimes there are classes not listed and must be included
                                elif "class" in i.extract():
                                        if i.xpath("@class").extract()[0] not in style:
                                                result += i.xpath("text()").extract()[0]
                                                
                        # Item initializer
                        item = ProxyfetcherItem()
                        item["ip"] = result
                        item["port"] = j.xpath("td[3]/text()").extract()[0].strip()
                        item["country"] = j.xpath("td[4]/span/text()").extract()[1].strip()
                        item["con_type"] = j.xpath("td[7]/text()").extract()[0].strip().lower()
                        item["full_address"] = "{}:{}".format(item["ip"], item["port"])
                        yield item.status_check(item)

                
               
