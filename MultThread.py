# -*- coding: utf-8 -*- 
#author : zhongzhen.cai
#CreateDate : 2015-12-05




from threading import Thread
import threading
import Config


class MT(object):
	def __init__(self, func, parameter):
		super(MT, self).__init__()

		#函数以及参数
		self.func = func
		self.param = parameter

		#锁
		self.mutex = threading.Lock()
		#定义进程池
		self.threads = []
		
		#全局配置
		config = Config.getConfig()
		self.threadNum = config['MultThread']['threadNum']

	def run(self):
		# 先创建线程对象
		for x in range(0, self.threadNum):
			self.threads.append(threading.Thread(target=self.func, args=(self.mutex, self.param)))
		# 启动所有线程
		for t in self.threads:
			t.start()
		# 主线程中等待所有子线程退出
		for t in self.threads:
			t.join()  
