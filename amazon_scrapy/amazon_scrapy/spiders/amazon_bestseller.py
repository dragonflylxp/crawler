# -*- coding: utf-8 -*-

import copy
import traceback

from pyquery import PyQuery as pq
from scrapy_redis.spiders import RedisSpider

from amazon_scrapy.items import GoodsItem


class AmazonSpider(RedisSpider):

    name = 'amazon_bestseller'
    redis_key = 'spider:targets:amz:bestseller'

    """
     BestSeller入口：
        lpush spider:targets:amz:bestseller https://www.amazon.com/Best-Sellers/zgbs
    """
    def parse(self, response):
        if response.status == 200:
            doc = pq(response.body)
            categoryList = doc("#zg_browseRoot").find("ul").find("li")
            for category in categoryList.items():
                text = category('a').text()
                href = category('a').attr("href") 
                if text in ["Baby", "Electronics"]:
                    yield response.follow(href, self.parse_category, 
                                          meta={'categoryLevel': 1, 
                                                'categoryName': text, 
                                                'categoryHref': href, 
                                                'categoryPath': text, 
                                                'pageNo': 1 
                                           })

    """
     处理本级分类，递归下级分类 
         步骤1：处理top1~50商品
         步骤2: 翻页处理top51~100商品
         步骤3: 递归解析下级分类  
             一级递归二级
             二级递归三级
             三级递归四级
             ...(无下级分类自动结束)
    """
    def parse_category(self,response):
        categoryLevel = response.meta['categoryLevel']
        categoryName  = response.meta['categoryName']
        categoryHref  = response.meta['categoryHref']
        categoryPath  = response.meta['categoryPath']
        pageNo        = response.meta['pageNo']
        if response.status == 200:
            try:
                # 步骤1：处理top1~50商品 
                doc = pq(response.body)
                goodsList = doc("#zg-ordered-list").find("li")
                for goods in goodsList.items():
                    href = "https://www.amazon.com" + goods.find("a").attr("href")
                    rank = goods(".zg-badge-text").text()[1:]
                    price = goods(".p13n-sc-price").text()[1:]
                    reviewStars = goods(".a-icon-alt").text()
                    reviewRating = goods(".a-size-small.a-link-normal").text()
                    yield response.follow(href, self.parse_goods, 
		        						  meta={'amzUrl': href,
                                                'rank': rank, 
                                                'price': price, 
                                                'reviewStars': reviewStars, 
                                                'reviewRating': reviewRating, 
                                                'categoryPath': categoryPath 
                                         })
                
                href = doc(".a-pagination").find("li").eq(2).find('a').attr("href")
                if pageNo == 1 and href:
                    # 步骤2: 翻页处理top51~100商品
                    yield response.follow(href, self.parse_category, 
		        						  meta={'categoryLevel': categoryLevel, 
                                                'categoryName': categoryName, 
                                                'categoryHref': href, 
                                                'categoryPath': categoryPath, 
                                                'pageNo': 2 
                                         })
                else:
                    # 步骤3: 解析下级分类  
                    self.logger.debug("{level}级分类[{name}]解析完成".format(level=categoryLevel, name=categoryPath))
                    categoryList = doc("#zg_browseRoot")
                    for level in range(categoryLevel+1):
                        categoryList = categoryList.find("ul")
                    categoryList = categoryList.find("li")
                    for category in categoryList.items():
                        text = category('a').text()
                        href = category('a').attr("href") 
                        if href is not None:
                            yield response.follow(href, self.parse_category, 
                                                  meta={'categoryLevel': categoryLevel+1, 
                                                        'categoryName': text, 
                                                        'categoryHref': href, 
                                                        'categoryPath': categoryPath+">>"+text, 
                                                        'pageNo': 1 
                                                 })
            except Exception as e:
                # 步骤4: 解析异常 
                self.logger.error("{level}级分类[{name}]解析失败:{error}".format(level=categoryLevel, name=categoryPath, error=e))
                traceback.print_exc()
        else:
            # 步骤5: 请求异常 
            self.logger.error("{level}级分类[{name}]请求失败:{status}".format(level=categoryLevel, name=categoryPath, status=response.status))

    """
       解析商品详情页
    """
    def parse_goods(self, response):
        #self._saveCategory(response)
        try:
            doc = pq(response.body)

            amzUrl = response.meta['amzUrl']
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

            categorys = response.meta['categoryPath'].split(">>", 4) 
            # 商品一级分类
            # category1 = doc("a[class='a-link-normal a-color-tertiary']:eq(0)").text()
            category1 = categorys[0] if len(categorys) > 0 else ''
            # 商品二级分类
            # category2 = doc("a[class='a-link-normal a-color-tertiary']:eq(1)").text()
            category2 = categorys[1] if len(categorys) > 1 else ''
            # 商品三级分类
            # category3 = doc("a[class='a-link-normal a-color-tertiary']:eq(2)").text()
            category3 = categorys[2] if len(categorys) > 2 else ''
            # 商品四级分类
            # category4 = doc("a[class='a-link-normal a-color-tertiary']:eq(3)").text()
            category4 = categorys[3] if len(categorys) > 3 else ''
            # ASIN码
            #asin = (doc("input[id='attach-baseAsin']")).attr("value")
            # 商品售价
            #price = doc("span[id='priceblock_ourprice']").text()[1:]
            # 是否亚马逊自营，0否、1是
            amzProprietary = doc("div[id='merchant-info']")
            # 平均分
            gradeAvg = doc("span[class='a-icon-alt']:eq(0)").text().split(" ")[0]
            # 评分次数
            gradeTimes = doc("span[id='acrCustomerReviewText']").text().split(" ")[0]
            # 评论次数
            commentTimes = doc("a[id='askATFLink']").find("span").text().split(" ")[0]
            # 商品简介
            #description = doc("div[id='delivery-message']").text()
            description = ''
            idx = 1
            for desc in doc("div[id=feature-bullets]").find("ul").find("li").items():
                description += str(idx) + '.' + desc('span').text() + '\n' 
                idx += 1
            # 商品图片，多个,分割
            imag1 =doc("div[id='altImages']").find("ul").find("li").find("img").eq(0).attr("src")
            imag2 =doc("div[id='altImages']").find("ul").find("li").find("img").eq(1).attr("src")
            imag3 =doc("div[id='altImages']").find("ul").find("li").find("img").eq(3).attr("src")
            imags = [imag1,imag2,imag3]
            pics =  ','.join(s for s in imags if  s!= None)
            merchantInfo = doc("div[id='merchant-info']").text()
            # 商品在当前top100的分类排名
            rank = response.meta['rank']
            # 商品售价
            price = response.meta['price']
            # custom review star
            reviewStars = response.meta['reviewStars'].split(" ")[0]
            # custom review rating 
            reviewRating = response.meta['reviewRating'].replace(',','')
            
            # 生成商品对象 
            item = GoodsItem()
            item['amzUrl'] = amzUrl
            item['name']  = name
            item['brand'] = brand
            item['rank'] = rank 
            item['reviewStars'] = reviewStars 
            item['reviewRating'] = reviewRating 
            item['category1'] = category1
            item['category2'] = category2
            item['category3'] = category3
            item['category4'] = category4
            #item['category'] = '|'.join([category1, category2, category3, category4]) 
            item['categoryPath'] = response.meta['categoryPath'] 
            item['asin'] = amzUrl.split("/")[5]
            item['price'] = price
            item['gradeAvg']= gradeAvg
            item['gradeTimes'] = gradeTimes.replace(",",".")
            item['commentTimes'] = commentTimes.replace("+","")
            item['description'] = description
            item['pics'] = pics
            #item['sold'] = self._convertSold(merchantInfo)
            #item['ship']= self._convertShip(merchantInfo)
            item['merchantInfo']= merchantInfo 
            item['overName'] = overName

            self.logger.info("捉取到的商品信息%s" % item)

            return  item

        except Exception as e:
            self.logger.error("解析商品异常:e" % response.url,e)
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

    def _convertSold(self, txt):
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

    def _convertShip(self, txt):
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
