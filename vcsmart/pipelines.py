# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import time
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
import sys

class LieyunPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool
        reload(sys)
        sys.setdefaultencoding('utf-8')
    @classmethod
    def from_settings(cls, settings):
        dbparams=dict(
            host=settings['MYSQL_HOST'],#读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',#编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams)#**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)
    
    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self._conditional_insert,item)#调用插入的方法
        query.addErrback(self._handle_error,item)#调用异常处理方法
        return item

    def _conditional_insert(self, tx, item):
        #print item['publish_time']
        md5id = md5(item['title']).hexdigest()
        tx.execute('select uuid from zt_news where uuid=%s',(md5id,))
        result = tx.fetchone()
        publish_time = time.time()
        if result:
            pass
            #print item['title']+'has exist'
        else:
            #print item['title']+'had inserted'
            if item['content']:
                industry_id = item['industry_id'] if 'industry_id' in item.keys() else 0
                type_id = item['type_id'] if 'type_id' in item.keys() else 0
                is_promote = item['is_promote'] if 'is_promote' in item.keys() else 0
                tx.execute('insert into zt_news(article_title, article_thumbnail, article_url, article_content, source, industry_id, type_id, is_promote, article_publish_time, create_time, uuid) values '
                       '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(item['title'], item['img'], item['url'], item['content'], item['source'], industry_id, type_id, is_promote, publish_time, publish_time, md5id))
                tx.execute('select id from zt_news where uuid=%s',(md5id,))
                new_row = tx.fetchone()
                tag_len = len(item['tags'])
            
                if tag_len>0:
                    itags = []
                    for tag in item['tags']:
                        tx.execute('select id from dict_tag where tag_name=%s',(tag,))
                        dtag = tx.fetchone()
                        if dtag==None:
                            tx.execute('insert into dict_tag(tag_name, create_time) values (%s, %s)',
                                   (tag, time.time()))
                            itags.append(tag)
                        else:
                            tx.execute('insert into zt_news_tag(tag_id, news_id, create_time) values (%s, %s, %s)',
                                   (dtag['id'], new_row['id'], time.time()))
                    if(len(itags)>0):
                        for tag in itags:
                            tx.execute('select id from dict_tag where tag_name=%s',(tag,))
                            ctag = tx.fetchone()
                            tx.execute('insert into zt_news_tag(tag_id, news_id, create_time) values (%s, %s, %s)',
                                   (ctag['id'], new_row['id'], time.time()))

                        
    def _handle_error(self, error, item):
        print error
