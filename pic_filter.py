# -*- coding: UTF-8 -*-

import requests
import re
from multiprocessing import Pool

def picBroken_Filter(path):
	try:
		r = requests.get(path)
		if r.text.startswith('GIF'):
			with open(r'./bad_url','a+',encoding='UTF-8') as f:
				f.write(path)
	except Exception as e:
		pass

def picBroken_delete():
	f = open(r'./url_pool','r+',encoding='UTF-8')
	urls = f.read()
	with open(r'./bad_url','r',encoding='UTF-8') as f1:
		for x in f1.readlines():
			urls = re.sub(x,'',urls)
		f.seek(0)
		f.truncate()
		f.write(urls)
	f.close()
		

if __name__ == '__main__':
	p = Pool(20)
	with open(r'./url_pool','r',encoding='UTF-8') as f:
		for x in f.readlines():
			p.apply_async(picBroken_Filter, args=(x,))
		p.close()
		p.join()
		picBroken_delete()
		print('All done!')
