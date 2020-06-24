#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from urllib import  request
def test1():

    html = ''

    with open('./index.html','r',encoding='utf-8') as r:
        html = r.read()
        r.close()

        all = Selector(text=html).xpath("//a[@name='alrp']").xpath("@href").getall()
    print(all)

def test2():
    url = 'http://db.sido.keio.ac.jp/kanseki/flipping/006659-001/index.html'
    i = url.rfind("/",0)
    url2 = url[0:i]
    ii =url2.rindex("/",0)
    bb = url2[ii+1:]
    cc = bb.split('-')
    baseUrl = url2[0:ii]
    arr = (baseUrl,cc[0])
    print(arr)
def test3():
    str = '\xa01 / 25'
    arr = str.split("/")
    print(arr[1].strip())

def test4():
    url = "http://db.sido.keio.ac.jp/kanseki/flipping/006659-001/006659-001/assets/basic-html/page-2.html"
    i = url.rindex("/",0)
    print(url[0:i])

def test5():
    page = 1;
    while  page <= 25:
        print(page)
        page += 1
def test6():
    url = 'http://db.sido.keio.ac.jp/kanseki/flipping/006659-001/006659-001/assets/common/page-substrates/page0001.jpg'
    filename = url[url.rindex("/",0)+1:]
    request.urlretrieve(url=url,filename=filename);
def test7():
    a = int('10')
    b = a - 1
    print(b)

test7()