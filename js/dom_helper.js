/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/

function dom_deleteAllChildNodes(holder){
    while(holder.hasChildNodes()){
        holder.removeChild(holder.lastChild);
    }
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/

function dom_HideElementsOfClass(targetClass){
    var s = dom_getElementsOfClass(targetClass);
    for(var e = 0; e < s.length; e++){
            s[e].style.display = 'none';
        }
}
/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/

function dom_showHideEl(el){
    if (el.style.display != 'block'){
        el.style.display = 'block';
    }else{
        el.style.display = 'none';
    }
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/

function dom_wrpGetElementsOfClass(container,targetClass){

    var matchingEls = [];
    var els = container.getElementsByTagName('*');
    for(var e = 0; e < els.length; e++){
    
        if (els[e].className == targetClass){
            matchingEls.push(els[e]);
        }  
        
    }
    return matchingEls;
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/

function dom_getElementsOfClass(targetClass){

    var matchingEls = [];
    var els = document.getElementsByTagName('*');
    for(var e = 0; e < els.length; e++){
        if (els[e].className == targetClass){
            matchingEls.push(els[e]);
        }   
    }
    return matchingEls;
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/

function dom_addPageHeader() {
    var headerDiv = document.createElement("div");
    headerDiv.setAttribute('id', 'pageHeader');
    // insert as body first node
    document.body.insertBefore(headerDiv, document.body.childNodes[0]);
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/

function dom_addDocumentTitleDiv() {
    var docDiv = document.createElement("div");
    docDiv.setAttribute('id', 'docDiv');
    
    var docTitle = document.title;
    var docText = document.createTextNode(docTitle);
    docDiv.appendChild(docText);
    
    document.body.appendChild(docDiv);
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/

function dom_onDomReady(function_name){
      document.addEventListener("DOMContentLoaded", function_name, false);
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/

function dom_addEventListener(target, eventType, eventFunction){  
    if(target.addEventListener){
        target.addEventListener(eventType,eventFunction,false);
    }else if(target.attachEvent){
        target.attachEvent("on"+eventType,eventFunction);
    }else{
        alert("Could not attach event");
    }  
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/

function dom_getEvtObj(event){  
    var theObj = 'not';
    if(event.target){var theObj = event.target;}
    if(event.srcElement){var theObj = event.srcElement;} 
    return theObj;
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/

function dom_getBrowserWindow() {

    /* http://www.howtocreate.co.uk/tutorials/javascript/browserwindow */

    var myWidth = 0, myHeight = 0;
    if( typeof( window.innerWidth ) == 'number' ) {
        //Non-IE
        myWidth = window.innerWidth;
        myHeight = window.innerHeight;
    } else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
        //IE 6+ in 'standards compliant mode'
        myWidth = document.documentElement.clientWidth;
        myHeight = document.documentElement.clientHeight;
    } else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
        //IE 4 compatible
        myWidth = document.body.clientWidth;
        myHeight = document.body.clientHeight;
    }

    var o = [myWidth,myHeight];
    return o;
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/


