# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
from scrapy_redis.spiders import RedisSpider

from amazon_scrapy.items import GoodsItem


class AmazonSpider(RedisSpider):

    name = 'amazon_goods'
    redis_key = 'spider:targets:amz:goods'


    def parse(self, response):
        if response.status == 200:
            self.logger.info("抓取网址成功 %s " % response.url)
            self.parse_doc(response)

    def parse_doc(self,response):
        """
        解析商品详情
        """
        try:
            doc = pq(response.body)
            amzUrl = response.url
            # 商品名称
            name = doc("span[id='productTitle']").text()
            # 品牌
            brand = doc("a[id='bylineInfo']").text()
            # 商品一级分类
            category1 =doc("a[class='a-link-normal a-color-tertiary']:eq(0)").text()
            # 商品二级分类
            category2 =doc("a[class='a-link-normal a-color-tertiary']:eq(1)").text()
            # ASIN码
            #asin = (doc("input[id='attach-baseAsin']")).attr("value")
            # 商品售价
            price = doc("span[id='priceblock_ourprice']").text()[1:]
            # 是否亚马逊自营，0否、1是
            amzProprietary = doc("div[id='merchant-info']")
            # 平均分
            gradeAvg = doc("span[class='a-icon-alt']:eq(0)").text().split(" ")[0]
            # 评分次数
            gradeTimes = doc("span[id='acrCustomerReviewText']").text().split(" ")[0]
            # 评论次数
            commentTimes = doc("a[id='askATFLink']").find("span").text().split(" ")[0]
            # 商品简介
            description = doc("div[id='delivery-message']").text()
            # 商品图片，多个,分割
            imag1 =doc("div[id='altImages']").find("ul").find("li").find("img").eq(0).attr("src")
            imag2 =doc("div[id='altImages']").find("ul").find("li").find("img").eq(1).attr("src")
            imag3 =doc("div[id='altImages']").find("ul").find("li").find("img").eq(3).attr("src")
            imags = [imag1,imag2,imag3]
            pics =  ','.join(s for s in imags if  s!= None)
            txt = doc("div[id='merchant-info']").text()

            # 生成商品对象 
            item = GoodsItem()
            item['amzUrl'] = amzUrl
            item['name']  = name
            item['brand'] = brand
            item['category1'] = category1
            item['category2'] = category2
            item['asin'] = amzUrl.split("/")[5]
            item['price'] = price
            item['gradeAvg']= gradeAvg
            item['gradeTimes'] = gradeTimes.replace(",",".")
            item['commentTimes'] = commentTimes.replace("+","")
            item['description'] = description
            item['pics'] = pics
            item['sold'] = self._covertSold(txt)
            item['ship']= self._covertShip(txt)
            item['shipAndSold'] = txt
            self.logger.info("提取商品信息%s" % item)
            return  item

        except Exception as e:
            self.logger.error("页面:%s 异常:e" % url,e)
            self.save_page(response)
            return

    def save_page(self,response):
        """
        保存html文件
        """
        filename = response.url.split("/")[5]+".html"
        with open(filename, 'wb') as f:
                f.write(response.body)
                self.logger.debug("保存网页成功 %s" % filename)

    def covert_sold(self, txt):
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

    def covert_ship(self, txt):
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
        elif (txt == "Ships from and sold by Amazon.com."):
            return 0
        else:
            return 1
