# -*- coding: UTF-8 -*-

import re
import shutil
from jsmin import jsmin

def render_template(path):
	s = r'{src:"{{src}}"},'
	with open(r'./url_pool','r',encoding='UTF-8') as f:
		links = ''
		for x in f.readlines():
			links = links+re.sub(r'{{src}}',x.strip(),s)
		# print(links)
	shutil.copy(r'static/js/main_temp.js',r'static/js/main.js')

	with open (path,'r+',encoding='UTF-8') as f1:
		s = re.sub(r'{{links}}',links,f1.read())
		f1.seek(0)
		f1.truncate()
		f1.write(s)

def js_compress(path):
	try:
		with open(path,'r+',encoding='UTF-8') as f:
			f1 = jsmin(f.read())
			f.seek(0)
			f.truncate()
			f.write(f1)
	except Exception as e:
		pass		

if __name__ == '__main__':
	render_template(r'static/js/main.js')






