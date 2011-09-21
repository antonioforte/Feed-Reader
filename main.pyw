#!/usr/bin/env python
from xml.etree import ElementTree as ET
import htmlentitydefs
import threading
import subprocess
import sqlite3
import sys
import os
import time

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4 import QtNetwork

import lib.common
import lib.templates
import lib.myconfig
import lib.getfeeds
import lib.publishfeeds


class getCategoryPage(QtCore.QObject):
    
    @QtCore.pyqtSlot(str)
    def go(self,category):
        print ('getCategoryPage.go')
        html = self.templates.Page(self.curdir, str(category))
        self.web.setHtml(html)
        wrapper = self.main_frame.findFirstElement("div#category_page_wrapper")

        cats = self.config_xml.findall('category')
        for cat in cats:
            cat_id = cat.attrib['id']
            if cat_id == category:
                
                feeds = cat.findall('feed')
                for feed in feeds:
                    feed_name = feed.attrib['name']
                    feed_url = feed.attrib['url']
                    
                    div = self.get_gui_html(cat_id, feed_name, feed_url)
                    wrapper.appendInside(ET.tostring(div))  
        self.apply_js_events()


    def get_gui_html(self, cat_id, feed_name, feed_url):
        div = ET.Element('div', {'class':'feed_wrapper'})
        span = ET.SubElement(div, 'span', {'class':'feed_title'})
        span.text = feed_name
        
        btn_getweb = ET.SubElement(div, 'button')
        btn_getweb.text = '::'
        btn_getweb.attrib['data-feed_cat'] = cat_id
        btn_getweb.attrib['data-feed_url'] = feed_url
        btn_getweb.attrib['data-feed_name'] = feed_name
        btn_getweb.attrib['data-mode'] = 'get_web_feed'
        
        btn_getdb = ET.SubElement(div, 'button')
        btn_getdb.text = '::'
        btn_getdb.attrib['data-feed_cat'] = cat_id
        btn_getdb.attrib['data-feed_url'] = feed_url
        btn_getdb.attrib['data-feed_name'] = feed_name
        btn_getdb.attrib['data-mode'] = 'get_db_feed'
        
        btn_viewtopics = ET.SubElement(div, 'button', {'class':'feed_view'})
        btn_viewtopics.text = '::'
        btn_viewtopics.attrib['data-mode'] = 'view_feed'
        
        feed_status = ET.SubElement(div, 'button', {'class':'feed_status'})
        feed_status.text = ''
        return div
    

    def apply_js_events(self):
        btns = self.main_frame.findAllElements("button").toList()
        for btn in btns:
            btn.evaluateJavaScript('''
                this.addEventListener("click", 
                    function(evt) { 
                        var name = this.getAttribute('data-feed_name');
                        var url = this.getAttribute('data-feed_url');
                        var cat = this.getAttribute('data-feed_cat');
                        var mode = this.getAttribute('data-mode');
                        if (mode == 'get_web_feed'){getwebfeeds.go(name,url,cat,mode);}
                        if (mode == 'get_db_feed'){getdbfeeds.go(name,url,cat,mode);}
                        if (mode == 'view_feed'){
                           var els = dom_wrpGetElementsOfClass(this.parentNode,'topic_wrapper');
                            for(var e = 0; e < els.length; e++){
                                dom_showHideEl(els[e]);
                            }
                        }
                    }, false);''')
                    

    def set_values(self,config_xml,web,curdir):
        self.config_xml = config_xml
        self.web = web
        self.main_frame = web.page().mainFrame()
        self.curdir = curdir
        self.lib = lib.common.common() 
        self.templates = lib.templates.templates()
        
        
        
class openBrowser(QtCore.QObject):
    @QtCore.pyqtSlot(str)
    def go(self,url):
        print('openBrowser : ',url)
        try:
            retval = subprocess.Popen(['firefox',url])
        except Exception as e:
            print ("Error could not open browser : ",e) 




