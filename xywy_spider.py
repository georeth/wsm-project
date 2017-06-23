import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
import json


class XywySpider(scrapy.Spider):
    name = "xywy"
    allowed_domains = ["club.xywy.com"]
    start_urls = [
        "http://club.xywy.com"
        # "http://www.baidu.com"
    ]

    # def parse(self, response):
    #     filename = response.url.replace("http://club.xywy.com/", "").replace('/', '__')
    #     if 'static' in filename or 'doc_card' in filename:
    #         # self.info_extractor(response)
    #         if 'qlx' not in filename:
    #             with open('data/pages/'+filename, 'wb') as f:
    #                 f.write(response.body)
    #                 f.close()
    #
    #     if 'doc_card' in filename:
    #         doc_id = filename.split('__')[1]
    #         if len(filename.split('__')) == 2:
    #             for i in range(2, 21):
    #                 full_url = 'http://club.xywy.com/doc_card/' + doc_id + '/' + str(i)
    #                 # yield scrapy.Request(full_url)
    #                 # print full_url
    #                 yield SplashRequest(full_url, self.parse, args={'wait': 0.5})
    #
    #         for href in response.xpath('//a/@href'):
    #             full_url = response.urljoin(href.extract())
    #             # if 'static' in href.extract() or 'doc_card' in href.extract():
    #             #     print full_url
    #
    #             if 'doc_card' in full_url and doc_id not in full_url:
    #                 # print full_url
    #                 yield SplashRequest(full_url, self.parse, args={'wait': 0.5})
    #             if 'static' in full_url:
    #                 # print full_url
    #                 yield SplashRequest(full_url, self.parse, args={'wait': 0.5})
    #
    #     elif 'static' in filename:
    #         for href in response.xpath('//a/@href'):
    #             full_url = response.urljoin(href.extract())
    #             # if 'static' in href.extract() or 'doc_card' in href.extract():
    #             #     print href.extract(), full_url
    #             if 'doc_card' in full_url:
    #                 # print full_url
    #                 yield SplashRequest(full_url, self.parse, args={'wait': 0.5})
    #             if 'static' in full_url:
    #                 # print full_url
    #                 yield SplashRequest(full_url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        url = response.url
        if url == "http://club.xywy.com":
            doctors = {}
            doctor_to_crawl = []
            with open('../project/data/doctor.json', 'r') as f:
                for line in f.readlines():
                    doctor = json.loads(line)
                    doc_id = doctor['doc_id']
                    if doc_id not in doctors:
                        doctors[doc_id] = ''
                f.close()
            with open('../project/data/question_format.json', 'r') as f:
                for line in f.readlines():
                    question = json.loads(line)
                    for item in question['reply_list']:
                        doc_id = item['doc_id']
                        if doc_id not in doctors and doc_id is not None:
                            doctors[doc_id] = ''
                            # doctor_to_crawl.append(doc_id)
                            doctor_to_crawl.append(doc_id.split('/')[-1])  # mistake
            # print len(doctor_to_crawl)
            # print doctor_to_crawl[1]
            for doc_id in doctor_to_crawl:
                for i in range(2, 21):
                    full_url = 'http://club.xywy.com/doc_card/' + doc_id + '/' + str(i)
                    yield scrapy.Request(full_url, self.parse)
        else:
            filename = response.url.replace("http://club.xywy.com/", "").replace('/', '__')
            with open('data/pages_doctor/'+filename, 'wb') as f:
                f.write(response.body)
                f.close()

    def info_extractor(self, response):
        filename = response.url.replace("http://club.xywy.com/", "").replace('/', '__')
        if 'doc_card' in filename:
            doc_id = filename.split('__')[1]
            doctor = {'doc_id': doc_id}
            doctor['img_url'] = response.xpath('/html/body/div[5]/div[2]/div/div[1]/div[1]/div[1]/div/a/img/@src').extract_first()
            doctor['name'] = response.xpath('/html/body/div[5]/div[2]/div/div[1]/div[1]/div[1]/ul/li[1]/span[2]/text()').extract_first()
            doctor['title'] = response.xpath('/html/body/div[5]/div[2]/div/div[1]/div[1]/div[1]/ul/li[2]/span[2]/text()').extract_first()
            doctor['department'] = response.xpath('/html/body/div[5]/div[2]/div/div[1]/div[1]/div[1]/ul/li[3]/span[2]/text()').extract_first()
            doctor['expert'] = response.xpath('//*[@id="jeje"]/p[1]/text()').extract_first()
            doctor['hospital'] = response.xpath('//*[@id="jeje"]/p[2]/text()').extract_first()
            doctor['profile'] = response.xpath('//*[@id="jeje"]/div/text()').extract_first()
            doctor['evaluations_list'] = response.xpath('/html/body/div[5]/div[2]/div/div[1]/div[2]/div[3]/ul//text()').extract()
            doctor['q&a_list'] = []
            # print response.xpath('//*[@id="wdList"]/div').extract_first()
            for index, item in enumerate(response.xpath('//*[@id="wdList"]/div')):
                # print item
                # print '-------'
                qa = {}
                qa['field'] = item.xpath('div/h2/span/text()').extract_first()
                qa['question'] = item.xpath('div/h2/a/text()').extract_first()
                qa['answer'] = item.xpath('div/p/text()').extract_first()
                doctor['q&a_list'].append(qa)
                # for key in qa:
                #     print key+':', qa[key]
                # print '-------'
            with open('data/doctors/'+filename, 'wb') as f:
                f.write(json.dumps(doctor, indent=4))
                f.close()

            # print doctor['img_url']
            # print doctor['name']
            # print doctor['title']
            # print doctor['department']
            # print doctor['expert']
            # print doctor['hospital']
            # print doctor['profile']
            # print doctor['evaluations_list']
            # for text in doctor['evaluations_list']:
            #     print text

        elif 'static' in filename and 'qlx' not in filename:
            question_id = filename.split('.')[0].replace('static__', '')
            question = {'question_id': question_id}
            question['title'] = response.xpath('/html/body/div[7]/p//text()')
            print question['title']



