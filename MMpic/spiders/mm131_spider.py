# -*- coding: UTF-8 -*-

import scrapy
import re

class mm131(scrapy.Spider):
	name = 'mm131'

	alloweded_domains = ['mm131.com']

	def start_requests(self):
		urls = [
			'http://www.mm131.com/xinggan/'
		]

		for url in urls:
			yield scrapy.Request(url=url,callback=self.parse)

	def parse(self,response):
		for href in response.css("div[class='main'] dd a[target=_blank]::attr(href)").extract():
			yield response.follow(href,self.parse_inner)

		for a in response.css("dd.page a"):
			yield response.follow(a,self.parse)


	def parse_inner(self,response):
		yield{
			'image_urls': response.css("div.content-pic a img::attr(src)").extract(),
		}

		for a in response.css("div.content-page a"):
			yield response.follow(a,self.parse_inner)
