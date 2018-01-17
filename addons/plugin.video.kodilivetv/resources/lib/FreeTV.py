# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import base64 
import urllib2,urllib,cgi, re, sys, platform

addon_id = 'plugin.video.kodilivetv'
selfAddon = xbmcaddon.Addon(id=addon_id)

try:
    import json
except:
    import simplejson as json

def tryplay(url,listitem, keepactive=False, aliveobject=None , pdialogue=None):    
    import CustomPlayer,time

    localobject=aliveobject
    player = CustomPlayer.MyXBMCPlayer()
    player.pdialogue=pdialogue
    start = time.time() 
    #xbmc.Player().play( liveLink,listitem)
    player.play( url, listitem)
    xbmc.sleep(1000)
    while player.is_active:
        xbmc.sleep(200)
        if player.urlplayed and not keepactive:
            print 'yes played'
            return True
        xbmc.sleep(1000)
    
    try:
        if localobject: localobject.close()
    except: pass
    print 'not played',url
    return False

def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None,jsonpost=False):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)
    if jsonpost:
        req.add_header('Content-Type', 'application/json')
    response = opener.open(req,post,timeout=timeout)
    if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            link = f.read()
    else:
        link=response.read()
    response.close()
    return link;


def PlayOtherUrl ( url,name ):

    url=base64.b64decode(url)

    if url.startswith('cid:'): url=base64.b64decode('aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwLzJfNS9neG1sL3BsYXkvJXM=')%url.replace('cid:','')
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    url = url.split('safe:')[1]
    
    import websocket, traceback
    ws = websocket.WebSocket()

    try:
        useragent=''
        headers = [('Referer', base64.b64decode('aHR0cDovL29ubGluZWRlbW8uc2FmZXJzdXJmLmNvbS9vbmxpbmV0di1saXZlZGVtby5odG1s')),('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
        import time
        od= base64.b64decode('aHR0cDovL29ubGluZWRlbW8uc2FmZXJzdXJmLmNvbS8=')
        mainhtml=getUrl(od,headers=headers)
        
        js=urllib.unquote(re.findall("StartScriptSpeedTest\(unescape\('(.*?)'",mainhtml)[0])
        speedhtml= urllib.unquote(re.findall("phpUrl = unescape\('(.*?)'",mainhtml)[0])
        
        servername,portnum=re.findall("\n\s*\{.*?url.*?:.*?['\"](.*?)?['\"].*?port.*?:(.*?)\}",mainhtml.split('man.AddServers')[1].split(']);')[0])[0]
        print servername,portnum
        if not js.startswith('http'):
            js=od+js
        header=[base64.b64decode("T3JpZ2luOiBodHRwOi8vb25saW5lZGVtby5zYWZlcnN1cmYuY29t"),"User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"]
        #wsfirst.connect(base64.b64decode("d3M6Ly81Mi40OC44Ni4xMzU6MTMzOC90Yi9tM3U4L21hc3Rlci9zaXRlaWQvY3VzdG9tZXIub25saW5ldHYudjM="),header=header)
        #wsfirst.recv() 
        ws.connect(base64.b64decode("d3M6Ly8lczolcy90Yi9tM3U4L21hc3Rlci9zaXRlaWQvY3VzdG9tZXIub25saW5ldHYudjM=")%(servername,portnum),header=header)
        result = ws.recv() 

        headers = [('Referer', base64.b64decode('aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20=')),('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'),('Origin',base64.b64decode('WC1SZXF1ZXN0ZWQtV2l0aDogWE1MSHR0cFJlcXVlc3Q=')),('Cookie','jwplayer.captionLabel=Off'),
            ('Accept-Encoding','gzip, deflate, sdch'),('Accept-Language','en-US,en;q=0.8')]

        import time
        print 'js',js
        st= time.time()
        getUrl(js+'?dt='+ str(int(time.time()*1000)),headers=headers)
        totaltime=time.time()- st
        print totaltime
        testsize,kbps, kbRes, res =safeFinishedTest(totaltime)
        bpsurl=base64.b64decode("JXM/ZHRwPQ==")%speedhtml+ str(int(time.time()*1000))
        bpsdata=getUrl( bpsurl,headers=headers)
        bpsres, bpstime=re.findall("'bpsResultDiv'>(.*?)<.*?bpsTimeResultDiv'>(.*?)<",bpsdata)[0]
        lastval=selfAddon.getSetting( "safeplaylastcode" ) 
        if lastval=="": lastval=bpsres
        selfAddon.setSetting( "safeplaylastcode",bpsres)
        #bpsres,bpstime="", ""#lastval
        #if usecode: bpsres=usecode
        
        jsdata='[{"key":"type","value":"info"},{"key":"info","value":"speedtest"},{"key":"country","value":"France"},{"key":"language","value":"en"},{"key":"speedTestSize","value": "%s"},{"key":"kbPs","value":"%s"},{"key":"speedResKb","value":"%s"},{"key":"bpsResult","value":"%s"},{"key":"speedResTime","value":"%s"},{"key":"websocketSupport","value":"true"},{"key":"speedTestInTime","value":"true"},{"key":"bpsTimeResult","value":"%s"},{"key":"flash","value":"true"},{"key":"touchScreen","value":"false"},{"key":"rotationSupport","value":"false"},{"key":"pixelRatio","value":"1"},{"key":"width","value":"1366"},{"key":"height","value":"768"},{"key":"mobilePercent","value":"33"}]'%( testsize,str(kbps),kbRes , bpsres, res, bpstime,)
        ws.send(jsdata)
        
        #result = ws.recv()   
        #xbmc.sleep(2000)
        jsdata='[{"key":"type","value":"channelrequest"},{"key":"dbid","value":"%s"},{"key":"tbid","value":""},{"key":"format","value":"masterm3u8"},{"key":"proxify","value":"true"},{"key":"bitrate","value":"1368000"},{"key":"maxbitrate","value":"3305000"}]'%url
        ws.send(jsdata)
        result = ws.recv()
        #result = ws.recv()
        print repr(result)

        headers = [('Referer', base64.b64decode('aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20vb25saW5ldHYuaHRtbA==')),('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'),('Origin',base64.b64decode('aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20='))]
        urlnew=re.findall('[\'"](http.*?)[\'"]',result)[0]
        result=getUrl(urlnew,headers=headers)
    except: 
        traceback.print_exc(file=sys.stdout)
    
    progress.update( 35, "", "Preparing url..", "" )
    
    urlToPlay=re.findall('(http.*?)\s',result)[-1]
    
    try:
        result2=getUrl(urlToPlay,headers=headers)
    except:
        traceback.print_exc(file=sys.stdout)
    
    #if recursive: 
    #    return urlnew
    
    import random
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    tryplay( urlnew+base64.b64decode('fE9yaWdpbj1odHRwOi8vY3VzdG9tZXIuc2FmZXJzdXJmLmNvbSZVc2VyLUFnZW50PU1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDYuMSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzUyLjAuMjc0My4xMTYgU2FmYXJpLzUzNy4zNiZSZWZlcmVyPWh0dHA6Ly9jdXN0b21lci5zYWZlcnN1cmYuY29tL29ubGluZXR2Lmh0bWw='), listitem, keepactive=True, aliveobject=ws, pdialogue=progress)

def safeFinishedTest(dur):
    import math
    res = "";
    kbMulti = 1
    if (dur > 5): #// 43 kb/s
        res = "GPRS"; 
    elif (dur > 2):# // 47 kb/s | onlinedemo : ~2.3s
        res = "2G"; 
        kbMulti = 2.6;
    elif (dur > 1.3):# // 89 kb/s | onlinedemo : ~1.3s
        res = "2G"; 
        kbMulti = 2.8;
    elif (dur > 0.7):# // 153 kb/s | onlinedemo : ~0.8s
        res = "3G"; 
        kbMulti = 3;
    elif (dur > 0.4):# // 358 kb/s | onlinedemo : ~0.45s
        res = "3G";
        kbMulti = 3;
    elif (dur > 0.3):# // 358 kb/s | onlinedemo : ~0.35s
        res = "DSL";
        kbMulti = 3.3;
    else:
        res = "4G"; 
        kbMulti = 4;
    kbps = (210 / dur) * 1.024 * kbMulti
    kbps = round(kbps * 100) / 100
    kbRes = "";
    if (kbps > 1500.0):
        kbRes = "4G";
    elif (kbps > 600.0):
        kbRes = "DSL";
    elif (kbps > 300.0):
        kbRes = "3G";
    elif (kbps > 100.0):
        kbRes = "2G";
    else:
        kbRes = "GPRS";
    
                
    return "210",kbps, kbRes, res 
     
