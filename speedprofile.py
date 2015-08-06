#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#Install Google Chrome
sudo apt-get install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo dpkg -i google-chrome*.deb
sudo apt-get install -f

# Install xvfb
sudo apt-get install -y xvfb
  
# Install API for browsermob-proxy, selenium and xvfb
sudo apt-get install python-pip
sudo pip install selenium browsermob-proxy xvfbwrapper --upgrade
 
# download browsermob proxy
wget https://github.com/downloads/lightbody/browsermob-proxy/browsermob-proxy-2.0-beta-6-bin.zip
unzip browsermob-proxy-2.0-beta-6-bin.zip

# copy browsermob-proxy to /var/lib
sudo cp -r browsermob-proxy /var/lib/
sudo chown -R a:a /var/lib/browsermob-proxy
 
# download selenium-server
wget http://selenium-release.storage.googleapis.com/2.41/selenium-server-standalone-2.41.0.jar
 
# start selenium-server
java /usr/bin/java -jar selenium-server.jar >> ./log/selenium.$(date +"%Y%d%m").log 2>&1&
 
# download chrome driver
sudo apt-get install unzip

wget -N http://chromedriver.storage.googleapis.com/2.10/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
 
"""

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
        if(args['path']!=NULL):
        	har_file = open(args['path']+'/'+title + '.json', 'w')
        else:
        	har_file = open(title + '.json', 'w')
        har_file.write(str(result))
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
        	chromedriver = "./bin/chromedriver"
        	os.environ["webdriver.chrome.driver"] = chromedriver
        	url = urlparse.urlparse (self.proxy.proxy).path
        	chrome_options = webdriver.ChromeOptions()
        	chrome_options.add_argument("--proxy-server={0}".format(url))
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
    	path = "./bin/browsermob-proxy/bin/browsermob-proxy"
    	RUN = performance(path)
    	RUN.start_all(args)
    	RUN.create_har(args)
    	RUN.stop_all()
