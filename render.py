# -*- coding: UTF-8 -*-

import re
import shutil

def render_template(path):
	s = r'{src:"{{src}}"},'
	with open(r'./url_pool','r',encoding='UTF-8') as f:
		links = ''
		for x in f.readlines():
			links = links+re.sub(r'{{src}}',x.strip(),s)
		# print(links)
	with open (path,'r+',encoding='UTF-8') as f1:
		s = re.sub(r'{{links}}',links,f1.read())
		f1.seek(0)
		f1.truncate()
		f1.write(s)

if __name__ == '__main__':
	render_template(r'static/js/main.js')






