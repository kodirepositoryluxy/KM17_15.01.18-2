import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,urlresolver,liveresolver

addon_id            = 'plugin.video.evilplayer'
AddonTitle          = '[COLOR yellowgreen]Evil Player[/COLOR]'
fanart              = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon                = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
dialog              = xbmcgui.Dialog()
dp                  = xbmcgui.DialogProgress()
HISTORY             = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'history.xml'))
DATA_FOLDER         = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
F4M                 = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.f4mTester'))
HOME                = xbmc.translatePath(os.path.join('special://home'))

def GetMenu():

	if not os.path.exists(DATA_FOLDER):
		os.makedirs(DATA_FOLDER)

	if not os.path.isfile(HISTORY):
		f = open(HISTORY,'w')
		f.write('#START OF FILE#')
		f.close()

	addDir('[COLOR khaki]Aggiungi indirizzo internet.............[/COLOR]','none',1,icon,fanart)
	addDir('[COLOR khaki]Aggiungi file.............[/COLOR]','none',4,icon,fanart)
	addLink('[COLOR lime]Formati Supportati: TS, M3U, M3U8, MP4, AVI, MKV, MP3 and MORE![/COLOR]','none',999,icon,fanart)
	addLink('[COLOR white]################HISTORY###################[/COLOR]','none',999,icon,fanart)
	addLink('[COLOR red]Cancella cronologia[/COLOR]','none',3,icon,fanart)

	f = open(HISTORY,mode='r'); msg = f.read(); f.close()
	msg = msg.replace('\n','')
	match = re.compile('<link>(.+?)</link>').findall(msg)
	for url in match:
		addLink('[COLOR powderblue]' + url + '[/COLOR]',url,1,icon,fanart)
	xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_Local_File():

	url = dialog.browse(1, AddonTitle, 'files', '', False, False, HOME)
	
	if '.m3u' in url:
		if not 'm3u8' in url:
			List_M3U8(url)
		else:
			Player(url,url,icon)
	else:
		Player(url,url,icon)
	
def Clear_History():

	if os.path.isfile(HISTORY):
		choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR white]Vuoi cancellare tutti i tuoi history?[/COLOR]','',yeslabel='[COLOR lime]YES[/COLOR]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 1:
			os.remove(HISTORY)
			f = open(HISTORY,'w')
			f.write('#START OF FILE#')
			f.close()
	xbmc.executebuiltin("Container.Refresh")

def Find_Out(url):

	if url == "none":

		string =''
		keyboard = xbmc.Keyboard(string, 'Enter The URL To Play')
		keyboard.doModal()
		if keyboard.isConfirmed():
			string = keyboard.getText().replace(' ','')
			if not (string == "") or (string == " "):
				passed = 0
				starts = ['http','rmtp','plugin']

				for type in starts:
					if type in string:
						passed = 1
				
				if not passed == 1:
					dialog.ok(AddonTitle, "Unsupported URL or File Type detected.")
					quit()
				else: url = string
			else: quit()

	if '.m3u' in url:
		if not 'm3u8' in url:
			List_M3U8(url)
		else:
			Player(name,url,iconimage)
	else:
		Player(name,url,iconimage)

def List_M3U8(url):

    original = url
    list = CREATE_M3U_LIST(url)

    a=open(HISTORY).read()
    b=a.replace('<link>'+url+'</link>','')
    f= open(HISTORY, mode='w')
    f.write(str(b))
    f.close()
    a=open(HISTORY).read()
    b=a.replace('#START OF FILE#', '#START OF FILE#\n<link>'+url+'</link>')
    f= open(HISTORY, mode='w')
    f.write(str(b))
    f.close()

    for channel in list:
        name = GetEncodeString(channel["display_name"])
        url = GetEncodeString(channel["url"])
        url = url.replace('\\r','').replace('\\t','').replace('\r','').replace('\t','').replace(' ','').replace('m3u8','m3u8')
        ext = url.split('.')[-1]
        try:
            ext = ext.split('?')[0]
        except: pass
        try:
            ext = ext.split('%')[0]
        except: pass
        addLink('[COLOR yellowgreen]' + ext.upper() + '[/COLOR] - ' + name ,url, 2, icon, fanart,'')

