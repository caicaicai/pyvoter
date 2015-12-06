# -*- coding: utf-8 -*- 
#author : zhongzhen.cai
#CreateDate : 2015-12-05

def getConfig():
	#参数配置
	config = {}

	#debug 模式
	config['debug'] = 1
	
	#投票配置
	config['Voter'] = {}
	#投票地址
	config['Voter']['url'] = "http://dl.xiaocaicai.com/voter.php"
	#保存成功投票的代理地址
	config['Voter']['file_greet_path'] = "./greet.txt"
	#成功投票标识前引导符
	config['Voter']['successPreMark'] = "o"
	#成功投票标识
	config['Voter']['successMark'] = "k"




	#多线程配置
	#投票的线程数量
	config['MultThread'] = {}
	config['MultThread']['threadNum'] = 300


	#蜘蛛配置
	config['Spider'] = {}
	#爬取到的IP保存位置
	config['Spider']['file_path'] = "./ipSpiders.txt"

	#挖掘代理服务器的地址和挖掘深度
	#config['prox_web']["服务器地址"] = 挖掘深度
	config['Spider']['prox_web'] = {}
	config['Spider']['prox_web']["http://www.youdaili.net/Daili/"] = 4
	config['Spider']['prox_web']["http://www.proxy360.cn/default.aspx"] = 4
	config['Spider']['prox_web']["http://www.xicidaili.com"] = 4
	config['Spider']['prox_web']["http://www.kuaidaili.com"] = 4
	config['Spider']['prox_web']["http://ip004.com"] = 4
	config['Spider']['prox_web']["http://www.haodailiip.com"] = 4
	config['Spider']['prox_web']["http://www.yun-daili.com"] = 4
	return config