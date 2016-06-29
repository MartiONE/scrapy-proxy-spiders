import scrapy
from ProxyFetcher.items import ProxyfetcherItem

class Spyspider(scrapy.Spider):
    
        name = "spys"
        allowed_domains = ["http://spys.ru/"]
        start_urls = [
            "http://spys.ru/en/free-proxy-list/"
        ]
        # Helper function to process the abstaction
        def process_operands(self, op, dictionary):
                if type(op) != int:
                        op = op.split("^")
                        return int(op[0])^dictionary[op[1]]
                else:
                        return op
                
        def parse(self, response):
                # Strong magic, converting the javascript variables into a dictionary
                dictionary = {y[0]:
                                 int(y[1]) if y[1].isdigit() else y[1]
                                 for y in [x.split("=") 
                                           for x in response.xpath("//body/script/text()").extract()[0].split(";") if x]}
                # Some of the values are backlinked to dictionary values, so we solve it.
                # We cannot do it in one iteration because we really need other dictionary values.
                dictionary = {x:self.process_operands(y, dictionary) for x,y in dictionary.items()}
                        
                for j in response.xpath("//body/table[2]/tr[4]/td/table/tr")[3:-1]:
                        
                        # Item creation and deployment
                        item = ProxyfetcherItem()
                        
                        item["ip"] = j.xpath("td[1]/font[2]/text()").extract()[0]
                        # Extracting the operands of the JS function
                        operands = [x.split("^") for x in j.xpath("td/font[@class='spy14']/script/text()").re("\((\w+\^\w+)\)")]
                        # Combine them all looking at the dictionary to form the port
                        item["port"] = "".join([str(dictionary[x[0]]^dictionary[x[1]]) for x in operands])
                        item["country"] = j.xpath("td[4]/a/font/text()").extract()[0].strip()
                        item["con_type"] = j.xpath("td[2]/a/font/text()").extract()[0].strip().lower()
                        item["full_address"] = "{}:{}".format(item["ip"], item["port"])
                        yield item.status_check(item)