def CREATE_M3U_LIST(url):

    if not 'http' in url:
        response=open(url).read()
    else:
		try:
			response = open_url(url)
		except:
			dialog.ok(AddonTitle, "There was an error opening the url. Please try another link.")
			quit()
    response = response.replace('#AAASTREAM:','#A:')
    response = response.replace('#EXTINF:','#A:')
    matches=re.compile('^#A:-?[0-9]*(.*?),(.*?)\n(.*?)$',re.I+re.M+re.U+re.S).findall(response)
    li = []
    for params, display_name, url in matches:
        item_data = {"params": params, "display_name": display_name, "url": url}
        li.append(item_data)
    list = []
    for channel in li:
        item_data = {"display_name": channel["display_name"], "url": channel["url"]}
        matches=re.compile(' (.+?)="(.+?)"',re.I+re.M+re.U+re.S).findall(channel["params"])
        for field, value in matches:
            item_data[field.strip().lower().replace('-', '_')] = value.strip()
        list.append(item_data)
	
    return list

def GetEncodeString(str):
	try:
		import chardet
		str = str.decode(chardet.detect(str)["encoding"]).encode("utf-8")
	except:
		try:
			str = str.encode("utf-8")
		except:
			pass
	return str

def Player(name,url,iconimage):

	dp.create(AddonTitle, "Opening.......", "Please Wait...")
	if "m3u8" in url:
		a=open(HISTORY).read()
		b=a.replace('<link>'+url+'</link>','')
		f= open(HISTORY, mode='w')
		f.write(str(b))
		f.close()
		a=open(HISTORY).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<link>'+url+'</link>')
		f= open(HISTORY, mode='w')
		f.write(str(b))
		f.close()
	elif not "m3u" in url:
		a=open(HISTORY).read()
		b=a.replace('<link>'+url+'</link>','')
		f= open(HISTORY, mode='w')
		f.write(str(b))
		f.close()
		a=open(HISTORY).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<link>'+url+'</link>')
		f= open(HISTORY, mode='w')
		f.write(str(b))
		f.close()
	
	if not 'f4m'in url:
		if '.m3u8'in url:
			url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+name+'&amp;url='+url		
		elif '.ts'in url:
			url = url.replace('.ts','.m3u8')
			url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+name+'&amp;url='+url		
		elif '.mpegts'in url:
			url = url.replace('.mpegts','.m3u8')
			url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+name+'&amp;url='+url	

	if "plugin://" in url:
		if not os.path.exists(F4M):
			dialog.ok('[COLOR red]F4M TESTER NOT INSTALLED![/COLOR]', "This link requires F4M Tester be installed. Please install F4M from the Shani Repo at http://fusion.tvaddons.ag")
			quit()

	if urlresolver.HostedMediaFile(url).valid_url(): 
		stream_url = urlresolver.HostedMediaFile(url).resolve()
		liz = xbmcgui.ListItem(url,iconImage=icon, thumbnailImage=icon)
		liz.setPath(stream_url)
		dp.close()
		xbmc.executebuiltin("Container.Refresh")
		xbmc.Player ().play(stream_url, liz, False)
		quit()
	elif liveresolver.isValid(url)==True: 
		stream_url=liveresolver.resolve(url)
		liz = xbmcgui.ListItem(url,iconImage=icon, thumbnailImage=icon)
		liz.setPath(stream_url)
		dp.close()
		xbmc.executebuiltin("Container.Refresh")
		xbmc.Player ().play(stream_url, liz, False)
		quit()
	else:
		if 'http' in url:
			url = url + '|User-Agent=Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
		liz = xbmcgui.ListItem(url, iconImage=icon, thumbnailImage=icon)
		dp.close()
		xbmc.executebuiltin("Container.Refresh")
		xbmc.Player ().play(url, liz, False)
		quit()

def open_url(url):

    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def addLink(name, url, mode, iconimage, fanart, description=''):

	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDir(name,url,mode,iconimage,fanart,description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                               
        return param

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
 
if mode==None or url==None or len(url)<1: GetMenu()
elif mode==1:Find_Out(url)
elif mode==2:Player(name,url,iconimage)
elif mode==3:Clear_History()
elif mode==4:Get_Local_File()

xbmcplugin.endOfDirectory(int(sys.argv[1]))