# -web-crawler-hackernews
Web crawler using scraping techniques to extract the first 30 entries from https://news.ycombinator.com/ . 
Extracts title, the number of the order, the number of comments, and points for each entry. 
It filters all previous entries with more than five words in the title ordered by the number of comments first. 
It filters all previous entries with less than or equal to five words in the title ordered by points.

It uses the scrapy tools to extract the data from the webpage. To run the program the following command line is used: 

            scrapy runspider hackernews2.py

A **for** loop is used to extract the data needed from each row. Each row is divided in tree rows: title, subtitle, spacer. 

The **title** and the ***number of order** is extracted from the first row as follows: 

            title = row.css('.titlelink').xpath('text()').get()
            number = row.css('.rank').xpath('text()').get()
            
To use later, the words of the title sentences were counted using the **re** library, as follows:

            len(re.findall(r'\w+', title))

The number of word of each title is also display in the final array of extracted data in order to apply the filters mentioned before. 

The first extraction give us strings. In the case of comments and points, they are converted into integers to be used later in the filters.
The conversion to integers is done as follows: 

For **points**: 

            array_span = row.css('.subtext').xpath('span/text()').getall()            
            if len(array_span) > 0:           #checks if there are points.
               text = array_span[0]
               points = int(text[0: len(text) - len('points') - 1])              
            else:                             #if there are no points then the value is 0
               points = 0
               
For **comments**: 

            text_a = row.css('.subtext').xpath('a/text()').getall()[-1]         #extract the last elemnts of the subtext which is comments   
            if 'comments' in text_a:                                            #if it has comments then it would return us only the number
               comments = int(text_a[0:len(text_a) - len('comments')-1])
            else:                                                               #if there are no comments, the value is 0 
               comments = 0     
             
             
Then, the array is ordered as follows:

0: number of order

1: title 

2: number of words in the title

3: points 

4: comments

which is coded as: 

              np.array_result.append([number, title, len(re.findall(r'\w+', title)), points, comments])

FInally, the filters are coded using the **operator library** to sort in descendant order and a filter **function lambda** to pick specific titles.

               #Filter all previous entries with more than five words in the title ordered by the number of comments first.
               firstfilter =  sorted(filter(lambda a: a[2] > 5, b), key=itemgetter(4), reverse= True)
        
              #Filter all previous entries with less than or equal to five words in the title ordered by points.
              secondfilter =  sorted(filter(lambda a: a[2] <= 5, b), key = operator.itemgetter(3), reverse = True)


