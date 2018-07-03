# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class MycartoonPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item

    def get_media_requests(self, item, info):
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        print('+++++++++++++')
        for image_url in item['imgUrl']:
            print('--------' + image_url+'++++++'+item['fileName'][0])
            yield Request(image_url,meta={'item':item,'image_guid':item['fileName'][0]})

    def file_path(self, request, response=None, info=None):
        item=request.meta['item']
        # print('--------'+item['fileName'][0])
        dirName=item['dirName']
        dirName = re.sub(r'[？\\*|“<>:/]', '', dirName)
        image_guid = request.meta['image_guid']
        filename = u'{0}/{1}'.format(dirName, image_guid)
        print('++++++++++------------+++++++++++---------'+filename)
        return filename