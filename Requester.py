# -*- coding: utf-8 -*- 
#author : zhongzhen.cai
#CreateDate : 2015-05-31
import  http.cookiejar, urllib
from urllib.error import URLError, HTTPError
import codecs
import random
import chardet


def fetch(url,proxy = None):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    user_agents = [
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",

                    ]
    agent = random.choice(user_agents)
    if(proxy):
        opener.add_handler(urllib.request.ProxyHandler(proxy))
    opener.addheaders = [("User-agent",agent),("Accept","*/*"),('Referer','http://www.google.com')]
    resp = opener.open(url, timeout = 3)
    respByteObj = resp.read()
    encodeType = chardet.detect(respByteObj)['encoding']
    if(encodeType is None):
    	return None
    html = respByteObj.decode(encodeType)
    return html