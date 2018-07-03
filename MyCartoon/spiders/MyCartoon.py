import scrapy
import re

from MyCartoon.items import MycartoonItem


class MyCarttoon(scrapy.Spider):
    name = 'cartoon'
    allowed_domains = ['comic.kukudm.com']
    start_urls = ['http://comic.kukudm.com/comiclist/3/']

    def __init__(self):
        # 图片链接server域名
        self.server_img = 'http://n.1whour.com/'
        # 章节链接server域名
        self.server_link = 'http://comic.kukudm.com'
        self.allowed_domains = ['comic.kukudm.com']
        self.start_urls = ['http://comic.kukudm.com/comiclist/3/']
        # 匹配图片地址的正则表达式
        self.pattern_img = re.compile(r'\+"(.+)\'><span')

    def parse(self, response):

        list=response.css("dd")
        items=[]
        for pageItem in list:
            item = MycartoonItem()
            href=pageItem.css('a::attr(href)').extract_first()
            text=pageItem.css('a::text').extract_first()
            item['dirName']=text
            item['linkUrl']=self.server_link+href
            items.append(item)
        for item in items[-2:-1]:
            yield scrapy.Request(url=item['linkUrl'], meta={'item':item},callback=self.parsePage)

    def parsePage(self, response):
        item = response.meta['item']
        script = response.css('body script').extract();
        img_url = re.findall(re.compile(r'\+"(.+)\'><span'), script[1])[0]
        item['imgUrl'] = [self.server_img + img_url]
        item['fileName'] = [response.url.split('/')[-1][:-3] + 'jpg']
        # print('**********************' + item['imgUrl'] + '-----------' + item['fileName'])
        yield item
        totalPage=response.css('td[valign="top"]')[0].re(u'共(\d+)页')[0]
        # for page in range(1,int(totalPage)+1):
        for page in range(2, 10):
            preLink=item['linkUrl'][:-5]
            newLink=preLink+str(page)+'.htm'
            yield scrapy.Request(url=newLink,meta={'item':item},callback=self.content)


    def content(self , response):
        num=response.url.split('/')[-1]
        item = response.meta['item']
        script = response.css('body script').extract();
        img_url = re.findall(re.compile(r'\+"(.+)\'><span'), script[1])[0]
        item['imgUrl'] = [self.server_img + img_url]
        item['fileName'] = [response.url.split('/')[-1][:-3]+ 'jpg']
        # print('**********************' + item['imgUrl'] + '-----------' + item['fileName'])
        yield item
