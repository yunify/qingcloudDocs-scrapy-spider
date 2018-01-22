# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from urllib.parse import urlparse
import validators


class DocscheckerSpider(Spider):
    name = 'docschecker'
    start_urls = ['https://docs.qingcloud.com/appcenter1/api/index.html']#'http://localhost:4000']
    handle_httpstatus_list = [404]

    def parse(self, response):
        if response.status == 404:
            self.logger.error("Found dead link %s" % response.url)
        elif response.headers['Content-Type'] == b'text/html' or response.headers['Content-Type'] == b'text/html; charset=utf-8':
            self.logger.info("Visiting %s" % response.url)
            items = response.css('a::attr(href)').extract()
            for item in items:
                if item[0] == '/':
                    baseurl = urlparse(response.url)
                    url = "{}://{}{}".format(baseurl.scheme, baseurl.netloc, item)
                    yield scrapy.Request(url)
                elif validators.url(item):
                    if urlparse(item).hostname in ['docs.qingcloud.com', 'localhost']:
                        yield scrapy.Request(item)
                elif item == "javascript:;" or item.startswith("mailto:"):
                    pass
                else:
                    yield scrapy.Request(response.urljoin(item))


