# -*- coding: utf-8 -*-
#code by Vania
import urllib2, urllib, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, shutil, time, zipfile, re, stat, xbmcvfs, base64

# Definizione variabili

AddonID = 'plugin.video.kodilivetv'
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')

addonDir = Addon.getAddonInfo('path')
addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ), AddonID)
pwdir = os.path.join(addon_data_dir, "password")
cdir = os.path.join(xbmc.translatePath("special://temp"),"files")

LOCAL_VERSION_FILE = os.path.join(os.path.join(addonDir), 'version.xml' )
REMOTE_VERSION_FILE = "https://kodilive.eu/repo/version.xml"

LOCAL_VERSION_FILE2 = os.path.join(os.path.join(addonDir), 'list.xml' )
REMOTE_VERSION_FILE2 = "https://kodilive.eu/update/list.xml"

libDir = os.path.join(addonDir, 'resources', 'lib')
f4mProxy = os.path.join(addonDir, 'f4mProxy')
chanDir = os.path.join(addonDir, 'resources', 'channels')
#XML_FILE  = os.path.join(libDir, 'advancedsettings.xml' )
#ACTIVESETTINGSFILE = os.path.join(xbmc.translatePath('special://profile'), 'advancedsettings.xml')
playlistsFile = os.path.join(addonDir, "playLists.txt")
Italian = os.path.join(addonDir, "italian.txt")
French = os.path.join(addonDir, "french.txt")
German = os.path.join(addonDir, "german.txt")
English = os.path.join(addonDir, "english.txt")
ydldir = os.path.join(xbmc.translatePath("special://home/addons/"),'script.module.youtube.dl')
streamtype = "HLS"

EXTL = [ '.m3u', '.m3u8', '.txt']
EXTV = [ '.mkv','.mp4','.avi','.ogv','.flv','.f4v','.wmv','.mpg','.mpeg','.3gp','.3g2','.webm','.ogg', '.part' ]
EXTA = [ '.mp3','.flac','.aac','.wav','.raw','.m4a','.wma','.f4a' ]

UAA = "Android / Chrome 40: Mozilla/5.0 (Linux; Android 5.1.1; Nexus 4 Build/LMY48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.89 Mobile Safari/537.36"

iconlist = "http://findicons.com/files/icons/1331/matrix_rebooted/128/text_clipping_file.png"
audio = "http://findicons.com/files/icons/1331/matrix_rebooted/128/music.png"
icondir = "http://findicons.com/files/icons/1331/matrix_rebooted/128/generic_folder_alt.png"
video = "http://findicons.com/files/icons/1331/matrix_rebooted/128/movies_2.png"
find = "https://kodilive.eu/icon/folder_search.png"

playlistsFile2 = os.path.join(addon_data_dir, "playLists.txt")
playlistsFile4 = os.path.join(addon_data_dir, "FolderLists.txt")
playlistsFile3 = os.path.join(addon_data_dir, "playLists.bkp")
playlistsFile5 = os.path.join(addon_data_dir, "FolderLists.bkp")

TVICO = os.path.join(addonDir, "resources", "images", "tv.png")
favoritesFile = os.path.join(addon_data_dir, 'favorites.txt')
SDownloader = "false"
#DFolder = os.path.join(addon_data_dir, 'download', '')

DF = xbmcaddon.Addon('plugin.video.kodilivetv').getSetting('download_path')
if not DF=='':  
    DFolder = DF
else:
    DFolder = os.path.join(addon_data_dir, 'download', '')

# Crezione cartelle

if not os.path.exists(addon_data_dir):
    os.makedirs(addon_data_dir)
if not os.path.exists(pwdir):
    os.makedirs(pwdir)	
if not os.path.exists(cdir):
    os.makedirs(cdir)
try:
    if not os.path.exists(DFolder):
        os.makedirs(DFolder)
except:
    pass

# Inizializzazione file favoriti

if not (os.path.isfile(favoritesFile)):
    f = open(favoritesFile, 'w') 
    f.write('[]') 
    f.close()

# Importo funzioni da common.py

sys.path.insert(0, libDir)
import common

# Funzioni gestione file

def zip_PM_data():
    import zipfile
    dialog = xbmcgui.Dialog()
    path = dialog.browse( int(3), localizedString(10124).encode('utf-8'), "myprograms", "", True )

    if not path == "":
        ZipFile = zipfile.ZipFile(os.path.join(path,"backup_pm.zip"), "w" )
        ZipFile.write(playlistsFile2, os.path.basename(playlistsFile2), compress_type=zipfile.ZIP_DEFLATED)
        ZipFile.write(playlistsFile4, os.path.basename(playlistsFile4), compress_type=zipfile.ZIP_DEFLATED)
        dirpath = os.path.join(addon_data_dir, 'password','')
        basedir = os.path.dirname(dirpath) + '/'
        for root, dirs, files in os.walk(dirpath):
            dirname = root.replace(basedir, '')
            for f in files:
                ZipFile.write(root + '/' + f,  'password/' + f)
        ZipFile.close()   
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("KLTV: " + "  "+ path + "backup_pm.zip",localizedString(10126).encode('utf-8'), 6500, icon))

def unzip_PM_data():
    import ziptools
    ZipFile = xbmcgui.Dialog().browse(int(1), localizedString(10122).encode('utf-8'), 'myprograms','.zip')
    if not ZipFile:
        return
    else:
        unzipper = ziptools.ziptools()
        unzipper.extract(os.path.join(xbmc.translatePath(ZipFile)),addon_data_dir)
        xbmc.sleep(450)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("KLTV: ",localizedString(10125).encode('utf-8'), 6500, icon))
        xbmc.sleep(850)
        xbmc.executebuiltin("XBMC.Container.Refresh()")

percent = 0

def DownloaderClass(url,dest):
    
    dp = xbmcgui.DialogProgress()
    dp.create("Kodi Live TV ZIP DOWNLOADER","Downloading File",url)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except: 
        percent = 100
        dp.update(percent)
        time.sleep(20)
        dp.close()
    if dp.iscanceled(): 
        dp.close()

def emptydir(top):
    
    if(top == '/' or top == "\\"): 
        return
    else:
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                if not bool('default.py' in name) and not bool('ziptools.py' in name):
                    os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name)) 
 
def clean_cache():

    for i in os.listdir(cdir):    
        rf = format(i)
        if not bool('.' in i):
            file = os.path.join( cdir , i )
            if os.path.isfile(file):
                os.remove(file)

    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ","m3u cache has been deleted!", 4500, icon))

def is_mp4(url):
    if url.find("openload.")>0 or url.find("pornhd.com")>0 or url.find("akvideo.")>0 or url.find("stream.moe")>0 or url.startswith("urlr://") or url.find("rapidvideo.")>0 or url.find("speedvideo.")>0 or url.find("fastvideo.")>0 or url.find("thevideo.me")>0 or url.find("wstream.")>0 or url.find("nowvideo.")>0 or url.find("streamango.")>0 or url.find("megadrive.")>0 or url.find("megahd.")>0 or url.find("vidto.me")>0:
        return True
    else:
        return False
##############################
# Inizia creazione pagine
    
def Categories():
    AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10250).encode('utf-8')), "search1" , 65, find, isFolder=True)
    AddDir("[COLOR ff74ff4a][B]{0}[/B][/COLOR]".format(localizedString(10106).encode('utf-8')), "update" ,46 ,os.path.join(addonDir, "resources", "images", "update.png"), isFolder=True)
    AddDir("[COLOR cyan][B][ {0} ][/B][/COLOR]".format(localizedString(10003).encode('utf-8')), "favorites" ,30 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"))
    AddDir("[COLOR blue][B]{0}[/B][/COLOR]".format(localizedString(10047).encode('utf-8')), "Manager" ,39 , os.path.join(addonDir, "resources", "images", "playlist.png"))
    AddDir("[COLOR violet][B]{0}[/B][/COLOR]".format(localizedString(10048).encode('utf-8')), "Channels" ,96 , os.path.join(addonDir, "resources", "images", "channels.png"))    
    
def Channels():    
    AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10250).encode('utf-8')), "search3" , 65, find, isFolder=True)
    AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(localizedString(10020).encode('utf-8')), "italian" ,35 , "https://kodilive.eu/flag/it.png")
    AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(localizedString(10021).encode('utf-8')), "french" ,36 , "https://kodilive.eu/flag/fr.png")
    AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(localizedString(10022).encode('utf-8')), "german" ,37 , "https://kodilive.eu/flag/de.png")
    AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(localizedString(10023).encode('utf-8')), "english" ,38 , "https://kodilive.eu/flag/uk.png")
    AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(localizedString(10028).encode('utf-8')), "mu.txt" ,2 , "https://kodilive.eu/flag/mu.png")
    AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(localizedString(10049).encode('utf-8')), "others" ,97 , os.path.join(addonDir, "resources", "images", "channels.png"))

def Others():    
    list = common.ReadList(playlistsFile)
    for item in list:
        mode = 2
        image = item.get('image', '')
        icon = image.encode("utf-8")
        name = localizedString(item["name"])
        cname = "[COLOR gold][B]{0}[/B][/COLOR]".format(name)
                            
        AddDir(cname ,item["url"], mode , icon)
    
    if xbmcaddon.Addon('plugin.video.kodilivetv').getSetting('XXX_section')=="true":
        AddDir("[COLOR red][B]Video XXX[/B][/COLOR]" ,"?l=pornazzi", 2 , "https://kodilive.eu/icon/XXX.png")
    
def importList():
    
    method = GetSourceLocation(localizedString(10120).encode('utf-8'), [localizedString(10122).encode('utf-8'), localizedString(10123).encode('utf-8')])
        
    if method == -1:
        return
    elif method == 0:
        listUrl = common.GetKeyboardText(localizedString(10005).encode('utf-8')).strip()
    else:
        listUrl = xbmcgui.Dialog().browse(int(1), localizedString(10006).encode('utf-8'), 'myprograms','.txt')
        if not listUrl:
            return
    if len(listUrl) < 1:
        return
 
    if common.check_url(listUrl):
        lista = common.OpenURL(listUrl)
    else:
        lista = common.ReadFile(listUrl)
 
    if os.path.isfile( playlistsFile3 ) : os.remove( playlistsFile3 )
    shutil.copyfile( playlistsFile2, playlistsFile3 )
    xbmc.sleep ( 500 )
    os.remove( playlistsFile2 )
    xbmc.sleep ( 500 )
    common.write_file( playlistsFile2, lista )
    xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ",localizedString(10124).encode('utf-8'), 3600, icon))    
  
def AddNewList():
	
    method1 = GetSourceLocation(localizedString(10001).encode('utf-8'), [localizedString(10040).encode('utf-8'), localizedString(10220).encode('utf-8'), localizedString(10042).encode('utf-8'), localizedString(10266).encode('utf-8')])
	
    if method1 == -1:
            return	
    elif method1 == 0:
        AddNewDir()
    elif method1 == 1:
        AddNewDir("xml")    
    elif method1 == 3:
        AddNewDir("pyt")
    else:
        listName = common.GetKeyboardText(localizedString(10004).encode('utf-8')).strip()
        if len(listName) < 1:
            return

        method = GetSourceLocation(localizedString(10002).encode('utf-8'), [localizedString(10016).encode('utf-8'), localizedString(10017).encode('utf-8')])	

        if method == -1:
            return
        elif method == 0:
            listUrl = common.GetKeyboardText(localizedString(10005).encode('utf-8')).strip()
        else:
            listUrl = xbmcgui.Dialog().browse(int(1), localizedString(10006).encode('utf-8'), 'myprograms','.m3u8|.m3u')
            if not listUrl:
                return
            
        if len(listUrl) < 1:
            return
        
        exists = ""
        list = common.ReadList(playlistsFile2)
        for item in list:
            if item["url"] == listUrl:
                exists = "yes"
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ",localizedString(10264).encode('utf-8'), 3600, icon))
                break       
        
        if exists == "":
            list.append({"name": listName, "url": listUrl})
            if common.SaveList(playlistsFile2, list):
                    xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
                    
