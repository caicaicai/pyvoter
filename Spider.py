# -*- coding: utf-8 -*- 
#author : zhongzhen.cai
#CreateDate : 2015-12-05


import json,time
import codecs
import re
import random
import time
import Requester
import Config
from MultThread import MT


class Spider():
    """docstring for Spider"""
    #存储遍历到的url
    visited = []
    #存储当前遍历到的url，用于存储到visited和urls，每次循环清空
    searched_url = []
    #存储上次遍历到的url，便于下次遍历
    urls = []
    depth = 0
    counter = 0
    #获取到的ip池
    ips = []

    def __init__(self):
        self.config = Config.getConfig()

    def run(self):
        #遍历代理服务器列表
        for (prox_web, deep) in self.config['Spider']['prox_web'].items():
            self.searched_url.append(prox_web)
            self.urls.append(prox_web)
            self.depth = deep
            self.counter = 0
            self.searched_url = []
            while self.counter < self.depth:
                for w in self.searched_url:
                    if w not in self.visited:
                        self.visited.append(w)
                        self.urls.append(w)
                self.searched_url = []
                #多线程调用蜘蛛
                mt = MT(self.fetch, None).run()
                print("第 " + str(self.counter) + " 轮遍历结束，当前获取到的链接数量：" + str(len(self.visited)))
                time.sleep(3)
                self.counter += 1
                print(self.counter)
        print("蜘蛛结束...")
        print("累计爬取页面数量: " + str(len(self.visited)))
        print("累计获取代理服务器数量: " + str(len(self.ips)))
        self.saveIP()
        time.sleep(3)
        return self

    def fetch(self, mutex, param):
        while (len(self.urls) > 0):
            mutex.acquire()
            if(len(self.urls) > 0):
                url = self.urls.pop(0)
            mutex.release()
            print('scanning..' + url)
            if re.match(r".+/", url):
                urlBase = re.findall(r".+/", url)[0]
            else:
                urlBase = url + '/'
            try:
                html = Requester.fetch(url)
                if(html):
                    results = re.findall('(?isu)(\d+\.\d+\.\d+\.\d+)\D+(\d+)', html)

                    if len(results) > 0:
                        mutex.acquire()
                        self.ips += results
                        print("当前获取到的IP数量: " + str(len(self.ips)))
                        mutex.release()

                    urls_1 = self.find_urls(html)
                    urls_2= []
                    for r in urls_1:
                        if re.match(r"^[^http]", r):
                            r = urlBase + r
                        urls_2.append(r)
                    mutex.acquire()
                    self.searched_url += urls_2
                    mutex.release()
            except Exception as e:
                if(self.config['debug']):
                    print(e)
    def find_urls(self, html):
        url_list = []
        for tag in re.findall('< *a +href[^>]+', html): # find the a tags
            m = re.search('href *= *[\'"]([^\'"]+)', tag) # find the href
            if m:
                url_list.append(m.group(1)) # add the sub match
        return url_list


    def saveIP(self):
        print(str(len(self.visited)) + ' urls get...')
        print(str(len(self.ips)) + ' ips get...')
        ok_ip = []
        for ip in self.ips:
            if ip not in ok_ip:
                ok_ip.append(ip)
        print("clear_ip count: " + str(len(ok_ip)))
        time.sleep(3)
        file_obj = open(self.config['Spider']['file_path'],'w',encoding="utf8")
        for ips_ in ok_ip:
            ip = ips_[0] + ":" + ips_[1]
            file_obj.write(ip + "\n")
        file_obj.close()
