# -*- coding: UTF-8 -*-

import re
import base64
import time,os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from multiprocessing import Pool

import config

class weibo_login(object):

	url = 'http://weibo.com/login.php'

	def __init__(self,account=config.account,passwd=config.passwd):
		self.__account = account
		self.__passwd = passwd
		self.__url = weibo_login.url

	def login(self):
	    chrome_options = ChromeOptions()
	    chrome_options.add_argument('--headless')
	    chrome_options.add_argument('--no-sandbox')
	    driver = webdriver.Chrome('chromedriver',
	                              chrome_options=chrome_options)
	    driver.maximize_window()
	    driver.set_page_load_timeout(30)
	    driver.set_window_size(1124, 850)
	    # locator = (By.)
	    driver.get(self.__url)
	    name_field = driver.find_element_by_id('loginname')
	    name_field.clear()
	    name_field.send_keys(self.__account)
	    password_field = driver.find_element_by_class_name('password').find_element_by_name('password')
	    password_field.clear()
	    password_field.send_keys(self.__passwd)

	    submit = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a/span')

	    ActionChains(driver).double_click(submit).perform()
	    time.sleep(5)
	    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'WB_miniblog')))

	    self.source = driver.page_source

	    if self.is_login(self.source):
	    	self.sina_cookies = driver.get_cookies()
	    	self.dict = {}
	    	for cookie in self.sina_cookies:
	    		self.dict[cookie['name']] = cookie['value']
	    	driver.quit()
	    	return self.dict
	    else:
	    	return None

	def is_login(self,source):
	    rs = re.search(r"CONFIG\['islogin'\]='(\d)'", source)
	    if rs:
	        return int(rs.group(1)) == 1
	    else:
	        return False


	def write_cookie(self):
		cookie = self.login()
		if cookie:
			with open('cookie','w+',encodeind='UTF-8') as f:
				f.write(cookie)

def pic2weibo(pic_path,cookies):
	with open(pic_path,'rb') as f:
		ba = base64.b64encode(f.read())
	data = {'b64_data':ba}
	r =requests.post(config.full_site,cookies=cookies,data=data)
	url = 'http://ww2.sinaimg.cn/large/'+re.search(r'"pid":"(.*)"',r.text).group(1)

	with open ('url_pool','a+') as f:
		f.write(url.strip()+'\n')

def images_path(images_folder_path):
	for x in os.listdir(images_folder_path):
		path = os.path.join(os.path.abspath(images_folder_path),x)
		yield path

# if __name__ == '__main__':
# 	w = weibo_login()
# 	cookies = w.login()
# 	if cookie:
# 		write_url_pool(r'images/full',cookies)
# 	else:
# 		print('Login failed!')

if __name__ == '__main__':
	w = weibo_login()
	cookies = w.login()
	if cookies:
		p = Pool(20)
		for x in images_path(r'images'):
			p.apply_async(pic2weibo, args=(x,cookies))
		p.close()
		p.join()
		print('All uploaded!')
	else:
		print('Login failed!')
