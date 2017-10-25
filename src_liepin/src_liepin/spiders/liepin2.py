# -*- coding: utf-8 -*-
import scrapy
import re,requests
from src_liepin.items import LiePinItem
from scrapy_redis.spiders import RedisSpider
import hashlib


class LiepinSpider(RedisSpider):
    name = 'lp'
    allowed_domains = ['liepin.com']
    redis_key = 'lp:start_urls'
    # start_urls = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key='
    headers = {
        "Connection":"keep-alive",
        "Pragma":"no-cache",
        "Cache-Control":"no-cache",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Upgrade-Insecure-Requests":"1",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"https://www.liepin.com/it/",
        # "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.8",
    }
    cookies = {
        "_fecdn_":"1",
        "__uuid":"1508721801747.49",
        "gr_user_id":"66e8807f-f514-4c28-ad26-20b0229cb21d",
        "lx_mscid":"s_00_pz1",
        "19b5a30f":"8af9d5966f9579f099bc69210d3abcec",
        "lt_auth":"uucIP3wMnVTxt3GM3TZW5Psc3d37UGjI93RZ1koDg9S6Xqbn4PriRgqHprAFxBMhwBpzccULNLD2%0D%0AMur8y3NJ7UYUwGmkloC2tOW40GEITd00cvukgP%2BqlZqDEckkkioHmnIw9HlIwk%2F0ukAhM4DtwGPh%0D%0Ajoju1bSl%2B%2Fs%3D%0D%0A",
        "UniqueKey":"c60b045321072d2a1a667e00ad0d9493",
        "user_kind":"0",
        "is_lp_user":"true",
        "c_flag":"9a80b7bfd9bd87691d4ec861b606e902",
        "new_user":"true",
        "_uuid":"46D9E135FFA8421F609CBB90736B883F",
        "login_temp":"islogin",
        "em_username":"4595430994e1723494273",
        "em_token":"YWMtpLadzreSEee-GGPb46U-tU8TxtBqMxHkgus5YKfC9XGksUpAt5IR55O6Rf9GHdMhAwMAAAFfRuAVBgBPGgDJRxZ_CIwaZDNmEln-2MbfgjlcBD-p5Hzd3Y5ZZPp98A",
        "iknowFlagPrivacyResume":"false",
        "_mscid":"00000000",
        "WebImPageId":"webim_pageid_59922108581.860634",
        "WebImConnect":"1",
        "JSESSIONID":"C908B39A53B370B19EC13E3CC1E3036B",
        "slide_goldcard_times20171023":"1",
        "fe_www_viewcount":"1",
        "Hm_lvt_a2647413544f5a04f00da7eee0d5e200":"1508721802,1508722280,1508722284",
        "Hm_lpvt_a2647413544f5a04f00da7eee0d5e200":"1508723152",
        "abtest":"0",
        "__tlog":"1508721801747.52%7C00000000%7CR000000075%7Cs_00_pz1%7Cs_00_pz1",
        "__session_seq":"19",
        "__uv_seq":"19",
        "user_vip":"0",
        "user_name":"%E5%B0%8F%E9%A3%9E",
        "user_photo":"55557f3b28ee44a8919620ce01a.gif",
        "gr_session_id_bad1b2d9162fab1f80dde1897f7a2972":"34387aea-40e4-4ffe-ad5c-ca3ff034e0bb",
        "gr_cs1_34387aea-40e4-4ffe-ad5c-ca3ff034e0bb":"UniqueKey%3Ac60b045321072d2a1a667e00ad0d9493",

    }
    def parse(self,response):
        start_urls = 'https://www.liepin.com/zhaopin/?&jobTitles=100070&ckid=a24ca5a7a6e93ced&fromSearchBtn=2&&init=-1&flushckid=1&dqs=010&industryType=&&&industries=&&key=&&headckid=4728e94611cc44ca&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg%7EgtPZh_DFC9H8iyDVQ-_DTg&d_headId=e2c0ab6effc2fa10b98b66bcf7f6cf1c&d_ckId=046c178fc6ffe97b60b2f8295b77dc92&d_sfrom=search_sub_site&d_curPage=0'
        yield scrapy.Request(url=start_urls,callback=self.parse_list,headers=self.headers,cookies=self.cookies)

    #获取所有的列表页
    def parse_list(self, response):

        # print response.body
        #获取所有的行业类别
        industry = response.xpath('//div[@class="sub-industry"]/a/@href').extract()
        # print industry

        #获取所有城市信息
        url = 'https://concat.lietou-static.com/dev/core/pc/revs/v3/static/js/plugins/localdata/city_cd0000c1.js'
        html = requests.get(url)
        html = html.content
        # print html
        pattern = re.compile(r'\d+')
        res = pattern.findall(html)
        city_list = []
        #删除所有的省,只留下细分的市
        for x in res:
            pattern_city = re.compile(r'\d{9}')
            city = pattern_city.findall(x)
            if city:
                city_list.append(city)
        # print city_list   #所有城市的代号,一个列表

        #所有职位类型
        work_type = [1,2,4]
        #企业规模
        compscale = ['010','020','030','040','050','060','070','080']
        #企业性质
        compkind = ['010','020','030','040','050','060','070','999',]
        print '开始循环爬取页面'
        #所有行业职业
        for x in industry:
            # print x
            hy_list = {}
            #行业类别  industryType=industry_12
            parrent_type = re.compile(r'industryType=industry_(\d{2})&')
            #具体行业
            parrent_hy = re.compile(r'industries=(\d+)')
            res1 = parrent_type.findall(x)
            res2 = parrent_hy.findall(x)
            print 1
            print res1[0],res2[0]  #所有的行业

                #所有的城市  城市暂时有bug
                # for city in city_list:
            #职位类型
            for job in work_type:
                #企业性质
                for comk in compkind:
                    #企业规模
                    for comp in compscale:
                        #页数
                        for page in range(101):
                            base_url = 'https://www.liepin.com/zhaopin/?&industryType=industry_%s&industries=%s&jobkind=%s&compscale=%s&compkind=%s&headckid=f82c74fd073cec50&curPage=%d'
                            starturl = base_url % (str(res1[0]),str(res2[0]),str(job),str(comp),str(comk),page)
                            # print starturl
                            yield scrapy.Request(starturl,callback=self.parse_content,headers=self.headers,cookies=self.cookies,priority=2)

    #获取所有的详情页
    def parse_content(self,response):
        # print response.body
        # print '*'*100
        url_list = response.xpath('//li/div/div/h3/a/@href').extract()
        pattern = re.compile(r'\d{9}')

        for url in url_list:

            print url
            res = pattern.findall(url)
            if res:

            #因为爬出来的链接有/a/10050995.shtml
                content =  int(res[0])
                base_url = 'https://www.liepin.com/job/%d.shtml'
                start = base_url % content
                print start
                yield scrapy.Request(url,callback=self.parse_title,priority=1)
            else:
                pass


    #解析详情页内容
    def parse_title(self,response):


        company = response.xpath('//div[@class="title-info"]/h3/a/text()').extract()
        position = response.xpath('//div[@class="title-info"]/h1/text()').extract()
        salary = response.xpath('//p[@class="job-item-title"]/text()').extract()
        if salary:
            salary = salary[0].strip()

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
        # print '*'*200
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
        print '开始处理item'
        yield item

    def md5(self,data):
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

