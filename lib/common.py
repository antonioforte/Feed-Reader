# -*- coding: utf-8 -*-
from xml.etree import ElementTree as ET
import Image
import ImageOps
import os
import pprint

class common:


    def printPretty(self,data):
        try:
            print('---------------------------------------------')
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(data)
            print('---------------------------------------------')
        except Exception as e:
            print ("Error could not printPretty: ", e)



    def getShortString(self,nC,theStr):
        strOut = ''
        if len(theStr) <= nC:
            strOut = theStr
        else:
            for c in range(0,nC):
                strOut += theStr[c]
            strOut += '...'
        return strOut


    def getXml(self,filename):
        try:
            tree = ET.parse(filename)
            return tree
        except Exception as e:
            print ("Error could not get xml file: ", e)
          
            
    def deleteFile(self,full_url):
        try:
            print ('Lib.common.deleteFile')
            if os.path.exists(full_url):
                os.remove(full_url)
        except Exception as e:
            print ("Error Lib.common.deleteFile : ", e)
          

    def getPicBase64(self,pic):
        src = 'not'
        if pic == 'race_season':
            src = "data:image/jpeg;base64,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"
        return src


    def walkDir(self,dir,exts):
        items = []
        try:
            for root,dirs,files in os.walk(unicode(dir)):
                for file in files:
                    full_url = os.path.join(dir,root,file)
                    url, ext = os.path.splitext(full_url)
                    if ext.lower() in exts:
                        items.append([full_url,ext,file])
        except Exception as e:
            print ("Error Lib.common.walkDir : ", e)
        return items
    

    def getFileDate(self,full_url):
        fileDate = 'not'
        try:
            fileDate = os.path.getmtime(full_url)
        except Exception as e:
            print ("Error Lib.common.getFileDate: ",e)
        return fileDate
    
 
    def getFileSize(self,full_url):
        fileSize = 0
        try:
            fileSize = os.path.getsize(full_url) /1024
        except Exception as e:
            print ("Error Lib.common.getFileSizeNew: ",e)
        return fileSize 
    

    def ET_getelbyid(self,xml,id):
        '''Iterate through all elements in xml
        to find the one with the specified id'''
        theel = 'not'
        for el in xml.getiterator():
            atrbs = el.items() # returns a list of pairs
            for pair in atrbs:
                if pair[0] == 'id' and pair[1] == id:
                    theel = el
        return theel 
    
            
    def createImgThumb(self,ori,dest,dims):
        try:
            w = int(dims[0])
            h = int(dims[1])
            im = Image.open(ori)  
            im.thumbnail([w,h], Image.ANTIALIAS)
            im.save(dest)
        except Exception as e:
            print ("Error Lib.common.createImgThumb: ",e)
            
            
    def createImgThumbFit(self,ori,dest,dims):
        try:
            w = int(dims[0])
            h = int(dims[1])
            im = Image.open(ori) 
             
            method = Image.ANTIALIAS
            bleed = 0
            centering = (0.5,0.5)
            e = ImageOps.fit(im,[w,h],method,bleed,centering)
            e.save(dest)
        except Exception as e:
            print ("Error Lib.common.createImgThumbFit: ",e)
             

    def getImgTagFolder(self,folder):
        f = 'no:default.png'    
        s = os.path.join(folder,'folder.jpg')
        z = os.path.join(folder,'folder.png')
        if os.path.exists(s):
            f = 'yes:folder.jpg'
        if os.path.exists(z):
            f = 'yes:folder.png'
        return f
         

    def createDirs(self,dir):
        if not os.path.exists(dir):
            try:
                os.makedirs(dir) 
            except Exception as e:
                print ("Error Lib.common.createDirs: ",e)
            


    def html_escape(self,text):
        # the chars 2 replace are quotes 
        # must put a \ before the quotes
        text = unicode(text)
        r = ["'",'"'] 
        for item in r:
            if item in text:
                text = text.replace(item,'\\'+item)
        return text
    

    def getEventClickString(self,curdir,label,galItem,mode):
        # assemble js function call string
        # to be applied to html element  
        f = "queryDB.go('arg1','arg2','arg3','arg4')"
        f = f.replace('arg1',curdir)
        f = f.replace('arg2',self.html_escape(label))    
        f = f.replace('arg3',self.html_escape(galItem))
        f = f.replace('arg4',mode)
        return f
            
            
            
# This is here because there are issues
# with the parameters in the js functions
# containing characters not allowed. 
            
#    def html_escape(self,text):
#        text = unicode(text)
#        html_escape_table = {
#                            "&": "&amp;",
#                            '"': "&quot;",
#                            "'": "&apos;",
#                            ">": "&gt;",
#                            "<": "&lt;"
#                            }
#        """Produce entities within text."""
#        return "".join(html_escape_table.get(c,c) for c in text)    
            
#    def getEventClickString(self,curdir,label,galItem,mode):
#        f = "Image_Gallery.go('arg1','arg2','arg3','arg4')"
#        f = f.replace('arg1',curdir)
#        f = f.replace('arg2',label)    
#        f = f.replace('arg3',galItem)
#        f = f.replace('arg4',mode)
#        return f
    
        
#    def getEventClickString(self,curdir,label,galItem,mode):
#        f = "Image_Gallery.go('1','2','3','4')"
#        f = f.replace('1',curdir)
#        f = f.replace('2',self.html_escape(str(label)))    
#        f = f.replace('3',self.html_escape(str(galItem)))
#        f = f.replace('4',mode)
#        return f    
            
            
            
            
            
            