def AddNewDir(loc = "l"):
    if loc == "xml":
        method = GetSourceLocation(localizedString(10221).encode('utf-8'), [localizedString(10222).encode('utf-8'), localizedString(10223).encode('utf-8')])
        
        if method == -1:
            return
        elif method == 0:
            listUrl = common.GetKeyboardText(localizedString(10224).encode('utf-8')).strip()
        else:
            listUrl = xbmcgui.Dialog().browse(int(1), localizedString(10225).encode('utf-8'), 'myprograms','.xml')
    elif loc == "pyt":
        listName = common.GetKeyboardText(localizedString(10265).encode('utf-8')).strip()
        listUrl = common.GetKeyboardText(localizedString(10226).encode('utf-8')).strip()
    else:
        if loc == "l":
            method2 = GetSourceLocation(localizedString(10040).encode('utf-8'), [localizedString(10260).encode('utf-8'), localizedString(10043).encode('utf-8'), localizedString(10261).encode('utf-8')] )
         
            if method2 == -1:
                return           
            elif method2 == 0:
                listName = common.GetKeyboardText(localizedString(10263).encode('utf-8')).strip()
                listUrl = xbmcgui.Dialog().browse(int(0), localizedString(10041).encode('utf-8'), 'myprograms')       
            elif method2 == 1:
                listName = common.GetKeyboardText(localizedString(10263).encode('utf-8')).strip()
                listUrl = xbmcgui.Dialog().browse(int(0), localizedString(10041).encode('utf-8'), 'files')
            else:
                listName = common.GetKeyboardText(localizedString(10263).encode('utf-8')).strip()
                listUrl = common.GetKeyboardText(localizedString(10262).encode('utf-8')).strip() 
               
	
    if not listUrl or len(listUrl) < 1:
            return

    list = common.ReadList(playlistsFile4)
    Url = ""
    pUrl = ""
    
    if listUrl.endswith(".xml") or loc == "xml":
        if common.check_url(listUrl):
            response = common.OpenURL(listUrl)
        else:
            response = common.ReadFile(listUrl)
            
        Url = common.find_single_match(response,"<url>([^<]+)</url>").strip()
        pUrl = common.find_single_match(response,"<web>([^<]+)</web>").strip()
        xUrl = common.find_single_match(response,"<xweb>([^<]+)</xweb>").strip()
        
        if not Url == "":
            loc = "repo"
            listUrl = Url
            listName = common.find_single_match(response,"<name>([^<]+)</name>").strip()
        elif not pUrl == "":
            loc = "page"
            listUrl = pUrl
            listName = common.find_single_match(response,"<name>([^<]+)</name>").strip()
        elif not xUrl == "":
            loc = "xml"
            listUrl = xUrl
            listName = common.find_single_match(response,"<name>([^<]+)</name>").strip()
        else:
            listName = common.GetKeyboardText(localizedString(10263).encode('utf-8')).strip()
    else:
        if not listName:
            listName = listName.split("/")[-2]
    
    exists = ""
    
    if len(listUrl)>0 and len(listName)>0:
        for item in list:
            if item["url"] == listUrl:
                exists = "yes"
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ",localizedString(10264).encode('utf-8'), 3600, icon))
                break
        
        if exists == "":
            if loc == "xml":
                list.append({"name": listName, "url": listUrl, "type":"xml"})
            elif loc == "page":
                list.append({"name": listName, "url": listUrl, "type":"page"})
            elif loc == "pyt":
                list.append({"name": listName, "url": listUrl, "type":"pyt"})
            else:
                list.append({"name": listName, "url": listUrl})
                
            if common.SaveList(playlistsFile4, list):
                    xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
	
def RemoveFromLists(url):
    
    list = common.ReadList(playlistsFile2)
    for item in list:
        if item["url"] == url:
            list.remove(item)
            if common.SaveList(playlistsFile2, list):
                xbmc.executebuiltin("XBMC.Container.Refresh()")
            break
			
def RemoveDirFromLists(url,name):
    
    return_value = xbmcgui.Dialog().yesno(localizedString(10045).encode('utf-8'), localizedString(10206).encode('utf-8') + " " + name + "?")
    if not return_value == 0:
                
        list = common.ReadList(playlistsFile4)
        for item in list:
            if item["url"] == url:
                list.remove(item)
                if common.SaveList(playlistsFile4, list):
                    xbmc.executebuiltin("XBMC.Container.Refresh()")
                break
				
def m3uCategory(url,Logo=True):
    
    try:
        urldec = base64.decodestring(url)
        if common.check_url(urldec):
            url = urldec
    except:
        pass
    
    if not common.check_url(url):
        list = common.m3u2list(os.path.join(chanDir, url)) 
    else :
        list = common.cachelist(url,cdir)
    
    playheaders = ""
    
    try:
        surl,playheaders=url.split('|')
    except:
        playheaders = ""
    
    for channel in list:
        name = channel["display_name"]

        if channel.get("tvg_logo", ""): 
            logo = channel.get("tvg_logo", "")
            iconname = "https://kodilive.eu/logo/" + logo
        else :
            iconname = TVICO
        
        if Logo == False:
            if channel.get("tvg_logo", "") and common.check_url(channel.get("tvg_logo", "")):
                iconname = channel.get("tvg_logo", "")
            else:
                iconname = TVICO
        
        channel["url"] = channel["url"].strip()
        if not playheaders == "":
            channel["url"] = channel["url"] + "|" + playheaders
        
        ext = "." + channel["url"].split(".")[-1]
        EXT = EXTV + EXTA
        if bool(ext in EXT):
            AddDir(name ,channel["url"],3, iconname, isFolder=False)
        else:
            FastDir(name,channel["url"],3,iconname,fanart="",description="",res=False,isFolder=False)
        
def FastDir(name,url,mode,icon="",fanart="",description="",res=False,isFolder=True,linkType=None):

        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+ str(mode) + "&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(icon)+"&description="+urllib.quote_plus(description)
        liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        ok = True
        
        if fanart == "":
            liz.setArt({'fanart': Addon.getAddonInfo('fanart')})
        else:
            liz.setArt({'fanart':fanart})
        
        items = [ ]
           
        if not isFolder and not mode==73:
            if not mode == 78:
                liz.setProperty('IsPlayable', 'true')
            liz.setProperty( "Video", "true")
            liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description })           
            items = [('{0}'.format(localizedString(10009).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=31&name={2}&iconimage={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name), urllib.quote_plus(icon)))]

        if not res and not mode==73:
            
            try:
                urldec = base64.decodestring(url)
                if common.check_url(urldec):
                    url = urldec
            except:
                pass
            
            if url.find(".m3u8")>0 or url.startswith("opus") or url.startswith("fotv"):
                items.append(('Play with HLS-Player','XBMC.RunPlugin({0}?url={1}&iconimage={2}&name={3}&mode=5)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name))))
        
            if os.path.exists(ydldir):
                items.append(('Youtube-dl Control','XBMC.RunPlugin({0}?url={1}&name={2}&mode=80)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            items.append(('Refresh', 'Container.Refresh'))
        
        if linkType:
            u="XBMC.RunPlugin(%s&linkType=%s)" % (u, linkType)
            
        liz.addContextMenuItems(items, replaceItems=True)            
        #xbmc.log("Channel -->" + u, xbmc.LOGNOTICE)   
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
        return ok
    
def PlayUrl(name,url,iconimage=None):
    
    url = url.replace("\n","").replace("\r","")
    #name = common.GetEncodeString(name)
    urldec = ""
    
    try:
        urldec = base64.decodestring(url)
        if common.check_url(urldec):
            url = urldec
    except:
        pass    
    
    if url.find("pornhd.com")>0:
        try:
            url = common.pornHD(url)
        except:
            pass
    
    urluhd = 0
    
    if url.find("urhd.tv")>0:
        try:
            url = common.urhd(url)
            urluhd = 1
        except:
            pass
    
    if url.startswith("opus"):
        url = Opus(url)    
    
    if url.startswith("fotv"):
        url = Get_url_fotv(url)
    
    if url.find(":enc")>0:
        url = rsich(url)
    
    if not url.endswith(".ts") and not url.find(".ts|")>-1 and not url.endswith(".f4m") and url.find(".f4m?") < 0 and not url.endswith("Player=HLS"):
        
        print '--- Playing "{0}". {1}'.format(name, url)
        listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
        listitem.setInfo(type="Video", infoLabels={ "Title": name })
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
                
    else :
        
        if xbmc.Player().isPlaying():
            xbmc.executebuiltin( "XBMC.Action(Stop)" )
            xbmc.sleep(4000)
            xbmc.executebuiltin('Dialog.Close(all, true)')

        #if Addon.getSetting('use_shani') == "true":
        #    MyF4m = False
        #else:
        
        MyF4m = True
            
        if url.endswith(".ts") or url.find(".ts|")>-1:        
            StreamType = 'TSDOWNLOADER'
        elif url.find("Player=HLS") > 0 or urluhd>0:
            StreamType = 'HLS'
        else:
            StreamType = 'HDS'
        
        if MyF4m :
            url = 'plugin://plugin.video.kodilivetv/?url='+urllib.quote_plus(url)+'&streamtype=' + StreamType + '&name='+urllib.quote(name)+'&mode=5&iconImage=' + iconimage
            xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
            xbmc.executebuiltin('Dialog.Close(all, true)')
        else:
            f4mDir = xbmcaddon.Addon('plugin.video.f4mTester').getAddonInfo('path')
            if not os.path.exists(f4mDir):
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName,"Plugin f4mTester required!", 3200, icon))
            else:
                url = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(url)+'&streamtype=' + StreamType + '&name='+urllib.quote(name)+'&iconImage=' + iconimage
                xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
                xbmc.executebuiltin('Dialog.Close(all, true)')

def findm3u(url, string="",live=False):
    
    if url == "ipbox":
        getIpBoxList(string=string,live=live)
        
    elif "urhd.tv" in url:
        
        ch_list = common.urhd_list()
        for idx, ch in enumerate(ch_list, 1):
            
            if ch["alive"]:
                active = ""
            else:
                active = " - [B][COLOR red][INACTIVE][/COLOR][/B]"
        
            display_name = ch["display_name"]
            url = "http://urhd.tv/" + ch["display_name"].lower()
            
            if string == "":    
                AddDir("[COLOR orangered]" + display_name + "[/COLOR]" + active, url, 3 , TVICO, "", isFolder=False)
            else:
                sname = common.BBTagRemove(display_name).replace("_"," ").lower()
                if sname.find(string)>-1:
                    listName = "  " + "[CR][I][COLOR blue][LIGHT]* {0}[/COLOR]".format(localizedString(10004).encode('utf-8')) + " -->  [COLOR yellow]{0}[/COLOR][/I][/LIGHT]".format("urhd.tv")
                    cname = "[COLOR orange][B]{0}[/B][/COLOR]".format(display_name) + active + listName
                    AddDir(cname , url, 3 , TVICO, "", isFolder=False)
    else:
        
        from bs4 import BeautifulSoup
        from urlparse import urlparse
        import html5lib
        
        try:
            urldec = base64.decodestring(url)
            if common.check_url(urldec):
                url = urldec
        except:
            pass
        
        data = common.cachepage(url,7200,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
        soup = BeautifulSoup(data,'html5lib')
        flink = 0
        
        if string == "":
            AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10250).encode('utf-8')), url, 81, find, isFolder=True)
        nu = 0
        for link in soup.find_all('a', href=True):
            if '.m3u' in link['href']:
                nu = nu + 1
                flink = 1
                nurl = urlparse(link['href'])
                listnamext = nurl.path.split("/")
                if url.find("SAM.html")>0:
                    ListName = "[B][COLOR green]S[/COLOR][COLOR withe]a[/COLOR][COLOR red]M[/COLOR] [COLOR orange]  " + str(nu) + " [/COLOR][/B]"
                else:
                    listname = listnamext[-1].split(".m3u")
                    ListName = listname[0]
                    
                listurl = link['href']
                if string == "":
                    AddDir("[COLOR green]" + ListName + "[/COLOR]", listurl, 51, "http://findicons.com/files/icons/1331/matrix_rebooted/128/text_clipping_file.png", isFolder=True)
                else:
                    sch_m3u(listurl,string,ListName,live=live)
        
        if flink == 0:
            patron = '>(http:\/\/(.*?)\/.*?get.php.*?)<'
            matches = re.compile(patron, re.DOTALL).findall(data)
            
            for scrapedurl in matches:
                
                listurl = scrapedurl[0].replace("&amp;","&")
                listname = scrapedurl[0].split("/")[-2]
                #xbmc.log("Finded url = " + listurl, xbmc.LOGNOTICE) 
                
                if string == "":
                    AddDir("[COLOR green]" + listname + "[/COLOR]", listurl, 51, "http://findicons.com/files/icons/1331/matrix_rebooted/128/text_clipping_file.png", isFolder=True)
                else:
                    sch_m3u(listurl,string,listname,live=live)
        
