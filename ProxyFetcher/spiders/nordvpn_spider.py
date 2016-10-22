import scrapy
import json
from ProxyFetcher.items import ProxyfetcherItem

class FreeProxyListNet(scrapy.Spider):
    
        name = "nordvpn"
        allowed_domains = ["nordvpn.com"]
        start_urls = [
            "https://nordvpn.com/wp-admin/admin-ajax.php?searchParameters%5B0%5D%5Bname%5D=proxy-country&searchParameters%5B0%5D%5Bvalue%5D=&searchParameters%5B1%5D%5Bname%5D=proxy-ports&searchParameters%5B1%5D%5Bvalue%5D=&searchParameters%5B2%5D%5Bname%5D=http&searchParameters%5B2%5D%5Bvalue%5D=on&searchParameters%5B3%5D%5Bname%5D=https&searchParameters%5B3%5D%5Bvalue%5D=on&limit=25&action=getProxies&offset=0"
        ]    
	
        def parse(self, response):
                for j in json.loads(response.body_as_unicode()):
                        # Item creation and deployment
                        item = ProxyfetcherItem()                        
                        item["ip"] = j["ip"]
                        item["port"] = j["port"]
                        item["country"] = j["country"]
                        item["con_type"] = j["type"].lower()
                        item["full_address"] = "{}:{}".format(item["ip"], item["port"])
                       	yield item.status_check(item)
                if j:
                        n = int(response.url.rsplit("=", 1)[1])+25
                        yield scrapy.Request("{}={}".format(response.url.rsplit("=", 1)[0], n), callback=self.parse)
                        
