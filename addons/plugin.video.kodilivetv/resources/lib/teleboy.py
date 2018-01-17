
import os, re, sys, base64
import cookielib, urllib, urllib2
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import simplejson
# Forked by Vania
__author__     = "Andreas Wetzel"
__copyright__  = "Copyright 2011-2015, mindmade.org"
__credits__    = [ "Roman Haefeli", "Francois Marbot" ]
__maintainer__ = "Andreas Wetzel"
__email__      = "xbmc@mindmade.org"

#
# constants definition
############################################
PLUGINID = "plugin.video.kodilivetv"


MODE_RECORDINGS = 28
MODE_PLAY = 27
MODE_PLAY_RECORDING = 29
PARAMETER_KEY_MODE = "mode"
PARAMETER_KEY_STATION = "station"
PARAMETER_KEY_USERID = "userid"
PARAMETER_KEY_RECID  = "recid"

Addon = xbmcaddon.Addon(PLUGINID)
addonDir = Addon.getAddonInfo('path').decode("utf-8")
addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ), PLUGINID)

mindmade = os.path.join(addonDir, 'resources', 'lib', 'mindmade')
sys.path.insert(0, mindmade)
from mindmade import *

TB_URL = "https://www.teleboy.ch"
IMG_URL = "http://media.cinergy.ch"
API_URL = "http://tv.api.teleboy.ch"
API_KEY = base64.b64decode( "ZjBlN2JkZmI4MjJmYTg4YzBjN2ExM2Y3NTJhN2U4ZDVjMzc1N2ExM2Y3NTdhMTNmOWMwYzdhMTNmN2RmYjgyMg==")
COOKIE_FILE = xbmc.translatePath( "special://home/addons/" + PLUGINID + "/resources/cookie.dat")
REC_ICON = xbmc.translatePath( "special://home/addons/" + PLUGINID + "/resources/images/rec.png")

pluginhandle = int(sys.argv[1])
settings = xbmcaddon.Addon( id=PLUGINID)
cookies = cookielib.LWPCookieJar( COOKIE_FILE)

def ensure_login():
    global cookies
    opener = urllib2.build_opener( urllib2.HTTPCookieProcessor(cookies))
    urllib2.install_opener( opener)
    try:
        cookies.revert( ignore_discard=True)
        for c in cookies:
            if c.name == "cinergy_s":
                return True
    except IOError:
        pass
    cookies.clear()
    fetchHttp( TB_URL + "/login?target=https://www.teleboy.ch/")

    log( "logging in...")
    login = settings.getSetting( id="login")
    password = settings.getSetting( id="password")
    url = TB_URL + "/login_check"
    args = { "login": login,
             "password": password,
             "keep_login": "1" }

    reply = fetchHttp( url, args, post=True);
    
    if "Falsche Eingaben" in reply or "Anmeldung war nicht erfolgreich" in reply:
        log( "login failure")
        log( reply)
        notify( "Login Failure!", "Please set your login/password in the addon settings")
        xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=False)
        return False
    res = cookies.save( ignore_discard=True)

    log( "login ok")
    return True

def fetchHttpWithCookies( url, args={}, hdrs={}, post=False):
    if ensure_login():
        html = fetchHttp( url, args, hdrs, post)
        if "Bitte melde dich neu an" in html:
            os.unlink( xbmc.translatePath( COOKIE_FILE));
            if not ensure_login():
                return "";
            html = fetchHttp( url, args, hdrs, post)
        return html
    return ""

def get_stationLogoURL( station):
    return IMG_URL + "/t_station/" + station + "/icon320_dark.png"

def fetchApiJson( user_id, url, args={}):
    # get session key from cookie
    global cookies
    cookies.revert( ignore_discard=True)
    session_cookie = ""
    for c in cookies:
        if c.name == "cinergy_s":
            session_cookie = c.value
            break

    if (session_cookie == ""):
        notify( "Session cookie not found!", "Please set your login/password in the addon settings")
        return False

    hdrs = { "x-teleboy-apikey": API_KEY,
             "x-teleboy-session": session_cookie }
    url = API_URL + "/users/%s/" % user_id + url
    ans = fetchHttpWithCookies( url, args, hdrs)
    if ans:
        return simplejson.loads( ans)
    else:
        return False

def get_videoJson( user_id, sid):
    url = "stream/live/%s" % sid
    return fetchApiJson( user_id, url, {"alternative": "false"})