def OpenXML(url, string="",live=False):
    
    from xml.dom import minidom
    
    try:
        urldec = base64.decodestring(url)
        if common.check_url(urldec):
            url = urldec
    except:
        pass
    
    enckey=False
    urlrec = url
    
    if common.check_url(url):
        
        if '$$ref=' in url:
            enckey=url.split('$$ref=')[1].split('$$')[0]
            rp='$$ref=%s$$'%enckey
            url=url.replace(rp,"")
        
        data = common.OpenURL(url,string=string)
        
    else:
        f = open(url,'r')
        data = f.read().replace("\n\n", "")
        f.close()
    
    datafile =  os.path.join(pwdir , base64.standard_b64encode(urlrec))
    if os.path.isfile(datafile):
        f = open(datafile,'r')
        dataf = f.read().replace("\n\n", "")
        f.close() 
        enckm = common.find_single_match(dataf,"<enckey>([^<]+)</enckey>").strip()
        if not enckm == "": 
            enckey = enckm
        
    if enckey:
        if enckey == "x" and string == "":
            
            stringa = common.GetKeyboardText("Enter a decryption key", "")
            if len(stringa) < 1:
                return
            enckey = stringa        
        
            content = "<enckey>" + enckey + "</enckey>"
            if not enckey == "":
                common.write_file(datafile, content)
        
        if not enckey == "x":
            import pyaes
            enckey=enckey.encode("ascii")
            print enckey
            missingbytes=16-len(enckey)
            enckey=enckey+(chr(0)*(missingbytes))
            #print repr(enckey)
            data=base64.b64decode(data)
            decryptor = pyaes.new(enckey , pyaes.MODE_ECB, IV=None)
            data=decryptor.decrypt(data).split('\0')[0]
    
    try:
        data64 = base64.decodestring(data)
        if data64.find("<data>")>-1:
            data = data64
    except:
        pass
    
    data = data.replace("&","&amp;").replace("&amp;amp;","&amp;")
    
    try:
        xmldoc = minidom.parseString(data)
        Data = xmldoc.getElementsByTagName('data')
        r = 0
        if  string == "":
            for d in Data:
                Type = d.getElementsByTagName("type")
                for node in Type:
                    nt = node.getAttribute('name')
                    if nt == "list":
                        r = 1
                        break
                    if nt == "folder":
                        r = 1
                        break
                
            if r==1:
                AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10250).encode('utf-8')), urlrec, 66, find, isFolder=True)
            
        for d in Data:
            Type = d.getElementsByTagName("type")
        
            for node in Type:
                nt = node.getAttribute('name')
                if nt == "channels":
                    mode = 3
                    icon = TVICO
                    isFolder=False                                
                elif nt == "list":
                    mode = 51
                    icon = iconlist
                    isFolder=True
                elif nt == "ylist":
                    mode = 93
                    icon = iconlist
                    isFolder=True
                elif nt == "folder":    
                    icon = icondir
                    
                itemlist = node.getElementsByTagName("item")
                
                Link = "" 

                for s in itemlist:

                    Name = s.getElementsByTagName("name")[0].childNodes[0].nodeValue.encode("UTF-8")
                    try:
                        Year = s.getElementsByTagName("year")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Year = ""                    
                    try:
                        Director = s.getElementsByTagName("director")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Director = ""
                    try:
                        Writer = s.getElementsByTagName("writer")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Writer = "" 
                    try:
                        Cast = s.getElementsByTagName("cast")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Cast = "" 
                    try:
                        Country = s.getElementsByTagName("country")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Country = "" 
                    try:
                        Genre = s.getElementsByTagName("genre")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Genre = ""
                    try:
                        Rating = str(float(s.getElementsByTagName("rating")[0].childNodes[0].nodeValue)).encode("UTF-8")
                    except:
                        Rating = ""
                    try:
                        Credit = str(float(s.getElementsByTagName("credit")[0].childNodes[0].nodeValue)).encode("UTF-8")
                    except:
                        Credit = ""
                    try:
                        Description = s.getElementsByTagName("description")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Description = ""
                    try:
                        Vid = s.getElementsByTagName("vid")[0].childNodes[0].nodeValue
                    except:
                        Vid = ""
                        pass
                    try:
                        Path = s.getElementsByTagName("path")[0].childNodes[0].nodeValue
                    except:
                        Path = ""
                        pass
                    try:
                        Link = s.getElementsByTagName("link")[0].childNodes[0].nodeValue
                    except:
                        Link = ""
                        pass

                    try:
                        Color = s.getElementsByTagName("color")[0].childNodes[0].nodeValue
                    except:
                        Color = ""
                        pass
                    try:
                        icon = s.getElementsByTagName("icon")[0].childNodes[0].nodeValue
                    except:
                        if not Link == "":
                            ext = "." + Link.split(".")[-1]
                            if bool(ext in EXTV):
                                icon = video
                            elif bool(ext in EXTA):
                                icon = audio
                    try:
                        fanart = s.getElementsByTagName("fanart")[0].childNodes[0].nodeValue
                    except:
                        fanart = ""
                    
                    if nt == "folder":
                        
                        if not Path == "":
                            if Path == "$download" and string == "":
                                Link = DFolder
                            else:
                                Link = Path
                            mode = 64
                            isFolder=True
                        else:
                            mode = 63
                            isFolder=True 

                    elif nt == "ylist":
                        mode = 93
                        Link = Vid                        
                        icon = icondir
                        isFolder=True                        
                    
                    if icon == "video":
                        icon = video
                    if icon == "audio":
                        icon = audio
                    if icon == "folder":
                        icon = icondir
                    if icon == "list":    
                        icon = iconlist
                    if not Color == "" :
                        cname = "[COLOR " + Color + "][B]{0}[/B][/COLOR]".format(Name)
                    else:
                        cname = "{0}".format(Name)
                        
                    if nt == "list" and Link.startswith('page://'):
                        Link = Link.replace("page://","")
                        mode = 79    
                        
                    if string == "":    
                        AddDir(cname,Link,mode,icon,description=Description,isFolder=isFolder,background=fanart,genre=Genre,year=Year,director=Director,writer=Writer,cast=Cast,country=Country,rating=Rating,credit=Credit)
                    else:
                        sname = common.BBTagRemove(Name).replace("_"," ").replace("%20"," ").lower()
                        if mode == 3 and sname.find(string)>-1:
                            EXT = EXTV + EXTA
                            if is_mp4(Link):
                                AddDir(cname,Link,mode,icon,description=Description,isFolder=isFolder,background=fanart,genre=Genre,year=Year,director=Director,writer=Writer,cast=Cast,country=Country,rating=Rating,credit=Credit)
                            elif not bool(ext in EXT) or not live:
                                if not bool(ext in EXT):
                                    FastDir(cname,Link,mode,icon,fanart=fanart,description=Description,res=True,isFolder=False)
                                else:
                                    AddDir(cname,Link,mode,icon,description=Description,isFolder=isFolder,background=fanart,genre=Genre,year=Year,director=Director,writer=Writer,cast=Cast,country=Country,rating=Rating,credit=Credit)
                        if mode == 51 or mode == 79:
                            sch_m3u(Link,string,sname,live=live)
                        if mode == 64:
                            PMFolder(Link,string,live=live)
                        if mode == 63:
                            OpenXML(Link,string,live=live)
                        if mode == 93:
                            Yplayl(Link,string,live=live)
    except:
        pass

def PMFolder( folder , string="",live=False):
    
    try:
        urldec = base64.decodestring(folder)
        if common.check_url(urldec):
            folder = urldec
    except:
        pass

    urlx = folder
    pw = ""
    
    if urlx.find("@")>-1:
        US = ""
        URL1 = urlx.split("@")[0]
    
        if urlx.startswith("http:"):
            proto = "http://"
        elif urlx.startswith("ftp:"):
            proto = "http://"
        else:
            proto = "https://" 
    
        URL1 = urlx.replace("http://","").replace("https://","").replace("ftp://","")
        us = URL1.split(":")[0]
        pw = URL1.split(":")[1]
        pw = pw.split("@")[0]
        
        datafile =  os.path.join( pwdir , base64.standard_b64encode(folder))
        pwm = ""
        usm = ""
        t = 0
        
        if os.path.isfile(datafile):
            f = open(datafile,'r')
            data = f.read().replace("\n\n", "")
            f.close() 
            pwm = common.find_single_match(data,"<password>([^<]+)</password>").strip()
            if not pwm == "": 
                pw = pwm
            usm = common.find_single_match(data,"<username>([^<]+)</username>").strip()
            if not usm == "": 
                us = usm
            folder = proto + us + ":" + pw + "@" + urlx.split("@")[1]
            
        if pw =="x" and string == "":
            if not us == "x":
                US = us
            stringa = common.GetKeyboardText("Enter username", US)
            if len(stringa) < 1:
                return
            us = stringa
            if not pw == "x":
                p = pw
            else:
                p = ""
                
            stringa = common.GetKeyboardText("Enter password", p)
            if len(stringa) < 1:
                return
            pw = stringa
            folder = proto + us + ":" + pw + "@" + urlx.split("@")[1]
            if os.path.isfile(datafile):
                os.remove(datafile)
                xbmc.sleep(1200)
            
        if not os.path.isfile(datafile) and string == "":
            content = "<username>" + us + "</username><password>" + pw + "</password>"
            common.write_file(datafile, content)
    
    DF =  folder
    dirs, files = xbmcvfs.listdir(DF)
    EXT = EXTL + EXTV + EXTA 
    
    files.sort()
    if  string == "":
        AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10250).encode('utf-8')), folder, 65, find, isFolder=True)
    
    if DF == DFolder and string == "":        
        src = os.path.join(xbmc.translatePath("special://userdata/addon_data" ), 'script.module.youtube.dl', 'tmp')
        AddDir("[COLOR red][B]{0}[/B][/COLOR]".format("Tmp"), src , 54, icondir, isFolder=True)
    
    for i in dirs:
        rf = format(i)
        cname = "[COLOR cyan][B]{0}[/B][/COLOR]".format(rf)
        
        if common.check_url(DF):
            url = DF  + rf + "/"
        else:
            url = os.path.join(DF, rf)

        url = url.replace("\r","").replace("\n","").strip()
        cname = cname.replace("%20"," ").replace("\r","").replace("\n","").strip()
        if string == "":
            AddDir(cname, url, 54, icondir, isFolder=True)
        else:
            PMFolder( url , string, live=live)
            
    for i in files:
        rf = format(i)
        ext = "." + rf.split(".")[-1]
        
        if ext == ".xml":
            
            Name = rf.replace("%20"," ").replace("\r","").replace("\n","").replace(".xml","").strip()
            Name = "[COLOR cyan][B]{0}[/B][/COLOR]".format(Name)
            
            if common.check_url(DF):
                url = DF + rf
            else:
                url = os.path.join(DF, rf)
            if string == "":
                AddDir(Name, url, 63, icondir, isFolder=True) 
            else:
                OpenXML(url,string,live=live)
    
    for i in files:    
        rf = format(i)
        ext = "." + rf.split(".")[-1]
        
        if bool(ext in EXT):
            
            Name = rf.replace("%20"," ").replace("\r","").replace("\n","").strip()
                
            if common.check_url(DF):
                url = DF + rf
            else:
                url = os.path.join(DF, rf)
		
            url = url.replace("\r","").replace("\n","").strip()

            if url.endswith(".m3u") or url.endswith(".txt") or url.endswith(".m3u8"):
                if string == "":
                    cname = "[COLOR green][B]{0}[/B][/COLOR]".format(Name)
                    AddDir(cname, url, 51, iconlist, isFolder=True)
                else:
                    sname = common.BBTagRemove(Name).replace("_"," ").replace("%20"," ").lower()
                    sch_m3u(url,string,sname,live=live)
            else:
                perc = -1
                p = ""
                EP = ""
                    
                if os.path.isfile(url + ".resume"):
                    EP = ".resume"
                elif os.path.isfile(url + ".stopped"):
                    EP = ".stopped"
                else:
                    perc = -1
                if not  EP == "":
                    PERC = common.ReadFile(url + EP).replace("\r","").split("\n")
                    perc = int(PERC[0])
                        
                if not perc <=0:
                    size = 0
                    size = os.stat(url).st_size
                        
                    if size > 0:
                        perc = round((100.0*size)/int(perc), 2)

                        col = "green"
                            
                        if perc <80:
                            col = "yellow"
                        if perc <55:
                            col = "orange"
                        if perc <35:
                            col = "orangered"
                        if perc <15:
                            col = "red"

                        p = " - [B][COLOR blue][ [COLOR " + col + "]" + str(perc) + "% [/COLOR]][/B][/COLOR]"
                
                elif not EP == "":
                    p = " - [B][COLOR blue][ [COLOR yellow] Download in progress [/COLOR]][/B][/COLOR]"

        
                if bool(ext in EXTV):
                    icon = video
                else:
                    icon = audio
                
                if string == "":    
                    cname = "[COLOR CCCCFFFF][B]{0}[/B][/COLOR]".format(Name) + p
                    AddDir(cname , url, 50 , icon, "", isFolder=False)
                else:
                    EXT1 = EXTV + EXTA 
                    if bool(ext in EXT1) and not live:
                        sname = common.BBTagRemove(Name).replace("_"," ").lower()
                        if sname.find(string)>-1:
                            cname = "[COLOR CCCCFFFF][B]{0}[/B][/COLOR]".format(Name) + p
                            AddDir(cname , url, 50 , icon, "", isFolder=False)
                        

