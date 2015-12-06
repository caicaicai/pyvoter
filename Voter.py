# -*- coding: utf-8 -*- 
#author : zhongzhen.cai
#CreateDate : 2015-12-05


import  http.cookiejar, urllib
from urllib.error import URLError, HTTPError
import json,time
import codecs
import re
import threading
import random
import time
import chardet
import Requester
from MultThread import MT
import Config


class Voter(object):
    """docstring for Voter"""
    def __init__(self):
        super(Voter, self).__init__()
        self.config = Config.getConfig()
        self.ipFile = self.config['Spider']['file_path']
        self.ipGreetFile = self.config['Voter']['file_greet_path']
        self.url = self.config['Voter']['url']
        self.successPreMark = self.config['Voter']['successPreMark']
        self.successMark = self.config['Voter']['successMark']
        self.Proxys = []
        self.greetServer = []
        #总节点数
        self.total = 0
        #成功投票数量
        self.voteCount = 0
        #当前节点指针
        self.curr = 0

        #当前进度
        self.currPercent = None

        #成功请求数
        self.successRequest = 0


    def get_proxys_server(self):
        file_object = open(self.ipFile,'r',encoding="utf8")
        print( "获取IP列表: " + self.ipFile )
        for line in file_object:
            #匹配IP地址正则
            results = re.findall('(?isu)(\d+\.\d+\.\d+\.\d+)\D+(\d+)', line)
            if results:
                ip = results[0][0] + ":" + results[0][1]
                self.Proxys.append(ip)
        file_object.close()
        print("新增代理服务器地址 " + str(len(self.Proxys)) + " 个")

    def fetch_server(self, mutex, param):
        while self.curr < len(self.Proxys):
            try:
                #加锁
                mutex.acquire()
                #获取代理服务器，更新当前节点
                server_ip = self.Proxys[self.curr]
                #当前节点位置后移
                self.curr += 1
                # 打印线程名和当前处理进度
                perc = (self.curr / self.total) * 100
                self.currPercent = str(float( '%.f' % perc))
                #释放锁
                mutex.release()

                html = Requester.fetch(self.url, {'http':server_ip})
                if(html):
                    self.successRequest += 1
                    print("successRequestCount:{0}, {1}% : 请求完毕,{2}".format(self.successRequest, self.currPercent, self.url))
                
                data = html.split(self.successPreMark)
                code = data[1][0]
                if(code == self.successMark):
                    #加锁
                    mutex.acquire()
                    self.voteCount += 1
                    print('[' + server_ip + '] > Request Success, Vote Success.Total Vote Count: ' + str(self.voteCount))
                    if self.ipFile != self.ipGreetFile:
                        file_greet = open(self.ipGreetFile,'a',encoding="utf8")
                        file_greet.write(server_ip + "\n")
                        file_greet.close()
                    #释放锁
                    mutex.release()
                else:
                    print('Request Success, But Success Mark not Match!')
            except Exception as e:
                if(self.config['debug']):
                    print(e)
                pass

    def run(self):

        self.get_proxys_server()
        
        #获取完服务器列表，更当前总节点数
        self.total = len(self.Proxys)

        mt = MT(self.fetch_server, None).run()
         
        # 打印执行结果
        print('Success Vote With Total Count : ' + str(self.voteCount))

        print('This is the end!')
        time.sleep(3)