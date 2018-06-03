# -*- coding: UTF-8 -*-

import scrapy
import re

class weimeitupian(scrapy.Spider):
	name = 'weimeitupian'

	alloweded_domains = ['weimeitupian.com']

	def start_requests(self):
		urls = [
			'http://www.weimeitupian.com/meinv/page/1'
		]

		for url in urls:
			yield scrapy.Request(url=url,callback=self.parse)

	def parse(self,response):
		for href in response.css("div.img>a[target=_blank]::attr(href)").extract():
			yield response.follow(href,self.parse_inner)

		for a in response.css("div#page a"):
			yield response.follow(a,self.parse)


	def parse_inner(self,response):
		yield{
			# 'title': response.css("div.post-txt a::attr(title)").extract(),
			'image_urls': response.css("div.post-txt a img::attr(src)").extract(),
			# "date": response.css("div.post-detail div.meta span::text").extract_first(),
		}