class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        
        self.lib = lib.common.common() 
        self.curdir = self.getMainDir()
        self.config_xml = self.lib.getXml(os.path.join(self.curdir, 'config.xml'))
        
        self.templates = lib.templates.templates()
        self.myconfig = lib.myconfig.MyConfig()
        
        self.getwebfeeds = lib.getfeeds.getFeeds()
        self.getwebfeeds.set_values(self.curdir)
        
        self.getdbfeeds = lib.publishfeeds.publishFeeds()
        self.getdbfeeds.set_values(self.curdir)
        
        self.get_category_page = getCategoryPage()
        self.open_browser = openBrowser()
        self.theinit()


    def get_starting_html(self):
        cats = []
        try:
            cats = self.config_xml.findall('category')
        except Exception as e:
            print ("Error could not feeds categories: ", e)
        
        self.get_category_page.set_values(
            self.config_xml,self.web,self.curdir)
        
        frame = self.web.page().mainFrame()
        document = frame.documentElement()
        index_wrapper = document.findFirst("div#indexWrapper")
        for cat in cats:
            cat_id = cat.attrib['id']
            div = ET.Element('div')
            div.text = cat_id
            div.attrib['onClick'] = "get_category_page.go('"+cat_id+"')"
            index_wrapper.appendInside(ET.tostring(div))  




    def theinit(self):
        self.resize(1200, 700)
        self.setWindowTitle('Feed Reader')
        self.setWindowIcon(
            QtGui.QIcon(os.path.join(self.curdir,'res','app_icon.png')))

        start_page = os.path.join(self.curdir,'index.html')
        self.web = QtWebKit.QWebView(self)
        self.web.load(QtCore.QUrl(start_page))

        # dom inspector, plugins and javascript 
        self.web.page().settings().setAttribute(
            QtWebKit.QWebSettings.DeveloperExtrasEnabled, 7)
        self.web.settings().setAttribute(
            QtWebKit.QWebSettings.PluginsEnabled, False)

        self.setCentralWidget(self.web)
        self.web.show()
        self.center()
        self.connect_signals()
        


    def connect_signals(self):
        QtCore.QObject.connect(self.web, 
            QtCore.SIGNAL("loadFinished (bool)"), self.wb_load_end)
        QtCore.QObject.connect(self.web.page().mainFrame(), 
            QtCore.SIGNAL("javaScriptWindowObjectCleared ()"), self.jsCleared)
        self.connect(self, QtCore.SIGNAL('keyPressEvent()'), self.keyPressEvent)

        # getwebfeeds signals
        self.connect(self.getwebfeeds, QtCore.SIGNAL(
            "thread_getwebfeeds(QString)"), self.thread_getwebfeeds)
        self.connect(self.getwebfeeds, QtCore.SIGNAL(
            "thread_getwebfeeds_start(QString)"), self.thread_getwebfeeds_start)
        
        # getdbfeeds
        self.connect(self.getdbfeeds, QtCore.SIGNAL(
            "thread_getdbfeeds(QString,QString)"), self.thread_getdbfeeds)
        self.connect(self.getdbfeeds, QtCore.SIGNAL(
            "thread_getdbfeeds_start(QString)"), self.thread_getdbfeeds_start)




    def thread_getdbfeeds(self, feed_name,html):
        frame = self.web.page().mainFrame()
        document = frame.documentElement()
        feeds_wrappers = document.findAll("div.feed_wrapper").toList()
        
        for feed_wrapper in feeds_wrappers:
            feed_wrapper_name = feed_wrapper.findFirst('span.feed_title').toPlainText()
            if feed_wrapper_name == feed_name:
                
                # remove existing topics
                has_topics = feed_wrapper.findAll('div.topic_wrapper').toList()
                for topic in has_topics:topic.removeFromDocument()
                
                # append topics
                html2 = self.fix_tags_html(html)
                feed_wrapper.appendInside(html2)
                
                # topic_wrappers show contents when clicked
                span_show_descs = feed_wrapper.findAll("span.span_show_desc").toList()
                for span_show_desc in span_show_descs:
                    span_show_desc.evaluateJavaScript('''
                        this.addEventListener("click", 
                            function(evt) { 
                               var topic_wrapper = this.parentNode.parentNode;
                               var topic_wrapper_childs = topic_wrapper.childNodes;
                               
                                for(var e = 0; e < topic_wrapper_childs.length; e++){
                                    if (topic_wrapper_childs[e].className != 'topic_title'){
                                        dom_showHideEl(topic_wrapper_childs[e]);
                                    }
                                }
                            }, false);''')
                
                # remove html tags from topic description
                desc_wrappers = feed_wrapper.findAll("span.topic_desc").toList()
                for desc_wrapper in desc_wrappers:
                    plain_text = desc_wrapper.toPlainText()
                    desc_wrapper.setPlainText(plain_text)
                    
                status = feed_wrapper.findFirst('button.feed_status')
                status.setPlainText('end db feed')



    def thread_getdbfeeds_start(self,feed_name):
        self.threads_post_text(feed_name,'start db feed')

    def thread_getwebfeeds(self, feed_name):
        self.threads_post_text(feed_name,'end web feed')

    def thread_getwebfeeds_start(self,feed_name):
        self.threads_post_text(feed_name,'start web feed')

    def threads_post_text(self,feed_name,text):
        frame = self.web.page().mainFrame()
        document = frame.documentElement()
        feeds_wrappers = document.findAll("div#category_page_wrapper div").toList()
        
        for feed_wrapper in feeds_wrappers:
            feed_wrapper_name = feed_wrapper.findFirst('span').toPlainText()
            if feed_wrapper_name == feed_name:
                status = feed_wrapper.findFirst('button.feed_status')
                status.setPlainText(text)



    def fix_tags_html(self,html):
        '''This function takes a string that has html with symbols represented by
        their html entities and replaces them with the symbols to form valid
        html.
        '''
        g = htmlentitydefs.entitydefs.keys()
        for ent in g:
            fent = '&'+ent+';'
            if ent in html:
                symbol = htmlentitydefs.entitydefs[ent]
                html.replace(fent,symbol)
        return html
        
        
        
    def wb_load_end(self):
        title = self.web.title()
        if title == 'Hall':
            self.get_starting_html()



    def jsCleared(self):
        frame = self.web.page().mainFrame()
        frame.addToJavaScriptWindowObject("getdbfeeds",self.getdbfeeds)
        frame.addToJavaScriptWindowObject("getwebfeeds",self.getwebfeeds)
        frame.addToJavaScriptWindowObject("get_category_page",self.get_category_page)
        frame.addToJavaScriptWindowObject("open_browser",self.open_browser)

   
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, 
                  (screen.height() - size.height()) / 2)
        
        
        
    def keyPressEvent(self, event):
        #print ("keyPressEvent : ",event.key())
        if event.key() == QtCore.Qt.Key_X:
            self.showFullScreen()
        if event.key() == QtCore.Qt.Key_C:
            self.showNormal()
        if event.key() == QtCore.Qt.Key_U:
               self.web.setZoomFactor(1.5)
        if event.key() == QtCore.Qt.Key_I:
               self.web.setZoomFactor(1)
        if event.key() == QtCore.Qt.Key_O:
               self.web.setZoomFactor(0.8)
               
               
               
    def about(self):
        info = "theBrowser"
        QtGui.QMessageBox.information(self, "Information", info)

        
        
    def getMainDir(self):
        '''Get script or exe directory.'''
        if hasattr(sys, 'frozen'): #py2exe, cx_freeze
            app_path = os.path.dirname(sys.executable)
            print ('Executing exe', app_path)
        elif __file__: #source file          
            app_path = os.path.abspath(os.path.dirname(__file__))
            print ('Executing source file', app_path)
        return app_path 
       
       

       
       
       
if __name__ == "__main__":
    '''Get script or exe directory.'''
    app_path = ''
    if hasattr(sys, 'frozen'): #py2exe, cx_freeze
        app_path = os.path.dirname(sys.executable)
    elif __file__: #source file
        app_path = os.path.dirname(__file__)
    
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Feed Reader")
    splash_pix = QtGui.QPixmap(os.path.join(app_path,'res','splash.png'))
    splash = QtGui.QSplashScreen(splash_pix)
    splash.setMask(splash_pix.mask())
    splash.show()

    #time.sleep(2)

    main = MainWindow()
    splash.finish(main)
    main.show()

    sys.exit(app.exec_())




        




