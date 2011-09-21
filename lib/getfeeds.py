import os
from xml.etree import ElementTree as ET
import templates
import common
import sqlite3
from PyQt4 import QtCore
import feedparser



class Worker(QtCore.QThread):
    
    
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.lib = common.common() 
        self.templates = templates.templates()


    def __del__(self):
        self.exiting = True


    def set_values(self,query_info,curdir):
        self.query_info = query_info
        self.curdir = curdir
        self.config_xml = self.lib.getXml(os.path.join(self.curdir,'config.xml'))
        self.db_path = os.path.join(self.curdir,'res','data.db')

        
    def run(self):
        self.get_web_feed()

 
    def get_web_feed(self): 
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        self.create_table_feeds(c)

        feed = self.parse_feed(self.query_info['feed_url'])
        _name = self.query_info['feed_name']
        _category = self.query_info['feed_category']

        if len(feed['entries']) > 0:
            self.delete_rows(_name,_category,c)

        for entry in feed['entries']:
            _title = entry.title
            _link = entry.link
            _description = entry.description
            _date = entry.date

            t = [_title,_link,_description,_date,_category,_name]
            try:
                c.execute('insert into feeds values (?,?,?,?,?,?)', t)
            except Exception as e:
                print ('Could not insert feed titles : ', e)
                
        conn.commit()
        c.close()




    def create_table_feeds(self, c):
        try:
            c.execute('''
        CREATE TABLE feeds  
        (title text,
        link text,
        description text,
        date text,
        category text,
        feed_name text
        )''')
        except Exception as e:
            print ('Table feeds already exists : ', e)


    def delete_rows(self,_name,_category,c):
        t = [_name,_category]
        c.execute('delete from feeds where feed_name=? and category=?', (t)) 


    def parse_feed(self,url):
        d = feedparser.parse(url)
        return d
        
            
            
class getFeeds(QtCore.QObject):

    @QtCore.pyqtSlot(str,str,str,str)
    def go(self,name,url,cat,mode):
        self.query_info = {'feed_name':str(name),
                                'feed_url':str(url),
                                'feed_category':str(cat),
                                'mode':str(mode) }

        self.thread = Worker()
        self.thread.set_values(self.query_info,self.curdir)
        self.connect(self.thread, QtCore.SIGNAL("started()"), self.say_start)
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.say_end)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.say_end)
        self.thread.start()

    def set_values(self,curdir):
        self.curdir = curdir

    def say_end(self):
        print ('get_web_feeds has ended')
        self.emit(QtCore.SIGNAL("thread_getwebfeeds(QString)"),self.query_info['feed_name'])
        
    def say_start(self):
        print ('get_web_feeds has started')
        self.emit(QtCore.SIGNAL("thread_getwebfeeds_start(QString)"),self.query_info['feed_name'])
        

        
        
        
        
        
        