############
# TEMP
############
def parameters_string_to_dict( parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = urllib.unquote( paramSplits[1])
    return paramDict

def addDirectoryItem( name, params={}, image="", total=0, isFolder=False):
    '''Add a list item to the XBMC UI.'''
    img = "DefaultVideo.png"
    if image != "": img = image

    name = htmldecode( name)
    li = xbmcgui.ListItem( name, iconImage=img, thumbnailImage=image)
    li.addContextMenuItems( [ ('Refresh', 'Container.Refresh') ] , replaceItems=True)
    if not isFolder:
	    li.setProperty( "Video", "true")

    params_encoded = dict()
    for k in params.keys():
        params_encoded[k] = params[k]
    
    url = sys.argv[0] + '?url=teleboy&' + urllib.urlencode( params_encoded)
    xbmc.log( "ITEM URL --> " + url )
    xbmc.log( "ITEM IMG --> " + img )
    return xbmcplugin.addDirectoryItem(handle=pluginhandle, url=url, listitem=li, isFolder = isFolder, totalItems=total)
###########
# END TEMP
###########

def show_main(lg):
    html = fetchHttpWithCookies( TB_URL + "/cockpit/")
    # extract user id
    user_id = ""
    patron = '<h3>User ID</h3>[^<]+<p>(.*?)</p>'
    matches = re.compile(patron, re.DOTALL).findall(html)
    
    for scrapedid in matches:
        user_id = scrapedid
        
    addDirectoryItem( "[ Recordings ]", { PARAMETER_KEY_MODE: MODE_RECORDINGS, PARAMETER_KEY_USERID: user_id}, REC_ICON, isFolder = True)
    
    content = fetchApiJson( user_id, "broadcasts/now", { "expand": "flags,station,previewImage", "stream": True })
    print( repr(content))
    for item in content["data"]["items"]:
        channel = item["station"]["name"]
        station_id = str(item["station"]["id"])
        title   = item["title"]
        tstart  = item["begin"][11:16]
        tend    = item["end"][11:16]
        label   = channel + ": " + title + " (" + tstart + "-" + tend +")"
        img     = get_stationLogoURL( station_id)
  
        if lg == "it":
            it = [ 283, 54, 339, 53, 52, 281, 300, 344, 335, 137, 276, 329, 366, 271, 340, 282, 194 ]
            if item["station"]["id"] in it:
                label = htmldecode( label ).replace("MTV:","TV8:")
                if img.find("/137/") > 0:
                    img = "http://kodilive.eu/flag/tv8.png"
                addDirectoryItem( label, { PARAMETER_KEY_STATION: station_id, PARAMETER_KEY_MODE: MODE_PLAY, PARAMETER_KEY_USERID: user_id }, img)
        elif lg == "fr":
            fr = [ 196, 61, 147, 331, 305, 296, 297, 269, 321, 330, 365, 288, 308, 58, 312, 270, 80, 268, 342, 299 ]
            if item["station"]["id"] in fr:
                addDirectoryItem( label, { PARAMETER_KEY_STATION: station_id, PARAMETER_KEY_MODE: MODE_PLAY, PARAMETER_KEY_USERID: user_id }, img)
        elif lg == "de":
            de = [ 363, 364, 19, 85, 86, 334, 343, 280, 141, 70, 38, 175, 172, 154, 40, 358, 301, 336, 313, 298, 67, 360, 350, 351, 352, 353, 354, 317, 356, 314, 357, 359, 361, 348, 347, 304, 337, 338, 328, 326, 323, 341, 345, 311, 310, 84, 5, 121, 72, 20, 21, 22, 31, 35, 36, 145, 303, 306, 307, 274, 182, 309, 362, 279  ]
            if item["station"]["id"] in de:
                addDirectoryItem( label, { PARAMETER_KEY_STATION: station_id, PARAMETER_KEY_MODE: MODE_PLAY, PARAMETER_KEY_USERID: user_id }, img) 
        elif lg == "en":
            en = [ 50, 37, 332, 333, 346, 263, 262, 255, 192, 193, 195, 191, 189, 148, 101, 131, 177 ]
            if item["station"]["id"] in en:
                addDirectoryItem( label, { PARAMETER_KEY_STATION: station_id, PARAMETER_KEY_MODE: MODE_PLAY, PARAMETER_KEY_USERID: user_id }, img)
        else:
            addDirectoryItem( label, { PARAMETER_KEY_STATION: station_id, PARAMETER_KEY_MODE: MODE_PLAY, PARAMETER_KEY_USERID: user_id }, img)
            
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True)


def show_recordings( user_id):
    content = fetchApiJson( user_id, "records/ready", { "limit": 500, "skip": 0})

    for item in content["data"]["items"]:
    	starttime = item["begin"].split("+")[0][:-3].replace( "T", " ")
    	label = starttime + " " + item["title"]
    	if "label" in item.keys():
    		label = starttime + " " + item["label"] + ": " + item["title"]
    	recid = str(item["id"])
    	addDirectoryItem( label, { PARAMETER_KEY_MODE: MODE_PLAY_RECORDING,PARAMETER_KEY_USERID: user_id,PARAMETER_KEY_RECID: recid }, REC_ICON)

    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True)


