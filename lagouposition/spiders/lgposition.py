# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.spider import Spider
from selenium import webdriver
from lagouposition.items import LagoupositionItem


class LgpositionSpider(scrapy.Spider):
    name = "lgposition"
    #allowed_domains = ["https://www.lagou.com/zhaopin"]
    start_urls = ['https://www.lagou.com/zhaopin/']

    def __init__(self):
        #self.browser = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
        self.browser = webdriver.PhantomJS()

    def __del__(self):
        self.browser.close()

    def parse(self, response):
        data = LagoupositionItem()
        self.browser.get(response.url)
        sampleSet = set()
        ItemList = self.browser.find_elements_by_xpath('//div[@class="list_item_top"]')
        for item in ItemList:
            title = item.find_element_by_xpath('div[@class="position"]/div[@class="p_top"]/a[@class="position_link"]/h2').text
            area = item.find_element_by_xpath('div[@class="position"]/div[@class="p_top"]/a[@class="position_link"]/span/em').text
            company = item.find_element_by_xpath('div[@class="company"]/div/a').text
            industry = item.find_element_by_xpath('div[@class="company"]/div[@class="industry"]').text
            salary = item.find_element_by_xpath('div[@class="position"]/div[@class="p_bot"]/div/span').text
            requirement = item.find_element_by_xpath('div[@class="position"]/div[@class="p_bot"]/div').text.split(" ")[1]
            data['title'] = title
            data['area'] = area
            data['company'] = company
            data['industry'] = industry
            data['salary'] = salary
            data['requirement'] = requirement
            yield data
        nextPage = self.browser.find_element_by_xpath('//div[@class="pager_container"]/a[last()]').get_attribute("data-index")
        if nextPage:
           nextPageUrl = 'https://www.lagou.com/zhaopin/' + nextPage + '/?filterOptio=' + nextPage
           yield scrapy.http.Request(nextPageUrl, callback=self.parse)