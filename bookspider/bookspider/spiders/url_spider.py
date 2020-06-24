#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scrapy

class urlSpider(scrapy.Spider):
    name = "urlSpider"

    def start_requests(self):
        urls = [
            'http://db.sido.keio.ac.jp/kanseki/T_bib_line_2.php'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        basepath = 'http://db.sido.keio.ac.jp/kanseki/'
        hrefs = response.xpath("//a[@name='alrp']").xpath("@href").getall()
        html =''
        for href in hrefs:
            path = basepath+href+","
            html += path

        with open("urls.txt",'w',encoding='utf-8') as wb:
            wb.write(html)
            wb.close()



