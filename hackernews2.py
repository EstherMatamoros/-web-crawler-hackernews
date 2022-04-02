import scrapy
from collections import Counter
import requests
import re
import string
import numpy as np
from operator import itemgetter
import operator


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://news.ycombinator.com/']

    def parse(self, response):
        table = response.css('.itemlist')
        i = 0
        np.array_result = []
        for row in table.xpath('tr'):
          if i == 0: #title
            title = row.css('.titlelink').xpath('text()').get()
            number = row.css('.rank').xpath('text()').get()

            if title is None:
              break
            i += 1
          elif i == 1: #subtext
            i += 1
            array_span = row.css('.subtext').xpath('span/text()').getall()            
            if len(array_span) > 0:
               text = array_span[0]
               points = int(text[0: len(text) - len('points') - 1])              
            else:
               points = 0
            # --- comments
            text_a = row.css('.subtext').xpath('a/text()').getall()[-1]            
            if 'comments' in text_a:
               comments = int(text_a[0:len(text_a) - len('comments')-1])
            else:
               comments = 0            
          else: #spacer
            i = 0            
            np.array_result.append([number, title, len(re.findall(r'\w+', title)), points, comments])
        
        print (np.array_result)  

        b = np.array_result
        #Filter all previous entries with more than five words in the title ordered by the number of comments first.
        firstfilter =  sorted(filter(lambda a: a[2] > 5, b), key=itemgetter(4), reverse= True)
        
        #Filter all previous entries with less than or equal to five words in the title ordered by points.
        secondfilter =  sorted(filter(lambda a: a[2] <= 5, b), key = operator.itemgetter(3), reverse = True)


        print(firstfilter)
        print(secondfilter)