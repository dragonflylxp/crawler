# -*- coding: utf-8 -*-

import copy

import scrapy
from pyquery import PyQuery as pq
from scrapy_redis.spiders import RedisSpider

from amazon_scrapy.items import GoodsItem


class AmazonSpider(RedisSpider):

    name = 'amazon_category'
    redis_key = 'spider:targets:amz:category'


    def parse(self, response):
        if response.status == 200:
            self._saveCategory(response)
            """
            解析商品类别列表,获取到商品详情
            TODO 需要根据页面解析下一页
            """
            doc = pq(response.body)
            urls = doc('.s-result-list h2').items('a')
            for url in urls:
                href = "https://www.amazon.com" + url.attr("href")
                self.logger.debug("提取到详情页:%s" % href)
                # yield scrapy.Request(href, callback=self.parse_goods, meta={'amzUrl': href})
                yield response.follow(href, self.parse_goods, meta={'amzUrl': copy.deepcopy(href)})

    def parse_goods(self, response):
        
        # self._saveHtml(response)
        try:       
            amzUrl = response.meta['amzUrl']
            doc = pq(response.body)
            # 商品名称
            name = doc("span[id='productTitle']").text()
            # 品牌
            bylineInfo = doc("div[data-feature-name='bylineInfo']").text()# doc("a[id='bylineInfo']").text()
            self.logger.info("brand: %s" % bylineInfo)
            if ('by ' in bylineInfo):
                overName = 0
                brand = ' '.join(s for s in bylineInfo.split(" ")[1:])
            else:
                overName = 1
                brand = bylineInfo

            # 商品一级分类
            category1 =doc("a[class='a-link-normal a-color-tertiary']:eq(0)").text()
            # 商品二级分类
            category2 =doc("a[class='a-link-normal a-color-tertiary']:eq(1)").text()
            # ASIN码
            #asin = (doc("input[id='attach-baseAsin']")).attr("value")
            # 商品售价
            price = doc("span[id='priceblock_ourprice']").text()
            # 平均分
            gradeAvg = doc("span[class='a-icon-alt']:eq(0)").text().split(" ")[0]
            # 评分次数
            gradeTimes = doc("span[id='acrCustomerReviewText']").text().split(" ")[0]
            # 评论次数
            commentTimes = doc("a[id='askATFLink']").find("span").text().split(" ")[0]
            # 商品简介
            description = doc("div[id='feature-bullets']").text()
            # 商品图片，多个,分割
            imag1 =doc("div[id='altImages']").find("ul").find("li").find("img").eq(0).attr("src")
            imag2 =doc("div[id='altImages']").find("ul").find("li").find("img").eq(1).attr("src")
            imag3 =doc("div[id='altImages']").find("ul").find("li").find("img").eq(3).attr("src")
            imags = [imag1,imag2,imag3]
            pics =  ','.join(s for s in imags if  s!= None)
            merchantInfo = doc("div[id='merchant-info']").text()


            # 生成商品对象 
            item = GoodsItem()
            item['amzUrl'] = amzUrl
            item['name']  = name
            item['brand'] = brand.replace("by ", "")
            item['category1'] = category1
            item['category2'] = category2
            item['asin'] = amzUrl.split("/")[5]
            item['price'] = price
            item['gradeAvg']= gradeAvg
            item['gradeTimes'] = gradeTimes.replace(",", "")
            item['commentTimes'] = commentTimes.replace("+", "").replace(",", "")
            item['description'] = description
            item['pics'] = pics
            item['merchantInfo'] = merchantInfo
            item['overName'] = overName

            self.logger.info("提取到商品信息%s" % item)

            return  item

        except Exception as e:
            self.logger.error("解析页面:%s 异常:e" % response.url,e)
            self._saveHtml(response)

    def _saveCategory(self,response):
        filename = "category.html"
        with open(filename, 'wb') as f:
                f.write(response.body)
                self.logger.debug("保存网页成功 %s" % filename)

    def _saveHtml(self,response):
        """
        保存html文件
        """
        filename = response.url.split("/")[5]+".html"
        with open(filename, 'wb') as f:
                f.write(response.body)
                self.logger.debug("保存网页成功 %s" % filename)

    def _covertSold(self, txt):
        """
        * 1、Ships from and sold by Amazon.com 自营：是，自发货：否 - 
        * 2、if 以 Fulfilled by Amazon 结尾
        *     自营：1，自发货：0
        *    else 
        *     自营：0，自发货：1
        * 3、空的话则 自营：-1，自发货：-1
        """
        if (None or not txt):
            return -1
        if ("sold by Amazon" in txt):
            return 1
        else:
            return 0

    def _covertShip(self, txt):
        """
        * 1、Ships from and sold by Amazon.com 自营：1，自发货：-1 
        * 2、if 以 Fulfilled by Amazon 结尾
        *     自营：0，自发货：0
        *    else 
        *     自营：0，自发货：1
        * 3、空的话则 自营：-1，自发货：-1
        """
        if (None or not txt):
            return -1 
        if("Fulfilled by Amazon" in txt):
            return 0
        elif ("Ships from and sold by Amazon.com" in txt):
            return 0
        else:
            return 1
