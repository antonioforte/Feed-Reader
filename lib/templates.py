

class templates:
    
    def Page(self,curdir,title):
        string = '''<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link href="file://'''+curdir+'''/style.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="file://''' + curdir + '''/js/dom_helper.js"></script>
<script type="text/javascript" src="file://''' + curdir + '''/js/common.js"></script>
<title>'''+title+'''</title>
</head>
<body>

<div id="goback">
    <a href="file://'''+curdir+'''/index.html">Home</a>
</div>

<div id="doc_div">'''+title+'''</div>

<div id="category_page_wrapper"></div>

</body></html>'''

        return string
    


