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
        self.get_db_feed()
            

    def get_db_feed(self):
        _name = self.query_info['feed_name']
        _category = self.query_info['feed_category']

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        t = [_name,_category]
        c.execute('select * from feeds where feed_name=? and category=?', (t)) 

        html = ''
        for row in c:
            _title = row[0]
            _link = row[1]
            _description = row[2]
            _date = row[3]

            div = ET.Element('div',
                {'class':'topic_wrapper'})
            
            div_title = ET.SubElement(div,'div',
                {'class':'topic_title'})
            div_title.text = _title
            
            span_show_desc = ET.SubElement(div_title,'span',
                {'class':'span_show_desc'})
            span_show_desc.text = '&crarr;' 
            
            span_desc = ET.SubElement(div,'span',
                {'class':'topic_desc'})
            span_desc.text = _description
            
            a_link = ET.SubElement(div,'a',
                {'href':_link,'class':'topic_link'})
            a_link.text = 'go'
            
            span_out_link = ET.SubElement(div,'span',
                {'data-url':_link, 
                 'class':'topic_link_out',
                 'onClick':"open_browser.go('"+_link+"')"})
            span_out_link.text = 'go2'

            span_date = ET.SubElement(div,'span',
                {'class':'topic_date'})
            span_date.text = _date

            html += ET.tostring(div)
        self.emit(QtCore.SIGNAL("postResultsThread(QString,QString)"), _name, html)

            
            
class publishFeeds(QtCore.QObject):

    @QtCore.pyqtSlot(str,str,str,str)
    def go(self,name,url,cat,mode):
        self.query_info = {'feed_name':str(name),
                                'feed_url':str(url),
                                'feed_category':str(cat)}

        self.thread = Worker()
        self.thread.set_values(self.query_info,self.curdir)
        self.connect(self.thread, QtCore.SIGNAL("started()"), self.say_start)
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.say_end)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.say_end)
        self.connect(self.thread, QtCore.SIGNAL("postResultsThread(QString,QString)"),self.post_html)
        self.thread.start()

    def set_values(self,curdir):
        self.curdir = curdir

    def say_end(self):
        print ('get_db_feeds has ended')
        
    def say_start(self):
        print ('get_db_feeds has ended')
        self.emit(QtCore.SIGNAL("thread_getdbfeeds_start(QString)"),self.query_info['feed_name'])
        
    def post_html(self,feed_name,html):
        print ('get_db_feeds : post_html')
        self.emit(QtCore.SIGNAL("thread_getdbfeeds(QString,QString)"),feed_name,html)
        
        

        
        
        
        
        
        
