import scrapy
from ProxyFetcher.items import ProxyfetcherItem
from scrapy.contrib.spiders import CrawlSpider, Rule

# Spider for the forum of the website hidemyass.com

class HideMyAssProxySpider(CrawlSpider):
    
        name = "hidemyass"
        allowed_domains = ["proxylist.hidemyass.com"]
        start_urls = [
            "http://proxylist.hidemyass.com/search-1304566"
        ]    
        
def parse(self, response):
        for i in response.xpath("//tbody/tr"):
                # Getting the styles
                style = i.xpath("td")[1].xpath("span/style/text()").extract()[0].rsplit()
                # Filter the ones that have the display property
                style = [re.match("\.(\w+){display:none}", x) for x in style]
                # Refine the array
                style = [x.group(1) for x in style if x]
                
                result = ""
                for i in response.xpath("//tbody/tr")[0].xpath("td")[1].xpath("span/*|span/text()")[2:]:
                        if (("class" in i.extract()) & (style[0] not in i.extract())) | ("display: inline" in i.extract()) | ("<" not in i.extract()):
                                result += i.xpath("text()").extract()[0] if i.xpath("text()").extract() else i.extract().strip()
                print(result) 
                item = ProxyfetcherItem()
                item["ip"] = result
                yield item

                
               