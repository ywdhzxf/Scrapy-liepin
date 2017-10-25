# -*- coding: utf-8 -*-
import scrapy
from src_liepin.items import LiePinItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
import hashlib
import re
import json

class CeshiSpider(RedisCrawlSpider):
    name = 'liepin'
    allowed_domains = ['liepin.com']
    redis_key = 'liepin:start_urls'

    #启动url = 'https://www.liepin.com/zhaopin/'

    rules = (
        # Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'job/\d+.shtml'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # print response.body
        #判断是否为手机端
        print response.url
        if 'm.liepin.com' in response.url:
            pass
        else:

            company = response.xpath('//div[@class="title-info"]/h3/a/text()').extract()
            position = response.xpath('//div[@class="title-info"]/h1/text()').extract()
            salary = response.xpath('//p[@class="job-item-title"]/text()').extract()
            if salary:
                salary = salary[0].strip()
                print salary

                print ('*')*100
            location = response.xpath('//p[@class="basic-infor"]/span/a/text()').extract()
            work_years = response.xpath('//div[@class="job-qualifications"]/span[2]/text()').extract()
            degree = response.xpath('//div[@class="job-qualifications"]/span[1]/text()').extract()
            position_type = response.xpath('//ul[@class="new-compintro"]/li[1]/a/text()').extract()
            tags = response.xpath('//div[@class="job-qualifications"]/span[3]/text()').extract()
            pub_date = response.xpath('//p[@class="basic-infor"]/time/text()').extract()
            position_desc = response.xpath('//div[@class="content content-word"]/text()').extract()
            work_address = response.xpath('//ul[@class="new-compintro"]/li[3]/text()').extract()
            print ''.join(company)
            print ''.join(position)
            print ''.join(salary)
            print ''.join(location)
            print ''.join(work_years)
            print ''.join(degree)
            print ''.join(position_type)
            print ''.join(tags)
            print ''.join(pub_date)
            print ''.join(position_desc)
            print ''.join(work_address)
            print '*'*200
            item = LiePinItem()
            item['url'] = self.md5(response.url)

            item['company'] = ''.join(company)
            item['position'] = ''.join(position)
            item['salary'] = ''.join(salary)
            item['location'] = ''.join(location)
            item['work_years'] = ''.join(work_years)
            item['degree'] = ''.join(degree)
            item['position_type'] = ''.join(position_type)
            item['tags'] = ''.join(tags)
            item['pub_date'] = ''.join(pub_date)
            item['position_desc'] = ''.join(position_desc)
            item['work_address'] = ''.join(work_address)
            yield item
    def md5(self,data):
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()