def play_url( url, title, img=""):
    if img.find("/137/") > 0:
        img = "http://kodilive.eu/flag/tv8.png"
        
    li = xbmcgui.ListItem( title, iconImage=img, thumbnailImage=img)
    li.setProperty( "IsPlayable", "true")
    li.setProperty( "Video", "true")
    xbmc.Player().play( url, li)
    #xbmc.executebuiltin("XBMC.Container.Refresh()")

def play_url2( url, title, img=""):
    import subprocess, json
    if 'linux' in sys.platform or 'win32' in sys.platform:
        #xbmc.audioSuspend()
        ret = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method": "Settings.getSettingValue", "params": {"setting":"screensaver.mode" } }')
        jsn = json.loads(ret)
        saver_mode = jsn['result']['value']
        xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method":"Settings.setSettingValue", "params": {"setting":"screensaver.mode", "value":""} } ' )
        if 'linux' in sys.platform:
            VLC = os.path.join('/', 'usr', 'bin', 'vlc')
        else:
            from knownpaths import *
            PFx86 = get_path(FOLDERID.ProgramFilesX86).replace("C:\\","")
            log( "PFx86:" + PFx86 )
            PF = get_path(FOLDERID.ProgramFiles).replace("C:\\","")
            log( "PF:" + PF )
            VLC = os.path.join('C:\\', PFx86, 'VideoLAN', 'VLC', 'vlc.exe')
            if not os.path.isfile(VLC): VLC = os.path.join('C:\\', PF, 'VideoLAN', 'VLC', 'vlc.exe')

        if os.path.isfile(VLC):    
            subprocess.call([VLC , '--fullscreen', '--no-video-title-show', '--network-caching=0', '--input-title-format=' + title, url])
            xbmc.executebuiltin("XBMC.Container.Refresh()")
            xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method": "Settings.SetSettingValue", "params": {"setting":"screensaver.mode", "value": "'+saver_mode+'" } }') 
        else:
            xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method": "Settings.SetSettingValue", "params": {"setting":"screensaver.mode", "value": "'+saver_mode+'" } }') 
            play_url( url, title, img="")
        #xbmc.audioResume()
    else:
        play_url( url, title, img="")


def make_list(): #to make Teleboy m3u list
    
    html = fetchHttpWithCookies( TB_URL + "/cockpit/")
    user_id = ""
    patron = '<h3>User ID</h3>[^<]+<p>(.*?)</p>'
    matches = re.compile(patron, re.DOTALL).findall(html)
    
    for scrapedid in matches:
        user_id = scrapedid
        
    addDirectoryItem( "[ Recordings ]", { PARAMETER_KEY_MODE: MODE_RECORDINGS, PARAMETER_KEY_USERID: user_id}, REC_ICON, isFolder = True)
    
    content = fetchApiJson( user_id, "broadcasts/now", { "expand": "flags,station,previewImage", "stream": True })
    print( repr(content))
    dati = ""
    x = 0
    it = [ 283, 54, 339, 53, 52, 281, 300, 344, 335, 137, 276, 329, 366, 271, 340, 282, 194 ]
    fr = [ 196, 61, 147, 331, 305, 296, 297, 269, 321, 330, 365, 288, 308, 58, 312, 270, 80, 268, 342, 299 ]
    de = [ 363, 364, 19, 85, 86, 334, 343, 280, 141, 70, 38, 175, 172, 154, 40, 358, 301, 336, 313, 298, 67, 360, 350, 351, 352, 353, 354, 317, 356, 314, 357, 359, 361, 348, 347, 304, 337, 338, 328, 326, 323, 341, 345, 311, 310, 84, 5, 121, 72, 20, 21, 22, 31, 35, 36, 145, 303, 306, 307, 274, 182, 309, 362, 279  ]
    en = [ 50, 37, 332, 333, 346, 263, 262, 255, 192, 193, 195, 191, 189, 148, 101, 131, 177 ]
    
    All = it + fr + de + en
    fh = open("TB.m3u", "wb")
    
    for item in content["data"]["items"]:
        channel = item["station"]["name"]
        station_id = str(item["station"]["id"])
        title   = item["title"]
        url = ""
        
        x = x + 1
        if item["station"]["id"] in All:
            if x>0:
                json = get_videoJson( user_id, station_id)
                if json:
                    title = json["data"]["epg"]["current"]["title"]
                    url = json["data"]["stream"]["url"]
            
                if not url == "":
                    xbmc.sleep(1650)
                    item = '#EXTINF:-1,[COLOR FFFF00FF]' + channel  + '[/COLOR]' + '\r\n' + url + '\r\n'
                    
                    fh.write(item.encode('utf-8'))

    fh.close()    
        