def AddDir(name,url,mode,iconimage,description="",isFolder=True,background="",genre="",year="",director="",writer="",cast="",country="",rating="",credit=""):
    
    url = url.replace('\n','')
    url = url.replace('\r','')
    url = url.strip()
    try:
        urlz = url.split("|")[1]
        #url = url.split("|")[0]
        #if urlz == "Player=HLS":
        #   url = url + '|' + urlz
    except:
        urlz = ""
    
    name = name.strip()
    if not mode == 32:
        name = common.GetEncodeString(name)
        
    EXTM = EXTV + EXTA
    
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)

    liz.setArt({'fanart': Addon.getAddonInfo('fanart')})
    liz.setArt({ 'thumb': iconimage})
    ext = ""
	
    if not background == "":
            liz.setProperty('fanart_image', background)
            
    if mode == 4 or mode == 21 or mode == 51 or mode == 54 or mode == 50 or mode == 60 or mode == 63 or mode == 64 or mode == 70 or mode == 79 or mode == 93:
        items = [ ]
        
        if mode == 54:
            items.append(('Youtube-dl Control','XBMC.RunPlugin({0}?url={1}&name={2}&mode=80)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
        
        if mode == 21 or mode == 63 or mode == 64 or mode == 70 or mode == 79 or mode == 93:
            urlE = url
            try:
                urldec = base64.decodestring(url)
                if common.check_url(urldec):
                    url = urldec
            except:
                pass            
            
            if not mode == 64 and not mode == 63:
                items = [('{0}'.format(localizedString(10008).encode('utf-8')) + name, 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=55)'.format(sys.argv[0], urllib.quote_plus(urlE), urllib.quote_plus(name)))]
                items.append(('{0}'.format(localizedString(10018).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=61)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
                if not url == "ipbox":
                    items.append(('{0}'.format(localizedString(10019).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=95)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            else:
                items.append(('Youtube-dl Control','XBMC.RunPlugin({0}?url={1}&name={2}&mode=80)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            
            if url.find("@")>0:
                datafile = os.path.join( pwdir , base64.standard_b64encode(url) )
                if os.path.isfile(datafile):
                    items.append((localizedString(10207).encode('utf-8'), 'XBMC.RunPlugin({0}?url={1}&mode=56)'.format(sys.argv[0], urllib.quote_plus(url))))

            if mode == 63 or mode == 70:
                if url.find("$$ref=x$$")>0:
                    datafile = os.path.join( pwdir , base64.standard_b64encode(url) )
                    if os.path.isfile(datafile):
                        items.append((localizedString(10215).encode('utf-8'), 'XBMC.RunPlugin({0}?url={1}&mode=56)'.format(sys.argv[0], urllib.quote_plus(url))))

            if mode == 63 or mode == 21 or mode == 70 or mode == 79 or mode == 93:
                listDir = common.ReadList(playlistsFile4)
                for fold in listDir:
                    if not url == urlE:
                        t1 = fold["url"]
                        t2 = urlE
                    else:
                        t1 = fold["url"].lower()
                        t2 = url.lower()
                        
                    if t1 == t2:
                        e = ""
                        try:
                            e = fold["exclude"]
                        except:
                            pass
                        
                        if e == "yes":
                            items.append((localizedString(10252).encode('utf-8'), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=68)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
                        else:
                            items.append((localizedString(10251).encode('utf-8'), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=67)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
                
                TempName = base64.standard_b64encode(url)
                tmp = os.path.join(cdir, TempName)
            
                if os.path.isfile(tmp):            
                    items.append(('{0}'.format(localizedString(10105).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=94)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
                
        if mode == 4:
            
            if url.find("get.php?username=")>0 or name.lower().find("fast open")>-1 or name.lower().find("slow open")>-1 or name.lower().find("tv_channels")>-1 or name.lower().find("[iptv]")>-1:
                items.append(('Check List : [COLOR yellow]' + common.BBTagRemove(name) + '[/COLOR]', 'XBMC.RunPlugin({0}?url={1}&mode=90&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name))))
                    
            items.append(('{0}'.format(localizedString(10008).encode('utf-8')) + name, 'XBMC.RunPlugin({0}?url={1}&mode=22)'.format(sys.argv[0], urllib.quote_plus(url))))
            
            items.append(('{0}'.format(localizedString(10018).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=23)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            items.append(('{0}'.format(localizedString(10019).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=24)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            
            TempName = base64.standard_b64encode(url)
            tmp = os.path.join(cdir, TempName)
            
            if os.path.isfile(tmp):
                items.append(('{0}'.format(localizedString(10105).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=94)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            
        if mode ==51 or mode == 50:
            name = common.BBTagRemove(name)
            
            try:
                urldec = base64.decodestring(url)
                if common.check_url(urldec):
                    url = urldec
            except:
                pass
                
            if not common.check_url(url):
                items = [('{0}'.format(localizedString(10205).encode('utf-8')) + ' : ' + name, 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=52)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name)))]
            if url.find("get.php?username=")>0 or name.lower().find("fast open")>-1 or name.lower().find("slow open")>-1 or name.lower().find("tv_channels")>-1 or name.lower().find("[iptv]")>-1:
                items.append(('Check List : [COLOR yellow]' + name + '[/COLOR]', 'XBMC.RunPlugin({0}?url={1}&mode=90&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name))))
            
            TempName = base64.standard_b64encode(url)
            tmp = os.path.join(cdir, TempName)
            
            if os.path.isfile(tmp):            
                items.append(('{0}'.format(localizedString(10105).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=94)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            
        if mode == 50:
            ext = url.split('.')[-1]
            namefile = urllib.unquote(os.path.basename(url)).replace("." + ext,"")
            if url.find("pornhd.com")>0:
                namefile = urllib.unquote(os.path.basename(url)).split('.')[-2]
            
            if os.path.isfile( url + ".stopped"):
                urlx = common.ReadFile(url + ".stopped").replace("\r","").split("\n")
                items.append((localizedString(10213).encode('utf-8') + ' : ' + namefile, 'XBMC.RunPlugin({0}?url={1}&mode=7&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(urlx[1]), urllib.quote_plus(iconimage), urllib.quote_plus(namefile))))
            elif os.path.isfile( url + ".resume"):
                urlx = common.ReadFile(url + ".resume").replace("\r","").split("\n")
                items.append((localizedString(10212).encode('utf-8') + ' : ' + namefile, 'XBMC.RunPlugin({0}?url={1}&mode=57&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(urlx[1]), urllib.quote_plus(iconimage), urllib.quote_plus(namefile))))
            
            items.append(('{0}'.format(localizedString(10009).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name))))
            
        if mode ==51 or mode == 50:
            if not common.check_url(url):
                if not os.path.isfile( url + ".stopped") and not os.path.isfile( url + ".resume"):
                    items.append(('{0}'.format(localizedString(10018).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=53)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            
            items.append(('Youtube-dl Control','XBMC.RunPlugin({0}?url={1}&name={2}&mode=80)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            items.append(('Refresh', 'Container.Refresh'))
        
        if mode == 50:
            if bool(ext in EXTV):
                liz.addContextMenuItems(items)
            else:
                liz.addContextMenuItems(items, replaceItems=True)
        else:
            liz.addContextMenuItems(items)
	
    
    if mode == 3 or mode == 32:
        liz.setProperty( "Video", "true")
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description,"Genre": genre, "Year" : year, "Director" : director, "Writer" : writer, "Cast" : cast.split(","), "Country" : country, "Rating": rating, "Credit": credit})
        liz.setProperty('IsPlayable', 'true')
        if mode == 3:
            items = [('{0}'.format(localizedString(10009).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))]
        else:
            items = [('{0}'.format(localizedString(10010).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=33&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))]
            items.append(('{0}'.format(localizedString(10018).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=69)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
        ext = '.' + url.split('.')[-1]
        ref = 1
        
        if bool(ext in EXTM) or url.find("openload.")>0 or url.find("pornhd.com")>0 or url.find("akvideo.")>0 or url.find("stream.moe")>0 or url.startswith("urlr://") or url.find("rapidvideo.")>0 or url.find("speedvideo.")>0 or url.find("fastvideo.")>0 or url.find("thevideo.me")>0 or url.find("wstream.")>0 or url.find("nowvideo.")>0 or url.find("streamango.")>0 or url.find("megadrive.")>0 or url.find("megahd.")>0 or url.find("vidto.me")>0:
            
            if url.find("pornhd.com")>0 or url.find("openload.")>0 or url.find("akvideo.")>0 or url.find("stream.moe")>0 or url.find("rapidvideo.")>0 or url.find("speedvideo.")>0 or url.find("fastvideo.")>0 or url.find("thevideo.me")>0 or url.find("wstream.")>0 or url.find("nowvideo.")>0 or url.find("streamango.")>0 or url.find("megadrive.")>0 or url.find("megahd.")>0 or url.find("vidto.me")>0:
                ext = '.mp4'
                xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            else:
                xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            
            if common.check_url(url):
                name = name.replace(","," ")
                name = name.replace("  "," ")
                pname = common.BBTagRemove(name).replace(":","-").replace(".","-").replace("/","-")
                
                try:
                    pname = pname.split('[CR]')[-2]
                    ref = 0
                except:
                    pass
                
                pname = pname.strip()
                            
                file = DFolder + pname + ext
                
                if url.startswith("xxxxx://") and not bool(ext in EXTM):
                    items.append(('Download : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=6&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(pname))))
    
                else:
                    if ref == 0:

                        if os.path.isfile( file + ".stopped") and os.path.isfile( file):
                            items.append((localizedString(10213).encode('utf-8') + ' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=6&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(pname))))
                            items.append((localizedString(10214).encode('utf-8') +' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=71&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(pname))))
                        elif os.path.isfile( file + ".resume") and os.path.isfile( file):
                            items.append((localizedString(10212).encode('utf-8') + ' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=72&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(pname))))
                        else:
                            items.append(('Download : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=6&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(pname))))                
                    
                    else:
                        if os.path.isfile( file + ".stopped") and os.path.isfile( file):
                            items.append((localizedString(10213).encode('utf-8') + ' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=7&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(pname))))
                            items.append((localizedString(10214).encode('utf-8') +' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=58&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(pname))))
                        elif os.path.isfile( file + ".resume") and os.path.isfile( file):
                            items.append((localizedString(10212).encode('utf-8') + ' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=57&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(pname))))
                        else:
                            items.append(('Download : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=7&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(pname))))
                        items.append(('Refresh', 'Container.Refresh'))
        elif ext == ".html" or url.find("plugin.video.youtube")>0 or url.find("dm://")>-1:
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        urldec = ""
        
        try:
            urldec = base64.decodestring(url)
            if common.check_url(urldec):
                url = urldec
        except:
            pass
        
        if url.find(".m3u8")>0 or urlz == "m3u8" or url.find("urhd.tv")>-1:
            items.append(('Play with HLS-Player','XBMC.RunPlugin({0}?url={1}&iconimage={2}&name={3}&mode=5)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name))))
        
        if os.path.exists(ydldir) and not url.find("pornhd.com")>0:
            items.append(('Youtube-dl Control','XBMC.RunPlugin({0}?url={1}&name={2}&mode=80)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))

        # openload megahd nowvideo fastvideo rapidvideo nowdownload speedvideo streamin.to abysstream.com/
        if url.find("Player=HLS")>0 or url.find("openload.")>0 or url.find("megahd.")>0 or url.find("nowvideo.")>0 or url.find("fastvideo.")>0 or url.find("rapidvideo.")>0 or url.find("nowdownload.")>0 or url.find("speedvideo.")>0 or url.find("streamin.to")>0 or url.find("abysstream.com/")>0:
            liz.addContextMenuItems(items, replaceItems=True)
        else:
            liz.addContextMenuItems(items)
    if mode == 20:        
        items = [('{0}'.format(localizedString(10120).encode('utf-8')) , 'XBMC.RunPlugin({0}?url={1}&mode=91)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))),  
                        ('{0}'.format(localizedString(10121).encode('utf-8')) , 'XBMC.RunPlugin({0}?url={1}&mode=92)'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))) ]

        liz.addContextMenuItems(items , replaceItems=True)
    
    if mode == 30 or mode == 48 or mode == 49 or mode == 46 or mode == 34:
        liz.addContextMenuItems( [] , replaceItems=True)
    if mode == 64 or mode == 63 or mode == 93:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)


def PM_index():
    
    AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10250).encode('utf-8')), "search2" , 65, find, isFolder=True)
    AddDir("[COLOR blue][B]{0}[/B][/COLOR]".format(localizedString(10001).encode('utf-8')), "settings" , 20, "http://findicons.com/files/icons/1331/matrix_rebooted/128/new_folder.png", isFolder=True)
            
    AddDir("[COLOR cyan][B]{0}[/B][/COLOR]".format(localizedString(10112).encode('utf-8')), DFolder , 60, "http://findicons.com/files/icons/1331/matrix_rebooted/128/drop_folder.png", isFolder=True)
    listDir = common.ReadList(playlistsFile4)
    
    for fold in listDir:
        name = "[COLOR cyan][B]{0}[/B][/COLOR]".format(fold["name"].encode("utf-8"))
        
        t = ""
        try:
            t = fold["type"]
        except:
            pass
        
        if t == "xml":
            mode = 70
        elif t == "page":
            mode = 79
        elif t == "pyt":
            mode = 98
        else:
            mode = 21
        
        AddDir(name, fold["url"].encode("utf-8"), mode, "http://findicons.com/files/icons/1331/matrix_rebooted/128/generic_folder_alt.png", isFolder=True)       
        
    list = common.ReadList(playlistsFile2)
    for channel in list:
        if channel["url"].find("://")>0:
            color = "FF00c100"
        else:
            color = "green"
            
        name = "[COLOR " + color + "][B]{0}[/B][/COLOR]".format(channel["name"].encode("utf-8"))
        AddDir(name, channel["url"].encode("utf-8"), 4, "http://findicons.com/files/icons/1331/matrix_rebooted/128/text_clipping_file.png", isFolder=True)
        
def ChangeName(name, listFile, key, title):
    
    list = common.ReadList(listFile)
    
    if not listFile == favoritesFile:
        name = common.BBTagRemove(name)
    
    string = common.GetKeyboardText(localizedString(title), name)
    if len(string) < 1:
            return
    for channel in list:    
        if channel["url"] == url:
            channel["name"] = string
            break
        else:
            try:
                ure = base64.b64encode(url)
            except:
                ure = ""
            
            if channel["url"] == ure:
                channel["name"] = string
                break
                
    if common.SaveList(listFile, list):
            xbmc.executebuiltin("XBMC.Container.Refresh()")
		
def ChangeUrl(url, listFile, key, title):
        
    list = common.ReadList(listFile)
	
    if not common.check_url(url):
        string = xbmcgui.Dialog().browse(int(1), localizedString(10006).encode('utf-8'), 'myprograms','.m3u8|.m3u')
        if not string:
            return
    else:
        string = common.GetKeyboardText(localizedString(title), url)
            
    if len(string) < 1:
            return
    for channel in list:    
        if channel["url"] == url:
            channel["url"] = string
            break
    if common.SaveList(listFile, list):
            xbmc.executebuiltin("XBMC.Container.Refresh()")

def ChangeUrl2(url, listFile, key, title):
        
    list = common.ReadList(listFile)
    
    string = ""

    for channel in list:
        
        try:
            urldec = base64.decodestring(channel["url"])
        except:
            urldec = ""
            pass
        
        if channel["url"] == url or urldec == url:
            try: 
                ty = channel["type"]
            except:
                ty = ""
            
            if not common.check_url(url) and not ty=="pyt":
                
                if ty == "":
                    string = xbmcgui.Dialog().browse(int(3), localizedString(10041).encode('utf-8'), 'myprograms','', True)
                elif ty == "xml":
                    string = xbmcgui.Dialog().browse(int(1), localizedString(10006).encode('utf-8'), 'myprograms','.xml')
                if not string:
                    return
            else:
                string = common.GetKeyboardText(localizedString(title), channel["url"])
                    
            if len(string) < 1:
                    return
            
            channel["url"] = string
            break
    if common.SaveList(listFile, list):
            xbmc.executebuiltin("XBMC.Container.Refresh()")

def GetSourceLocation(title, list):
    
    dialog = xbmcgui.Dialog()
    answer = dialog.select(title, list)
    return answer
	
def AddFavorites(url, iconimage, name):
    
    favList = common.ReadList(favoritesFile)
    for item in favList:
        if item["url"] == url:
            xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10011).encode('utf-8'), icon))
            return
        
    name = name.replace('\r','').replace('\r','').strip()
    url = url.replace('\n','').replace('\r','').strip()
	
    if not iconimage:
        iconimage = ""
    else:
        iconimage = iconimage.replace('\r','').replace('\n','').strip()
        
    data = {"url": url, "image": iconimage, "name": name }
    favList.append(data)
    common.SaveList(favoritesFile, favList)
    xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10012).encode('utf-8'), icon))
		
def ListFavorites():
    
    AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10013).encode('utf-8')), "favorites" ,34 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"), isFolder=False)
    if 'win32' or 'linux' or 'darwin' in sys.platform:
        AddDir("[COLOR red][B]{0}[/B][/COLOR]".format(localizedString(10099).encode('utf-8')) + " - Press [ALT] + [F4] to close", "Netflix" ,48 ,os.path.join(addonDir, "resources", "images", "netflix.png"), isFolder=False)
    if 'win32' or 'linux' or 'darwin' in sys.platform:
        AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format((localizedString(10098)).encode('utf-8')) + " - Press [ALT] + [F4] to close", "Offer" ,49 , os.path.join(addonDir, "resources", "images", "paypal.png"), isFolder=False)
	
    list = common.ReadList(favoritesFile)
    for channel in list:
        name = channel["name"].encode("utf-8")
        iconimage = channel["image"].encode("utf-8")
        if iconimage=="":
            iconimage = TVICO 
        
        AddDir(name, channel["url"].encode("utf-8"), 32, iconimage, isFolder=False) 
        #FastDir(name,channel["url"].encode("utf-8"),32,iconimage,isFolder=False)
        
def ListSub(lng):
    
    list = common.ReadList(lng)
    for item in list:
        mode =  2
        image = item.get('image', '')
        if not "http" in image:
                icon = os.path.join(addonDir, "resources", "images", image.encode("utf-8"))
        else:
                icon = image.encode("utf-8")
                
        try:
            name = int(item["name"])
            name = localizedString(name)
        except:
            name = item["name"]
                
        cname = "[COLOR gold][B]{0}[/B][/COLOR]".format(name)
        AddDir(cname ,item["url"], mode , icon)

def ListTB(lg):
    
    ok = show_main(lg)

def RemoveFavorties(url):
    
    list = common.ReadList(favoritesFile) 
    for channel in list:
        if channel["url"].lower() == url.lower():
            list.remove(channel)
            break
			
    common.SaveList(favoritesFile, list)
    xbmc.executebuiltin("XBMC.Container.Refresh()")

def AddNewFavortie():
    
    chName = common.GetKeyboardText("{0}".format(localizedString(10014).encode('utf-8'))).strip()
    if len(chName) < 1:
            return
    chUrl = common.GetKeyboardText("{0}".format(localizedString(10015).encode('utf-8'))).strip()
    if len(chUrl) < 1:
            return
		
    favList = common.ReadList(favoritesFile)
    for item in favList:
            if item["url"].lower() == url.lower():
                    xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, localizedString(10011).encode('utf-8'), icon))
                    return
			
    data = {"url": chUrl, "image": "", "name": chName.decode("utf-8")}
    favList.append(data)
    if common.SaveList(favoritesFile, favList):
            xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}?mode=30&url=favorites')".format(AddonID))

############################################################################################
#    Modulo ricerca    

def sch_channels_it(string,live=False):
    #0 - search in italian channels
    sch_m3u(os.path.join(chanDir, "it.txt"),string,localizedString(10052).encode('utf-8'),live=live)
    sch_m3u(os.path.join(chanDir, "vpnit.txt"),string,localizedString(10051).encode('utf-8'),live=live)
    sch_m3u(os.path.join(chanDir, "w_it.txt"),string,localizedString(10055).encode('utf-8'),live=live)    
    sch_m3u(os.path.join(chanDir, "rsi.txt"),string,localizedString(10053).encode('utf-8'),live=live)
    if live==False:
        sch_m3u(os.path.join(chanDir, "regionali.txt"),string,localizedString(10050).encode('utf-8'),live=live)
        sch_m3u(os.path.join(chanDir, "radioit.txt"),string,localizedString(10070).encode('utf-8'),live=live)

def sch_index(string,live=False):
    sch_channels_it(string,live=live)
    # french
    sch_m3u(os.path.join(chanDir, "fr.txt"),string,localizedString(10058).encode('utf-8'),live=live)
    sch_m3u(os.path.join(chanDir, "radiofr.txt"),string,localizedString(10071).encode('utf-8'),live=live)
    sch_m3u(os.path.join(chanDir, "vpnfr.txt"),string,"VPN/IP FR",live=live)
    sch_m3u(os.path.join(chanDir, "rts.txt"),string,"RTS.ch",live=live)
    sch_m3u(os.path.join(chanDir, "w_fr.txt"),string,localizedString(10055).encode('utf-8'),live=live)
    # german
    sch_m3u(os.path.join(chanDir, "de.txt"),string,localizedString(10022).encode('utf-8'),live=live)
    sch_m3u(os.path.join(chanDir, "radiode.txt"),string,localizedString(10072).encode('utf-8'),live=live)
    sch_m3u(os.path.join(chanDir, "srf.txt"),string,"SRF.ch",live=live)
    sch_m3u(os.path.join(chanDir, "vpnat.txt"),string,localizedString(10060).encode('utf-8'),live=live)
    sch_m3u(os.path.join(chanDir, "w_de.txt"),string,localizedString(10055).encode('utf-8'),live=live)
    # english
    sch_m3u(os.path.join(chanDir, "en.txt"),string,localizedString(10057).encode('utf-8'),live=live)
    sch_m3u(os.path.join(chanDir, "radioen.txt"),string,localizedString(10073).encode('utf-8'),live=live)
    sch_m3u(os.path.join(chanDir, "bbc_radio.txt"),string,localizedString(10074).encode('utf-8'),live=live)
    sch_m3u(os.path.join(chanDir, "vpnuk.txt"),string,localizedString(10059).encode('utf-8'),live=live)
    sch_m3u(os.path.join(chanDir, "w_en.txt"),string,localizedString(10055).encode('utf-8'),live=live)
    # music
    sch_m3u(os.path.join(chanDir, "mu.txt"),string,localizedString(10028).encode('utf-8'),live=live)
    
def sch_global_PM(string,live=False):
    
    # 1 - search in download folder 
    PMFolder(DFolder,string,live=live)
    
    # 2 - search in m3ulist-index
    list = common.ReadList(playlistsFile2)
    for channel in list:
        url = channel["url"]
        sname = common.BBTagRemove(channel["name"]).replace("_"," ").replace("%20"," ").lower()
        sch_m3u(url,string,sname,live=live)

    # 3 - search in folder/xml-index
    listDir = common.ReadList(playlistsFile4)
    
    for fold in listDir:
        name = fold["name"]

        try:
            t = fold["type"]
        except:
            t = ""
        try:
            e = fold["exclude"]
        except:
            e = ""
        
        if e == "":
            if t == "xml":
                OpenXML(fold["url"],string,live=live)
            elif t == "pyt":
                Yplayl(fold["url"],string,live=live)
            elif t == "page":
                findm3u(fold["url"],string,live=live)
            else:
                PMFolder(fold["url"],string,live=live)

def sch_global(string,live=False):
    sch_index(string,live=live)
    sch_global_PM(string,live=live)
    
def sch_filmtvit(string,live=True):
    sch_channels_it(string,live=live)
    sch_global_PM(string,live=live)

        
def sch_folder(url,string):
    string = string.lower()
    PMFolder(url,string)

def sch_xml(url,string):
    string = string.lower()
    OpenXML(url,string)

def sch_m3u(url,string,sname,live=False):

    try:
        urldec = base64.decodestring(url)
        if common.check_url(urldec):
            url = urldec
    except:
        pass

    list = common.cachelist(url,cdir)
    
    for channel in list:
        name = channel["display_name"]
        name = common.BBTagRemove(name) 
        Name = name
        name = name.replace("_"," ").lower().strip()
        url = channel["url"].strip()
        ext = "." + url.split(".")[-1].strip()
        EXT = EXTV + EXTA
        
        if not bool(ext in EXT) or not live:
        
            if name.find(string)>-1:
                if channel.get("tvg_logo", ""):
                    if common.check_url(channel.get("tvg_logo", "")):
                        iconname = channel.get("tvg_logo", "")
                    else:
                        logo = channel.get("tvg_logo", "")
                        iconname = "https://kodilive.eu/logo/" + logo
                else :
                    iconname = TVICO

                listName = "  " + "[CR][I][COLOR blue][LIGHT]* {0}[/COLOR]".format(localizedString(10004).encode('utf-8')) + " -->  [COLOR yellow]{0}[/COLOR][/I][/LIGHT]".format(sname)
                cname = "[COLOR orange][B]{0}[/B][/COLOR]".format(Name) + listName
                if live or not bool(ext in EXT):
                    FastDir(cname,url,3,iconname,res=True,isFolder=False)
                else:
                    AddDir(cname,url,3,iconname,isFolder=False)

def sch_exclude(url, listFile, key):
    
    list = common.ReadList(listFile)

    for channel in list:    
        if channel["url"].lower() == url.lower():
            channel["exclude"] = key
            break
        else:
            try:
                ure = base64.b64encode(url)
            except:
                ure = ""
            
            if channel["url"] == ure:
                channel["exclude"] = key
                break
            
    if common.SaveList(listFile, list):
        xbmc.executebuiltin("XBMC.Container.Refresh()")

##########################
# Specials Channels


def rsich(cid):
    pid = cid.split(":")[0]
    cid = cid.split(":")[1]
    url = "http://tp.srgssr.ch/akahd/token?acl=/i/" + cid +"/*"
    
    from random import randint
    a = str(randint(0,8))
    b = str(randint(0,256))
    c = str(randint(0,256))
    ip = "85."+a+'.'+b+'.'+c
    
    #xbmc.log("random ip = "+ip, xbmc.LOGNOTICE)
    
    data = common.OpenURL(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
    token = common.find_param('authparams":"(.*?)"',data)
    #xbmc.log("RSI token = " + token, xbmc.LOGNOTICE)

    
    url = 'https://srgssruni' + pid +'ch-lh.akamaihd.net/i/' + cid + '/master.m3u8?' + token + '|X-Forwarded-For='+ip
    #xbmc.log("RSI url = " + url, xbmc.LOGNOTICE)
    return url

def Opus(cid,headers={'Referer':'http://opus.re','User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'}):
    
    cid = cid.split(":")
    
    pre = "http://opus.cf/allfrtvstrm/tkn/"
    
    if cid[1] == "fr":
        url = "http://opus.re/"
        pre = "http://opus.cf/allfrtvstrm/tkn/wild/"
    elif cid[1] == "it":
        url = "http://opus.re/iptv-italia-tv-canale.php"
    elif cid[1] == "en":
        url = "http://opus.re/iptv-english-tv-channels.php"
    else:
        return
    
    if cid[2] == "arte" or cid[2] == "rmc-decouverte":
        pre = "http://opus.re/tkn/s0/"
    
    data = common.OpenURL(url,headers)
    #xbmc.log("##### url opus index = " + data,xbmc.LOGNOTICE)
    if cid[2] == "3009":
        itemlink = common.find_param(pre + "(.*?)/rai_2",data)
        ret = pre + itemlink + "/" + cid[2] + "/17.m3u8?fuseau=5400"
    elif cid[2] == "rai_4":
        itemlink = common.find_param(pre + "tvone/(.*?).m3u8",data)
        ret = pre + "tvone/" +itemlink + ".m3u8"
    else:
        if cid[2] == "tf11" or cid[2] == "hd1":
            itemlink = common.find_param(pre + cid[2] + "/(.*?).m3u8'",data)
            ret = pre + cid[2] + "/" + itemlink + '.m3u8'
            xbmc.log("##### ret = " + ret,xbmc.LOGNOTICE)
            
        elif cid[2] == "rmc-decouverte":
            itemlink = common.find_param(pre + "(.*?)/rmc-decouverte.m3u8'",data)
            ret = pre + itemlink + '/rmc-decouverte.m3u8'
            xbmc.log("##### ret = " + ret,xbmc.LOGNOTICE)
            
        #elif cid[1] == "fr" and cid[2].find("France_")>-1:
        #    itemlink = common.find_param(pre + "francetv2017/(.*?)/" + cid[2],data)
        #    itemlink2 = common.find_param('/' + cid[2] + '/(.*?).m3u8',data)
        #
        #    ret = pre + "francetv2017/" + itemlink + '/' + cid[2] + "/" + itemlink2 + '.m3u8'
        #    xbmc.log("##### ret = " + ret,xbmc.LOGNOTICE)

        else:
            itemlink = common.find_param(pre + "(.*?)/" + cid[2],data)
    
            #xbmc.log("##### itemlink = " + itemlink,xbmc.LOGNOTICE)
    
            if cid[2] == "arte" or cid[2] == "103" or cid[2] == "101":
                ret = pre + itemlink + "/" + cid[2] + ".m3u8?quality=high"
                #xbmc.log("##### itemlink = " + ret,xbmc.LOGNOTICE)
            else:
                ret = pre + itemlink + "/" + cid[2] + "/17.m3u8?fuseau=300" 
                xbmc.log("##### itemlink = " + ret,xbmc.LOGNOTICE)
    return ret

def getIpBoxList(string="",live=False):
    ret=[]
    try:
        servers=common.cachepage("http://pastebin.com/raw/GrYKMHrF",3650)
        servers=servers.splitlines()

        import time
        for ln in servers:
            if not ln.startswith("##") and len(ln)>0:
                try:
                    print 'ln',ln
                    servername,surl=ln.split('$')
                    
                    if not servername.startswith("---"):
                        if '[gettext]' in surl:
                            surl,fileheaders,playheaders=surl.split('|')
                            surl = common.cachepage(surl.replace('[gettext]',''),3600)
                            if ' ' in surl or '>' in surl:
                                surl=surl.replace(' ','%20')
                                surl=surl.replace('>','%3E')
                                surl=surl.replace('<','%3C')
                            
                            try:
                                playheaders = playheaders.split("=")[1]
                                surl = surl + "|User-Agent=" + common.OpenURL(playheaders)
                            except:
                                pass
                            
                        if string == "":
                            typ = "- [COLOR yellow][mpeg][/COLOR]"
                            if surl.find("output=hls")>-1:
                                typ = "- [COLOR pink][hls][/COLOR]"
                                
                            AddDir("[B][COLOR green]" + servername + " List[/COLOR][/B] " + typ, surl, 51, iconlist, isFolder=True)
                        else:
                            sch_m3u(surl,string,servername,live=live)
                        
                except: traceback.print_exc(file=sys.stdout)
    except:
        traceback.print_exc(file=sys.stdout)


##########################
# First One TV
##########################

def json2list(page1):
    page1 = page1.replace('{','').replace('}','').replace('"','').split(',')
    return page1

def Firstone(chid,country):
    import requests
    UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    base = 'http://www.firstone.tv/'
    api = "https://www.firstone.tv/api/"
    args1 = "?action=hiro&result=get"
    url = urllib2.Request(api+args1)
    url.add_header('User-Agent',UA)
    url.add_header('Referer',base)
    url = urllib2.urlopen(url)
    page=url.read()
    url.close()
    xbmc.log("##### fiestonetv = " + page,xbmc.LOGNOTICE)
    page = json2list(page)
    for i in page:
        if i.find('[]);')>-1:
            n=page.index(i)
            page[n]='hiro:0'
    hash1 = page[4].split('hash:')[1]
    time1 = page[5].split('time:')[1]
    rss1 = page[6].split('rss:')[1]
    args2 = '?action=hiro&result='+rss1+'&time='+time1+'&hash='+hash1
    url2 = urllib2.Request(api+args2)
    url2.add_header('User-Agent',UA)
    url2.add_header('Referer',base)
    url2 = urllib2.urlopen(url2)
    page2=url2.read()
    url2.close
    page2 = json2list(page2)
    ctoken=page2[3].split('ctoken:')[1]
    #print ctoken
    args3 = '?action=channel&ctoken='+ctoken+'&c='+country+'&id='+chid
    #print api+args3
    url3 = urllib2.Request(api+args3)
    url3.add_header('User-Agent',UA)
    url3.add_header('Referer',base)
    url3 = urllib2.urlopen(url3)
    page3 = url3.read()
    url3.close()
    page3 = json2list(page3)
    n2 = 0
    for i in page3:
        page3[n2] = page3[n2].replace("\\",'')
        n2 +=1
    for i in page3:
        if i.find('surl')>-1:
            play = i[i.find('http:'):]
    return play

def Get_url_fotv(cid):
    cid = cid.split(":")
    return Firstone(cid[1],cid[2])

##########################
# Youtube Playlist

def Yplayl(url,string="",live=False):
    if url.find("dm://")>-1:
        url = url.replace("dm://","")
        Daiplayl(url,string,live)
    else:
        youdir = os.path.join(xbmc.translatePath("special://home/addons/"),'plugin.video.youtube')
        if not os.path.exists(youdir):
            if string == "":
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("For this feature you need to install","[B][COLOR violet]Youtube video plugin[/COLOR][/B]", 6800, icon))
        else:
            
            if not string == "":
                listName = "  " + "[CR][I][COLOR blue][LIGHT]Youtube-Playlist[/COLOR] -->  [COLOR yellow]{0}[/COLOR][/I][/LIGHT]".format(url)

            url1 = "https://www.youtube.com/playlist?list=" + url    
            data = common.cachepage(url1,1200,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
            try:
                url2 = "https://www.youtube.com" + common.find_param('data-uix-load-more-href="([^",]+)',data)
                #xbmc.log("****** url2 = " + url2, xbmc.LOGNOTICE)
                data2 = common.cachepage(url2,1200,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
                data2 = data2.replace("\\","").replace("u0026#39;","'").replace("u0026amp;","&")
                #xbmc.log("****** data2 = " + data2, xbmc.LOGNOTICE)
                data = data + data2
            except:
                pass
            patron = 'data-title="([^"]+)(.*?)data-thumb="([^"]+)(.*?)data-video-ids="([^"]+)'
            matches = re.compile(patron, re.DOTALL).findall(data)
            
            for scrapedtitle, sep, thumb, sep2, scrapedvid in matches:
                scrapedtitle = common.decodeHtmlentities(scrapedtitle).strip()
                titolo = "[COLOR pink]" + scrapedtitle + "[/COLOR]"
                url = "plugin://plugin.video.youtube/play/?video_id=" + scrapedvid
                
                img = "https://i.ytimg.com/vi/" + scrapedvid + "/hqdefault.jpg"
                fanart = "https://i.ytimg.com/vi/" + scrapedvid + "/maxresdefault.jpg"        
                if not thumb.find("no_thumbnail")>-1:
                    if string == "":
                        AddDir(titolo,url,3,img,background=fanart,isFolder=False)
                    else:
                        sname = scrapedtitle.replace("_"," ").replace("%20"," ").lower()
                        if sname.find(string)>-1:
                            titolo = "[COLOR orangered]" + scrapedtitle + "[/COLOR]" + listName
                            AddDir(titolo,url,3,img,background=fanart,isFolder=False)

##########################
# Dailymotion Playlist

def Daiplayl(url,string="",live=False):
    
    id = url
    
    if not string == "":
        listName = "  " + "[CR][I][COLOR blue][LIGHT]Dailymotion-Playlist[/COLOR] -->  [COLOR yellow]{0}[/COLOR][/I][/LIGHT]".format(url)
    
    url = "https://api.dailymotion.com/playlist/" + id + "?fields=description,name,thumbnail_url,videos_total,"    
    data = common.cachepage(url,7200,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})    
    totv = int(common.find_param('"videos_total":([^,]+)(.*?)}',data))    
    #thumb = common.find_param('"thumbnail_url": ([^,]+)(.*?)}',data)
    pgn = totv/100
    import math
    #xbmc.log("##### Number of item = " + str(totv),xbmc.LOGNOTICE) 
    pgn = int(pgn)+1
    #xbmc.log("##### Number of pages = " + str(pgn),xbmc.LOGNOTICE) 
    cic = range(1,pgn+1)
    for count in cic:
        url = "https://api.dailymotion.com/playlist/" + id + "/videos?fields=id,thumbnail_1080_url,thumbnail_480_url,title,&sort=recent&page=" + str(count) + "&limit=100"
        xbmc.log("##### url = " + url,xbmc.LOGNOTICE) 
        data = common.cachepage(url,3600,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
        data = data.decode('unicode_escape').encode('iso-8859-1').replace("\/","/")
        patron = 'id":"([^"]+)(.*?)"thumbnail_1080_url":"([^"]+)(.*?)"thumbnail_480_url":"([^"]+)(.*?)"title":"([^"]+)'
        matches = re.compile(patron, re.DOTALL).findall(data)     
        
        for scrapedvid, sep1, fanart, sep2, img, sep3, scrapedtitle in matches:
            scrapedtitle = common.decodeHtmlentities(scrapedtitle).strip()
            #xbmc.log("##### scrapedtitle = " + scrapedtitle,xbmc.LOGNOTICE)
            titolo = "[COLOR pink]" + scrapedtitle + "[/COLOR]"
            url = "dm://" + scrapedvid
            if string == "":
                AddDir(titolo,url,3,img,background=fanart,isFolder=False)            
            else:
                sname = scrapedtitle.replace("_"," ").replace("%20"," ").lower()
                if sname.find(string)>-1:
                    titolo = "[COLOR orangered]" + scrapedtitle + "[/COLOR]" + listName
                    AddDir(titolo,url,3,img,background=fanart,isFolder=False)            
            
##########################
# Luci Rosse

def Pornazzi(url):
    
    if url == "index":
        urlbase = "http://www.pornhd.com/category"
        data = common.cachepage(urlbase,360000,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
        patron = 'data-original="([^"]+)[^<]+[^<]+</span>(.*?)</a>'
        matches = re.compile(patron, re.DOTALL).findall(data)

        for scrapedimg, scrapedtitle in matches:
        
            scrapedtitle = common.decodeHtmlentities(scrapedtitle).strip()
            titolo = "[COLOR pink] " + scrapedtitle + "[/COLOR]"
            url = urlbase + "/" + scrapedtitle.replace(" ","-").lower() + "-videos"
            
            FastDir(titolo,url,77,scrapedimg,fanart="http://3da9975e9b4bda14573affe3f9f02618.lswcdn.net/343/Zy8RGV1LK7/1280x720new/37.jpg", isFolder=True)
    else:
        data = common.cachepage(url,360000,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
        patron = 'src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7".*?data-original="([^"]+)[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<.*?title" href="(.*?)">(.*?)</a>'
        urlbase = "http://www.pornhd.com"
        
        matches = re.compile(patron, re.DOTALL).findall(data)
 
        for scrapedimg, scrapedlink, scrapedtitle in matches:

            scrapedtitle = common.decodeHtmlentities(scrapedtitle).strip()
            titolo = "[COLOR gold] " + scrapedtitle + "[/COLOR]"          
            link = urlbase + scrapedlink
            fanart = scrapedimg.replace("320x180new","1280x720new")
            
            AddDir(titolo,link,3,scrapedimg,background=fanart, isFolder=False)
        
        n = re.search("Videos \(([^\),]+)", data) 
        N = int(int(n.group(1))/96)
        
        if not url.find("?page=")>-1:
            link = url + "?page=2"
            numb = 1
        else:
            urlb = url.split("?page=")
            link = urlb[0]
            numb = int(urlb[1])+1
            link = link + "?page=" + str(numb)
        
        if not numb>N:
            FastDir("[B] NEXT PAGE >>> [/B]",link,77,"http://c88016e5e72cbf2a8fd798c753f8a45a.lswcdn.net/139/fftJZJnQrF/320x180new/81.jpg",fanart="http://c88016e5e72cbf2a8fd798c753f8a45a.lswcdn.net/139/fftJZJnQrF/1280x720new/81.jpg", isFolder=True)
  
##########################
# Oggi in TV

def tvoggi(url):
    
    urlbase = "http://www.comingsoon.it/filmtv"
    
    #if url == "/":
    #    t = 159
    #else:
    #    t = 359
    
    data = common.OpenURL(urlbase + url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
    
    patron = '<div class="col-xs-5 box-immagine">[^<]+<img src="([^"]+)[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<.*?titolo">(.*?)</div>[^<]+<div class="h5 ora-e-canale">[^<]+<span>(.*?)</span><br />(.*?)<[^<]+</div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, scrapetime, scrapedtv in matches:

        scrapedtitle = common.decodeHtmlentities(scrapedtitle).strip()
        titolo = scrapetime + " : [COLOR gold] " + scrapedtitle + "[/COLOR] - [COLOR orange] " + scrapedtv + "[/COLOR]"
        url = scrapedtv.lower() 
        url = url.replace("la2","la 2").replace("la1","la 1")
        
        FastDir(titolo,url,73,icon=scrapedthumbnail,fanart="http://www.ore12.net/wp-content/uploads/2016/08/cinema.jpg")

       
def SetteGiorniTV(day=""):
    if day == "":
        import datetime
        from datetime import date, timedelta
        start = date.today()
        icon = ""
        
        Link = ["/","/domani/","/dopodomani/","/giorno-3/","/giorno-4/","/giorno-5/","/giorno-6/"]
        Days = ["Oggi","Domani","Dopodomani","Fra 3 giorni","Fra 4 giorni","Fra 5 giorni","Fra 6 giorni"]
        
        AddDir("[COLOR gold][B]" + str(date.today()) + " - Film in TV " + Days[0] + "[/B][/COLOR]", Link[0], 75, icon, isFolder=True)
        for add in range(1, 7):
            future = start + timedelta(days=add)
            AddDir("[COLOR gold][B]" + str(future) + " - Film in TV " + Days[add] + "[/B][/COLOR]", Link[add], 75, icon, isFolder=True)
    else:
        if day == "/":
            AddDir("[COLOR red][B]ORA IN ONDA[/B][/COLOR]", day, 74, "http://a2.mzstatic.com/eu/r30/Purple/v4/3d/63/6b/3d636b8d-0001-dc5c-a0b0-42bdf738b1b4/icon_256.png", isFolder=True) 
        AddDir("[COLOR azure][B]Mattina[/B][/COLOR]", day + "?range=mt", 74, "http://www.creattor.com/files/23/787/morning-pleasure-icons-screenshots-17.png", isFolder=True)
        AddDir("[COLOR azure][B]Pomeriggio[/B][/COLOR]", day + "?range=pm", 74, "http://icons.iconarchive.com/icons/custom-icon-design/weather/256/Sunny-icon.png", isFolder=True)
        AddDir("[COLOR azure][B]Preserale[/B][/COLOR]", day + "?range=pr", 74, "https://s.evbuc.com/https_proxy?url=http%3A%2F%2Ftriumphbar.com%2Fimages%2Fhappyhour_icon.png&sig=ADR2i7_K2FSfbQ6b3dy12Xjgkq9NCEdkKg", isFolder=True)
        AddDir("[COLOR azure][B]Prima serata[/B][/COLOR]", day + "?range=ps", 74, "http://icons.iconarchive.com/icons/icons-land/vista-people/256/Occupations-Pizza-Deliveryman-Male-Light-icon.png", isFolder=True)
        AddDir("[COLOR azure][B]Seconda serata[/B][/COLOR]", day + "?range=ss", 74, "http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png", isFolder=True)
        AddDir("[COLOR azure][B]Notte[/B][/COLOR]", day + "?range=nt", 74, "http://icons.iconarchive.com/icons/oxygen-icons.org/oxygen/256/Status-weather-clear-night-icon.png", isFolder=True)
        
################################################################################################
# Ricerca aggiornamenti 

def checkforupdates(url,loc,aut):
    import ziptools
    xbmc.log('Start check for updates')
    try:
        data = urllib2.urlopen(url).read()
        #xbmc.log('read xml remote data:' + data,xbmc.LOGNOTICE)
    except:
        data = ""
        xbmc.log('fail read xml remote data:' + url, xbmc.LOGNOTICE)
    try:
        f = open(loc,'r')
        data2 = f.read().replace("\n\n", "")
        f.close()
        #xbmc.log('read xml local data:' + data2, xbmc.LOGNOTICE)
    except:
        data2 = ""
        xbmc.log('fail read xml local data', xbmc.LOGNOTICE)

    version_publicada = common.find_single_match(data,"<version>([^<]+)</version>").strip()
    tag_publicada = common.find_single_match(data,"<tag>([^<]+)</tag>").strip()

    version_local = common.find_single_match(data2,"<version>([^<]+)</version>").strip()
    tag_local = common.find_single_match(data,"<tag>([^<]+)</tag>").strip()

    try:
        numero_version_publicada = int(version_publicada)
        xbmc.log('number remote version:' + version_publicada, xbmc.LOGNOTICE)
        numero_version_local = int(version_local)
        xbmc.log('number local version:' + version_local, xbmc.LOGNOTICE)
    except:
        version_publicada = ""
        xbmc.log('number local version:' + version_local, xbmc.LOGNOTICE)
        xbmc.log('Check fail !@*', xbmc.LOGNOTICE)
            
    if version_publicada!="" and version_local!="":
        if (numero_version_publicada > numero_version_local):

            extpath = os.path.join(xbmc.translatePath("special://home/addons/")) 
            dest = addon_data_dir + '/lastupdate.zip'                
            UPDATE_URL = 'https://github.com/vania70/Kodi-Live-TV/raw/master/plugin.video.kodilivetv-' + tag_publicada + '.zip'
            xbmc.log('START DOWNLOAD UPDATE:' + UPDATE_URL, xbmc.LOGNOTICE)
                
            DownloaderClass(UPDATE_URL,dest)  

            import ziptools
            unzipper = ziptools.ziptools()
            unzipper.extract(dest,extpath)
                
            line7 = 'New version installed .....'
            line8 = 'Version: ' + tag_publicada 
            xbmcgui.Dialog().ok('Kodi Live TV', line7, line8)
                
            if os.remove( dest ):
                xbmc.log('TEMPORARY ZIP REMOVED', xbmc.LOGNOTICE)
            xbmc.executebuiltin("UpdateLocalAddons")
            xbmc.executebuiltin("UpdateAddonRepos")
            xbmc.sleep(1500)

    url = REMOTE_VERSION_FILE2
    loc = LOCAL_VERSION_FILE2
        
    try:
        data = urllib2.urlopen(url).read()
        #xbmc.log('read xml remote data:' + data, xbmc.LOGNOTICE)
    except:
        data = ""
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName,"Check for updates fail !", 3600, icon))
        xbmc.log('fail read xml remote data:' + url, xbmc.LOGNOTICE)
    try:
        f = open(loc,'r')
        data2 = f.read().replace("\n\n", "")
        f.close()
        #xbmc.log('read xml local data:' + data2, xbmc.LOGNOTICE)
    except:
        data2 = ""
        xbmc.log('fail read xml local data', xbmc.LOGNOTICE)
            
    version_publicada = common.find_single_match(data,"<version>([^<]+)</version>").strip()
    tag_publicada = common.find_single_match(data,"<tag>([^<]+)</tag>").strip()

    version_local = common.find_single_match(data2,"<version>([^<]+)</version>").strip()
    dinamic_url = common.find_single_match(data,"<url>([^<]+)</url>").strip()
        
    try:
        numero_version_publicada = int(version_publicada)
        xbmc.log('number remote version:' + version_publicada, xbmc.LOGNOTICE)
        numero_version_local = int(version_local)
        xbmc.log('number local version:' + version_local, xbmc.LOGNOTICE)
    except:
        version_publicada = ""
        xbmc.log('number local version:' + version_local, xbmc.LOGNOTICE)
        xbmc.log('Check fail !@*', xbmc.LOGNOTICE)
        u = True
            
    if version_publicada!="" and version_local!="":
        if (numero_version_publicada > numero_version_local):

            extpath = os.path.join(xbmc.translatePath("special://home/addons/")) 
            dest = addon_data_dir + '/temp.zip'  
            
            xbmc.log('START DOWNLOAD PATCH : ' + dinamic_url, xbmc.LOGNOTICE)         
            urllib.urlretrieve(dinamic_url,dest)
            xbmc.sleep ( 150 )
            
            import ziptools
            unzipper = ziptools.ziptools()
            unzipper.extract(dest,extpath)
            xbmc.log('EXTRACT PATCH ' + version_publicada, xbmc.LOGNOTICE) 
            
            line7 = 'Plugin data updated .....'
            line8 = 'Description: ' + tag_publicada
            xbmcgui.Dialog().ok('Kodi Live TV', line7, line8)
                    
            if os.remove( dest ): 
                xbmc.log('TEMPORARY ZIP REMOVED', xbmc.LOGNOTICE)
            xbmc.executebuiltin("UpdateLocalAddons")
            xbmc.executebuiltin("UpdateAddonRepos")
            u = False
        else:
            xbmc.log('Partial updates not available', xbmc.LOGNOTICE)
            u = True
                        
    if aut<1 and u:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(localizedString(10106).encode('utf-8') + " :",localizedString(10044).encode('utf-8'), 4500, icon))
        xbmc.log('Check updates:No updates are available', xbmc.LOGNOTICE)

# Ricerca automatica aggiornamenti
Tfile = os.path.join(addon_data_dir, 'time.txt')

if Addon.getSetting('autoupdate') == "true":

    if os.path.isfile(Tfile):
        t = time.time() - os.path.getmtime(Tfile)
        if t > 80000:
            try:
                checkforupdates(REMOTE_VERSION_FILE, LOCAL_VERSION_FILE,86400-t)
            except:
                pass
            common.write_file(Tfile  , '*')
    else:
        try:
            checkforupdates(REMOTE_VERSION_FILE, LOCAL_VERSION_FILE,0)
        except:
            pass
        common.write_file(Tfile  , '*')

###################

def Play_dm(id):
    
    import dailymotion, YDStreamExtractor
    Quality=2
    d = dailymotion.Dailymotion()
    video=d.get('/video/'+id+'?fields=url')
    url=video["url"]
    vid = YDStreamExtractor.getVideoInfo(url,quality=Quality) #quality is 0=SD, 1=720p, 2=1080p and is a maximum
    try:
        stream_url = vid.streamURL() #This is what Kodi (XBMC) will play
        stream_url=stream_url.split("|")[0]

        listitem = xbmcgui.ListItem(path=stream_url)  
        xbmcplugin.setResolvedUrl(int(sys.argv[1]),True, listitem) 
    except:
        xbmc.executebuiltin('XBMC.Notification("Kodi Live TV","VideoURL not found")')    
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

###################

def ytdl_extract(url):
    from youtube_dl import YoutubeDL
    ytdl = YoutubeDL()
    info = ytdl.extract_info(url, download=False)
    return info[url]

###################

def Play_f4mProxy(url, name, iconimage):
    
    #maxbitrate = Addon.getSetting('BitRateMax')
    maxbitrate = "0"
    #if Addon.getSetting('use_simple') == "true":
    #    simpledownloader = True
    #else:
    simpledownloader = False
    sys.path.insert(0, f4mProxy)
    from F4mProxy import f4mProxyHelper
    player=f4mProxyHelper()
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
    
    if streamtype == "HLS":
        maxbitrate = 9000000
    player.playF4mLink(url, name, None, True, maxbitrate, simpledownloader, None, streamtype, False, None, None, None, iconimage)    
    
####################

def get_params():
    
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?','')
        if (params[len(params)-1] == '/'):
                params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
                splitparams = {}
                splitparams = pairsofparams[i].split('=')
                if (len(splitparams)) == 2:
                        param[splitparams[0].lower()] = splitparams[1]
    return param

params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
station = None
user_id = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass
try:        
    mode = int(params["mode"])
except:
    pass
try:        
    user_id = params["userid"]
except:
    pass
try:        
    rec_id = params["recid"]
except:
    pass    
try:        
    station = urllib.unquote_plus(params["station"])
except:
    pass    
    
try:        
    description = urllib.unquote_plus(params["description"])
except:
    pass
try:
    streamtype = urllib.unquote_plus(params["streamtype"])
except:
    pass    

if url and url.find("l=chit") >= 0:
    from teleboy import *
    ListTB("it")
    url = None
elif url and url.find("l=chfr") >= 0:
    from teleboy import *
    ListTB("fr")
    url = None
elif url and url.find("l=chde") >= 0:
    from teleboy import *
    ListTB("de")
    url = None
elif url and url.find("l=chen") >= 0:
    from teleboy import *
    ListTB("en")
    url = None
elif url and url.find("l=oggitv") >= 0:
    SetteGiorniTV()
    xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True)
    sys.exit()    
elif url and url.find("l=pornazzi") >= 0:
    Pornazzi("index")
    xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True)
    sys.exit()     

if mode == None or url == None or len(url) < 1:
    Categories()
elif mode == 96:
    Channels()
elif mode == 97:
    Others()    
elif mode == 1:
    xml_settings = os.path.join(addon_data_dir, "settings.xml")
    if os.path.isfile(xml_settings):
        os.remove(xml_settings)
        sys.exit()
elif mode == 2:
    m3uCategory(url)
elif mode == 4 or mode == 51:
    m3uCategory(url,False)
elif mode == 63 or mode == 70:
    OpenXML(url)
elif mode == 3 or mode == 32:
    
    if url.startswith("opus") or url.startswith("enc") or url.startswith("fotv"):
        PlayUrl(name, url, iconimage)
    elif url.startswith("dm://"):
        id = url.replace("dm://","")
        Play_dm(id)
    elif url.startswith("yte://"): 
        url = url.replace("yte://","")
        url = ytdl_extract(url)
        PlayUrl(name, url, iconimage)
        
    elif url.startswith("urlr://"):
        url = url.replace("urlr://","")
        try:
            import urlr
            url = urlr.resolve(url)        
            PlayUrl(name, url, iconimage)
        except:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName,"Error: video url no found!".encode('utf-8'), 3900, icon))
            sys.exit()

    else:
        if not url.endswith(".ts") and not url.find(".ts|")>-1 and not url.endswith(".f4m") and url.find(".f4m?") < 0 and not url.endswith("Player=HLS"):
            url = common.unshortenit(url)
            url = common.urlresolve(url)
        PlayUrl(name, url, iconimage)

elif mode == 5:   
    if url.find("urhd.tv")>0:
        try:
            url = common.urhd(url)
        except:
            pass
    if url.startswith("opus"):
        url = Opus(url)    
    if url.startswith("fotv"):
        url = Get_url_fotv(url)
    
    Play_f4mProxy(url, name, iconimage)

elif mode == 6 or mode == 7:
        
    if url.startswith("urlr://"):
        url = url.replace("urlr://","")
        try:
            import urlr
            url = urlr.resolve(url).split("|")[0]        
        except:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName,"Error: video url no found!".encode('utf-8'), 3900, icon))
            sys.exit()
       
    #xbmc.log("*** Download video url = " + url, xbmc.LOGNOTICE)
    
    ext = "." + url.split('.')[-1]
    if not ext in EXTV:
        ext = ".mp4"
    fileS = DFolder + name + ext + ".stopped"
    if not os.path.isfile(fileS):
        title = localizedString(10203).encode('utf-8')
        string = common.GetKeyboardText(title, name)
        if len(string) >0:    
            common.StartDowloader(url,string,mode,DFolder)
    else:
        common.StartDowloader(url,name,mode,DFolder)
        
    #common.StartDowloader(url,name,mode,DFolder)
        
elif mode == 59:   
    common.StartDowloader(url,name,mode,DFolder)                 
elif mode == 57 or mode == 72:   
    common.StopDowloader(url,name,mode,DFolder)
elif mode == 58 or mode == 71:   
    common.DeletePartialDowload(url,name,mode,DFolder)
elif mode == 10:
    # deleted
    sys.exit()
elif mode == 20:
    AddNewList()
    sys.exit()
elif mode == 21 or mode == 54 or mode == 60 or mode == 64:
    PMFolder( url )
elif mode == 22:
    RemoveFromLists(url)
elif mode == 23:
    ChangeName(name,playlistsFile2,"name",10004)
elif mode == 24:
    ChangeUrl(url,playlistsFile2,"url",10005)
elif mode == 61:
    ChangeName(name,playlistsFile4,"name",10004)
elif mode == 95:    
    ChangeUrl2(url,playlistsFile4,"url",10005)
elif mode == 69:
    ChangeName(name,favoritesFile,"name",10004)
elif mode == 25:
    importList()
elif mode == 26:
    if os.path.isfile( playlistsFile3 ) :
        if os.path.isfile( playlistsFile2 ) : os.remove( playlistsFile2 )
        shutil.copyfile( playlistsFile3, playlistsFile2 )
        xbmc.sleep ( 200 )
        os.remove( playlistsFile3 )
        xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName,localizedString(10125).encode('utf-8'), 3600, icon)) 
    else:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName,localizedString(10126).encode('utf-8'), 3600, icon))
elif mode == 30:
    ListFavorites()
elif mode == 31: 
    AddFavorites(url, iconimage, name)
elif mode == 55:
    RemoveDirFromLists(url,name)
elif mode == 56:
    os.remove( os.path.join(pwdir, base64.standard_b64encode(url))) 
    xbmc.executebuiltin("XBMC.Container.Refresh()")
elif mode == 33:
    RemoveFavorties(url)
elif mode == 34:
    AddNewFavortie()
elif mode == 35:
    ListSub(Italian)
elif mode == 36:
    ListSub(French)
elif mode == 37:
    ListSub(German)
elif mode == 38:
    ListSub(English)
elif mode == 39:
    PM_index()
elif mode == 40:
    common.DelFile(playlistsFile2)
    sys.exit()
elif mode == 41:
    common.DelFile(favoritesFile)
    sys.exit()
elif mode == 42:
    write_xml()
    sys.exit()
elif mode == 43:
    restore_xml()
    sys.exit()   
elif mode == 44:
    remove_xml()
    sys.exit()
elif mode == 45:        
    clean_cache()
    sys.exit()
elif mode == 46:       
    checkforupdates(REMOTE_VERSION_FILE, LOCAL_VERSION_FILE,0)
    if Addon.getSetting('autoupdate') == "true":
        common.write_file(Tfile , '*')        
    sys.exit()
elif mode == 47:
    xbmc.executebuiltin("StopPVRManager")
    xbmc.executebuiltin("StartPVRManager") 
    sys.exit()
elif mode == 48:
    common.Open_Netflix()        
elif mode == 49:
    common.Open_Paypal()
elif mode == 50:
    print '--- Playing "{0}". {1}'.format(name, url)
    listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
    listitem.setInfo(type="Video", infoLabels={ "Title": name })
    xbmc.Player().play( url , listitem)
elif mode == 52:
    common.DeleteFile(url,name)
elif mode == 53:
    string = common.GetKeyboardText(localizedString(10203).encode('utf-8'), name)
    if len(string) < 1:
        sys.exit()
    else:
        nurl = url.replace(name,string)
        xbmcvfs.rename(os.path.join(url) ,os.path.join(nurl))
        xbmc.executebuiltin("XBMC.Container.Refresh()")
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10202).encode('utf-8'), 5200, icon))
        sys.exit()
elif mode == 62:
    cook = os.path.join(addonDir,'resources','cookie.dat')
    if os.path.isfile(cook):
        os.remove(cook)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ","Teleboy cookie has been deleted!", 4700, icon))
    sys.exit()
elif mode == 65 or mode == 81:
    title = localizedString(10250).encode('utf-8')
    string = common.GetKeyboardText(title, "")
    if len(string) >0:
        string = string.lower()
        if url == "search1":
            sch_global(string)
        elif url == "search2":
            sch_global_PM(string)
        elif url == "search3":    
            sch_index(string)
        elif mode == 81:
            findm3u(url, string)
        else:
            sch_folder(url,string)
elif mode == 66:
    title = localizedString(10250).encode('utf-8')
    string = common.GetKeyboardText(title, "")
    if len(string) >0:
        sch_xml(url,string)

elif mode == 73:
    sch_filmtvit(url,live=True)
#elif mode == 76:
    #sch_global(name,live=False)
elif mode == 67:
    sch_exclude(url, playlistsFile4, "yes")
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ","Folder " + name + " to global research excluded!", 4000, icon))
    sys.exit()
elif mode == 68:
    sch_exclude(url, playlistsFile4, "")
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ","Folder " + name + " to global research included!", 4000, icon))
    sys.exit()
elif mode == 74:
    tvoggi(url)
elif mode == 75:    
    SetteGiorniTV(url)
elif mode == 77:
    Pornazzi(url)
    xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode == 78:
    import FreeTV
    FreeTV.PlayOtherUrl ( url, name )

##########################
# Teleboy

elif mode == 27:
    from teleboy import *
    try:
        json = get_videoJson( user_id, station)
        if not json:
            exit( 1)

        title = json["data"]["epg"]["current"]["title"]
        url = json["data"]["stream"]["url"]
        if not url: 
            exit( 1)
        img = get_stationLogoURL( station )
        Player = xbmcaddon.Addon('plugin.video.kodilivetv').getSetting('player')
        if  Addon.getSetting('player') == "true":
            play_url2( url, title, img )  
        else:
            play_url( url, title, img )
    except:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName, "Swiss IP needed. Your bags ready!", 3600, icon))
elif mode == 28:
    from teleboy import *
    show_recordings(user_id)
    #make_list()
elif mode == 29:
    from teleboy import *
    url = "stream/record/%s" % rec_id
    json    = fetchApiJson( user_id, url)
    title = json["data"]["record"]["title"]
    url   = json["data"]["stream"]["url"]
    img = REC_ICON
    play_url( url, title, img )
elif mode == 79:
    findm3u(url)
elif mode == 80:
    import control
elif mode == 90:
    TestCheck = ""
    TestCheck = common.find_lpanel(url)

    if not TestCheck == "":
        
        panel =  common.OpenURL(TestCheck,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
        
        s = common.find_param('"status" *: *"([^",]+)',panel)
        if s == "":
            s = "unknown"
        status = "Status : " + s
        
        try:
            exp_date = "Exp. date : " + str(time.ctime(int(common.find_param('"exp_date" *: *"([^",]+)',panel))))
        except:
            exp_date = "Exp. date : unknown"
        try:    
            created_at = "Created at : " + str(time.ctime(int(common.find_param('"created_at" *: *"([^",]+)',panel))))
        except:
            created_at = "Created at : unknown"
            
        active_cons = "Active connections : " + common.find_param('"active_cons" *: *"([^",]+)',panel)
        max_connections = "Max connections : " + common.find_param('"max_connections" *: *"([^",]+)',panel) 
        
        Line = status + "\n" + created_at + "\n" + exp_date + "\n" + max_connections + " - " + active_cons
        
        common.OKmsg(name,Line)
elif mode == 91:
    zip_PM_data()
elif mode == 92:
    unzip_PM_data()
elif mode == 93 or mode == 98:
    Yplayl(url)
elif mode == 94:
    TempName = base64.standard_b64encode(url)
    tmp = os.path.join(cdir, TempName)
    if os.path.isfile(tmp):
        common.DelFile(tmp)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('[COLOR yellow]' +name + '[/COLOR]', 'Cache file was deleted!', 4000, icon))
        xbmc.executebuiltin("XBMC.Container.Refresh()")

###########################
#end directory
xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True)
