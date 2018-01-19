# -*- coding: utf-8 -*-
from selenium import webdriver
from lxml import etree
import sys
import re
import time
import MySQLdb
from hashlib import md5

class Jspage(object):

    def __init__(self):
        self.driver = webdriver.PhantomJS("/usr/local/bin/phantomjs")
        self.start_url = "http://36kr.com"
        self.db = MySQLdb.connect(host='121.40.56.198',user='zhucloud',passwd='DcABxPQuGhyesqe2',db='vcsmarttest',charset='utf8')

    def indexList(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        try:
            index_page = self.getHtml(self.start_url)
            links = []
            for item in index_page.xpath('//ul[@class="feed_ul"]/li'):
                href = item.xpath('div/a/@href')
                img = item.xpath('div/a/div[@class="img_box"]/div/img/@data-src')
                title = item.xpath('div/a/div[@class="intro"]/h3/text()')
                type_name = item.xpath('div/span/text()')
                if len(href)>0:
                    type_id=0
                    recom=0
                    if type_name:
                        if type_name[0]==u'早期项目':
                            type_id=1
                            recom=1
                    link = {"href":self.start_url+href[0],"img":img[0],"title":title[0],"type_id":type_id,"recom":recom}
                    links.append(link)
            if len(links)>0:
                for row in links:
                    content=''
                    detail = self.getHtml(row['href'], 1)
                    publish_time = int(time.time())
                    md5id = md5(row['title']).hexdigest()
                    
                    m1 = re.search(r'<section\s+class="headimg">[\s\S]*?</section>', detail)
                    m2 = re.search(r'<section\s+class="textblock">[\s\S]*?</section>', detail)
                    if m1:
                        content+=m1.group(0)
                    if m2:
                        content+=m2.group(0)
                    content1 = re.sub('=""=""','',content)
                    content2 = re.sub('data-src','src',content1)
                    tags = re.findall(r'<a\s+class="kr-tag-gray".*?>([\s\S]*?)</a>',detail)
                    cur = self.db.cursor()
                    cur.execute('select id from zt_news where uuid=%s',(md5id,))
                    result = cur.fetchone()
                    if result:
                        print 'news has exist!'
                    else:
                        #print 'insert one'
                        cur.execute('insert into zt_news(article_title, article_thumbnail, article_url, article_content, source, article_publish_time,is_promote,type_id, create_time, uuid) values '
                           '(%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)',(row['title'], row['img'], row['href'], content2, '36氪',publish_time,row['recom'],row['type_id'], publish_time, md5id))
                        #self.db.commit()
                        cur.execute('select id from zt_news where uuid=%s',(md5id,))

                        new_row = cur.fetchone()
                        #print new_row
                        tag_len = len(tags)
                        #tag_len = 0
                        if tag_len>0:
                            itags = []
                            for tag in tags:
                                cur.execute('select id from dict_tag where tag_name=%s',(tag,))
                                dtag = cur.fetchone()

                                if dtag==None:
                                    cur.execute('insert into dict_tag(tag_name, create_time) values (%s, %s)',
                                           (tag, time.time()))
                                    itags.append(tag)
                                else:
                                    cur.execute('insert into zt_news_tag(tag_id, news_id, create_time) values (%s, %s, %s)',
                                           (dtag[0], new_row[0], time.time()))
                            if(len(itags)>0):
                                for tag in itags:
                                    cur.execute('select id from dict_tag where tag_name=%s',(tag,))
                                    ctag = cur.fetchone()
                                    cur.execute('insert into zt_news_tag(tag_id, news_id, create_time) values (%s, %s, %s)',
                                          (ctag[0], new_row[0], time.time()))
            self.db.commit()
        except Exception,e:
            print Exception,e
        finally:    
            self.db.close()
            self.driver.quit()
                    
    def getHtml(self, href, source=0):
        try:
            self.driver.get(href)
            data = self.driver.page_source
            if source==0:
                data = etree.HTML(data)
            return data
        except:
            pass
            
        
        

js = Jspage()

js.indexList()
