#!/usr/bin/env python
# -*- coding: utf-8 -*-

from browsermobproxy import Server
from selenium import webdriver
from xvfbwrapper import Xvfb
import json
import argparse
import urlparse
import sys
import os


class performance(object):
    #create performance data

    def __init__(self, mob_path):
        #initialize
        from datetime import datetime
        print "%s: Go "%(datetime.now())
        self.browser_mob = mob_path
        self.server = self.driver = self.proxy = None

    @staticmethod
    def __store_into_file(args,title, result):
        #store data collected into file
        if 'path' in args:
        	har_file = open(args['path']+'/'+title + '.json', 'w')
        else:
        	har_file = open(title + '.json', 'w')
        har_file.write(result.encode('utf-8'))
       	har_file.close()

    def __start_server(self):
        #prepare and start server
        self.server = Server(self.browser_mob)
        self.server.start()
        self.proxy = self.server.create_proxy()

    def __start_driver(self,args):
        #prepare and start driver
        
        #chromedriver
        if args['browser'] == 'chrome':
        	print "Browser: Chrome"
        	print "URL: {0}".format(args['url'])
        	chromedriver = os.getenv("CHROMEDRIVER_PATH", "/chromedriver")
        	os.environ["webdriver.chrome.driver"] = chromedriver
        	url = urlparse.urlparse (self.proxy.proxy).path
        	chrome_options = webdriver.ChromeOptions()
        	chrome_options.add_argument("--proxy-server={0}".format(url))
        	chrome_options.add_argument("--no-sandbox")
        	self.driver = webdriver.Chrome(chromedriver,chrome_options = chrome_options)
        #firefox
        if args['browser'] == 'firefox':
            print "Browser: Firefox"
            profile = webdriver.FirefoxProfile()
            profile.set_proxy(self.proxy.selenium_proxy())
            self.driver = webdriver.Firefox(firefox_profile=profile)
		
			

    def start_all(self,args):
        #start server and driver
        self.__start_server()
        self.__start_driver(args)

    def create_har(self,args):
        #start request and parse response
        self.proxy.new_har(args['url'], options={'captureHeaders': True})
        self.driver.get(args['url'])
        
        result = json.dumps(self.proxy.har, ensure_ascii=False)
        self.__store_into_file(args,'har', result)
        
        performance = json.dumps(self.driver.execute_script("return window.performance"), ensure_ascii=False)
        self.__store_into_file(args,'perf', performance)

    def stop_all(self):
        #stop server and driver
        from datetime import datetime
        print "%s: Finish"%(datetime.now())
        
        self.server.stop()
        self.driver.quit()


if __name__ == '__main__':
	# for headless execution
    with Xvfb() as xvfb:
    	parser = argparse.ArgumentParser(description='Performance Testing using Browsermob-Proxy and Python')
    	parser.add_argument('-u','--url',help='URL to test',required=True)
    	parser.add_argument('-b','--browser',help='Select Chrome or Firefox',required=True)
    	parser.add_argument('-p','--path',help='Select path for output files',required=False)
    	args = vars(parser.parse_args())
    	path = os.getenv('BROWSERMOB_PROXY_PATH', '/browsermob-proxy-2.1.2/bin/browsermob-proxy')
    	RUN = performance(path)
    	RUN.start_all(args)
    	RUN.create_har(args)
    	RUN.stop_all()
