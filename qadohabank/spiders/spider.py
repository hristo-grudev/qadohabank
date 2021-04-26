import scrapy

from scrapy.loader import ItemLoader

from ..items import QadohabankItem
from itemloaders.processors import TakeFirst


class QadohabankSpider(scrapy.Spider):
	name = 'qadohabank'
	start_urls = ['https://qa.dohabank.com/press-room/']

	def parse(self, response):
		post_links = response.xpath('//h3[@class="entry-title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="nav-previous"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="entry-title"]/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//time[@class="entry-date published"]/text()').get()

		item = ItemLoader(item=QadohabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
