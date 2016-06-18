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
                        #self.logger.info(str(j))
                        # Getting the styles
                        style = j.xpath("td")[1].xpath("span/style/text()").extract()[0].rsplit()
                        # Filter the ones that have the display property
                        style = [re.match("\.([^\{]+){display:none}", x) for x in style]
                        # Refine the array
                        style = [x.group(1) for x in style if x]
                        
                        result = ""
                        for i in j.xpath("td")[1].xpath("span/*|span/text()")[2:]:
                                
                                if ("display: inline" in i.extract()) | ("<" not in i.extract()):
                                        result += i.xpath("text()").extract()[0] if i.xpath("text()").extract() else i.extract().strip()
                                elif "class" in i.extract():
                                        if i.xpath("@class").extract()[0] not in style:
                                                #print(i)
                                                result += i.xpath("text()").extract()[0]
                        self.logger.info(result) 
                        item = ProxyfetcherItem()
                        item["ip"] = result
                        item["port"] = j.xpath("td[3]/text()").extract()[0].strip()
                        item["country"] = j.xpath("td[4]/span/text()").extract()[1].strip()
                        item["con_type"] = j.xpath("td[7]/text()").extract()[0].strip().lower()
                        item["full_address"] = "{}:{}".format(item["ip"], item["port"])
                        yield item.status_check(item)
                        #print(result if re.match("([0-9]{1,3}\.){3}[0-9]{1,3}", result) else [result, j.extract(), style])

                
               
