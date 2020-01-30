FROM python:3.5
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt && cp fake_useragent_0.1.11.json /tmp
CMD /usr/local/bin/scrapy crawl amazon_bestseller
