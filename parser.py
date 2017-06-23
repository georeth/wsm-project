# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
import os
import os.path
import codecs

def format_info(item, mode='none'):
    if type([]) == type(item):
        result = []
        for element in item:
            element = element.strip()
            if element != '':
                result.append(element)
        if mode == 'text':
            result = ''.join(result)
    elif item is not None:
        result = item.strip()
    else:
        result = item
    return result


def print_info(tag, item):
    if type([]) == type(item):
        print tag + ':'
        for element in item:
            print element
    else:
        print tag + ':', item


def question_extractor(path):
    # with open('test.html', 'r') as f_in:
    question = {}
    with open(path, 'r') as f_in:
        filename = path.split('/')[-1]
        selector = Selector(text=f_in.read())
        question_id = filename.split('.')[0].replace('static__', '')
        question ['question_id'] = question_id
        question['title'] = format_info(selector.xpath('/html/body/div[7]/p//text()').extract(), 'text')
        question['detail'] = format_info(selector.xpath('//*[@id="qdetailc"]/text()').extract(), 'text')
        question['reply_list'] = []

        # print type(selector.xpath('//*[@id="qdetailc"]/text()').extract_first())
        # print selector.xpath('/html/body/div[7]/p//text()').extract()
        # print_info('question_id', question['question_id'])
        # print_info('title', question['title'])
        # print_info('detail', question['detail'])

        for index, reply_selector in enumerate(selector.xpath('//*[contains(@id, "reply")]')):
            reply = {}
            # print reply_selector.xpath('.').extract_first()
            reply['doctor_img_url'] = format_info(reply_selector.xpath('.//a[contains(@href, "doc_card")]//img/@src').extract_first())
            reply['doctor_infos'] = format_info(reply_selector.xpath('.//div[contains(@class, "Doc_zytpmd")]//text()').extract())
            reply['detail'] = format_info(reply_selector.xpath('.//div[contains(@class, "Doc_dochf")]/div[1]/text()').extract(), 'text')
            reply['doc_id'] = format_info(reply_selector.xpath('.//a[contains(@href, "doc_card")]/@href').extract_first(), 'text')
            question['reply_list'].append(reply)

            # print_info('doctor_img_url', reply['doctor_img_url'])
            # print_info('doctor_infos', reply['doctor_infos'])
            # print_info('detail', reply['detail'])
            # print_info('doc_id', reply['doc_id'])

        # for text in question['title_list']:
        #     print text
        # print question['detail']
        if question['title'] != '':
            with open('question_format.json', 'a') as f_out:
                f_out.write(json.dumps(question)+'\n')
                f_out.close()
        f_in.close()


def doctor_extractor(path):
    doctor = {}
    with codecs.open(path, 'r', 'gbk') as f_in:
        filename = path.split('/')[-1]
        doc_id = filename.split('__')[1]
        try:
            selector = Selector(text=f_in.read())
        except Exception, e:
            print e
            f_in.close()
            return
        doctor['doc_id'] = doc_id
        doctor['img_url'] = selector.xpath('//div[contains(@class, "bldle")]//img/@src').extract_first()
        doctor['name'] = selector.xpath('//ul[contains(@class, "bdul")]/li[1]/span[2]/text()').extract_first()
        doctor['title'] = selector.xpath('//ul[contains(@class, "bdul")]/li[2]/span[2]/text()').extract_first()
        doctor['department'] = selector.xpath('//ul[contains(@class, "bdul")]/li[3]/span[2]/text()').extract_first()
        doctor['expert'] = selector.xpath('//*[@id="jeje"]/p[1]/text()').extract_first()
        doctor['hospital'] = selector.xpath('//*[@id="jeje"]/p[2]/text()').extract_first()
        doctor['profile'] = selector.xpath('//*[@id="jeje"]/div/text()').extract_first()
        doctor['evaluations_list'] = format_info(selector.xpath('//ul[contains(@class, "bdxli")]//li//text()').extract())
        doctor['q&a_list'] = []
        # print selector.xpath('//*[@id="wdList"]/div').extract_first()
        for index, item in enumerate(selector.xpath('//*[@id="wdList"]/div')):
            # print item
            # print '-------'
            qa = {}
            qa['field'] = item.xpath('div/h2/span/text()').extract_first()
            qa['question'] = item.xpath('div/h2/a/text()').extract_first()
            qa['question_url'] = item.xpath('a/@href').extract_first()
            qa['answer'] = item.xpath('div/p/text()').extract_first()
            doctor['q&a_list'].append(qa)
        #     print_info('field', qa['field'])
        #     print_info('question', qa['question'])
        #     print_info('question_url', qa['question_url'])
        #     print_info('answer', qa['answer'])
        #
        # print_info('doc_id', doctor['doc_id'])
        # print_info('img_url', doctor['img_url'])
        # print_info('name', doctor['name'])
        # print_info('title', doctor['title'])
        # print_info('department', doctor['department'])
        # print_info('expert', doctor['expert'])
        # print_info('hospital', doctor['hospital'])
        # print_info('profile', doctor['profile'])
        # print_info('evaluations_list', doctor['evaluations_list'])
        if doctor['name'] is not None:
            with open('../project/data/doctor.json', 'a') as f_out:
                f_out.write(json.dumps(doctor)+'\n')
                f_out.close()
        f_in.close()


def format_doctor():
    doctors = {}
    # self.info_extractor(response)
    with open('../project/data/doctor.json', 'r') as f:
        for line in f.readlines():
            doctor = json.loads(line)
            doc_id = doctor['doc_id']
            if doc_id not in doctors:
                doctors[doc_id] = doctor
            else:
                for key in doctor:
                    if key == 'q&a_list':
                        for item in doctor[key]:
                            doctors[doc_id][key].append(item)
                    else:
                        if doctors[doc_id][key] is None:
                            doctors[doc_id][key] = doctor[key]
    with open('../project/data/doctor_format.json', 'a') as f_out:
        for doc_id in doctors:
            f_out.write(json.dumps(doctors[doc_id]) + '\n')
    print len(doctors.keys())




format_doctor()
# question_extractor('question3.htm')
# doctor_extractor('doc_card__123456')
# rootdir = '../project/data/pages_doctor'
# cnt = 0
# for parent, dirname, filenames in os.walk(rootdir):
#     for filename in filenames:
#         cnt += 1
#         print cnt
#         # print "parent is:" + parent
#         print "filename is:" + filename
#         # print "the full name of the file is:" + os.path.join(parent, filename)
#         # if 'static' in filename:
#         #     question_extractor(os.path.join(parent, filename))
#         if 'doc_card' in filename and cnt >= 1191:
#             doctor_extractor(os.path.join(parent, filename))
