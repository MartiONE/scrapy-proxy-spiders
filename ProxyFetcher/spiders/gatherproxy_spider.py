import scrapy
from ProxyFetcher.items import ProxyfetcherItem

class GatherProxySpider(scrapy.Spider):
    
        name = "gatherproxy"
        allowed_domains = ["gatherproxy.com"]
        def start_requests(self):
                yield scrapy.FormRequest('http://gatherproxy.com/proxylist/anonymity/?t=Elite',
                                         formdata={'Uptime': '0', 'Type': 'elite', 'PageIdx': '1'},
                                         callback=self.parse)
                yield scrapy.FormRequest('http://gatherproxy.com/proxylist/anonymity/?t=Transparent',
                                         formdata={'Uptime': '0', 'Type': 'transparent', 'PageIdx': '1'},
                                         callback=self.parse)
                yield scrapy.FormRequest('http://gatherproxy.com/proxylist/anonymity/?t=Anonymous',
                                         formdata={'Uptime': '0', 'Type': 'anonymous', 'PageIdx': '1'},
                                         callback=self.parse)

        def parse(self, response):
                # Parse the footer page list
                for i in response.xpath("//div[@class='pagenavi']/a/text()"):
                        self.logger.warning(i.extract())
                        yield scrapy.FormRequest(url=response.url,
                                                 formdata={'Uptime': '0', 'Type': 'anonymous', 'PageIdx': i.extract()},
                                                 callback=self.parse_page)
        def parse_page(self, response):
                from scrapy.shell import inspect_response
                inspect_response(response, self)
                for row in response.xpath("//table/tr")[2:]:
                        # Item creation and deployment
                        item = ProxyfetcherItem()
                        item["ip"] = row.xpath("td")[1].re("document.write\('(.+?)'")[0].strip()
                        # The port is "encoded" as hexadecimal
                        item["port"] = str(int(row.xpath("td")[2].re("gp.dep\('(.+?)'")[0], 16))
                        item["country"] = row.xpath("td[5]/text()").extract()[0]
                        item["con_type"] = 'http'
                        item["full_address"] = "{}:{}".format(item["ip"], item["port"])
                        yield item.status_check(item)
