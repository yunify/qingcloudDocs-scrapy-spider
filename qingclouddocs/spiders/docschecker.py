# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import SitemapSpider
from urllib.parse import urlparse
import validators
import requests


class DocscheckerSpider(SitemapSpider):
    name = 'docschecker'
    sitemap_urls = ['http://localhost:4000/sitemap.xml','https://docs.qingcloud.com/sitemap.xml']
    handle_httpstatus_list = [404]

    def parse(self, response):
        if response.status == 404:
            self.logger.error("Found dead link %s" % response.url)
        elif response.headers['Content-Type'] == b'text/html' or response.headers['Content-Type'] == b'text/html; charset=utf-8':
            items = response.css('a::attr(href)').extract()
            for item in items:
                if item[0] == '/':
                    baseurl = urlparse(response.url)
                    url = "{}://{}{}".format(baseurl.scheme, baseurl.netloc, item)
                    self.validateUrl(response.url, url)
                elif validators.url(item):
                    if urlparse(item).hostname in ['docs.qingcloud.com', 'localhost']:
                        self.validateUrl(response.url,item)
                elif item == "javascript:;" or item.startswith("mailto:"):
                    pass
                else:
                    self.validateUrl(response.url,response.urljoin(item))

    def validateUrl(self,base,url):
        r = requests.get(url)
        if r.status_code == 404:
            self.logger.error("{} found deadlink {}".format(base, url))
