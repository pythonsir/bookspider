#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scrapy
import os
import os.path as opath
from urllib.request import  urlretrieve
class bookSpider(scrapy.Spider):
    name = "book"
    urlStrs = ''
    def start_requests(self):
        with open("urls.txt",'r',encoding='utf-8') as f:
            urlStrs = f.read()
            f.close()
        urls = urlStrs.split(',')

        yield scrapy.Request(url=urls[0],callback=self.parse)

    def parse(self, response):
        books = response.xpath("//div[@id='basic']/ul/li/p/text()").getall()
        iframeUrl = response.xpath("//iframe/@src").get()
        self.logger.info('---------> iframe url is %s',iframeUrl)
        info = self.getUrlInfo(iframeUrl)
        self.logger.info("%s 有 %s 册",info[1],books)
        path='/Users/lxl/Documents/pythonProject/myspider/book/'+info[1]
        if opath.exists(path) is False:
            os.makedirs(path)
        for bookid in books:
            bookurl = info[0]+'/'+info[1]+'-'+self.getbookid(bookid)+'/'+info[1]+'-'+self.getbookid(bookid)+'/assets/basic-html/page-1.html'
            if opath.exists(path+"/"+self.getbookid(bookid)) is False:
                os.mkdir(path+"/"+self.getbookid(bookid))
            yield scrapy.Request(url=bookurl,callback=self.parsebook,meta={'path':path+"/"+self.getbookid(bookid)})

    '''
    解析每册书的信息，并且开始保存图片
    '''
    def parsebook(self,response):
        numstr = response.xpath("//span[@class='pager']/text()").get()
        pages = numstr.split("/")[1].strip() # 总页数
        page = 1
        while page <= int(pages):
            pageurl = self.getPageBasePath(response.url)+'/'+'page-'+str(page)+'.html'
            self.logger.info("处理页面：%s",pageurl)
            yield  scrapy.Request(url=pageurl,callback =self.pageImg,meta={'path':response.meta['path']})
            page += 1


    def pageImg(self,response):
        url = response.xpath("//div[@id='pageContainer']/img/@src").get()
        imgurl = response.urljoin(response.xpath("//div[@id='pageContainer']/img/@src").get())
        self.download(url=imgurl,path=response.meta['path'])
    '''
     解析 iframe 中的 http://db.sido.keio.ac.jp/kanseki/flipping/006659-001/index.html
     返回 （'http://db.sido.keio.ac.jp/kanseki/flipping','006659'）
     006659-001 
     006659:代表书号
     001: 代表册号
    '''
    def getUrlInfo(self,url):
        i = url.rfind("/", 0)
        urlSub = url[0:i]
        ii = urlSub.rindex("/", 0)
        _str = urlSub[ii + 1:]
        cc = _str.split('-')
        baseUrl = urlSub[0:ii]
        arr = (baseUrl, cc[0])
        return arr

    def getbookid(self,bookid):
        if int(bookid) >= 10 and int(bookid) < 100:
            return '0'+bookid
        else:
            return '00'+bookid

    def getPageBasePath(self,url):
        i = url.rindex("/", 0)
        return url[0:i]

    def download(self,url,path):
        i = url.rindex("/",0)
        filename = url[i+1:]
        if opath.exists(path+'/'+filename) is False:
            urlretrieve(url, path + '/' + filename)
            self.logger.info("下载图片链接：%s",url)

