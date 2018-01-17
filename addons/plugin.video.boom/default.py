# -*- coding: utf-8 -*-
import urllib
import urllib2
import datetime
import re
import os
import base64
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import traceback
import cookielib
from BeautifulSoup import BeautifulStoneSoup , BeautifulSoup , BeautifulSOAP
try :
 import json
except :
 import simplejson as json
import SimpleDownloader as downloader
import time
import requests
import Regex
import downloader as Get_Files
import extract
if 64 - 64: i11iIiiIii
OO0o = [ '180upload.com' , 'allmyvideos.net' , 'bestreams.net' , 'clicknupload.com' , 'cloudzilla.to' , 'movshare.net' , 'novamov.com' , 'nowvideo.sx' , 'videoweed.es' , 'daclips.in' , 'datemule.com' , 'fastvideo.in' , 'faststream.in' , 'filehoot.com' , 'filenuke.com' , 'sharesix.com' , 'docs.google.com' , 'plus.google.com' , 'picasaweb.google.com' , 'gorillavid.com' , 'gorillavid.in' , 'grifthost.com' , 'hugefiles.net' , 'ipithos.to' , 'ishared.eu' , 'kingfiles.net' , 'mail.ru' , 'my.mail.ru' , 'videoapi.my.mail.ru' , 'mightyupload.com' , 'mooshare.biz' , 'movdivx.com' , 'movpod.net' , 'movpod.in' , 'movreel.com' , 'mrfile.me' , 'nosvideo.com' , 'openload.io' , 'played.to' , 'bitshare.com' , 'filefactory.com' , 'k2s.cc' , 'oboom.com' , 'rapidgator.net' , 'uploaded.net' , 'primeshare.tv' , 'bitshare.com' , 'filefactory.com' , 'k2s.cc' , 'oboom.com' , 'rapidgator.net' , 'uploaded.net' , 'sharerepo.com' , 'stagevu.com' , 'streamcloud.eu' , 'streamin.to' , 'thefile.me' , 'thevideo.me' , 'tusfiles.net' , 'uploadc.com' , 'zalaa.com' , 'uploadrocket.net' , 'uptobox.com' , 'v-vids.com' , 'veehd.com' , 'vidbull.com' , 'videomega.tv' , 'vidplay.net' , 'vidspot.net' , 'vidto.me' , 'vidzi.tv' , 'vimeo.com' , 'vk.com' , 'vodlocker.com' , 'xfileload.com' , 'xvidstage.com' , 'zettahost.tv' ]
Oo0Ooo = [ 'plugin.video.dramasonline' , 'plugin.video.f4mTester' , 'plugin.video.shahidmbcnet' , 'plugin.video.SportsDevil' , 'plugin.stream.vaughnlive.tv' , 'plugin.video.ZemTV-shani' ]
if 85 - 85: OOO0O0O0ooooo % IIii1I . II1 - O00ooooo00
class I1IiiI ( urllib2 . HTTPErrorProcessor ) :
 def http_response ( self , request , response ) :
  return response
 https_response = http_response
 if 27 - 27: iIiiiI1IiI1I1 * IIiIiII11i * IiIIi1I1Iiii - Ooo00oOo00o
I1IiI = Regex . addon
o0OOO = I1IiI . getAddonInfo ( 'version' )
iIiiiI = xbmc . translatePath ( I1IiI . getAddonInfo ( 'profile' ) . decode ( 'utf-8' ) )
Iii1ii1II11i = xbmc . translatePath ( I1IiI . getAddonInfo ( 'path' ) . decode ( 'utf-8' ) )
iI111iI = os . path . join ( iIiiiI , 'favorites' )
IiII = os . path . join ( iIiiiI , 'history' )
iI1Ii11111iIi = 'http://slimsrepo.uk/boomtest/home.xml'
i1i1II = os . path . join ( iIiiiI , 'list_revision' )
O0oo0OO0 = os . path . join ( Iii1ii1II11i , 'icon.png' )
I1i1iiI1 = os . path . join ( Iii1ii1II11i , 'fanart.jpg' )
iiIIIII1i1iI = os . path . join ( iIiiiI , 'source_file' )
o0oO0 = iIiiiI
oo00 = base64 . b64decode ( "W0NPTE9SIHJlZF1bQl1CT09NWy9DT0xPUl1bQ09MT1IgeWVsbG93XSFbL0JdWy9DT0xPUl0=" )
o00 = xbmc . translatePath ( os . path . join ( 'special://home/userdata/addon_data/plugin.video.boom' , 'favorites' ) )
downloader = downloader . SimpleDownloader ( )
Oo0oO0ooo = I1IiI . getSetting ( 'debug' )
if os . path . exists ( iI111iI ) == True :
 o0oOoO00o = open ( iI111iI ) . read ( )
else : o0oOoO00o = [ ]
if os . path . exists ( iiIIIII1i1iI ) == True :
 i1 = open ( iiIIIII1i1iI ) . read ( )
else : i1 = [ ]
if 64 - 64: oo % O0Oooo00
Ooo0 = xbmc . translatePath ( os . path . join ( 'special://home/addons' , 'plugin.video.f4mTester' ) )
if not os . path . exists ( Ooo0 ) :
 oo00000o0 = xbmcgui . Dialog ( ) . yesno ( oo00 , '[COLOR red]It is recommended that you have [B][COLOR yellow]F4M Tester[/COLOR][/B] installed for this addon to work to its full potential. Would you like to install [B][COLOR yellow]F4M Tester[/COLOR][/B] now?[/COLOR]' , '' , yeslabel = '[B][COLOR white]YES[/COLOR][/B]' , nolabel = '[B][COLOR grey]NO[/COLOR][/B]' )
 if oo00000o0 == 1 :
  I11i1i11i1I = xbmc . translatePath ( os . path . join ( 'special://home/addons' , 'packages' ) )
  if not os . path . exists ( I11i1i11i1I ) :
   os . makedirs ( I11i1i11i1I )
  Iiii = base64 . b64decode ( b'aHR0cDovL3JlZGlyZWN0LnN1cGVycmVwby5vcmcvdjcvYWRkb25zL3BsdWdpbi52aWRlby5mNG1UZXN0ZXIvcGx1Z2luLnZpZGVvLmY0bVRlc3Rlci0yLjcuMS56aXA=' )
  OOO0O = xbmcgui . DialogProgress ( )
  OOO0O . create ( oo00 , "" , "" , "Installing F4M Tester" )
  oo0ooO0oOOOOo = os . path . join ( I11i1i11i1I , 'f4m.zip' )
  if 71 - 71: O00OoOoo00
  try :
   os . remove ( oo0ooO0oOOOOo )
  except :
   pass
   if 31 - 31: iI1 + OoOooOOOO
  Get_Files . download ( Iiii , oo0ooO0oOOOOo , OOO0O )
  i11iiII = xbmc . translatePath ( os . path . join ( 'special://home' , 'addons' ) )
  time . sleep ( 2 )
  OOO0O . update ( 0 , "" , "Extracting F4M Tester Please Wait" , "" )
  extract . all ( oo0ooO0oOOOOo , i11iiII , OOO0O )
  xbmc . executebuiltin ( "UpdateAddonRepos" )
  xbmc . executebuiltin ( "UpdateLocalAddons" )
  I1iiiiI1iII = xbmcgui . Dialog ( )
  I1iiiiI1iII . ok ( oo00 , 'F4M Tester has now been installed!' , '' )
  if 20 - 20: I1 + i1Ii % o00O00O0O0O / ooO0O * ooiii11iII
  if 42 - 42: O00OoO000O + I1
OoOo = xbmc . translatePath ( os . path . join ( 'special://home/addons' , 'script.module.urlresolver' ) )
if not os . path . exists ( OoOo ) :
 oo00000o0 = xbmcgui . Dialog ( ) . yesno ( oo00 , '[COLOR red]It is recommended that you have [B][COLOR yellow]URL Resolver[/COLOR][/B] installed for this addon to work to its full potential. Would you like to install [B][COLOR yellow]URL RESOLVER[/COLOR][/B] now?[/COLOR]' , '' , yeslabel = '[B][COLOR white]YES[/COLOR][/B]' , nolabel = '[B][COLOR grey]NO[/COLOR][/B]' )
 if oo00000o0 == 1 :
  I11i1i11i1I = xbmc . translatePath ( os . path . join ( 'special://home/addons' , 'packages' ) )
  if not os . path . exists ( I11i1i11i1I ) :
   os . makedirs ( I11i1i11i1I )
  Iiii = base64 . b64decode ( b'aHR0cDovL2JyZXR0dXNidWlsZHMuY29tLy5XSElURSUyMERFVklML3doaXRlLmRldmlsLnJlcG8vZmlsZXMvc2NyaXB0Lm1vZHVsZS51cmxyZXNvbHZlci9zY3JpcHQubW9kdWxlLnVybHJlc29sdmVyLTQuMC4wOS56aXA=' )
  OOO0O = xbmcgui . DialogProgress ( )
  OOO0O . create ( oo00 , "" , "" , "Installing URL RESOLVER" )
  oo0ooO0oOOOOo = os . path . join ( I11i1i11i1I , 'f4m.zip' )
  if 34 - 34: II1 + IIii1I + i11iIiiIii - O00OoOoo00 + i11iIiiIii
  try :
   os . remove ( oo0ooO0oOOOOo )
  except :
   pass
   if 65 - 65: oo
  Get_Files . download ( Iiii , oo0ooO0oOOOOo , OOO0O )
  i11iiII = xbmc . translatePath ( os . path . join ( 'special://home' , 'addons' ) )
  time . sleep ( 2 )
  OOO0O . update ( 0 , "" , "Extracting URL RESOLVER Please Wait" , "" )
  extract . all ( oo0ooO0oOOOOo , i11iiII , OOO0O )
  xbmc . executebuiltin ( "UpdateAddonRepos" )
  xbmc . executebuiltin ( "UpdateLocalAddons" )
  I1iiiiI1iII = xbmcgui . Dialog ( )
  I1iiiiI1iII . ok ( oo00 , 'URL RESOLVER Tester has now been installed!' , '' )
  if 6 - 6: IIiIiII11i / IiIIi1I1Iiii % i1Ii
  if 84 - 84: i11iIiiIii . O0Oooo00
def o0O00oooo ( string ) :
 if Oo0oO0ooo == 'true' :
  xbmc . log ( "[addon.live.boom Lists-%s]: %s" % ( o0OOO , string ) )
  if 67 - 67: OoOooOOOO / II1 % I1 - IIii1I
  if 82 - 82: i11iIiiIii . OoOooOOOO / IiIIi1I1Iiii * OOO0O0O0ooooo % iI1 % IIii1I
def Oo00OOOOO ( url , headers = None ) :
 try :
  if headers is None :
   headers = { 'User-agent' : 'O0oO0o0o0o' }
  O0O = urllib2 . Request ( url , None , headers )
  O00o0OO = urllib2 . urlopen ( O0O )
  I11i1 = O00o0OO . read ( )
  O00o0OO . close ( )
  return I11i1
 except urllib2 . URLError , iIi1ii1I1 :
  o0O00oooo ( 'URL: ' + url )
  if hasattr ( iIi1ii1I1 , 'code' ) :
   o0O00oooo ( '[COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR] with error code - %s.' % iIi1ii1I1 . code )
   xbmc . executebuiltin ( "XBMC.Notification([COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR],We failed with error code - " + str ( iIi1ii1I1 . code ) + ",10000," + O0oo0OO0 + ")" )
  elif hasattr ( iIi1ii1I1 , 'reason' ) :
   o0O00oooo ( 'We failed to reach a server.' )
   o0O00oooo ( 'Reason: %s' % iIi1ii1I1 . reason )
   xbmc . executebuiltin ( "XBMC.Notification([COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR],We failed to reach a server. - " + str ( iIi1ii1I1 . reason ) + ",10000," + O0oo0OO0 + ")" )
   if 71 - 71: ooiii11iII . OOO0O0O0ooooo
   if 73 - 73: OoOooOOOO % oo - i1Ii
def iiIIII1i1i ( ) :
 o0O00oooo ( "SKindex" )
 iiI1 ( '[COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR] [COLOR yellow] - FAVORITES[/COLOR]' , 'Favorites' , 4 , 'https://i.imgur.com/jOo0ut5.png' , I1i1iiI1 , '' , '' , '' , '' )
 i11Iiii ( iI , '' )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 28 - 28: OoOooOOOO - ooO0O . ooO0O + oo - II1 + OOO0O0O0ooooo
 if 95 - 95: Ooo00oOo00o % iI1 . OOO0O0O0ooooo
def I1i1I ( ) :
 if os . path . exists ( iI111iI ) == True :
  iiI1 ( 'Favorites' , 'url' , 4 , os . path . join ( Iii1ii1II11i , 'resources' , 'favorite.png' ) , I1i1iiI1 , '' , '' , '' , '' )
 if I1IiI . getSetting ( "browse_xml_database" ) == "true" :
  iiI1 ( 'XML Database' , 'http://xbmcplus.xb.funpic.de/www-data/filesystem/' , 15 , O0oo0OO0 , I1i1iiI1 , '' , '' , '' , '' )
 if I1IiI . getSetting ( "browse_community" ) == "true" :
  iiI1 ( 'Community Files' , 'community_files' , 16 , O0oo0OO0 , I1i1iiI1 , '' , '' , '' , '' )
 if os . path . exists ( IiII ) == True :
  iiI1 ( 'Search History' , 'history' , 25 , os . path . join ( Iii1ii1II11i , 'resources' , 'favorite.png' ) , I1i1iiI1 , '' , '' , '' , '' )
 if I1IiI . getSetting ( "searchyt" ) == "true" :
  iiI1 ( 'Search:Youtube' , 'youtube' , 25 , O0oo0OO0 , I1i1iiI1 , '' , '' , '' , '' )
 if I1IiI . getSetting ( "searchDM" ) == "true" :
  iiI1 ( 'Search:dailymotion' , 'dmotion' , 25 , O0oo0OO0 , I1i1iiI1 , '' , '' , '' , '' )
 if I1IiI . getSetting ( "PulsarM" ) == "true" :
  iiI1 ( 'Pulsar:IMDB' , 'IMDBidplay' , 27 , O0oo0OO0 , I1i1iiI1 , '' , '' , '' , '' )
 if os . path . exists ( iiIIIII1i1iI ) == True :
  oOO00oOO = json . loads ( open ( iiIIIII1i1iI , "r" ) . read ( ) )
  if 75 - 75: O00ooooo00 / II1 - OOO0O0O0ooooo / oo . iIiiiI1IiI1I1 - O00ooooo00
  if len ( oOO00oOO ) > 1 :
   for O000OO0 in oOO00oOO :
    if 43 - 43: ooiii11iII - OOO0O0O0ooooo % IIiIiII11i . I1
    if isinstance ( O000OO0 , list ) :
     iiI1 ( O000OO0 [ 0 ] . encode ( 'utf-8' ) , O000OO0 [ 1 ] . encode ( 'utf-8' ) , 1 , O0oo0OO0 , I1i1iiI1 , '' , '' , '' , '' , 'source' )
    else :
     o00OooOooo = O0oo0OO0
     O000oo0O = I1i1iiI1
     OOOO = ''
     i11i1 = ''
     credits = ''
     IIIii1II1II = ''
     if O000OO0 . has_key ( 'thumbnail' ) :
      o00OooOooo = O000OO0 [ 'thumbnail' ]
     if O000OO0 . has_key ( 'fanart' ) :
      O000oo0O = O000OO0 [ 'fanart' ]
     if O000OO0 . has_key ( 'description' ) :
      OOOO = O000OO0 [ 'description' ]
     if O000OO0 . has_key ( 'date' ) :
      i11i1 = O000OO0 [ 'date' ]
     if O000OO0 . has_key ( 'genre' ) :
      IIIii1II1II = O000OO0 [ 'genre' ]
     if O000OO0 . has_key ( 'credits' ) :
      credits = O000OO0 [ 'credits' ]
     iiI1 ( O000OO0 [ 'title' ] . encode ( 'utf-8' ) , O000OO0 [ 'url' ] . encode ( 'utf-8' ) , 1 , o00OooOooo , O000oo0O , OOOO , IIIii1II1II , i11i1 , credits , 'source' )
     if 42 - 42: i1Ii + iI1
  else :
   if len ( oOO00oOO ) == 1 :
    if isinstance ( oOO00oOO [ 0 ] , list ) :
     i11Iiii ( oOO00oOO [ 0 ] [ 1 ] . encode ( 'utf-8' ) , I1i1iiI1 )
    else :
     i11Iiii ( oOO00oOO [ 0 ] [ 'url' ] , oOO00oOO [ 0 ] [ 'fanart' ] )
     if 76 - 76: ooiii11iII - Ooo00oOo00o
     if 70 - 70: O00OoO000O

def II1I ( url = None ) :
 if url is None :
  if not I1IiI . getSetting ( "new_file_source" ) == "" :
   O0i1II1Iiii1I11 = I1IiI . getSetting ( 'new_file_source' ) . decode ( 'utf-8' )
  elif not I1IiI . getSetting ( "new_url_source" ) == "" :
   O0i1II1Iiii1I11 = I1IiI . getSetting ( 'new_url_source' ) . decode ( 'utf-8' )
 else :
  O0i1II1Iiii1I11 = url
 if O0i1II1Iiii1I11 == '' or O0i1II1Iiii1I11 is None :
  return
 o0O00oooo ( 'Adding New Source: ' + O0i1II1Iiii1I11 . encode ( 'utf-8' ) )
 if 9 - 9: O00OoOoo00 / IiIIi1I1Iiii - IIiIiII11i / II1 / IIii1I - O0Oooo00
 o00oooO0Oo = None
 if 78 - 78: i1Ii % ooiii11iII + O00OoOoo00
 I11i1 = OOooOoooOoOo ( O0i1II1Iiii1I11 )
 print 'source_url' , O0i1II1Iiii1I11
 if isinstance ( I11i1 , BeautifulSOAP ) :
  if I11i1 . find ( 'channels_info' ) :
   o00oooO0Oo = I11i1 . channels_info
  elif I11i1 . find ( 'items_info' ) :
   o00oooO0Oo = I11i1 . items_info
 if o00oooO0Oo :
  o0OOOO00O0Oo = { }
  o0OOOO00O0Oo [ 'url' ] = O0i1II1Iiii1I11
  try : o0OOOO00O0Oo [ 'title' ] = o00oooO0Oo . title . string
  except : pass
  try : o0OOOO00O0Oo [ 'thumbnail' ] = o00oooO0Oo . thumbnail . string
  except : pass
  try : o0OOOO00O0Oo [ 'fanart' ] = o00oooO0Oo . fanart . string
  except : pass
  try : o0OOOO00O0Oo [ 'genre' ] = o00oooO0Oo . genre . string
  except : pass
  try : o0OOOO00O0Oo [ 'description' ] = o00oooO0Oo . description . string
  except : pass
  try : o0OOOO00O0Oo [ 'date' ] = o00oooO0Oo . date . string
  except : pass
  try : o0OOOO00O0Oo [ 'credits' ] = o00oooO0Oo . credits . string
  except : pass
 else :
  if '/' in O0i1II1Iiii1I11 :
   ii = O0i1II1Iiii1I11 . split ( '/' ) [ - 1 ] . split ( '.' ) [ 0 ]
  if '\\' in O0i1II1Iiii1I11 :
   ii = O0i1II1Iiii1I11 . split ( '\\' ) [ - 1 ] . split ( '.' ) [ 0 ]
  if '%' in ii :
   ii = urllib . unquote_plus ( ii )
  oOooOOOoOo = xbmc . Keyboard ( ii , 'Displayed Name, Rename?' )
  oOooOOOoOo . doModal ( )
  if ( oOooOOOoOo . isConfirmed ( ) == False ) :
   return
  i1Iii1i1I = oOooOOOoOo . getText ( )
  if len ( i1Iii1i1I ) == 0 :
   return
  o0OOOO00O0Oo = { }
  o0OOOO00O0Oo [ 'title' ] = i1Iii1i1I
  o0OOOO00O0Oo [ 'url' ] = O0i1II1Iiii1I11
  o0OOOO00O0Oo [ 'fanart' ] = O000oo0O
  if 91 - 91: O00OoOoo00 + IIiIiII11i . OoOooOOOO * O00OoOoo00 + IIiIiII11i * IiIIi1I1Iiii
 if os . path . exists ( iiIIIII1i1iI ) == False :
  O000OOOOOo = [ ]
  O000OOOOOo . append ( o0OOOO00O0Oo )
  Iiii1i1 = open ( iiIIIII1i1iI , "w" )
  Iiii1i1 . write ( json . dumps ( O000OOOOOo ) )
  Iiii1i1 . close ( )
 else :
  oOO00oOO = json . loads ( open ( iiIIIII1i1iI , "r" ) . read ( ) )
  oOO00oOO . append ( o0OOOO00O0Oo )
  Iiii1i1 = open ( iiIIIII1i1iI , "w" )
  Iiii1i1 . write ( json . dumps ( oOO00oOO ) )
  Iiii1i1 . close ( )
 I1IiI . setSetting ( 'new_url_source' , "" )
 I1IiI . setSetting ( 'new_file_source' , "" )
 xbmc . executebuiltin ( "XBMC.Notification([COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR],New source added.,5000," + O0oo0OO0 + ")" )
 if not url is None :
  if 'xbmcplus.xb.funpic.de' in url :
   xbmc . executebuiltin ( "XBMC.Container.Update(%s?mode=14,replace)" % sys . argv [ 0 ] )
  elif 'community-links' in url :
   xbmc . executebuiltin ( "XBMC.Container.Update(%s?mode=10,replace)" % sys . argv [ 0 ] )
 else : I1IiI . openSettings ( )
 if 84 - 84: IIiIiII11i . IIii1I % II1 + i1Ii % II1 % Ooo00oOo00o
 if 42 - 42: Ooo00oOo00o / I1 / O0Oooo00 + o00O00O0O0O / oo
def o0OoOO000ooO0 ( name ) :
 oOO00oOO = json . loads ( open ( iiIIIII1i1iI , "r" ) . read ( ) )
 for o0o0o0oO0oOO in range ( len ( oOO00oOO ) ) :
  if isinstance ( oOO00oOO [ o0o0o0oO0oOO ] , list ) :
   if oOO00oOO [ o0o0o0oO0oOO ] [ 0 ] == name :
    del oOO00oOO [ o0o0o0oO0oOO ]
    Iiii1i1 = open ( iiIIIII1i1iI , "w" )
    Iiii1i1 . write ( json . dumps ( oOO00oOO ) )
    Iiii1i1 . close ( )
    break
  else :
   if oOO00oOO [ o0o0o0oO0oOO ] [ 'title' ] == name :
    del oOO00oOO [ o0o0o0oO0oOO ]
    Iiii1i1 = open ( iiIIIII1i1iI , "w" )
    Iiii1i1 . write ( json . dumps ( oOO00oOO ) )
    Iiii1i1 . close ( )
    break
 xbmc . executebuiltin ( "XBMC.Container.Refresh" )
 if 3 - 3: O0Oooo00
 if 24 - 24: i11iIiiIii + o00O00O0O0O * i1Ii - iIiiiI1IiI1I1 . OoOooOOOO % IIii1I
 if 71 - 71: OOO0O0O0ooooo . o00O00O0O0O / O0Oooo00
def Ooo ( url , browse = False ) :
 if url is None :
  url = 'http://xbmcplus.xb.funpic.de/www-data/filesystem/'
 iIi1IiIiiII = BeautifulSoup ( Oo00OOOOO ( url ) , convertEntities = BeautifulSoup . HTML_ENTITIES )
 for O000OO0 in iIi1IiIiiII ( 'a' ) :
  ii1iII1II = O000OO0 [ 'href' ]
  if not ii1iII1II . startswith ( '?' ) :
   Iii1I1I11iiI1 = O000OO0 . string
   if Iii1I1I11iiI1 not in [ 'Parent Directory' , 'recycle_bin/' ] :
    if ii1iII1II . endswith ( '/' ) :
     if browse :
      iiI1 ( Iii1I1I11iiI1 , url + ii1iII1II , 15 , O0oo0OO0 , O000oo0O , '' , '' , '' )
     else :
      iiI1 ( Iii1I1I11iiI1 , url + ii1iII1II , 14 , O0oo0OO0 , O000oo0O , '' , '' , '' )
    elif ii1iII1II . endswith ( '.xml' ) :
     if browse :
      iiI1 ( Iii1I1I11iiI1 , url + ii1iII1II , 1 , O0oo0OO0 , O000oo0O , '' , '' , '' , '' , 'download' )
     else :
      if os . path . exists ( iiIIIII1i1iI ) == True :
       if Iii1I1I11iiI1 in i1 :
        iiI1 ( Iii1I1I11iiI1 + ' (in use)' , url + ii1iII1II , 11 , O0oo0OO0 , O000oo0O , '' , '' , '' , '' , 'download' )
       else :
        iiI1 ( Iii1I1I11iiI1 , url + ii1iII1II , 11 , O0oo0OO0 , O000oo0O , '' , '' , '' , '' , 'download' )
      else :
       iiI1 ( Iii1I1I11iiI1 , url + ii1iII1II , 11 , O0oo0OO0 , O000oo0O , '' , '' , '' , '' , 'download' )
       if 18 - 18: OoOooOOOO + o00O00O0O0O - i1Ii . iIiiiI1IiI1I1 + i11iIiiIii
       if 20 - 20: ooiii11iII
def Oo0oO00o ( browse = False ) :
 Iiii = 'http://community-links.googlecode.com/svn/trunk/'
 iIi1IiIiiII = BeautifulSoup ( Oo00OOOOO ( Iiii ) , convertEntities = BeautifulSoup . HTML_ENTITIES )
 i11I1II1I11i = iIi1IiIiiII ( 'ul' ) [ 0 ] ( 'li' ) [ 1 : ]
 for O000OO0 in i11I1II1I11i :
  Iii1I1I11iiI1 = O000OO0 ( 'a' ) [ 0 ] [ 'href' ]
  if browse :
   iiI1 ( Iii1I1I11iiI1 , Iiii + Iii1I1I11iiI1 , 1 , O0oo0OO0 , O000oo0O , '' , '' , '' , '' , 'download' )
  else :
   iiI1 ( Iii1I1I11iiI1 , Iiii + Iii1I1I11iiI1 , 11 , O0oo0OO0 , O000oo0O , '' , '' , '' , '' , 'download' )
   if 61 - 61: IIiIiII11i - OoOooOOOO . iI1 / OoOooOOOO + IiIIi1I1Iiii
   if 5 - 5: O00OoO000O + O00OoO000O / OOO0O0O0ooooo * IiIIi1I1Iiii - OoOooOOOO % O00OoO000O
def OOooOoooOoOo ( url , data = None ) :
 print 'getsoup' , url , data
 if url . startswith ( 'http://' ) or url . startswith ( 'https://' ) :
  data = Oo00OOOOO ( url )
  if re . search ( "#EXTM3U" , data ) or 'm3u' in url :
   print 'found m3u data' , data
   return data
   if 15 - 15: i11iIiiIii % i1Ii . IiIIi1I1Iiii + O00OoOoo00
 elif data == None :
  if xbmcvfs . exists ( url ) :
   if url . startswith ( "smb://" ) or url . startswith ( "nfs://" ) :
    OO0OOOOoo0OOO = xbmcvfs . copy ( url , os . path . join ( iIiiiI , 'temp' , 'sorce_temp.txt' ) )
    if OO0OOOOoo0OOO :
     data = open ( os . path . join ( iIiiiI , 'temp' , 'sorce_temp.txt' ) , "r" ) . read ( )
     xbmcvfs . delete ( os . path . join ( iIiiiI , 'temp' , 'sorce_temp.txt' ) )
    else :
     o0O00oooo ( "failed to copy from smb:" )
   else :
    data = open ( url , 'r' ) . read ( )
    if re . match ( "#EXTM3U" , data ) or 'm3u' in url :
     print 'found m3u data' , data
     return data
  else :
   o0O00oooo ( "Soup Data not found!" )
   return
 return BeautifulSOAP ( data , convertEntities = BeautifulStoneSoup . XML_ENTITIES )
 if 27 - 27: O00OoO000O + iIiiiI1IiI1I1
 if 92 - 92: ooO0O . ooO0O + Ooo00oOo00o
def i11Iiii ( url , fanart ) :
 print 'url-getData' , url
 IiIiI1111I1I = "List"
 if 13 - 13: i1Ii . i11iIiiIii
 iIi1IiIiiII = OOooOoooOoOo ( url )
 if 56 - 56: O00OoOoo00 % OOO0O0O0ooooo - IIiIiII11i
 if isinstance ( iIi1IiIiiII , BeautifulSOAP ) :
  if len ( iIi1IiIiiII ( 'layoutype' ) ) > 0 :
   IiIiI1111I1I = "Thumbnail"
   if 100 - 100: i1Ii - OOO0O0O0ooooo % iI1 * OoOooOOOO + IIiIiII11i
  if len ( iIi1IiIiiII ( 'channels' ) ) > 0 :
   Oo0O0oooo = iIi1IiIiiII ( 'channel' )
   for I111iI in Oo0O0oooo :
    if 56 - 56: IIiIiII11i
    if 54 - 54: ooiii11iII / OoOooOOOO . iI1 % o00O00O0O0O
    Oo = ''
    O0OOOOo0O = 0
    try :
     Oo = I111iI ( 'externallink' ) [ 0 ] . string
     O0OOOOo0O = len ( I111iI ( 'externallink' ) )
    except : pass
    if 81 - 81: OOO0O0O0ooooo / Ooo00oOo00o . O00ooooo00 + IIiIiII11i - I1
    if O0OOOOo0O > 1 : Oo = ''
    if 74 - 74: IIii1I * O00OoOoo00 + oo / O00ooooo00 / iIiiiI1IiI1I1 . IiIIi1I1Iiii
    Iii1I1I11iiI1 = I111iI ( 'name' ) [ 0 ] . string
    oooOo0OOOoo0 = I111iI ( 'thumbnail' ) [ 0 ] . string
    if oooOo0OOOoo0 == None :
     oooOo0OOOoo0 = ''
     if 51 - 51: IiIIi1I1Iiii / oo . OoOooOOOO * O0Oooo00 + Ooo00oOo00o * ooO0O
    try :
     if not I111iI ( 'fanart' ) :
      if I1IiI . getSetting ( 'use_thumb' ) == "true" :
       OOOoOo = oooOo0OOOoo0
      else :
       OOOoOo = fanart
     else :
      OOOoOo = I111iI ( 'fanart' ) [ 0 ] . string
     if OOOoOo == None :
      raise
    except :
     OOOoOo = fanart
     if 51 - 51: O00OoO000O / IIii1I % IiIIi1I1Iiii * IIiIiII11i % ooiii11iII
    try :
     OOOO = I111iI ( 'info' ) [ 0 ] . string
     if OOOO == None :
      raise
    except :
     OOOO = ''
     if 76 - 76: O0Oooo00 - i11iIiiIii
    try :
     IIIii1II1II = I111iI ( 'genre' ) [ 0 ] . string
     if IIIii1II1II == None :
      raise
    except :
     IIIii1II1II = ''
     if 14 - 14: oo + iI1
    try :
     i11i1 = I111iI ( 'date' ) [ 0 ] . string
     if i11i1 == None :
      raise
    except :
     i11i1 = ''
     if 52 - 52: II1 - O00OoO000O
    try :
     credits = I111iI ( 'credits' ) [ 0 ] . string
     if credits == None :
      raise
    except :
     credits = ''
     if 74 - 74: o00O00O0O0O + O0Oooo00
    try :
     if Oo == '' :
      iiI1 ( Iii1I1I11iiI1 . encode ( 'utf-8' , 'ignore' ) , url . encode ( 'utf-8' ) , 2 , oooOo0OOOoo0 , OOOoOo , OOOO , IIIii1II1II , i11i1 , credits , True )
     else :
      if 71 - 71: IiIIi1I1Iiii % OoOooOOOO
      iiI1 ( Iii1I1I11iiI1 . encode ( 'utf-8' ) , Oo . encode ( 'utf-8' ) , 1 , oooOo0OOOoo0 , OOOoOo , OOOO , IIIii1II1II , i11i1 , None , 'source' )
    except :
     o0O00oooo ( 'There was a problem adding directory from getData(): ' + Iii1I1I11iiI1 . encode ( 'utf-8' , 'ignore' ) )
  else :
   o0O00oooo ( 'No Channels: getItems' )
   O00oO000O0O ( iIi1IiIiiII ( 'item' ) , fanart )
 else :
  I1i1i1iii ( iIi1IiIiiII )
  if 16 - 16: i1Ii + ooO0O * OOO0O0O0ooooo % O00ooooo00 . IIiIiII11i
 if IiIiI1111I1I == "Thumbnail" :
  Oo0OO ( )
  if 78 - 78: OoOooOOOO - II1 - O00OoOoo00 / O00OoO000O / iIiiiI1IiI1I1
  if 29 - 29: IIiIiII11i % IIiIiII11i
  if 94 - 94: IIii1I / IiIIi1I1Iiii % o00O00O0O0O * o00O00O0O0O * iIiiiI1IiI1I1
  if 29 - 29: Ooo00oOo00o + oo / O0Oooo00 / OoOooOOOO * IIii1I
  if 62 - 62: OoOooOOOO / iI1 - Ooo00oOo00o . I1
def I1i1i1iii ( data ) :
 II = data . rstrip ( )
 o0Oo0oO0oOO00 = re . compile ( r'#EXTINF:(.+?),(.*?)[\n\r]+([^\n]+)' ) . findall ( II )
 oo00OO0000oO = len ( o0Oo0oO0oOO00 )
 print 'total m3u links' , oo00OO0000oO
 for I1II1 , oooO , i1I1i111Ii in o0Oo0oO0oOO00 :
  if 'tvg-logo' in I1II1 :
   oooOo0OOOoo0 = ooo ( I1II1 , 'tvg-logo=[\'"](.*?)[\'"]' )
   if oooOo0OOOoo0 :
    if oooOo0OOOoo0 . startswith ( 'http' ) :
     oooOo0OOOoo0 = oooOo0OOOoo0
     if 27 - 27: O00OoO000O % IIiIiII11i
    elif not I1IiI . getSetting ( 'logo-folderPath' ) == "" :
     o0oooOO00 = I1IiI . getSetting ( 'logo-folderPath' )
     oooOo0OOOoo0 = o0oooOO00 + oooOo0OOOoo0
     if 32 - 32: ooiii11iII
    else :
     oooOo0OOOoo0 = oooOo0OOOoo0
     if 30 - 30: IIii1I / I1 . Ooo00oOo00o - O0Oooo00
     if 48 - 48: O00ooooo00 - i1Ii / OOO0O0O0ooooo * Ooo00oOo00o
  else :
   oooOo0OOOoo0 = ''
  if 'type' in I1II1 :
   ooOOOooO = ooo ( I1II1 , 'type=[\'"](.*?)[\'"]' )
   if ooOOOooO == 'yt-dl' :
    i1I1i111Ii = i1I1i111Ii + "&mode=18"
   elif ooOOOooO == 'regex' :
    Iiii = i1I1i111Ii . split ( '&regexs=' )
    if 12 - 12: OOO0O0O0ooooo - O0Oooo00
    oOoO00O0 = OO ( OOooOoooOoOo ( '' , data = Iiii [ 1 ] ) )
    if 7 - 7: OOO0O0O0ooooo * i11iIiiIii * i1Ii + O00OoO000O % Ooo00oOo00o - O00OoO000O
    II1IIIIiII1i ( Iiii [ 0 ] , oooO , oooOo0OOOoo0 , '' , '' , '' , '' , '' , None , oOoO00O0 , oo00OO0000oO )
    continue
  II1IIIIiII1i ( i1I1i111Ii , oooO , oooOo0OOOoo0 , '' , '' , '' , '' , '' , None , '' , oo00OO0000oO )
  if 1 - 1: iIiiiI1IiI1I1
 xbmc . executebuiltin ( "Container.SetViewMode(50)" )
 if 68 - 68: o00O00O0O0O - IIiIiII11i / ooiii11iII / I1
def I11iiii ( name , url , fanart ) :
 iIi1IiIiiII = OOooOoooOoOo ( url )
 O0i1iI = iIi1IiIiiII . find ( 'channel' , attrs = { 'name' : name . decode ( 'utf-8' ) } )
 IiI1iiiIii = O0i1iI ( 'item' )
 try :
  OOOoOo = O0i1iI ( 'fanart' ) [ 0 ] . string
  if OOOoOo == None :
   raise
 except :
  OOOoOo = fanart
 for I111iI in O0i1iI ( 'subchannel' ) :
  name = I111iI ( 'name' ) [ 0 ] . string
  try :
   oooOo0OOOoo0 = I111iI ( 'thumbnail' ) [ 0 ] . string
   if oooOo0OOOoo0 == None :
    raise
  except :
   oooOo0OOOoo0 = ''
  try :
   if not I111iI ( 'fanart' ) :
    if I1IiI . getSetting ( 'use_thumb' ) == "true" :
     OOOoOo = oooOo0OOOoo0
   else :
    OOOoOo = I111iI ( 'fanart' ) [ 0 ] . string
   if OOOoOo == None :
    raise
  except :
   pass
  try :
   OOOO = I111iI ( 'info' ) [ 0 ] . string
   if OOOO == None :
    raise
  except :
   OOOO = ''
   if 7 - 7: ooiii11iII * Ooo00oOo00o - O00OoO000O + OoOooOOOO * IIiIiII11i % Ooo00oOo00o
  try :
   IIIii1II1II = I111iI ( 'genre' ) [ 0 ] . string
   if IIIii1II1II == None :
    raise
  except :
   IIIii1II1II = ''
   if 15 - 15: oo % IIiIiII11i * I1
  try :
   i11i1 = I111iI ( 'date' ) [ 0 ] . string
   if i11i1 == None :
    raise
  except :
   i11i1 = ''
   if 81 - 81: O00OoO000O - IIii1I - O00ooooo00 / ooiii11iII - OOO0O0O0ooooo * I1
  try :
   credits = I111iI ( 'credits' ) [ 0 ] . string
   if credits == None :
    raise
  except :
   credits = ''
   if 20 - 20: iI1 % ooO0O
  try :
   iiI1 ( name . encode ( 'utf-8' , 'ignore' ) , url . encode ( 'utf-8' ) , 3 , oooOo0OOOoo0 , OOOoOo , OOOO , IIIii1II1II , credits , i11i1 )
  except :
   o0O00oooo ( 'There was a problem adding directory - ' + name . encode ( 'utf-8' , 'ignore' ) )
 O00oO000O0O ( IiI1iiiIii , OOOoOo )
 if 19 - 19: O00OoOoo00 % ooO0O + O00OoO000O / ooiii11iII . O00OoO000O
 if 12 - 12: O00ooooo00 + O00ooooo00 - O00OoOoo00 * IiIIi1I1Iiii % IiIIi1I1Iiii - iIiiiI1IiI1I1
def o0O ( name , url , fanart ) :
 iIi1IiIiiII = OOooOoooOoOo ( url )
 O0i1iI = iIi1IiIiiII . find ( 'subchannel' , attrs = { 'name' : name . decode ( 'utf-8' ) } )
 IiI1iiiIii = O0i1iI ( 'subitem' )
 O00oO000O0O ( IiI1iiiIii , fanart )
 if 84 - 84: Ooo00oOo00o + O00ooooo00 - iIiiiI1IiI1I1 . O00OoOoo00 * II1 + IIiIiII11i
 if 38 - 38: OoOooOOOO + iIiiiI1IiI1I1 % O00OoO000O % oo - i1Ii / II1
def oOOoo0000O0o0 ( name , url , iconimage , fanart ) :
 II1III = [ ] ; III1 = [ ] ; OooooO0oOOOO = 0
 o0O00oOOoo = i1I1iIi ( url , 'sublink:' , '#' )
 for IIii11Ii1i1I in o0O00oOOoo :
  Oooo0O = IIii11Ii1i1I . replace ( 'sublink:' , '' ) . replace ( '#' , '' )
  if 90 - 90: IIii1I % O00OoO000O
  if len ( Oooo0O ) > 10 :
   OooooO0oOOOO = OooooO0oOOOO + 1 ; II1III . append ( name + ' Source [' + str ( OooooO0oOOOO ) + ']' ) ; III1 . append ( Oooo0O )
   if 73 - 73: OOO0O0O0ooooo * o00O00O0O0O + i1Ii + O00OoO000O
 if OooooO0oOOOO == 1 :
  try :
   if 40 - 40: iIiiiI1IiI1I1 . oo * ooiii11iII + OoOooOOOO + OoOooOOOO
   I1ii1I1iiii = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; I1ii1I1iiii . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
   iiI = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = III1 [ 0 ] , listitem = I1ii1I1iiii )
   xbmc . Player ( ) . play ( oOIIiIi ( III1 [ 0 ] ) , I1ii1I1iiii )
  except :
   pass
 else :
  I1iiiiI1iII = xbmcgui . Dialog ( )
  OOoOooOoOOOoo = I1iiiiI1iII . select ( '[COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR] ~ Select A Source' , II1III )
  if OOoOooOoOOOoo >= 0 :
   Iiii1iI1i = name
   I1ii1ii11i1I = str ( III1 [ OOoOooOoOOOoo ] )
   if 58 - 58: o00O00O0O0O + IiIIi1I1Iiii
   try :
    I1ii1I1iiii = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; I1ii1I1iiii . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
    iiI = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = I1ii1ii11i1I , listitem = I1ii1I1iiii )
    xbmc . Player ( ) . play ( oOIIiIi ( I1ii1ii11i1I ) , I1ii1I1iiii )
   except :
    pass
    if 12 - 12: O0Oooo00 - O00OoOoo00 % oo * I1
    if 44 - 44: o00O00O0O0O % i1Ii
def iiI11i1II ( ) :
 if 51 - 51: O0Oooo00 % IiIIi1I1Iiii % O0Oooo00 * OOO0O0O0ooooo - OoOooOOOO % IiIIi1I1Iiii
 o0O00OooOOOOO = 'Name of channel show or movie'
 IIIiiI1i1 = ''
 oOooOOOoOo = xbmc . Keyboard ( IIIiiI1i1 , o0O00OooOOOOO )
 oOooOOOoOo . doModal ( )
 if oOooOOOoOo . isConfirmed ( ) :
  IIIiiI1i1 = oOooOOOoOo . getText ( ) . replace ( '\n' , '' ) . strip ( )
  if len ( IIIiiI1i1 ) == 0 :
   xbmcgui . Dialog ( ) . ok ( 'RobinHood' , 'Nothing Entered' )
   return
   if 15 - 15: O00ooooo00 + oo
 IIIiiI1i1 = IIIiiI1i1 . lower ( )
 II1III = [ ]
 II1III . append ( Regex . MainBase )
 iii1i1I1i1 = 0
 iI1iIIi = 1
 oO0o00oo0 = 0
 ii1IIII = 0
 oO00oOooooo0 = xbmcgui . DialogProgress ( )
 oO00oOooooo0 . create ( '[COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR] Searching Please wait' , ' ' )
 if 52 - 52: IiIIi1I1Iiii . iI1 / OoOooOOOO
 while iI1iIIi <> oO0o00oo0 :
  OOooOoOo = II1III [ oO0o00oo0 ] . strip ( )
  print 'read this one from file list (' + str ( oO0o00oo0 ) + ')'
  oO0o00oo0 = oO0o00oo0 + 1
  if 14 - 14: O0Oooo00 * OoOooOOOO + o00O00O0O0O + OOO0O0O0ooooo + i11iIiiIii
  oOoO0 = ''
  try :
   oOoO0 = net . http_GET ( OOooOoOo ) . content
   oOoO0 = oOoO0 . encode ( 'ascii' , 'ignore' ) . decode ( 'ascii' )
   if 77 - 77: IIii1I . o00O00O0O0O % o00O00O0O0O + i11iIiiIii
  except :
   pass
   if 72 - 72: IIii1I * i1Ii % O00OoO000O / Ooo00oOo00o
  if len ( oOoO0 ) < 10 :
   oOoO0 = ''
   iii1i1I1i1 = iii1i1I1i1 + 1
   print '*** PASSED ****' + OOooOoOo + '  ************* Total Passed Urls: ' + str ( iii1i1I1i1 )
   time . sleep ( .5 )
   if 35 - 35: O00OoO000O + O00ooooo00 % O00OoOoo00 % I1 + iI1
  iiiI = int ( ( oO0o00oo0 / 300 ) * 100 )
  I1ii1 = '     Pages Read: ' + str ( oO0o00oo0 ) + '        Matches Found: ' + str ( ii1IIII )
  oO00oOooooo0 . update ( iiiI , "" , I1ii1 , "" )
  if 99 - 99: O00OoO000O . ooiii11iII % ooO0O * ooO0O . O00ooooo00
  if oO00oOooooo0 . iscanceled ( ) :
   return
   if 72 - 72: OoOooOOOO % O00OoOoo00 + Ooo00oOo00o / iI1 + ooO0O
  if len ( oOoO0 ) > 10 :
   I1I1i = i1I1iIi ( oOoO0 , '<channel>' , '</channel>' )
   for IIii11Ii1i1I in I1I1i :
    Oooo0O = I1IIIiIiIi ( IIii11Ii1i1I , '<externallink>' , '</externallink>' )
    if 27 - 27: O00OoOoo00 + oo - OoOooOOOO + OOO0O0O0ooooo . i1Ii
    if 46 - 46: ooO0O
    if len ( Oooo0O ) > 5 :
     iI1iIIi = iI1iIIi + 1
     II1III . append ( Oooo0O )
     if 45 - 45: O00OoO000O
     if 21 - 21: iI1 . ooiii11iII . OoOooOOOO / IiIIi1I1Iiii / ooiii11iII
   i1iI1 = i1I1iIi ( oOoO0 , '<item>' , '</item>' )
   for IIii11Ii1i1I in i1iI1 :
    Oooo0O = I1IIIiIiIi ( IIii11Ii1i1I , '<link>' , '</link>' )
    Iii1I1I11iiI1 = I1IIIiIiIi ( IIii11Ii1i1I , '<title>' , '</title>' )
    ii1 = '  ' + Iii1I1I11iiI1 . lower ( ) + '  '
    if 1 - 1: O00OoO000O % IIii1I + IiIIi1I1Iiii . IIii1I % IIiIiII11i
    if len ( Oooo0O ) > 5 and ii1 . find ( IIIiiI1i1 ) > 0 :
     ii1IIII = ii1IIII + 1
     O000oo0O = ''
     oooOo0OOOoo0 = I1IIIiIiIi ( IIii11Ii1i1I , '<thumbnail>' , '</thumbnail>' )
     O000oo0O = I1IIIiIiIi ( IIii11Ii1i1I , '<fanart>' , '</fanart>' )
     if len ( O000oo0O ) < 5 :
      O000oo0O = O0oo0OO0
     if Oooo0O . find ( 'sublink' ) > 0 :
      iiI1 ( Iii1I1I11iiI1 , Oooo0O , 30 , oooOo0OOOoo0 , O000oo0O , '' , '' , '' , '' )
     else :
      II1IIIIiII1i ( str ( Oooo0O ) , Iii1I1I11iiI1 , oooOo0OOOoo0 , O000oo0O , '' , '' , '' , True , None , '' , 1 )
      if 89 - 89: i1Ii
      if 76 - 76: O00OoO000O
 oO00oOooooo0 . close ( )
 xbmc . executebuiltin ( "Container.SetViewMode(50)" )
 if 15 - 15: OoOooOOOO . I1 + II1 - Ooo00oOo00o
def Oo0 ( data , Searchkey ) :
 II = data . rstrip ( )
 o0Oo0oO0oOO00 = re . compile ( r'#EXTINF:(.+?),(.*?)[\n\r]+([^\n]+)' ) . findall ( II )
 oo00OO0000oO = len ( o0Oo0oO0oOO00 )
 print 'total m3u links' , oo00OO0000oO
 for I1II1 , oooO , i1I1i111Ii in o0Oo0oO0oOO00 :
  if 'tvg-logo' in I1II1 :
   oooOo0OOOoo0 = ooo ( I1II1 , 'tvg-logo=[\'"](.*?)[\'"]' )
   if oooOo0OOOoo0 :
    if oooOo0OOOoo0 . startswith ( 'http' ) :
     oooOo0OOOoo0 = oooOo0OOOoo0
     if 59 - 59: IIiIiII11i * iIiiiI1IiI1I1 . OOO0O0O0ooooo
    elif not I1IiI . getSetting ( 'logo-folderPath' ) == "" :
     o0oooOO00 = I1IiI . getSetting ( 'logo-folderPath' )
     oooOo0OOOoo0 = o0oooOO00 + oooOo0OOOoo0
     if 56 - 56: i1Ii - o00O00O0O0O % IIiIiII11i - O0Oooo00
    else :
     oooOo0OOOoo0 = oooOo0OOOoo0
     if 51 - 51: OOO0O0O0ooooo / O00OoO000O * IIii1I + O00OoOoo00 + O0Oooo00
     if 98 - 98: IIii1I * O00OoOoo00 * OoOooOOOO + O00OoO000O % i11iIiiIii % OOO0O0O0ooooo
  else :
   oooOo0OOOoo0 = ''
  if 'type' in I1II1 :
   ooOOOooO = ooo ( I1II1 , 'type=[\'"](.*?)[\'"]' )
   if ooOOOooO == 'yt-dl' :
    i1I1i111Ii = i1I1i111Ii + "&mode=18"
   elif ooOOOooO == 'regex' :
    Iiii = i1I1i111Ii . split ( '&regexs=' )
    if 27 - 27: OOO0O0O0ooooo
    oOoO00O0 = OO ( OOooOoooOoOo ( '' , data = Iiii [ 1 ] ) )
    if 79 - 79: O0Oooo00 - I1 + O0Oooo00 . iI1
    II1IIIIiII1i ( Iiii [ 0 ] , oooO , oooOo0OOOoo0 , '' , '' , '' , '' , '' , None , oOoO00O0 , oo00OO0000oO )
    continue
  II1IIIIiII1i ( i1I1i111Ii , oooO , oooOo0OOOoo0 , '' , '' , '' , '' , '' , None , '' , oo00OO0000oO )
  if 28 - 28: O00ooooo00 - o00O00O0O0O
def o00o000oo ( text , pattern ) :
 ii11i11i1 = ""
 try :
  Ooo0o00o0o = re . findall ( pattern , text , flags = re . DOTALL )
  ii11i11i1 = Ooo0o00o0o [ 0 ]
 except :
  ii11i11i1 = ""
  if 7 - 7: OOO0O0O0ooooo - IiIIi1I1Iiii + O00OoOoo00 + iIiiiI1IiI1I1 + IIii1I
 return ii11i11i1
 if 58 - 58: O0Oooo00 / ooO0O . oo / II1 + ooiii11iII
def i1I1iIi ( text , start_with , end_with ) :
 O0OoO0ooOO0o = re . findall ( "(?i)(" + start_with + "[\S\s]+?" + end_with + ")" , text )
 return O0OoO0ooOO0o
 if 81 - 81: OOO0O0O0ooooo * iIiiiI1IiI1I1 + IIiIiII11i * i11iIiiIii - O00OoOoo00 / IIiIiII11i
def I1IIIiIiIi ( text , from_string , to_string , excluding = True ) :
 if excluding :
  try : O0OoO0ooOO0o = re . search ( "(?i)" + from_string + "([\S\s]+?)" + to_string , text ) . group ( 1 )
  except : O0OoO0ooOO0o = ''
 else :
  try : O0OoO0ooOO0o = re . search ( "(?i)(" + from_string + "[\S\s]+?" + to_string + ")" , text ) . group ( 1 )
  except : O0OoO0ooOO0o = ''
 return O0OoO0ooOO0o
 if 63 - 63: oo - II1 % ooiii11iII
def O00oO000O0O ( items , fanart ) :
 oo00OO0000oO = len ( items )
 print 'START GET ITEMS *****'
 o0O00oooo ( 'Total Items: %s' % oo00OO0000oO )
 for oOi11iI11iIiIi in items :
  O00 = False
  O0ooo0 = False
  try :
   Iii1I1I11iiI1 = oOi11iI11iIiIi ( 'title' ) [ 0 ] . string
   if Iii1I1I11iiI1 is None :
    Iii1I1I11iiI1 = 'unknown?'
  except :
   o0O00oooo ( 'Name Error' )
   Iii1I1I11iiI1 = ''
   if 8 - 8: O00OoO000O + iIiiiI1IiI1I1 / o00O00O0O0O / I1
   if 74 - 74: OOO0O0O0ooooo / O00ooooo00
  try :
   if oOi11iI11iIiIi ( 'epg' ) :
    if oOi11iI11iIiIi . epg_url :
     o0O00oooo ( 'Get EPG Regex' )
     OoO = oOi11iI11iIiIi . epg_url . string
     Iiiiii111i1ii = oOi11iI11iIiIi . epg_regex . string
     i1i1iII1 = iii11i1IIII ( OoO , Iiiiii111i1ii )
     if i1i1iII1 :
      Iii1I1I11iiI1 += ' - ' + i1i1iII1
    elif oOi11iI11iIiIi ( 'epg' ) [ 0 ] . string > 1 :
     Iii1I1I11iiI1 += Ii ( oOi11iI11iIiIi ( 'epg' ) [ 0 ] . string )
   else :
    pass
  except :
   o0O00oooo ( 'EPG Error' )
  try :
   Iiii = [ ]
   if len ( oOi11iI11iIiIi ( 'link' ) ) > 0 :
    if 91 - 91: ooiii11iII . IIiIiII11i % i11iIiiIii
    for O000OO0 in oOi11iI11iIiIi ( 'link' ) :
     if not O000OO0 . string == None :
      Iiii . append ( O000OO0 . string )
      if 47 - 47: o00O00O0O0O - IiIIi1I1Iiii
   elif len ( oOi11iI11iIiIi ( 'sportsdevil' ) ) > 0 :
    for O000OO0 in oOi11iI11iIiIi ( 'sportsdevil' ) :
     if not O000OO0 . string == None :
      IiiioooOOoooo = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + O000OO0 . string
      O0000OOO0 = oOi11iI11iIiIi ( 'referer' ) [ 0 ] . string
      if O0000OOO0 :
       if 51 - 51: IIiIiII11i / ooO0O / i1Ii
       IiiioooOOoooo = IiiioooOOoooo + '%26referer=' + O0000OOO0
      Iiii . append ( IiiioooOOoooo )
   elif len ( oOi11iI11iIiIi ( 'p2p' ) ) > 0 :
    for O000OO0 in oOi11iI11iIiIi ( 'p2p' ) :
     if not O000OO0 . string == None :
      if 'sop://' in O000OO0 :
       I111iIi1 = 'plugin://plugin.video.p2p-streams/?url=' + O000OO0 . string + '&amp;mode=2&amp;' + 'name=' + Iii1I1I11iiI1
       Iiii . append ( I111iIi1 )
      else :
       oo00O00oO000o = 'plugin://plugin.video.p2p-streams/?url=' + O000OO0 . string + '&amp;mode=1&amp;' + 'name=' + Iii1I1I11iiI1
       Iiii . append ( oo00O00oO000o )
   elif len ( oOi11iI11iIiIi ( 'vaughn' ) ) > 0 :
    for O000OO0 in oOi11iI11iIiIi ( 'vaughn' ) :
     if not O000OO0 . string == None :
      OOo00OoO = 'plugin://plugin.stream.vaughnlive.tv/?mode=PlayLiveStream&amp;channel=' + O000OO0 . string
      Iiii . append ( OOo00OoO )
   elif len ( oOi11iI11iIiIi ( 'ilive' ) ) > 0 :
    for O000OO0 in oOi11iI11iIiIi ( 'ilive' ) :
     if not O000OO0 . string == None :
      if not 'http' in O000OO0 . string :
       iIi1 = 'plugin://plugin.video.tbh.ilive/?url=http://www.streamlive.to/view/' + O000OO0 . string + '&amp;link=99&amp;mode=iLivePlay'
      else :
       iIi1 = 'plugin://plugin.video.tbh.ilive/?url=' + O000OO0 . string + '&amp;link=99&amp;mode=iLivePlay'
   elif len ( oOi11iI11iIiIi ( 'yt-dl' ) ) > 0 :
    for O000OO0 in oOi11iI11iIiIi ( 'yt-dl' ) :
     if not O000OO0 . string == None :
      i11iiI1111 = O000OO0 . string + '&mode=18'
      Iiii . append ( i11iiI1111 )
   elif len ( oOi11iI11iIiIi ( 'utube' ) ) > 0 :
    for O000OO0 in oOi11iI11iIiIi ( 'utube' ) :
     if not O000OO0 . string == None :
      if len ( O000OO0 . string ) == 11 :
       oOoooo000Oo00 = 'plugin://plugin.video.youtube/play/?video_id=' + O000OO0 . string
      elif O000OO0 . string . startswith ( 'PL' ) and not '&order=' in O000OO0 . string :
       oOoooo000Oo00 = 'plugin://plugin.video.youtube/play/?&order=default&playlist_id=' + O000OO0 . string
      else :
       oOoooo000Oo00 = 'plugin://plugin.video.youtube/play/?playlist_id=' + O000OO0 . string
    Iiii . append ( oOoooo000Oo00 )
   elif len ( oOi11iI11iIiIi ( 'imdb' ) ) > 0 :
    for O000OO0 in oOi11iI11iIiIi ( 'imdb' ) :
     if not O000OO0 . string == None :
      if I1IiI . getSetting ( 'genesisorpulsar' ) == '0' :
       OOoo = 'plugin://plugin.video.genesis/?action=play&imdb=' + O000OO0 . string
      else :
       OOoo = 'plugin://plugin.video.pulsar/movie/tt' + O000OO0 . string + '/play'
      Iiii . append ( OOoo )
   elif len ( oOi11iI11iIiIi ( 'f4m' ) ) > 0 :
    for O000OO0 in oOi11iI11iIiIi ( 'f4m' ) :
     if not O000OO0 . string == None :
      if '.f4m' in O000OO0 . string :
       o00O00oO00 = 'plugin://plugin.video.f4mTester/?url=' + urllib . quote_plus ( O000OO0 . string )
      elif '.m3u8' in O000OO0 . string :
       o00O00oO00 = 'plugin://plugin.video.f4mTester/?url=' + urllib . quote_plus ( O000OO0 . string ) + '&amp;streamtype=HLS'
       if 23 - 23: IIii1I * O00ooooo00 % II1 * ooO0O
      else :
       o00O00oO00 = 'plugin://plugin.video.f4mTester/?url=' + urllib . quote_plus ( O000OO0 . string ) + '&amp;streamtype=SIMPLE'
    Iiii . append ( o00O00oO00 )
   elif len ( oOi11iI11iIiIi ( 'ftv' ) ) > 0 :
    for O000OO0 in oOi11iI11iIiIi ( 'ftv' ) :
     if not O000OO0 . string == None :
      I1Iiiiiii = 'plugin://plugin.video.F.T.V/?name=' + urllib . quote ( Iii1I1I11iiI1 ) + '&url=' + O000OO0 . string + '&mode=125&ch_fanart=na'
     Iiii . append ( I1Iiiiiii )
   if len ( Iiii ) < 1 :
    raise
  except :
   o0O00oooo ( 'Error <link> element, Passing:' + Iii1I1I11iiI1 . encode ( 'utf-8' , 'ignore' ) )
   continue
   if 39 - 39: ooO0O * IiIIi1I1Iiii + IIii1I - ooO0O + OoOooOOOO
  O00 = False
  if 69 - 69: OOO0O0O0ooooo
  try :
   O00 = oOi11iI11iIiIi ( 'externallink' ) [ 0 ] . string
  except : pass
  if 85 - 85: O00OoO000O / OOO0O0O0ooooo
  if O00 :
   iI1iIIIi1i = [ O00 ]
   O00 = True
  else :
   O00 = False
  try :
   O0ooo0 = oOi11iI11iIiIi ( 'jsonrpc' ) [ 0 ] . string
  except : pass
  if O0ooo0 :
   iI1iIIIi1i = [ O0ooo0 ]
   O0ooo0 = True
  else :
   O0ooo0 = False
  try :
   oooOo0OOOoo0 = oOi11iI11iIiIi ( 'thumbnail' ) [ 0 ] . string
   if oooOo0OOOoo0 == None :
    raise
  except :
   oooOo0OOOoo0 = ''
  try :
   if not oOi11iI11iIiIi ( 'fanart' ) :
    if I1IiI . getSetting ( 'use_thumb' ) == "true" :
     OOOoOo = oooOo0OOOoo0
    else :
     OOOoOo = fanart
   else :
    OOOoOo = oOi11iI11iIiIi ( 'fanart' ) [ 0 ] . string
   if OOOoOo == None :
    raise
  except :
   OOOoOo = fanart
  try :
   OOOO = oOi11iI11iIiIi ( 'info' ) [ 0 ] . string
   if OOOO == None :
    raise
  except :
   OOOO = ''
   if 89 - 89: IIii1I
  try :
   IIIii1II1II = oOi11iI11iIiIi ( 'genre' ) [ 0 ] . string
   if IIIii1II1II == None :
    raise
  except :
   IIIii1II1II = ''
   if 21 - 21: I1 % I1
  try :
   i11i1 = oOi11iI11iIiIi ( 'date' ) [ 0 ] . string
   if i11i1 == None :
    raise
  except :
   i11i1 = ''
   if 27 - 27: i11iIiiIii / O00OoOoo00
  oOoO00O0 = None
  if oOi11iI11iIiIi ( 'regex' ) :
   try :
    oOoOOo = oOi11iI11iIiIi ( 'regex' )
    oOoO00O0 = OO ( oOoOOo )
   except :
    pass
    if 3 - 3: OOO0O0O0ooooo / o00O00O0O0O
  try :
   if len ( Iiii ) > 1 :
    if 31 - 31: OoOooOOOO + O0Oooo00 . II1
    ooOooo0 = 0
    oO0OO0 = [ ]
    for O000OO0 in Iiii :
     if I1IiI . getSetting ( 'ask_playlist_items' ) == 'true' :
      if oOoO00O0 :
       oO0OO0 . append ( O000OO0 + '&regexs=' + oOoO00O0 )
      elif any ( x in O000OO0 for x in OO0o ) and O000OO0 . startswith ( 'http' ) :
       oO0OO0 . append ( O000OO0 + '&mode=19' )
     else :
      oO0OO0 . append ( O000OO0 )
    if I1IiI . getSetting ( 'add_playlist' ) == "false" :
     for O000OO0 in Iiii :
      ooOooo0 += 1
      print 'ADDLINK 1'
      II1IIIIiII1i ( O000OO0 , '%s) %s' % ( ooOooo0 , Iii1I1I11iiI1 . encode ( 'utf-8' , 'ignore' ) ) , oooOo0OOOoo0 , OOOoOo , OOOO , IIIii1II1II , i11i1 , True , oO0OO0 , oOoO00O0 , oo00OO0000oO )
    else :
     II1IIIIiII1i ( '' , Iii1I1I11iiI1 . encode ( 'utf-8' , 'ignore' ) , oooOo0OOOoo0 , OOOoOo , OOOO , IIIii1II1II , i11i1 , True , oO0OO0 , oOoO00O0 , oo00OO0000oO )
   else :
    if O00 :
     iiI1 ( Iii1I1I11iiI1 . encode ( 'utf-8' ) , iI1iIIIi1i [ 0 ] . encode ( 'utf-8' ) , 1 , oooOo0OOOoo0 , fanart , OOOO , IIIii1II1II , i11i1 , None , 'source' )
    elif O0ooo0 :
     iiI1 ( Iii1I1I11iiI1 . encode ( 'utf-8' ) , iI1iIIIi1i [ 0 ] , 53 , oooOo0OOOoo0 , fanart , OOOO , IIIii1II1II , i11i1 , None , 'source' )
    elif Iiii [ 0 ] . find ( 'sublink' ) > 0 :
     iiI1 ( Iii1I1I11iiI1 . encode ( 'utf-8' ) , Iiii [ 0 ] , 30 , oooOo0OOOoo0 , fanart , '' , '' , '' , '' )
     if 82 - 82: ooO0O - ooO0O + oo
    else :
     II1IIIIiII1i ( Iiii [ 0 ] , Iii1I1I11iiI1 . encode ( 'utf-8' , 'ignore' ) , oooOo0OOOoo0 , OOOoOo , OOOO , IIIii1II1II , i11i1 , True , None , oOoO00O0 , oo00OO0000oO )
     if 8 - 8: O0Oooo00 % o00O00O0O0O * iI1 % i1Ii . O00OoO000O / O00OoO000O
     if 81 - 81: Ooo00oOo00o
  except :
   o0O00oooo ( 'There was a problem adding item - ' + Iii1I1I11iiI1 . encode ( 'utf-8' , 'ignore' ) )
 print 'FINISH GET ITEMS *****'
 if 99 - 99: iI1 * iIiiiI1IiI1I1 * ooiii11iII
def OO ( reg_item ) :
 try :
  oOoO00O0 = { }
  for O000OO0 in reg_item :
   oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] = { }
   if 92 - 92: IiIIi1I1Iiii
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'expre' ] = O000OO0 ( 'expres' ) [ 0 ] . string
    if not oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'expre' ] :
     oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'expre' ] = ''
   except :
    o0O00oooo ( "Regex: -- No Referer --" )
   oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'page' ] = O000OO0 ( 'page' ) [ 0 ] . string
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'refer' ] = O000OO0 ( 'referer' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- No Referer --" )
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'connection' ] = O000OO0 ( 'connection' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- No connection --" )
    if 40 - 40: oo / ooO0O
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'notplayable' ] = O000OO0 ( 'notplayable' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- No notplayable --" )
    if 79 - 79: Ooo00oOo00o - IIii1I + i1Ii - ooiii11iII
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'noredirect' ] = O000OO0 ( 'noredirect' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- No noredirect --" )
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'origin' ] = O000OO0 ( 'origin' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- No origin --" )
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'includeheaders' ] = O000OO0 ( 'includeheaders' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- No includeheaders --" )
    if 93 - 93: iIiiiI1IiI1I1 . IIiIiII11i - IiIIi1I1Iiii + oo
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'x-req' ] = O000OO0 ( 'x-req' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- No x-req --" )
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'x-forward' ] = O000OO0 ( 'x-forward' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- No x-forward --" )
    if 61 - 61: iIiiiI1IiI1I1
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'agent' ] = O000OO0 ( 'agent' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- No User Agent --" )
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'post' ] = O000OO0 ( 'post' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- Not a post" )
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'rawpost' ] = O000OO0 ( 'rawpost' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- Not a rawpost" )
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'htmlunescape' ] = O000OO0 ( 'htmlunescape' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- Not a htmlunescape" )
    if 15 - 15: i11iIiiIii % IIiIiII11i * I1 / ooiii11iII
    if 90 - 90: o00O00O0O0O
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'readcookieonly' ] = O000OO0 ( 'readcookieonly' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- Not a readCookieOnly" )
    if 31 - 31: OoOooOOOO + OOO0O0O0ooooo
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'cookiejar' ] = O000OO0 ( 'cookiejar' ) [ 0 ] . string
    if not oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'cookiejar' ] :
     oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'cookiejar' ] = ''
   except :
    o0O00oooo ( "Regex: -- Not a cookieJar" )
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'setcookie' ] = O000OO0 ( 'setcookie' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- Not a setcookie" )
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'appendcookie' ] = O000OO0 ( 'appendcookie' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- Not a appendcookie" )
    if 87 - 87: O00OoO000O
   try :
    oOoO00O0 [ O000OO0 ( 'name' ) [ 0 ] . string ] [ 'ignorecache' ] = O000OO0 ( 'ignorecache' ) [ 0 ] . string
   except :
    o0O00oooo ( "Regex: -- no ignorecache" )
    if 45 - 45: Ooo00oOo00o / II1 - o00O00O0O0O / i1Ii % ooO0O
    if 83 - 83: IIiIiII11i . IIii1I - ooO0O * i11iIiiIii
    if 20 - 20: O00ooooo00 * ooiii11iII + iIiiiI1IiI1I1 % O0Oooo00 % iI1
    if 13 - 13: IiIIi1I1Iiii
    if 60 - 60: O00OoOoo00 * IIiIiII11i
  oOoO00O0 = urllib . quote ( repr ( oOoO00O0 ) )
  return oOoO00O0
  if 17 - 17: OoOooOOOO % IiIIi1I1Iiii / O00OoOoo00 . ooO0O * OoOooOOOO - iIiiiI1IiI1I1
 except :
  oOoO00O0 = None
  o0O00oooo ( 'regex Error: ' + Iii1I1I11iiI1 . encode ( 'utf-8' , 'ignore' ) )
  if 41 - 41: i1Ii
def oOOoo0o0OOOO ( url ) :
 try :
  for O000OO0 in range ( 1 , 51 ) :
   ii11i11i1 = i1IiII1III ( url )
   if "EXT-X-STREAM-INF" in ii11i11i1 : return url
   if not "EXTM3U" in ii11i11i1 : return
   xbmc . sleep ( 2000 )
  return
 except :
  return
  if 30 - 30: OOO0O0O0ooooo
  if 99 - 99: iIiiiI1IiI1I1 * ooO0O % IIii1I / i1Ii
def OOO00O0oOOo ( regexs , url , cookieJar = None , forCookieJarOnly = False , recursiveCall = False , cachedPages = { } , rawPost = False , cookie_jar_file = None ) :
 if not recursiveCall :
  regexs = eval ( urllib . unquote ( regexs ) )
  if 71 - 71: I1 / O0Oooo00 / ooiii11iII % OoOooOOOO
  if 51 - 51: ooO0O * OOO0O0O0ooooo / iIiiiI1IiI1I1 . i1Ii % OoOooOOOO / IIiIiII11i
 ii1iii1I1I = re . compile ( '\$doregex\[([^\]]*)\]' ) . findall ( url )
 if 95 - 95: ooO0O
 Ooo0oo = True
 if 41 - 41: oo * I1 / oo % iI1
 if 18 - 18: iIiiiI1IiI1I1 . II1 % oo % i1Ii
 if 9 - 9: Ooo00oOo00o - IiIIi1I1Iiii * II1 . IiIIi1I1Iiii
 if 2 - 2: II1 % OoOooOOOO
 for oOoOOo0oo0 in ii1iii1I1I :
  if oOoOOo0oo0 in regexs :
   if 60 - 60: O00OoO000O * ooiii11iII + IiIIi1I1Iiii
   IIi1i1IiIIi1i = regexs [ oOoOOo0oo0 ]
   if 54 - 54: O00OoO000O
   O0iIi1IiII = False
   if 27 - 27: o00O00O0O0O . I1 . IIii1I . IIii1I
   if 20 - 20: O0Oooo00 / O00ooooo00
   if 'cookiejar' in IIi1i1IiIIi1i :
    if 71 - 71: oo . O00ooooo00
    O0iIi1IiII = IIi1i1IiIIi1i [ 'cookiejar' ]
    if '$doregex' in O0iIi1IiII :
     cookieJar = OOO00O0oOOo ( regexs , IIi1i1IiIIi1i [ 'cookiejar' ] , cookieJar , True , True , cachedPages )
     O0iIi1IiII = True
    else :
     O0iIi1IiII = True
     if 94 - 94: OoOooOOOO . ooiii11iII
   if O0iIi1IiII :
    if cookieJar == None :
     if 84 - 84: OOO0O0O0ooooo . I1 - iIiiiI1IiI1I1 . O00OoO000O / iIiiiI1IiI1I1
     cookie_jar_file = None
     if 'open[' in IIi1i1IiIIi1i [ 'cookiejar' ] :
      cookie_jar_file = IIi1i1IiIIi1i [ 'cookiejar' ] . split ( 'open[' ) [ 1 ] . split ( ']' ) [ 0 ]
      if 47 - 47: II1
     cookieJar = ii1i1i1IiII ( cookie_jar_file )
     if cookie_jar_file :
      O0o ( cookieJar , cookie_jar_file )
      if 41 - 41: IiIIi1I1Iiii / i1Ii * i1Ii - OoOooOOOO . ooiii11iII . II1
      if 42 - 42: OoOooOOOO % IiIIi1I1Iiii / i11iIiiIii + OoOooOOOO
      if 84 - 84: ooiii11iII . Ooo00oOo00o . iIiiiI1IiI1I1 . I1 / i1Ii % O00OoOoo00
    elif 'save[' in IIi1i1IiIIi1i [ 'cookiejar' ] :
     cookie_jar_file = IIi1i1IiIIi1i [ 'cookiejar' ] . split ( 'save[' ) [ 1 ] . split ( ']' ) [ 0 ]
     OOO0oOoO0O = os . path . join ( iIiiiI , cookie_jar_file )
     print 'complete_path' , OOO0oOoO0O
     O0o ( cookieJar , cookie_jar_file )
     if 84 - 84: OOO0O0O0ooooo * II1 - ooO0O * ooO0O
     if 8 - 8: O00OoO000O / O00ooooo00 . iI1
   if IIi1i1IiIIi1i [ 'page' ] and '$doregex' in IIi1i1IiIIi1i [ 'page' ] :
    IIi1i1IiIIi1i [ 'page' ] = OOO00O0oOOo ( regexs , IIi1i1IiIIi1i [ 'page' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages )
    if 41 - 41: o00O00O0O0O + Ooo00oOo00o
   if 'setcookie' in IIi1i1IiIIi1i and IIi1i1IiIIi1i [ 'setcookie' ] and '$doregex' in IIi1i1IiIIi1i [ 'setcookie' ] :
    IIi1i1IiIIi1i [ 'setcookie' ] = OOO00O0oOOo ( regexs , IIi1i1IiIIi1i [ 'setcookie' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages )
   if 'appendcookie' in IIi1i1IiIIi1i and IIi1i1IiIIi1i [ 'appendcookie' ] and '$doregex' in IIi1i1IiIIi1i [ 'appendcookie' ] :
    IIi1i1IiIIi1i [ 'appendcookie' ] = OOO00O0oOOo ( regexs , IIi1i1IiIIi1i [ 'appendcookie' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages )
    if 86 - 86: oo . IIii1I - Ooo00oOo00o
    if 56 - 56: OOO0O0O0ooooo
   if 'post' in IIi1i1IiIIi1i and '$doregex' in IIi1i1IiIIi1i [ 'post' ] :
    IIi1i1IiIIi1i [ 'post' ] = OOO00O0oOOo ( regexs , IIi1i1IiIIi1i [ 'post' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages )
    print 'post is now' , IIi1i1IiIIi1i [ 'post' ]
    if 61 - 61: O0Oooo00 / OoOooOOOO / IiIIi1I1Iiii * OOO0O0O0ooooo
   if 'rawpost' in IIi1i1IiIIi1i and '$doregex' in IIi1i1IiIIi1i [ 'rawpost' ] :
    IIi1i1IiIIi1i [ 'rawpost' ] = OOO00O0oOOo ( regexs , IIi1i1IiIIi1i [ 'rawpost' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages , rawPost = True )
    if 23 - 23: iI1 - OoOooOOOO + I1
    if 12 - 12: IIiIiII11i / O00OoO000O % O0Oooo00 / i11iIiiIii % II1
   if 'rawpost' in IIi1i1IiIIi1i and '$epoctime$' in IIi1i1IiIIi1i [ 'rawpost' ] :
    IIi1i1IiIIi1i [ 'rawpost' ] = IIi1i1IiIIi1i [ 'rawpost' ] . replace ( '$epoctime$' , IiIi1II11i ( ) )
    if 42 - 42: O00OoOoo00 * oo % O00OoO000O - oo . i11iIiiIii - ooiii11iII
   if 'rawpost' in IIi1i1IiIIi1i and '$epoctime2$' in IIi1i1IiIIi1i [ 'rawpost' ] :
    IIi1i1IiIIi1i [ 'rawpost' ] = IIi1i1IiIIi1i [ 'rawpost' ] . replace ( '$epoctime2$' , o0oO0oOO ( ) )
    if 89 - 89: O00OoO000O + i1Ii * O00OoO000O / O00OoO000O
    if 46 - 46: Ooo00oOo00o
   O0000 = ''
   if IIi1i1IiIIi1i [ 'page' ] and IIi1i1IiIIi1i [ 'page' ] in cachedPages and not 'ignorecache' in IIi1i1IiIIi1i and forCookieJarOnly == False :
    O0000 = cachedPages [ IIi1i1IiIIi1i [ 'page' ] ]
   else :
    if IIi1i1IiIIi1i [ 'page' ] and not IIi1i1IiIIi1i [ 'page' ] == '' and IIi1i1IiIIi1i [ 'page' ] . startswith ( 'http' ) :
     if '$epoctime$' in IIi1i1IiIIi1i [ 'page' ] :
      IIi1i1IiIIi1i [ 'page' ] = IIi1i1IiIIi1i [ 'page' ] . replace ( '$epoctime$' , IiIi1II11i ( ) )
     if '$epoctime2$' in IIi1i1IiIIi1i [ 'page' ] :
      IIi1i1IiIIi1i [ 'page' ] = IIi1i1IiIIi1i [ 'page' ] . replace ( '$epoctime2$' , o0oO0oOO ( ) )
      if 64 - 64: iIiiiI1IiI1I1 - IIiIiII11i
      if 68 - 68: O00OoO000O - OoOooOOOO - IIii1I / oo + OoOooOOOO - Ooo00oOo00o
     O00Oo = IIi1i1IiIIi1i [ 'page' ] . split ( '|' )
     I1ii = O00Oo [ 0 ]
     Ii1i1i1111 = None
     if len ( O00Oo ) > 1 :
      Ii1i1i1111 = O00Oo [ 1 ]
     O0O = urllib2 . Request ( I1ii )
     O0O . add_header ( 'User-Agent' , 'O0oO0o0o0o' )
     if 'refer' in IIi1i1IiIIi1i :
      O0O . add_header ( 'Referer' , IIi1i1IiIIi1i [ 'refer' ] )
     if 'agent' in IIi1i1IiIIi1i :
      O0O . add_header ( 'User-agent' , IIi1i1IiIIi1i [ 'agent' ] )
     if 'x-req' in IIi1i1IiIIi1i :
      O0O . add_header ( 'X-Requested-With' , IIi1i1IiIIi1i [ 'x-req' ] )
     if 'x-forward' in IIi1i1IiIIi1i :
      O0O . add_header ( 'X-Forwarded-For' , IIi1i1IiIIi1i [ 'x-forward' ] )
     if 'setcookie' in IIi1i1IiIIi1i :
      print 'adding cookie' , IIi1i1IiIIi1i [ 'setcookie' ]
      O0O . add_header ( 'Cookie' , IIi1i1IiIIi1i [ 'setcookie' ] )
     if 'appendcookie' in IIi1i1IiIIi1i :
      print 'appending cookie to cookiejar' , IIi1i1IiIIi1i [ 'appendcookie' ]
      o0oO0O00oOo = IIi1i1IiIIi1i [ 'appendcookie' ]
      o0oO0O00oOo = o0oO0O00oOo . split ( ';' )
      for I1111I1II11 in o0oO0O00oOo :
       iiiIIIIiIi , Iii = I1111I1II11 . split ( '=' )
       IIIII1iii , iiiIIIIiIi = iiiIIIIiIi . split ( ':' )
       IIiiii = cookielib . Cookie ( version = 0 , name = iiiIIIIiIi , value = Iii , port = None , port_specified = False , domain = IIIII1iii , domain_specified = False , domain_initial_dot = False , path = '/' , path_specified = True , secure = False , expires = None , discard = True , comment = None , comment_url = None , rest = { 'HttpOnly' : None } , rfc2109 = False )
       cookieJar . set_cookie ( IIiiii )
       if 37 - 37: O0Oooo00 % O00OoO000O
       if 83 - 83: OoOooOOOO . ooiii11iII + iI1 - OoOooOOOO * ooiii11iII / ooiii11iII
       if 39 - 39: ooiii11iII / IiIIi1I1Iiii % Ooo00oOo00o % i11iIiiIii
       if 90 - 90: ooiii11iII - II1
     if 'origin' in IIi1i1IiIIi1i :
      O0O . add_header ( 'Origin' , IIi1i1IiIIi1i [ 'origin' ] )
     if Ii1i1i1111 :
      Ii1i1i1111 = Ii1i1i1111 . split ( '&' )
      for I1111I1II11 in Ii1i1i1111 :
       iiiIIIIiIi , Iii = I1111I1II11 . split ( '=' )
       O0O . add_header ( iiiIIIIiIi , Iii )
       if 96 - 96: OOO0O0O0ooooo . i1Ii % Ooo00oOo00o * IIii1I
       if 54 - 54: i1Ii * ooiii11iII - II1 % IIiIiII11i + OOO0O0O0ooooo
     if not cookieJar == None :
      if 6 - 6: O00OoOoo00 - iIiiiI1IiI1I1 / iI1 + i11iIiiIii + OoOooOOOO
      O0O0o0o0o = urllib2 . HTTPCookieProcessor ( cookieJar )
      IIIIIiI = urllib2 . build_opener ( O0O0o0o0o , urllib2 . HTTPBasicAuthHandler ( ) , urllib2 . HTTPHandler ( ) )
      IIIIIiI = urllib2 . install_opener ( IIIIIiI )
      if 'noredirect' in IIi1i1IiIIi1i :
       Oo0000O0OOooO = urllib2 . build_opener ( I1IiiI )
       IIIIIiI = urllib2 . install_opener ( Oo0000O0OOooO )
       if 54 - 54: I1 / IIiIiII11i * iI1 + II1 - o00O00O0O0O / II1
     if 'connection' in IIi1i1IiIIi1i :
      print '..........................connection//////.' , IIi1i1IiIIi1i [ 'connection' ]
      from keepalive import HTTPHandler
      I111IIiii1Ii = HTTPHandler ( )
      IIIIIiI = urllib2 . build_opener ( I111IIiii1Ii )
      urllib2 . install_opener ( IIIIIiI )
      if 13 - 13: iI1 . IIiIiII11i * iI1 + IIiIiII11i
      if 59 - 59: IIiIiII11i + i11iIiiIii + O00ooooo00 / I1
     I11 = None
     if 47 - 47: O00OoOoo00 / iI1 / o00O00O0O0O
     if 'post' in IIi1i1IiIIi1i :
      oo0oooOo = IIi1i1IiIIi1i [ 'post' ]
      if '$LiveStreamRecaptcha' in oo0oooOo :
       ( o0OO0O0Oo , OOOOO ) = OOoOOo0O00O ( IIi1i1IiIIi1i [ 'page' ] )
       if o0OO0O0Oo :
        oo0oooOo += 'recaptcha_challenge_field:' + o0OO0O0Oo + ',recaptcha_response_field:' + OOOOO
      iiIii1I = oo0oooOo . split ( ',' ) ;
      I11 = { }
      for i1I11iIiII in iiIii1I :
       iiiIIIIiIi = i1I11iIiII . split ( ':' ) [ 0 ] ;
       Iii = i1I11iIiII . split ( ':' ) [ 1 ] ;
       I11 [ iiiIIIIiIi ] = Iii
      I11 = urllib . urlencode ( I11 )
      if 66 - 66: IiIIi1I1Iiii - O0Oooo00 * ooO0O + oo + O0Oooo00 - IIii1I
     if 'rawpost' in IIi1i1IiIIi1i :
      I11 = IIi1i1IiIIi1i [ 'rawpost' ]
      if '$LiveStreamRecaptcha' in I11 :
       ( o0OO0O0Oo , OOOOO ) = OOoOOo0O00O ( IIi1i1IiIIi1i [ 'page' ] )
       if o0OO0O0Oo :
        I11 += '&recaptcha_challenge_field=' + o0OO0O0Oo + '&recaptcha_response_field=' + OOOOO
        if 17 - 17: iI1
        if 22 - 22: I1 + IIii1I
        if 24 - 24: oo % O00ooooo00 + o00O00O0O0O . i11iIiiIii . O00OoOoo00
        if 17 - 17: O00OoOoo00 . iIiiiI1IiI1I1 . O00OoO000O / O00OoOoo00
     if I11 :
      O00o0OO = urllib2 . urlopen ( O0O , I11 )
     else :
      O00o0OO = urllib2 . urlopen ( O0O )
      if 57 - 57: I1
     O0000 = O00o0OO . read ( )
     O0000 = oO0 ( O0000 )
     if 87 - 87: iI1 % i1Ii
     if 'includeheaders' in IIi1i1IiIIi1i :
      O0000 += str ( O00o0OO . headers . get ( 'Set-Cookie' ) )
      if 83 - 83: iIiiiI1IiI1I1 - I1
     O00o0OO . close ( )
     cachedPages [ IIi1i1IiIIi1i [ 'page' ] ] = O0000
     if 35 - 35: O00ooooo00 - IIii1I + O00ooooo00
     if 86 - 86: IIii1I + oo . i11iIiiIii - i1Ii
     if 51 - 51: oo
     if forCookieJarOnly :
      return cookieJar
    elif IIi1i1IiIIi1i [ 'page' ] and not IIi1i1IiIIi1i [ 'page' ] . startswith ( 'http' ) :
     if IIi1i1IiIIi1i [ 'page' ] . startswith ( '$pyFunction:' ) :
      I11IIIiIi11 = I11iiIi1i1 ( IIi1i1IiIIi1i [ 'page' ] . split ( '$pyFunction:' ) [ 1 ] , '' , cookieJar )
      if forCookieJarOnly :
       return cookieJar
      O0000 = I11IIIiIi11
     else :
      O0000 = IIi1i1IiIIi1i [ 'page' ]
   if '$pyFunction:playmedia(' in IIi1i1IiIIi1i [ 'expre' ] or 'ActivateWindow' in IIi1i1IiIIi1i [ 'expre' ] or any ( x in url for x in Oo0Ooo ) :
    Ooo0oo = False
   if '$doregex' in IIi1i1IiIIi1i [ 'expre' ] :
    IIi1i1IiIIi1i [ 'expre' ] = OOO00O0oOOo ( regexs , IIi1i1IiIIi1i [ 'expre' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages )
    if 41 - 41: i1Ii % O00OoOoo00
    if 12 - 12: OoOooOOOO
   if not IIi1i1IiIIi1i [ 'expre' ] == '' :
    print 'doing it ' , IIi1i1IiIIi1i [ 'expre' ]
    if '$LiveStreamCaptcha' in IIi1i1IiIIi1i [ 'expre' ] :
     I11IIIiIi11 = ooOo0O ( IIi1i1IiIIi1i , O0000 , cookieJar )
     if 37 - 37: i1Ii % Ooo00oOo00o
     url = url . replace ( "$doregex[" + oOoOOo0oo0 + "]" , I11IIIiIi11 )
    elif IIi1i1IiIIi1i [ 'expre' ] . startswith ( '$pyFunction:' ) :
     if 79 - 79: O00OoOoo00 + IIiIiII11i / IIiIiII11i
     I11IIIiIi11 = I11iiIi1i1 ( IIi1i1IiIIi1i [ 'expre' ] . split ( '$pyFunction:' ) [ 1 ] , O0000 , cookieJar )
     if 'ActivateWindow' in IIi1i1IiIIi1i [ 'expre' ] : return
     print 'still hre'
     print 'url k val' , url , oOoOOo0oo0 , I11IIIiIi11
     if 71 - 71: OoOooOOOO * Ooo00oOo00o % II1 % Ooo00oOo00o / IIiIiII11i
     url = url . replace ( "$doregex[" + oOoOOo0oo0 + "]" , I11IIIiIi11 )
    else :
     if not O0000 == '' :
      Oo0ooo0Ooo = re . compile ( IIi1i1IiIIi1i [ 'expre' ] ) . search ( O0000 )
      I11IIIiIi11 = ''
      try :
       I11IIIiIi11 = Oo0ooo0Ooo . group ( 1 ) . strip ( )
      except : traceback . print_exc ( )
     else :
      I11IIIiIi11 = IIi1i1IiIIi1i [ 'expre' ]
     if rawPost :
      print 'rawpost'
      I11IIIiIi11 = urllib . quote_plus ( I11IIIiIi11 )
     if 'htmlunescape' in IIi1i1IiIIi1i :
      if 9 - 9: IiIIi1I1Iiii
      import HTMLParser
      I11IIIiIi11 = HTMLParser . HTMLParser ( ) . unescape ( I11IIIiIi11 )
     url = url . replace ( "$doregex[" + oOoOOo0oo0 + "]" , I11IIIiIi11 )
     if 99 - 99: I1 - ooiii11iII - iI1 % Ooo00oOo00o
   else :
    url = url . replace ( "$doregex[" + oOoOOo0oo0 + "]" , '' )
 if '$epoctime$' in url :
  url = url . replace ( '$epoctime$' , IiIi1II11i ( ) )
 if '$epoctime2$' in url :
  url = url . replace ( '$epoctime2$' , o0oO0oOO ( ) )
  if 21 - 21: iIiiiI1IiI1I1 % O00OoOoo00 . O00ooooo00 - II1
 if '$GUID$' in url :
  import uuid
  url = url . replace ( '$GUID$' , str ( uuid . uuid1 ( ) ) . upper ( ) )
 if '$get_cookies$' in url :
  url = url . replace ( '$get_cookies$' , iiOOOO0o ( cookieJar ) )
  if 10 - 10: ooiii11iII % IIiIiII11i
 if recursiveCall : return url
 print 'final url' , url
 if url == "" :
  return
 else :
  return url , Ooo0oo
  if 97 - 97: II1 - ooiii11iII
  if 58 - 58: IIii1I + OOO0O0O0ooooo
  if 30 - 30: O00OoO000O % o00O00O0O0O * OoOooOOOO - O00OoOoo00 * i1Ii % O00OoO000O
def iiiiI11ii ( t ) :
 import hashlib
 I1111I1II11 = hashlib . md5 ( )
 I1111I1II11 . update ( t )
 return I1111I1II11 . hexdigest ( )
 if 96 - 96: o00O00O0O0O . OOO0O0O0ooooo / o00O00O0O0O % OOO0O0O0ooooo
def o0o000 ( encrypted ) :
 i1iiiIii11 = ""
 for I11IIIiIi11 in encrypted . split ( ':' ) :
  i1iiiIii11 += chr ( int ( I11IIIiIi11 . replace ( "0m0" , "" ) ) / 84 / 5 )
 return i1iiiIii11
 if 67 - 67: O0Oooo00 % oo . oo - O00OoO000O
def O00ooOo ( media_url ) :
 try :
  import CustomPlayer
  oOO0o00O = CustomPlayer . MyXBMCPlayer ( )
  oOoO = xbmcgui . ListItem ( label = str ( Iii1I1I11iiI1 ) , iconImage = "DefaultVideo.png" , thumbnailImage = xbmc . getInfoImage ( "ListItem.Thumb" ) , path = media_url )
  oOO0o00O . play ( media_url , oOoO )
  xbmc . sleep ( 1000 )
  while oOO0o00O . is_active :
   xbmc . sleep ( 200 )
 except :
  traceback . print_exc ( )
 return ''
 if 26 - 26: oo / IiIIi1I1Iiii - O00ooooo00 + I1
 if 38 - 38: II1 / O00OoOoo00 . OOO0O0O0ooooo / O00ooooo00 / IiIIi1I1Iiii + IIii1I
def ooO00O00oOO ( page_value , referer = None ) :
 if referer :
  referer = [ ( 'Referer' , referer ) ]
 if page_value . startswith ( "http" ) :
  I1IIII1ii = page_value
  page_value = i1IiII1III ( page_value , headers = referer )
  if 13 - 13: II1 * iI1 - i1Ii / OoOooOOOO + I1 + ooO0O
 iii1III1i = "(eval\(function\(p,a,c,k,e,(?:r|d).*)"
 if 17 - 17: iIiiiI1IiI1I1 / iIiiiI1IiI1I1
 o0OO0Oo = re . compile ( iii1III1i ) . findall ( page_value )
 O0OoO0ooOO0o = ""
 if o0OO0Oo and len ( o0OO0Oo ) > 0 :
  for Iii in o0OO0Oo :
   I11iiii1I = iiiiI1iiiIi ( Iii )
   o0oO0OoO0 = ooo ( I11iiii1I , '\'(.*?)\'' )
   if 'unescape' in I11iiii1I :
    I11iiii1I = urllib . unquote ( o0oO0OoO0 )
   O0OoO0ooOO0o += I11iiii1I + '\n'
  print 'final value is ' , O0OoO0ooOO0o
  if 70 - 70: iI1 - iI1
  I1IIII1ii = ooo ( O0OoO0ooOO0o , 'src="(.*?)"' )
  if 57 - 57: IIiIiII11i - O0Oooo00 + Ooo00oOo00o % IiIIi1I1Iiii
  page_value = i1IiII1III ( I1IIII1ii , headers = referer )
  if 26 - 26: o00O00O0O0O . o00O00O0O0O
  if 35 - 35: ooiii11iII . oo * i11iIiiIii
  if 44 - 44: i11iIiiIii / IiIIi1I1Iiii
 Ii1IIi = ooo ( page_value , 'streamer\'.*?\'(.*?)\'\)' )
 i111i11I1ii = ooo ( page_value , 'file\',\s\'(.*?)\'' )
 if 64 - 64: iI1 / i11iIiiIii / O0Oooo00 . II1
 if 11 - 11: I1 % O00ooooo00
 return Ii1IIi + ' playpath=' + i111i11I1ii + ' pageUrl=' + I1IIII1ii
 if 16 - 16: IIiIiII11i + O00OoO000O % oo
def o0o0oOo000o0 ( page_value , referer = None ) :
 if referer :
  referer = [ ( 'Referer' , referer ) ]
 if page_value . startswith ( "http" ) :
  page_value = i1IiII1III ( page_value , headers = referer )
 iii1III1i = "var a = (.*?);\s*var b = (.*?);\s*var c = (.*?);\s*var d = (.*?);\s*var f = (.*?);\s*var v_part = '(.*?)';"
 o0OO0Oo = re . compile ( iii1III1i ) . findall ( page_value ) [ 0 ]
 if 25 - 25: I1 + oo . O0Oooo00 % oo * OoOooOOOO
 IIii11Ii1i1I , Iiii1i1 , OooooO0oOOOO , ii1IiIi11 , iiiii1ii1 , Iii = ( o0OO0Oo )
 iiiii1ii1 = int ( iiiii1ii1 )
 IIii11Ii1i1I = int ( IIii11Ii1i1I ) / iiiii1ii1
 Iiii1i1 = int ( Iiii1i1 ) / iiiii1ii1
 OooooO0oOOOO = int ( OooooO0oOOOO ) / iiiii1ii1
 ii1IiIi11 = int ( ii1IiIi11 ) / iiiii1ii1
 if 48 - 48: OOO0O0O0ooooo + OOO0O0O0ooooo . ooiii11iII - O00OoO000O
 o00oo0000 = 'rtmp://' + str ( IIii11Ii1i1I ) + '.' + str ( Iiii1i1 ) + '.' + str ( OooooO0oOOOO ) + '.' + str ( ii1IiIi11 ) + Iii ;
 return o00oo0000
 if 44 - 44: IiIIi1I1Iiii % IIii1I
def oo0ooO0 ( url , useragent = None ) :
 str = '#EXTM3U'
 str += '\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=361816'
 str += '\n' + url + '&bytes=0-200000'
 iiIIIII1i1iI = os . path . join ( iIiiiI , 'testfile.m3u' )
 str += '\n'
 IIiiiiIiIIii ( iiIIIII1i1iI , str )
 if 86 - 86: I1 / O0Oooo00 - O0Oooo00 + O00OoOoo00 + iI1
 return iiIIIII1i1iI
 if 33 - 33: O0Oooo00 . o00O00O0O0O . ooO0O . O00ooooo00
def IIiiiiIiIIii ( file_name , page_data , append = False ) :
 if append :
  iiiii1ii1 = open ( file_name , 'a' )
  iiiii1ii1 . write ( page_data )
  iiiii1ii1 . close ( )
 else :
  iiiii1ii1 = open ( file_name , 'wb' )
  iiiii1ii1 . write ( page_data )
  iiiii1ii1 . close ( )
  return ''
  if 49 - 49: O00OoOoo00
def O0oOOo0o ( file_name ) :
 iiiii1ii1 = open ( file_name , 'rb' )
 ii1IiIi11 = iiiii1ii1 . read ( )
 iiiii1ii1 . close ( )
 return ii1IiIi11
 if 50 - 50: o00O00O0O0O . O00OoOoo00 . Ooo00oOo00o * I1 + iIiiiI1IiI1I1 % i11iIiiIii
def i1i1IiIiIi1Ii ( page_data ) :
 import re , base64 , urllib ;
 oO0Oo = page_data
 while 'geh(' in oO0Oo :
  if oO0Oo . startswith ( 'lol(' ) : oO0Oo = oO0Oo [ 5 : - 1 ]
  if 64 - 64: OoOooOOOO + II1 * II1
  oO0Oo = re . compile ( '"(.*?)"' ) . findall ( oO0Oo ) [ 0 ] ;
  oO0Oo = base64 . b64decode ( oO0Oo ) ;
  oO0Oo = urllib . unquote ( oO0Oo ) ;
 print oO0Oo
 return oO0Oo
 if 41 - 41: O00OoO000O . IiIIi1I1Iiii + IIiIiII11i
def o0O0OO ( page_data ) :
 print 'get_dag_url2' , page_data
 Ii1II11II1iii = i1IiII1III ( page_data ) ;
 o0oOO0ooOoO = '(http.*)'
 import uuid
 ooO0000o00O = str ( uuid . uuid1 ( ) ) . upper ( )
 O0Ooo = re . compile ( o0oOO0ooOoO ) . findall ( Ii1II11II1iii )
 oO00oOOo0Oo = [ ( 'X-Playback-Session-Id' , ooO0000o00O ) ]
 for IIi in O0Ooo :
  try :
   IIIIii = i1IiII1III ( IIi , headers = oO00oOOo0Oo ) ;
   if 40 - 40: OOO0O0O0ooooo
  except : pass
  if 58 - 58: IiIIi1I1Iiii
 return page_data + '|&X-Playback-Session-Id=' + ooO0000o00O
 if 9 - 9: IIii1I % O00OoOoo00 . OoOooOOOO + II1
 if 62 - 62: OOO0O0O0ooooo / IIiIiII11i % OOO0O0O0ooooo * Ooo00oOo00o % IIiIiII11i
def IiOOoo0oO00oo00 ( page_data ) :
 print 'get_dag_url' , page_data
 if page_data . startswith ( 'http://dag.total-stream.net' ) :
  oO00oOOo0Oo = [ ( 'User-Agent' , 'Verismo-BlackUI_(2.4.7.5.8.0.34)' ) ]
  page_data = i1IiII1III ( page_data , headers = oO00oOOo0Oo ) ;
  if 87 - 87: OoOooOOOO . oo . O00ooooo00 . O00ooooo00 - O0Oooo00
 if '127.0.0.1' in page_data :
  return ii1iIIiii1 ( page_data )
 elif ooo ( page_data , 'wmsAuthSign%3D([^%&]+)' ) != '' :
  ooOo0O0o0 = ooo ( page_data , '&ver_t=([^&]+)&' ) + '?wmsAuthSign=' + ooo ( page_data , 'wmsAuthSign%3D([^%&]+)' ) + '==/mp4:' + ooo ( page_data , '\\?y=([^&]+)&' )
 else :
  ooOo0O0o0 = ooo ( page_data , 'href="([^"]+)"[^"]+$' )
  if len ( ooOo0O0o0 ) == 0 :
   ooOo0O0o0 = page_data
 ooOo0O0o0 = ooOo0O0o0 . replace ( ' ' , '%20' )
 return ooOo0O0o0
 if 65 - 65: O00OoO000O + OOO0O0O0ooooo
def ooo ( data , re_patten ) :
 o0Oo0oO0oOO00 = ''
 IIi1i1IiIIi1i = re . search ( re_patten , data )
 if IIi1i1IiIIi1i != None :
  o0Oo0oO0oOO00 = IIi1i1IiIIi1i . group ( 1 )
 else :
  o0Oo0oO0oOO00 = ''
 return o0Oo0oO0oOO00
 if 32 - 32: II1 - oo - i11iIiiIii * O0Oooo00 / IiIIi1I1Iiii + II1
def ii1iIIiii1 ( page_data ) :
 ooOo0O0o0 = ''
 if '127.0.0.1' in page_data :
  ooOo0O0o0 = ooo ( page_data , '&ver_t=([^&]+)&' ) + ' live=true timeout=15 playpath=' + ooo ( page_data , '\\?y=([a-zA-Z0-9-_\\.@]+)' )
  if 35 - 35: O00ooooo00 - O0Oooo00 * o00O00O0O0O
 if ooo ( page_data , 'token=([^&]+)&' ) != '' :
  ooOo0O0o0 = ooOo0O0o0 + '?token=' + ooo ( page_data , 'token=([^&]+)&' )
 elif ooo ( page_data , 'wmsAuthSign%3D([^%&]+)' ) != '' :
  ooOo0O0o0 = ooo ( page_data , '&ver_t=([^&]+)&' ) + '?wmsAuthSign=' + ooo ( page_data , 'wmsAuthSign%3D([^%&]+)' ) + '==/mp4:' + ooo ( page_data , '\\?y=([^&]+)&' )
 else :
  ooOo0O0o0 = ooo ( page_data , 'HREF="([^"]+)"' )
  if 63 - 63: o00O00O0O0O * O00OoOoo00 . II1 / OoOooOOOO * IiIIi1I1Iiii . O00OoO000O
 if 'dag1.asx' in ooOo0O0o0 :
  return IiOOoo0oO00oo00 ( ooOo0O0o0 )
  if 62 - 62: O00ooooo00 / O00OoO000O . IIiIiII11i * O0Oooo00
 if 'devinlivefs.fplive.net' not in ooOo0O0o0 :
  ooOo0O0o0 = ooOo0O0o0 . replace ( 'devinlive' , 'flive' )
 if 'permlivefs.fplive.net' not in ooOo0O0o0 :
  ooOo0O0o0 = ooOo0O0o0 . replace ( 'permlive' , 'flive' )
 return ooOo0O0o0
 if 21 - 21: O0Oooo00
 if 81 - 81: I1 / IIii1I - O00OoO000O * ooiii11iII . IIiIiII11i * O00OoOoo00
def o0000 ( str_eval ) :
 i111i1i = ""
 try :
  IiIii1I1I = "w,i,s,e=(" + str_eval + ')'
  exec ( IiIii1I1I )
  i111i1i = OO0Oooo0oo ( w , i , s , e )
 except : traceback . print_exc ( file = sys . stdout )
 if 42 - 42: i1Ii * ooiii11iII . ooO0O * IIiIiII11i + oo
 return i111i1i
 if 25 - 25: I1 . IIiIiII11i + iI1
def OO0Oooo0oo ( w , i , s , e ) :
 O00OO0o0 = 0 ;
 oOOOooOo0O = 0 ;
 III1i111i = 0 ;
 iI1i = [ ] ;
 i111iiIIII = [ ] ;
 while True :
  if ( O00OO0o0 < 5 ) :
   i111iiIIII . append ( w [ O00OO0o0 ] )
  elif ( O00OO0o0 < len ( w ) ) :
   iI1i . append ( w [ O00OO0o0 ] ) ;
  O00OO0o0 += 1 ;
  if ( oOOOooOo0O < 5 ) :
   i111iiIIII . append ( i [ oOOOooOo0O ] )
  elif ( oOOOooOo0O < len ( i ) ) :
   iI1i . append ( i [ oOOOooOo0O ] )
  oOOOooOo0O += 1 ;
  if ( III1i111i < 5 ) :
   i111iiIIII . append ( s [ III1i111i ] )
  elif ( III1i111i < len ( s ) ) :
   iI1i . append ( s [ III1i111i ] ) ;
  III1i111i += 1 ;
  if ( len ( w ) + len ( i ) + len ( s ) + len ( e ) == len ( iI1i ) + len ( i111iiIIII ) + len ( e ) ) :
   break ;
   if 80 - 80: IiIIi1I1Iiii * i1Ii + O00OoOoo00 * OoOooOOOO
 I1Ii = '' . join ( iI1i )
 ooooOoO0O = '' . join ( i111iiIIII )
 oOOOooOo0O = 0 ;
 IIII = [ ] ;
 for O00OO0o0 in range ( 0 , len ( iI1i ) , 2 ) :
  if 8 - 8: O0Oooo00 / O00OoOoo00 - i11iIiiIii % IIii1I
  o00o0oOo0O0O = - 1 ;
  if ( ord ( ooooOoO0O [ oOOOooOo0O ] ) % 2 ) :
   o00o0oOo0O0O = 1 ;
   if 79 - 79: O00OoOoo00 + ooiii11iII
  IIII . append ( chr ( int ( I1Ii [ O00OO0o0 : O00OO0o0 + 2 ] , 36 ) - o00o0oOo0O0O ) ) ;
  oOOOooOo0O += 1 ;
  if ( oOOOooOo0O >= len ( i111iiIIII ) ) :
   oOOOooOo0O = 0 ;
 o00oo0000 = '' . join ( IIII )
 if 'eval(function(w,i,s,e)' in o00oo0000 :
  print 'STILL GOing'
  o00oo0000 = re . compile ( 'eval\(function\(w,i,s,e\).*}\((.*?)\)' ) . findall ( o00oo0000 ) [ 0 ]
  return o0000 ( o00oo0000 )
 else :
  print 'FINISHED'
  return o00oo0000
  if 10 - 10: IiIIi1I1Iiii + OOO0O0O0ooooo
def iiiiI1iiiIi ( page_value , regex_for_text = '' , iterations = 1 , total_iteration = 1 ) :
 try :
  Ii1iI = None
  if page_value . startswith ( "http" ) :
   page_value = i1IiII1III ( page_value )
  print 'page_value' , page_value
  if regex_for_text and len ( regex_for_text ) > 0 :
   page_value = re . compile ( regex_for_text ) . findall ( page_value ) [ 0 ]
   if 53 - 53: IIii1I - iI1 % oo * ooiii11iII % O00OoO000O
  page_value = II1Ii ( page_value , iterations , total_iteration )
 except : traceback . print_exc ( file = sys . stdout )
 print 'unpacked' , page_value
 if 'sav1live.tv' in page_value :
  page_value = page_value . replace ( 'sav1live.tv' , 'sawlive.tv' )
  print 'sav1 unpacked' , page_value
 return page_value
 if 57 - 57: oo - iI1 / O00OoO000O % i11iIiiIii
def II1Ii ( sJavascript , iteration = 1 , totaliterations = 2 ) :
 print 'iteration' , iteration
 if sJavascript . startswith ( 'var _0xcb8a=' ) :
  I11oOOooo = sJavascript . split ( 'var _0xcb8a=' )
  IiIii1I1I = "myarray=" + I11oOOooo [ 1 ] . split ( "eval(" ) [ 0 ]
  exec ( IiIii1I1I )
  ooo0O0Oo = 62
  i111II = int ( I11oOOooo [ 1 ] . split ( ",62," ) [ 1 ] . split ( ',' ) [ 0 ] )
  OO0O00o0 = myarray [ 0 ]
  I111 = myarray [ 3 ]
  with open ( 'temp file' + str ( iteration ) + '.js' , "wb" ) as Ii1I1 :
   Ii1I1 . write ( str ( I111 ) )
   if 58 - 58: ooO0O - I1 % IIiIiII11i
 else :
  if 4 - 4: O00ooooo00 + O00OoO000O + O00ooooo00
  I11oOOooo = sJavascript . split ( "rn p}('" )
  print I11oOOooo
  if 31 - 31: i1Ii
  OO0O00o0 , ooo0O0Oo , i111II , I111 = ( '' , '0' , '0' , '' )
  if 78 - 78: i11iIiiIii + O0Oooo00 + ooiii11iII / O0Oooo00 % IIii1I % ooO0O
  IiIii1I1I = "p1,a1,c1,k1=('" + I11oOOooo [ 1 ] . split ( ".spli" ) [ 0 ] + ')'
  exec ( IiIii1I1I )
 I111 = I111 . split ( '|' )
 I11oOOooo = I11oOOooo [ 1 ] . split ( "))'" )
 if 83 - 83: IIii1I % oo % O0Oooo00 % ooiii11iII . O00OoOoo00 % OOO0O0O0ooooo
 if 47 - 47: O0Oooo00
 if 66 - 66: IIiIiII11i - ooO0O
 if 33 - 33: IIiIiII11i / Ooo00oOo00o
 if 12 - 12: iIiiiI1IiI1I1
 if 2 - 2: O00ooooo00 - IIiIiII11i + I1 . iIiiiI1IiI1I1
 if 25 - 25: iI1
 if 34 - 34: oo . IIii1I % OOO0O0O0ooooo
 if 43 - 43: O00OoOoo00 - o00O00O0O0O
 if 70 - 70: o00O00O0O0O / OoOooOOOO % O00OoO000O - i1Ii
 if 47 - 47: o00O00O0O0O
 if 92 - 92: OoOooOOOO + oo % O00ooooo00
 if 23 - 23: ooiii11iII - OoOooOOOO + i1Ii - oo * oo . IiIIi1I1Iiii
 if 47 - 47: iI1 % IIii1I
 if 11 - 11: IIiIiII11i % i1Ii - Ooo00oOo00o - iI1 + O0Oooo00
 if 98 - 98: o00O00O0O0O + i1Ii - Ooo00oOo00o
 if 79 - 79: OoOooOOOO / ooiii11iII . oo - O00OoOoo00
 if 47 - 47: II1 % OOO0O0O0ooooo * o00O00O0O0O . i1Ii
 if 38 - 38: OOO0O0O0ooooo - ooO0O % ooiii11iII
 if 64 - 64: IIii1I
 if 15 - 15: O00OoOoo00 + OoOooOOOO / O00OoOoo00 / ooiii11iII
 if 31 - 31: O00OoO000O + OOO0O0O0ooooo + O00OoO000O . IIii1I + IiIIi1I1Iiii / O0Oooo00
 iIi1ii1I1 = ''
 ii1IiIi11 = ''
 if 6 - 6: IiIIi1I1Iiii % ooO0O * I1 / IIiIiII11i + IiIIi1I1Iiii
 if 39 - 39: oo - IiIIi1I1Iiii / o00O00O0O0O * II1
 Oooo0oOOO0 = str ( oOOO ( OO0O00o0 , ooo0O0Oo , i111II , I111 , iIi1ii1I1 , ii1IiIi11 , iteration ) )
 if 36 - 36: O00OoOoo00 - o00O00O0O0O
 if 24 - 24: O0Oooo00 + O00OoO000O + I1 - IIii1I
 if 49 - 49: I1 . O00OoO000O * oo % ooO0O . OOO0O0O0ooooo
 if 48 - 48: OOO0O0O0ooooo * i1Ii - OOO0O0O0ooooo / i1Ii + oo
 if 52 - 52: Ooo00oOo00o % i1Ii * iIiiiI1IiI1I1
 if iteration >= totaliterations :
  if 4 - 4: I1 % OOO0O0O0ooooo - II1 + O00OoO000O . iI1 % iIiiiI1IiI1I1
  return Oooo0oOOO0
 else :
  if 9 - 9: iIiiiI1IiI1I1 * iIiiiI1IiI1I1 . i11iIiiIii * IIii1I
  return II1Ii ( Oooo0oOOO0 , iteration + 1 )
  if 18 - 18: Ooo00oOo00o . iIiiiI1IiI1I1 % oo % i1Ii
def oOOO ( p , a , c , k , e , d , iteration , v = 1 ) :
 if 87 - 87: IIii1I . II1 * oo
 if 100 - 100: Ooo00oOo00o / O00ooooo00 - IIiIiII11i % i1Ii - IIii1I
 if 17 - 17: I1 / O0Oooo00 % IiIIi1I1Iiii
 while ( c >= 1 ) :
  c = c - 1
  if ( k [ c ] ) :
   o0o = str ( o00o0O0O00 ( c , a ) )
   if v == 1 :
    p = re . sub ( '\\b' + o0o + '\\b' , k [ c ] , p )
   else :
    p = iII ( p , o0o , k [ c ] )
    if 78 - 78: O00OoOoo00 % IIiIiII11i / II1 % OoOooOOOO - o00O00O0O0O
    if 2 - 2: IIii1I
    if 45 - 45: II1 / i11iIiiIii
    if 10 - 10: o00O00O0O0O - iI1 * IIii1I % IIii1I * ooO0O - O00OoOoo00
    if 97 - 97: iIiiiI1IiI1I1 % ooiii11iII + ooiii11iII - Ooo00oOo00o / i1Ii * IIiIiII11i
    if 17 - 17: i1Ii
 return p
 if 39 - 39: O00OoO000O . iIiiiI1IiI1I1
 if 45 - 45: iI1 * oo / IIii1I
 if 77 - 77: ooiii11iII - I1
def iII ( source_str , word_to_find , replace_with ) :
 iiI1iI1I = None
 iiI1iI1I = source_str . split ( word_to_find )
 if len ( iiI1iI1I ) > 1 :
  III1II111Ii1 = [ ]
  o0O0OO0o = 0
  for OOOoOoOOoO0oo0O in iiI1iI1I :
   if 49 - 49: O0Oooo00
   III1II111Ii1 . append ( OOOoOoOOoO0oo0O )
   I11IIIiIi11 = word_to_find
   if 31 - 31: Ooo00oOo00o * i11iIiiIii * i1Ii . i11iIiiIii
   if 12 - 12: oo % ooO0O % O00OoOoo00 . i11iIiiIii * IIii1I
   if o0O0OO0o == len ( iiI1iI1I ) - 1 :
    I11IIIiIi11 = ''
   else :
    if len ( OOOoOoOOoO0oo0O ) == 0 :
     if ( len ( iiI1iI1I [ o0O0OO0o + 1 ] ) == 0 and word_to_find [ 0 ] . lower ( ) not in 'abcdefghijklmnopqrstuvwxyz1234567890_' ) or ( len ( iiI1iI1I [ o0O0OO0o + 1 ] ) > 0 and iiI1iI1I [ o0O0OO0o + 1 ] [ 0 ] . lower ( ) not in 'abcdefghijklmnopqrstuvwxyz1234567890_' ) :
      I11IIIiIi11 = replace_with
      if 66 - 66: i11iIiiIii * IIii1I % II1
    else :
     if ( iiI1iI1I [ o0O0OO0o ] [ - 1 ] . lower ( ) not in 'abcdefghijklmnopqrstuvwxyz1234567890_' ) and ( ( len ( iiI1iI1I [ o0O0OO0o + 1 ] ) == 0 and word_to_find [ 0 ] . lower ( ) not in 'abcdefghijklmnopqrstuvwxyz1234567890_' ) or ( len ( iiI1iI1I [ o0O0OO0o + 1 ] ) > 0 and iiI1iI1I [ o0O0OO0o + 1 ] [ 0 ] . lower ( ) not in 'abcdefghijklmnopqrstuvwxyz1234567890_' ) ) :
      I11IIIiIi11 = replace_with
      if 5 - 5: oo % II1
   III1II111Ii1 . append ( I11IIIiIi11 )
   o0O0OO0o += 1
   if 60 - 60: oo . O00ooooo00 % Ooo00oOo00o % O00OoO000O % OoOooOOOO
  source_str = '' . join ( III1II111Ii1 )
 return source_str
 if 33 - 33: IIii1I - i1Ii * O00OoOoo00 % IIii1I + Ooo00oOo00o . OoOooOOOO
def ooo0O0oOoooO0 ( num , radix ) :
 if 42 - 42: OoOooOOOO % iI1 / Ooo00oOo00o - iI1 * i11iIiiIii
 ii11i11i1 = ""
 if num == 0 : return '0'
 while num > 0 :
  ii11i11i1 = "0123456789abcdefghijklmnopqrstuvwxyz" [ num % radix ] + ii11i11i1
  num /= radix
 return ii11i11i1
 if 19 - 19: iI1 * IIiIiII11i % i11iIiiIii
def o00o0O0O00 ( cc , a ) :
 o0o = "" if cc < a else o00o0O0O00 ( int ( cc / a ) , a )
 cc = ( cc % a )
 iiI1Ii1I = chr ( cc + 29 ) if cc > 35 else str ( ooo0O0oOoooO0 ( cc , 36 ) )
 return o0o + iiI1Ii1I
 if 28 - 28: OoOooOOOO % O00OoO000O
 if 48 - 48: i11iIiiIii % iI1
def iiOOOO0o ( cookieJar ) :
 try :
  i11i11 = ""
  for o0o0o0oO0oOO , Ii11Iii in enumerate ( cookieJar ) :
   i11i11 += Ii11Iii . name + "=" + Ii11Iii . value + ";"
 except : pass
 if 68 - 68: IIiIiII11i % OOO0O0O0ooooo
 return i11i11
 if 74 - 74: O00ooooo00 + oo + IIii1I * oo * IIii1I + I1
 if 64 - 64: IIii1I / OOO0O0O0ooooo % ooO0O . II1 + ooO0O + iI1
def O0o ( cookieJar , COOKIEFILE ) :
 try :
  OOO0oOoO0O = os . path . join ( iIiiiI , COOKIEFILE )
  cookieJar . save ( OOO0oOoO0O , ignore_discard = True )
 except : pass
 if 79 - 79: II1 - ooO0O * ooO0O . oo
def ii1i1i1IiII ( COOKIEFILE ) :
 if 100 - 100: iIiiiI1IiI1I1 * I1 % IIiIiII11i / O00OoOoo00
 OOo = None
 if COOKIEFILE :
  try :
   OOO0oOoO0O = os . path . join ( iIiiiI , COOKIEFILE )
   OOo = cookielib . LWPCookieJar ( )
   OOo . load ( OOO0oOoO0O , ignore_discard = True )
  except :
   OOo = None
   if 99 - 99: oo
 if not OOo :
  OOo = cookielib . LWPCookieJar ( )
  if 77 - 77: O0Oooo00
 return OOo
 if 48 - 48: oo % O00OoOoo00 / I1 . IIii1I * iIiiiI1IiI1I1
def I11iiIi1i1 ( fun_call , page_data , Cookie_Jar ) :
 oo000oO = ''
 if o0oO0 not in sys . path :
  sys . path . append ( o0oO0 )
  if 78 - 78: i1Ii + oo + ooO0O - ooO0O . i11iIiiIii / Ooo00oOo00o
 print fun_call
 try :
  I11i11i1 = 'import ' + fun_call . split ( '.' ) [ 0 ]
  print I11i11i1 , sys . path
  exec ( I11i11i1 )
  print 'done'
 except :
  print 'error in import'
  traceback . print_exc ( file = sys . stdout )
 print 'ret_val=' + fun_call
 exec ( 'ret_val=' + fun_call )
 print oo000oO
 if 68 - 68: IiIIi1I1Iiii . IiIIi1I1Iiii - O00OoOoo00 / I1 . O00OoO000O / O00ooooo00
 return str ( oo000oO )
 if 12 - 12: O00OoOoo00 * O00ooooo00 * I1
def OOoOOo0O00O ( url ) :
 i1iiI = i1IiII1III ( url )
 I11o0000o0Oo = ""
 ooo0O0OOo0OoO = ""
 Ii1i1 = "<script.*?src=\"(.*?recap.*?)\""
 o0Oo0oO0oOO00 = re . findall ( Ii1i1 , i1iiI )
 oOoO00 = False
 i1i = None
 ooo0O0OOo0OoO = None
 if 27 - 27: i1Ii * IiIIi1I1Iiii . oo
 if o0Oo0oO0oOO00 and len ( o0Oo0oO0oOO00 ) > 0 :
  Ii111Iiiii = o0Oo0oO0oOO00 [ 0 ]
  oOoO00 = True
  if 13 - 13: O00OoOoo00 / i11iIiiIii
  iIii1I = 'challenge.*?\'(.*?)\''
  iii11i1 = '\'(.*?)\''
  i1IiI1I111iIi = i1IiII1III ( Ii111Iiiii )
  I11o0000o0Oo = re . findall ( iIii1I , i1IiI1I111iIi ) [ 0 ]
  IiiIIi1 = 'http://www.google.com/recaptcha/api/reload?c=' ;
  iI1iIiiI = Ii111Iiiii . split ( 'k=' ) [ 1 ]
  IiiIIi1 += I11o0000o0Oo + '&k=' + iI1iIiiI + '&captcha_k=1&type=image&lang=en-GB'
  Oo0OOo = i1IiII1III ( IiiIIi1 )
  i1i = re . findall ( iii11i1 , Oo0OOo ) [ 0 ]
  Ii1I11i11I1i = 'http://www.google.com/recaptcha/api/image?c=' + i1i
  if not Ii1I11i11I1i . startswith ( "http" ) :
   Ii1I11i11I1i = 'http://www.google.com/recaptcha/api/' + Ii1I11i11I1i
  import random
  iiiIIIIiIi = random . randrange ( 100 , 1000 , 5 )
  oO00 = os . path . join ( iIiiiI , str ( iiiIIIIiIi ) + "captcha.img" )
  IiI1II11iiI = open ( oO00 , "wb" )
  IiI1II11iiI . write ( i1IiII1III ( Ii1I11i11I1i ) )
  IiI1II11iiI . close ( )
  o0oOOooo00O = OO0ooo0 ( captcha = oO00 )
  ooo0O0OOo0OoO = o0oOOooo00O . get ( )
  os . remove ( oO00 )
 return i1i , ooo0O0OOo0OoO
 if 7 - 7: O00OoOoo00 - iI1 * OoOooOOOO + O0Oooo00 . O00OoOoo00
def i1IiII1III ( url , cookieJar = None , post = None , timeout = 20 , headers = None ) :
 if 85 - 85: OOO0O0O0ooooo
 if 32 - 32: II1 . Ooo00oOo00o / IiIIi1I1Iiii * O0Oooo00 / O0Oooo00 * i1Ii
 O0O0o0o0o = urllib2 . HTTPCookieProcessor ( cookieJar )
 IIIIIiI = urllib2 . build_opener ( O0O0o0o0o , urllib2 . HTTPBasicAuthHandler ( ) , urllib2 . HTTPHandler ( ) )
 if 19 - 19: i1Ii
 O0O = urllib2 . Request ( url )
 O0O . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36' )
 if headers :
  for I1111I1II11 , O0o00oO0oOO in headers :
   O0O . add_header ( I1111I1II11 , O0o00oO0oOO )
   if 49 - 49: IIii1I * O00ooooo00 . II1
 O00o0OO = IIIIIiI . open ( O0O , post , timeout = timeout )
 O0000 = O00o0OO . read ( )
 O00o0OO . close ( )
 return O0000 ;
 if 90 - 90: O0Oooo00 % O00OoOoo00 - IIii1I % oo
def IIiI11I1I1i1i ( str , reg = None ) :
 if reg :
  str = re . findall ( reg , str ) [ 0 ]
 oooo = urllib . unquote ( str [ 0 : len ( str ) - 1 ] ) ;
 O0o0O = '' ;
 for O000OO0 in range ( len ( oooo ) ) :
  O0o0O += chr ( ord ( oooo [ O000OO0 ] ) - oooo [ len ( oooo ) - 1 ] ) ;
 O0o0O = urllib . unquote ( O0o0O )
 print O0o0O
 return O0o0O
 if 6 - 6: iIiiiI1IiI1I1
def oO0 ( str ) :
 I11i1iIi111 = re . findall ( 'unescape\(\'(.*?)\'' , str )
 print 'js' , I11i1iIi111
 if ( not I11i1iIi111 == None ) and len ( I11i1iIi111 ) > 0 :
  for i1iIiIii in I11i1iIi111 :
   if 20 - 20: O0Oooo00 * O00OoO000O
   str = str . replace ( i1iIiIii , urllib . unquote ( i1iIiIii ) )
 return str
 if 10 - 10: I1 - IiIIi1I1Iiii
ooOOooo0ooo00 = 0
def ooOo0O ( m , html_page , cookieJar ) :
 global ooOOooo0ooo00
 ooOOooo0ooo00 += 1
 oooOo = m [ 'expre' ]
 I1IIII1ii = m [ 'page' ]
 oo0oo0O0 = re . compile ( '\$LiveStreamCaptcha\[([^\]]*)\]' ) . findall ( oooOo ) [ 0 ]
 if 18 - 18: IIii1I + OoOooOOOO + IIii1I . O00OoOoo00 + ooiii11iII . O00OoO000O
 Ii111Iiiii = re . compile ( oo0oo0O0 ) . findall ( html_page ) [ 0 ]
 print oooOo , oo0oo0O0 , Ii111Iiiii
 if not Ii111Iiiii . startswith ( "http" ) :
  II1i11 = 'http://' + "" . join ( I1IIII1ii . split ( '/' ) [ 2 : 3 ] )
  if Ii111Iiiii . startswith ( "/" ) :
   Ii111Iiiii = II1i11 + Ii111Iiiii
  else :
   Ii111Iiiii = II1i11 + '/' + Ii111Iiiii
   if 28 - 28: iIiiiI1IiI1I1 - iI1 % oo + Ooo00oOo00o - oo
 oO00 = os . path . join ( iIiiiI , str ( ooOOooo0ooo00 ) + "captcha.jpg" )
 IiI1II11iiI = open ( oO00 , "wb" )
 print ' c capurl' , Ii111Iiiii
 O0O = urllib2 . Request ( Ii111Iiiii )
 O0O . add_header ( 'User-Agent' , 'O0oO0o0o0o' )
 if 'refer' in m :
  O0O . add_header ( 'Referer' , m [ 'refer' ] )
 if 'agent' in m :
  O0O . add_header ( 'User-agent' , m [ 'agent' ] )
 if 'setcookie' in m :
  print 'adding cookie' , m [ 'setcookie' ]
  O0O . add_header ( 'Cookie' , m [ 'setcookie' ] )
  if 28 - 28: iIiiiI1IiI1I1 . iI1 + OOO0O0O0ooooo . OOO0O0O0ooooo . OoOooOOOO
  if 98 - 98: II1 % OOO0O0O0ooooo - OOO0O0O0ooooo
  if 76 - 76: O00ooooo00 % oo - IIiIiII11i / O0Oooo00 * O00OoO000O
  if 4 - 4: IiIIi1I1Iiii * IiIIi1I1Iiii / oo
 urllib2 . urlopen ( O0O )
 O00o0OO = urllib2 . urlopen ( O0O )
 if 4 - 4: IIiIiII11i * oo % I1 . oo
 IiI1II11iiI . write ( O00o0OO . read ( ) )
 O00o0OO . close ( )
 IiI1II11iiI . close ( )
 o0oOOooo00O = OO0ooo0 ( captcha = oO00 )
 ooo0O0OOo0OoO = o0oOOooo00O . get ( )
 return ooo0O0OOo0OoO
 if 11 - 11: OoOooOOOO - oo - O0Oooo00 * oo + O00OoO000O
class OO0ooo0 ( xbmcgui . WindowDialog ) :
 def __init__ ( self , * args , ** kwargs ) :
  self . cptloc = kwargs . get ( 'captcha' )
  self . img = xbmcgui . ControlImage ( 335 , 30 , 624 , 60 , self . cptloc )
  self . addControl ( self . img )
  self . kbd = xbmc . Keyboard ( )
  if 62 - 62: IIiIiII11i * i11iIiiIii . o00O00O0O0O
 def get ( self ) :
  self . show ( )
  time . sleep ( 2 )
  self . kbd . doModal ( )
  if ( self . kbd . isConfirmed ( ) ) :
   I1iIIIiI = self . kbd . getText ( )
   self . close ( )
   return I1iIIIiI
  self . close ( )
  return False
  if 60 - 60: IIiIiII11i . i11iIiiIii + oo / O00OoOoo00 * iIiiiI1IiI1I1 * OoOooOOOO
def IiIi1II11i ( ) :
 import time
 return str ( int ( time . time ( ) * 1000 ) )
 if 59 - 59: IiIIi1I1Iiii + o00O00O0O0O - OoOooOOOO . O0Oooo00 + IIiIiII11i % iI1
def o0oO0oOO ( ) :
 import time
 return str ( int ( time . time ( ) ) )
 if 37 - 37: o00O00O0O0O + o00O00O0O0O % O0Oooo00
def iIi1i1iIi1Ii1 ( ) :
 oOOoOOO0oo0 = [ ]
 O00O = sys . argv [ 2 ]
 if len ( O00O ) >= 2 :
  O0OOOOOoo = sys . argv [ 2 ]
  oo0ooO0oOooo0OOO = O0OOOOOoo . replace ( '?' , '' )
  if ( O0OOOOOoo [ len ( O0OOOOOoo ) - 1 ] == '/' ) :
   O0OOOOOoo = O0OOOOOoo [ 0 : len ( O0OOOOOoo ) - 2 ]
  oooO00O = oo0ooO0oOooo0OOO . split ( '&' )
  oOOoOOO0oo0 = { }
  for O000OO0 in range ( len ( oooO00O ) ) :
   II1oOo00o = { }
   II1oOo00o = oooO00O [ O000OO0 ] . split ( '=' )
   if ( len ( II1oOo00o ) ) == 2 :
    oOOoOOO0oo0 [ II1oOo00o [ 0 ] ] = II1oOo00o [ 1 ]
 return oOOoOOO0oo0
 if 12 - 12: O0Oooo00 * ooiii11iII % iIiiiI1IiI1I1 * O00ooooo00 * IIii1I
 if 81 - 81: IiIIi1I1Iiii - I1
def ii1iII1iI111 ( ) :
 IiI1iiiIii = json . loads ( open ( iI111iI ) . read ( ) )
 oo00OO0000oO = len ( IiI1iiiIii )
 for O000OO0 in IiI1iiiIii :
  Iii1I1I11iiI1 = O000OO0 [ 0 ]
  Iiii = O000OO0 [ 1 ]
  o0o0O0O000 = O000OO0 [ 2 ]
  try :
   OOOoOo = O000OO0 [ 3 ]
   if OOOoOo == None :
    raise
  except :
   if I1IiI . getSetting ( 'use_thumb' ) == "true" :
    OOOoOo = o0o0O0O000
   else :
    OOOoOo = O000oo0O
  try : oO0OO0 = O000OO0 [ 5 ]
  except : oO0OO0 = None
  try : oOoO00O0 = O000OO0 [ 6 ]
  except : oOoO00O0 = None
  if 24 - 24: O00OoO000O / o00O00O0O0O + ooO0O . ooO0O
  if O000OO0 [ 4 ] == 0 :
   II1IIIIiII1i ( Iiii , Iii1I1I11iiI1 , o0o0O0O000 , OOOoOo , '' , '' , '' , 'fav' , oO0OO0 , oOoO00O0 , oo00OO0000oO )
  else :
   iiI1 ( Iii1I1I11iiI1 , Iiii , O000OO0 [ 4 ] , o0o0O0O000 , O000oo0O , '' , '' , '' , '' , 'fav' )
   if 39 - 39: O00OoO000O + OOO0O0O0ooooo / O00ooooo00 % ooO0O / iI1 * ooO0O
   if 77 - 77: ooO0O . ooiii11iII % oo
def I1111III11 ( name , url , iconimage , fanart , mode , playlist = None , regexs = None ) :
 iIOOO = [ ]
 if not os . path . exists ( iI111iI + 'txt' ) :
  os . makedirs ( iI111iI + 'txt' )
 if not os . path . exists ( IiII ) :
  os . makedirs ( IiII )
 try :
  if 32 - 32: II1
  name = name . encode ( 'utf-8' , 'ignore' )
 except :
  pass
 if os . path . exists ( iI111iI ) == False :
  o0O00oooo ( 'Making Favorites File' )
  iIOOO . append ( ( name , url , iconimage , fanart , mode , playlist , regexs ) )
  IIii11Ii1i1I = open ( iI111iI , "w" )
  IIii11Ii1i1I . write ( json . dumps ( iIOOO ) )
  IIii11Ii1i1I . close ( )
 else :
  o0O00oooo ( 'Appending Favorites' )
  IIii11Ii1i1I = open ( iI111iI ) . read ( )
  I11i1 = json . loads ( IIii11Ii1i1I )
  I11i1 . append ( ( name , url , iconimage , fanart , mode ) )
  Iiii1i1 = open ( iI111iI , "w" )
  Iiii1i1 . write ( json . dumps ( I11i1 ) )
  Iiii1i1 . close ( )
  if 52 - 52: i1Ii % OoOooOOOO * IIiIiII11i % I1 + OoOooOOOO / o00O00O0O0O
  if 80 - 80: II1 + ooO0O
def O00OOo0oOOooO0o0O ( name ) :
 I11i1 = json . loads ( open ( iI111iI ) . read ( ) )
 for o0o0o0oO0oOO in range ( len ( I11i1 ) ) :
  if I11i1 [ o0o0o0oO0oOO ] [ 0 ] == name :
   del I11i1 [ o0o0o0oO0oOO ]
   Iiii1i1 = open ( iI111iI , "w" )
   Iiii1i1 . write ( json . dumps ( I11i1 ) )
   Iiii1i1 . close ( )
   break
 xbmc . executebuiltin ( "XBMC.Container.Refresh" )
 if 92 - 92: IIii1I % II1 % ooO0O
def oOIIiIi ( url ) :
 if I1IiI . getSetting ( 'Updatecommonresolvers' ) == 'true' :
  IIi = os . path . join ( Iii1ii1II11i , 'genesisresolvers.py' )
  if xbmcvfs . exists ( IIi ) :
   os . remove ( IIi )
   if 79 - 79: IIii1I + ooO0O
  O0OOo = 'https://raw.githubusercontent.com/lambda81/lambda-addons/master/plugin.video.genesis/commonresolvers.py'
  i1I1Iiii1 = urllib . urlretrieve ( O0OOo , IIi )
  I1IiI . setSetting ( 'Updatecommonresolvers' , 'false' )
 try :
  import genesisresolvers
 except Exception :
  xbmc . executebuiltin ( "XBMC.Notification(Please enable Update Commonresolvers to Play in Settings. - ,10000)" )
  if 69 - 69: I1 % OOO0O0O0ooooo / IIiIiII11i . ooiii11iII / O00OoO000O
 O0ooOoOO0 = genesisresolvers . get ( url ) . result
 if url == O0ooOoOO0 or O0ooOoOO0 is None :
  if 56 - 56: O0Oooo00 / ooO0O * IIiIiII11i . O0Oooo00
  xbmc . executebuiltin ( "XBMC.Notification([COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR],Using Urlresolver module.. - ,5000)" )
  import urlresolver
  iiO0o0O0oo0o = urlresolver . HostedMediaFile ( url )
  if iiO0o0O0oo0o :
   O0Oooo = urlresolver . resolve ( url )
   O0ooOoOO0 = O0Oooo
 if O0ooOoOO0 :
  if isinstance ( O0ooOoOO0 , list ) :
   for oOoOOo0oo0 in O0ooOoOO0 :
    I11iI1I = I1IiI . getSetting ( 'quality' )
    if oOoOOo0oo0 [ 'quality' ] == 'HD' :
     O0Oooo = oOoOOo0oo0 [ 'url' ]
     break
    elif oOoOOo0oo0 [ 'quality' ] == 'SD' :
     O0Oooo = oOoOOo0oo0 [ 'url' ]
    elif oOoOOo0oo0 [ 'quality' ] == '1080p' and I1IiI . getSetting ( '1080pquality' ) == 'true' :
     O0Oooo = oOoOOo0oo0 [ 'url' ]
     break
  else :
   O0Oooo = O0ooOoOO0
 return O0Oooo
def Iii1iiIi1II1 ( name , mu_playlist ) :
 import urlparse
 if I1IiI . getSetting ( 'ask_playlist_items' ) == 'true' :
  Oo000o = [ ]
  for O000OO0 in mu_playlist :
   OO00oo = urlparse . urlparse ( O000OO0 ) . netloc
   if OO00oo == '' :
    Oo000o . append ( name )
   else :
    Oo000o . append ( OO00oo )
  I1iiiiI1iII = xbmcgui . Dialog ( )
  o0o0o0oO0oOO = I1iiiiI1iII . select ( 'Choose a video source' , Oo000o )
  if o0o0o0oO0oOO >= 0 :
   if "&mode=19" in mu_playlist [ o0o0o0oO0oOO ] :
    xbmc . Player ( ) . play ( oOIIiIi ( mu_playlist [ o0o0o0oO0oOO ] . replace ( '&mode=19' , '' ) ) )
   elif "$doregex" in mu_playlist [ o0o0o0oO0oOO ] :
    if 84 - 84: O00OoO000O + i11iIiiIii - OoOooOOOO * O00OoO000O
    I1IiiIiii1 = mu_playlist [ o0o0o0oO0oOO ] . split ( '&regexs=' )
    if 39 - 39: O00OoO000O / OOO0O0O0ooooo * ooO0O
    Iiii , Ooo0oo = OOO00O0oOOo ( I1IiiIiii1 [ 1 ] , I1IiiIiii1 [ 0 ] )
    xbmc . Player ( ) . play ( Iiii )
   else :
    Iiii = mu_playlist [ o0o0o0oO0oOO ]
    xbmc . Player ( ) . play ( Iiii )
 else :
  oO0OO0 = xbmc . PlayList ( 1 )
  oO0OO0 . clear ( )
  oOi11iI11iIiIi = 0
  for O000OO0 in mu_playlist :
   oOi11iI11iIiIi += 1
   I1IiII1iI1 = xbmcgui . ListItem ( '%s) %s' % ( str ( oOi11iI11iIiIi ) , name ) )
   oO0OO0 . add ( O000OO0 , I1IiII1iI1 )
   xbmc . executebuiltin ( 'playlist.playoffset(video,0)' )
   if 52 - 52: oo * Ooo00oOo00o - i1Ii
   if 82 - 82: Ooo00oOo00o + IIiIiII11i . O00ooooo00 + OoOooOOOO
def iIiI1Iii1 ( name , url ) :
 if I1IiI . getSetting ( 'save_location' ) == "" :
  xbmc . executebuiltin ( "XBMC.Notification('[COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR]','Choose a location to save files.',15000," + O0oo0OO0 + ")" )
  I1IiI . openSettings ( )
 O0OOOOOoo = { 'url' : url , 'download_path' : I1IiI . getSetting ( 'save_location' ) }
 downloader . download ( name , O0OOOOOoo )
 I1iiiiI1iII = xbmcgui . Dialog ( )
 o00oo0000 = I1iiiiI1iII . yesno ( '[COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR]' , 'Do you want to add this file as a source?' )
 if o00oo0000 :
  II1I ( os . path . join ( I1IiI . getSetting ( 'save_location' ) , name ) )
  if 85 - 85: i11iIiiIii / i11iIiiIii . Ooo00oOo00o . OOO0O0O0ooooo
  if 67 - 67: iIiiiI1IiI1I1 / O0Oooo00 . OoOooOOOO . II1
def iiI1 ( name , url , mode , iconimage , fanart , description , genre , date , credits , showcontext = False ) :
 if 19 - 19: ooO0O . O00OoOoo00 / oo
 O00oo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&fanart=" + urllib . quote_plus ( fanart )
 iiI = True
 if date == '' :
  date = None
 else :
  description += '\n\nDate: %s' % date
 I1ii1I1iiii = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 I1ii1I1iiii . setInfo ( type = "Video" , infoLabels = { "Title" : name , "Plot" : description , "Genre" : genre , "dateadded" : date , "credits" : credits } )
 I1ii1I1iiii . setProperty ( "Fanart_Image" , fanart )
 if showcontext :
  OoOoooO000OO = [ ]
  if showcontext == 'source' :
   if name in str ( i1 ) :
    OoOoooO000OO . append ( ( 'Remove from Sources' , 'XBMC.RunPlugin(%s?mode=8&name=%s)' % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) ) ) )
  elif showcontext == 'download' :
   OoOoooO000OO . append ( ( 'Download' , 'XBMC.RunPlugin(%s?url=%s&mode=9&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
  elif showcontext == 'fav' :
   OoOoooO000OO . append ( ( 'Remove from Add-on Favorites' , 'XBMC.RunPlugin(%s?mode=6&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) ) ) )
   if 62 - 62: OoOooOOOO + IiIIi1I1Iiii % IIii1I / IIii1I . O00OoO000O . ooO0O
  if not name in o0oOoO00o :
   OoOoooO000OO . append ( ( 'Add to [COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR] Favorites' , 'XBMC.RunPlugin(%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) , urllib . quote_plus ( url ) , urllib . quote_plus ( iconimage ) , urllib . quote_plus ( fanart ) , mode ) ) )
  I1ii1I1iiii . addContextMenuItems ( OoOoooO000OO )
 iiI = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = O00oo , listitem = I1ii1I1iiii , isFolder = True )
 if 21 - 21: Ooo00oOo00o - i1Ii - IIiIiII11i / oo
 return iiI
iI = base64 . b64decode ( 'aHR0cDovL2J1cnJ0di50ZWNoL0JPT00vU3BvcnQvaG9tZS54bWw=' )
def ii1oOoO0ooO0000 ( url , title , media_type = 'video' ) :
 if 60 - 60: oo / O00OoOoo00 + OoOooOOOO - o00O00O0O0O
 if 49 - 49: Ooo00oOo00o - OOO0O0O0ooooo / Ooo00oOo00o * oo + ooiii11iII
 import youtubedl
 if not url == '' :
  if media_type == 'audio' :
   youtubedl . single_YD ( url , download = True , audio = True )
  else :
   youtubedl . single_YD ( url , download = True )
 elif xbmc . Player ( ) . isPlaying ( ) == True :
  import YDStreamExtractor
  if YDStreamExtractor . isDownloading ( ) == True :
   if 35 - 35: iIiiiI1IiI1I1 . IIiIiII11i / O00ooooo00 / IIiIiII11i * iI1
   YDStreamExtractor . manageDownloads ( )
  else :
   Oo0O0000Oo00o = xbmc . Player ( ) . getPlayingFile ( )
   if 20 - 20: Ooo00oOo00o . IIiIiII11i * i11iIiiIii / i11iIiiIii
   Oo0O0000Oo00o = Oo0O0000Oo00o . split ( '|User-Agent=' ) [ 0 ]
   I1IiII1iI1 = { 'url' : Oo0O0000Oo00o , 'title' : title , 'media_type' : media_type }
   youtubedl . single_YD ( '' , download = True , dl_info = I1IiII1iI1 )
 else :
  xbmc . executebuiltin ( "XBMC.Notification(DOWNLOAD,First Play [COLOR yellow]WHILE playing download[/COLOR] ,10000)" )
  if 89 - 89: o00O00O0O0O . i11iIiiIii * OOO0O0O0ooooo
def Iiii1 ( site_name , search_term = None ) :
 oooOo0OOOoo0 = ''
 if os . path . exists ( IiII ) == False or I1IiI . getSetting ( 'clearseachhistory' ) == 'true' :
  IIiiiiIiIIii ( IiII , '' )
  I1IiI . setSetting ( "clearseachhistory" , "false" )
 if site_name == 'history' :
  II = O0oOOo0o ( IiII )
  o0Oo0oO0oOO00 = re . compile ( '(.+?):(.*?)(?:\r|\n)' ) . findall ( II )
  if 27 - 27: OoOooOOOO
  for Iii1I1I11iiI1 , search_term in o0Oo0oO0oOO00 :
   if 'plugin://' in search_term :
    II1IIIIiII1i ( search_term , Iii1I1I11iiI1 , oooOo0OOOoo0 , '' , '' , '' , '' , '' , None , '' , total = int ( len ( o0Oo0oO0oOO00 ) ) )
   else :
    iiI1 ( Iii1I1I11iiI1 + ':' + search_term , Iii1I1I11iiI1 , 26 , O0oo0OO0 , I1i1iiI1 , '' , '' , '' , '' )
 if not search_term :
  oOooOOOoOo = xbmc . Keyboard ( '' , 'Enter Search Term' )
  oOooOOOoOo . doModal ( )
  if ( oOooOOOoOo . isConfirmed ( ) == False ) :
   return
  search_term = oOooOOOoOo . getText ( )
  if len ( search_term ) == 0 :
   return
 search_term = search_term . replace ( ' ' , '+' )
 search_term = search_term . encode ( 'utf-8' )
 if 'youtube' in site_name :
  if 52 - 52: ooiii11iII % oo + IIii1I * iI1 . i1Ii
  import _ytplist
  if 95 - 95: IIii1I . ooO0O - II1 * Ooo00oOo00o / O0Oooo00
  oOo0OO0o0 = { }
  oOo0OO0o0 = _ytplist . YoUTube ( 'searchYT' , youtube = search_term , max_page = 4 , nosave = 'nosave' )
  oo00OO0000oO = len ( oOo0OO0o0 )
  for oOi11iI11iIiIi in oOo0OO0o0 :
   try :
    Iii1I1I11iiI1 = oOo0OO0o0 [ oOi11iI11iIiIi ] [ 'title' ]
    i11i1 = oOo0OO0o0 [ oOi11iI11iIiIi ] [ 'date' ]
    try :
     II1I1I = oOo0OO0o0 [ oOi11iI11iIiIi ] [ 'desc' ]
    except Exception :
     II1I1I = 'UNAVAIABLE'
     if 23 - 23: Ooo00oOo00o + ooO0O + IiIIi1I1Iiii % IIii1I . i11iIiiIii
    Iiii = 'plugin://plugin.video.youtube/play/?video_id=' + oOo0OO0o0 [ oOi11iI11iIiIi ] [ 'url' ]
    oooOo0OOOoo0 = 'http://img.youtube.com/vi/' + oOo0OO0o0 [ oOi11iI11iIiIi ] [ 'url' ] + '/0.jpg'
    II1IIIIiII1i ( Iiii , Iii1I1I11iiI1 , oooOo0OOOoo0 , '' , '' , '' , '' , '' , None , '' , oo00OO0000oO )
   except Exception :
    o0O00oooo ( 'This item is ignored::' )
  Oo0iII1iI1IIiI = site_name + ':' + search_term + '\n'
  IIiiiiIiIIii ( os . path . join ( iIiiiI , 'history' ) , Oo0iII1iI1IIiI , append = True )
 elif 'dmotion' in site_name :
  O00ooOOoO0O000O = "https://api.dailymotion.com"
  if 20 - 20: IIiIiII11i . I1
  import _DMsearch
  oooOO0oo0Oo00 = str ( I1IiI . getSetting ( 'familyFilter' ) )
  _DMsearch . listVideos ( O00ooOOoO0O000O + "/videos?fields=description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&search=" + search_term + "&sort=relevance&limit=100&family_filter=" + oooOO0oo0Oo00 + "&localization=en_EN&page=1" )
  if 99 - 99: OOO0O0O0ooooo
  Oo0iII1iI1IIiI = site_name + ':' + search_term + '\n'
  IIiiiiIiIIii ( os . path . join ( iIiiiI , 'history' ) , Oo0iII1iI1IIiI , append = True )
 elif 'IMDBidplay' in site_name :
  O00ooOOoO0O000O = "http://www.omdbapi.com/?t="
  Iiii = O00ooOOoO0O000O + search_term
  if 38 - 38: i11iIiiIii + IIii1I - I1 / oo
  oO00oOOo0Oo = dict ( { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; rv:33.0) Gecko/20100101 Firefox/33.0' , 'Referer' : 'http://joker.org/' , 'Accept-Encoding' : 'gzip, deflate' , 'Content-Type' : 'application/json;charset=utf-8' , 'Accept' : 'application/json, text/plain, */*' } )
  if 99 - 99: O00OoOoo00 * iI1 * O00OoOoo00 - iIiiiI1IiI1I1 + i1Ii
  O0OoO0ooOO0o = requests . get ( Iiii , headers = oO00oOOo0Oo )
  I11i1 = O0OoO0ooOO0o . json ( )
  OOooO0Oo00 = I11i1 [ 'Response' ]
  if OOooO0Oo00 == 'True' :
   iIIIIIIIiIII = I11i1 [ 'imdbID' ]
   Iii1I1I11iiI1 = I11i1 [ 'Title' ] + I11i1 [ 'Released' ]
   I1iiiiI1iII = xbmcgui . Dialog ( )
   o00oo0000 = I1iiiiI1iII . yesno ( 'Check Movie Title' , 'PLAY :: %s ?' % Iii1I1I11iiI1 )
   if o00oo0000 :
    Iiii = 'plugin://plugin.video.pulsar/movie/' + iIIIIIIIiIII + '/play'
    Oo0iII1iI1IIiI = Iii1I1I11iiI1 + ':' + Iiii + '\n'
    IIiiiiIiIIii ( IiII , Oo0iII1iI1IIiI , append = True )
    return Iiii
  else :
   xbmc . executebuiltin ( "XBMC.Notification([COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR],No IMDB match found ,7000," + O0oo0OO0 + ")" )
   if 94 - 94: o00O00O0O0O * IIii1I . I1
def IiiI11I1IIiI ( string ) :
 if isinstance ( string , basestring ) :
  if isinstance ( string , unicode ) :
   string = string . encode ( 'ascii' , 'ignore' )
 return string
def i1iI1i ( string , encoding = 'utf-8' ) :
 if isinstance ( string , basestring ) :
  if not isinstance ( string , unicode ) :
   string = unicode ( string , encoding , 'ignore' )
 return string
def o0o0OoO0OOO0 ( s ) : return "" . join ( filter ( lambda Oo0OoO00oOO0o : ord ( Oo0OoO00oOO0o ) < 128 , s ) )
if 79 - 79: iI1 % O0Oooo00 % oo
def ii1IIiII111I ( command ) :
 I11i1 = ''
 try :
  I11i1 = xbmc . executeJSONRPC ( i1iI1i ( command ) )
 except UnicodeEncodeError :
  I11i1 = xbmc . executeJSONRPC ( IiiI11I1IIiI ( command ) )
  if 87 - 87: i1Ii - O00OoOoo00 % O00OoOoo00 . iI1 / O00OoOoo00
 return i1iI1i ( I11i1 )
 if 6 - 6: oo / IIii1I * II1 * i11iIiiIii
 if 79 - 79: ooO0O % Ooo00oOo00o
def Oo0OO ( ) :
 Oo0oOO = xbmc . getSkinDir ( )
 if Oo0oOO == 'skin.confluence' :
  xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 elif Oo0oOO == 'skin.aeon.nox' :
  xbmc . executebuiltin ( 'Container.SetViewMode(511)' )
 else :
  xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  if 86 - 86: IIii1I / OOO0O0O0ooooo
  if 17 - 17: iIiiiI1IiI1I1
def iiIiii ( url ) :
 iiI1ii = i1iI1i ( '{"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"%s","media":"video","properties":["thumbnail","title","year","dateadded","fanart","rating","season","episode","studio"]},"id":1}' ) % url
 if 76 - 76: i1Ii + IIii1I + oo . Ooo00oOo00o
 i1i1 = json . loads ( ii1IIiII111I ( iiI1ii ) )
 for O000OO0 in i1i1 [ 'result' ] [ 'files' ] :
  url = O000OO0 [ 'file' ]
  Iii1I1I11iiI1 = o0o0OoO0OOO0 ( O000OO0 [ 'label' ] )
  oooOo0OOOoo0 = o0o0OoO0OOO0 ( O000OO0 [ 'thumbnail' ] )
  try :
   O000oo0O = o0o0OoO0OOO0 ( O000OO0 [ 'fanart' ] )
  except Exception :
   O000oo0O = ''
  try :
   i11i1 = O000OO0 [ 'year' ]
  except Exception :
   i11i1 = ''
  try :
   o0oOoOo0 = O000OO0 [ 'episode' ]
   III1IiI1i1i = O000OO0 [ 'season' ]
   if o0oOoOo0 == - 1 or III1IiI1i1i == - 1 :
    II1I1I = ''
   else :
    II1I1I = '[COLOR yellow] S' + str ( III1IiI1i1i ) + '[/COLOR][COLOR hotpink] E' + str ( o0oOoOo0 ) + '[/COLOR]'
  except Exception :
   II1I1I = ''
  try :
   o0OOOOOo0 = O000OO0 [ 'studio' ]
   if o0OOOOOo0 :
    II1I1I += '\n Studio:[COLOR steelblue] ' + o0OOOOOo0 [ 0 ] + '[/COLOR]'
  except Exception :
   o0OOOOOo0 = ''
   if 57 - 57: IIii1I + IIii1I
  if O000OO0 [ 'filetype' ] == 'file' :
   II1IIIIiII1i ( url , Iii1I1I11iiI1 , oooOo0OOOoo0 , O000oo0O , II1I1I , '' , i11i1 , '' , None , '' , total = len ( i1i1 [ 'result' ] [ 'files' ] ) )
   if 56 - 56: iI1 + O00OoO000O
   if 32 - 32: iIiiiI1IiI1I1 + oo % O00OoO000O / oo + O00OoOoo00
  else :
   iiI1 ( Iii1I1I11iiI1 , url , 53 , oooOo0OOOoo0 , O000oo0O , II1I1I , '' , i11i1 , '' )
   if 2 - 2: i11iIiiIii - ooiii11iII + Ooo00oOo00o % I1 * i1Ii
   if 54 - 54: OOO0O0O0ooooo - o00O00O0O0O . OoOooOOOO % o00O00O0O0O + o00O00O0O0O
def II1IIIIiII1i ( url , name , iconimage , fanart , description , genre , date , showcontext , playlist , regexs , total , setCookie = "" ) :
 if 36 - 36: OoOooOOOO % i11iIiiIii
 OoOoooO000OO = [ ]
 try :
  name = name . encode ( 'utf-8' )
 except : pass
 iiI = True
 if 47 - 47: O00ooooo00 + iIiiiI1IiI1I1 . IiIIi1I1Iiii * iI1 . I1 / O00ooooo00
 if regexs :
  i11ii = '17'
  if 83 - 83: O00OoOoo00 * O00OoOoo00 + OoOooOOOO
  OoOoooO000OO . append ( ( '[COLOR white]!!Download Currently Playing!![/COLOR]' , 'XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
 elif any ( x in url for x in OO0o ) and url . startswith ( 'http' ) :
  i11ii = '19'
  if 57 - 57: OOO0O0O0ooooo - OOO0O0O0ooooo . O00OoOoo00 / O0Oooo00 / i1Ii
  OoOoooO000OO . append ( ( '[COLOR white]!!Download Currently Playing!![/COLOR]' , 'XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
 elif url . endswith ( '&mode=18' ) :
  url = url . replace ( '&mode=18' , '' )
  i11ii = '18'
  if 20 - 20: OoOooOOOO * iIiiiI1IiI1I1 - oo - iI1 * ooiii11iII
  OoOoooO000OO . append ( ( '[COLOR white]!!Download!![/COLOR]' , 'XBMC.RunPlugin(%s?url=%s&mode=23&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
  if I1IiI . getSetting ( 'dlaudioonly' ) == 'true' :
   OoOoooO000OO . append ( ( '!!Download [COLOR seablue]Audio!![/COLOR]' , 'XBMC.RunPlugin(%s?url=%s&mode=24&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
 elif url . startswith ( 'magnet:?xt=' ) or '.torrent' in url :
  if 6 - 6: O00OoO000O + OoOooOOOO / IiIIi1I1Iiii + ooO0O % iIiiiI1IiI1I1 / Ooo00oOo00o
  if '&' in url and not '&amp;' in url :
   url = url . replace ( '&' , '&amp;' )
  url = 'plugin://plugin.video.pulsar/play?uri=' + url
  i11ii = '12'
  if 45 - 45: II1
 else :
  i11ii = '12'
  if 9 - 9: I1 . Ooo00oOo00o * O00ooooo00 . II1
  OoOoooO000OO . append ( ( '[COLOR white]!!Download Currently Playing!![/COLOR]' , 'XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
 O00oo = sys . argv [ 0 ] + "?"
 II1OoooOo = False
 if 34 - 34: i1Ii * i1Ii - O00OoOoo00 - OOO0O0O0ooooo . i11iIiiIii
 if playlist :
  if I1IiI . getSetting ( 'add_playlist' ) == "false" :
   O00oo += "url=" + urllib . quote_plus ( url ) + "&mode=" + i11ii
  else :
   O00oo += "mode=13&name=%s&playlist=%s" % ( urllib . quote_plus ( name ) , urllib . quote_plus ( str ( playlist ) . replace ( ',' , '||' ) ) )
   name = name + '[COLOR magenta] (' + str ( len ( playlist ) ) + ' items )[/COLOR]'
   II1OoooOo = True
 else :
  O00oo += "url=" + urllib . quote_plus ( url ) + "&mode=" + i11ii
 if regexs :
  O00oo += "&regexs=" + regexs
 if not setCookie == '' :
  O00oo += "&setCookie=" + urllib . quote_plus ( setCookie )
  if 32 - 32: IIii1I . Ooo00oOo00o * iI1 / OoOooOOOO . iIiiiI1IiI1I1 - IiIIi1I1Iiii
 if date == '' :
  date = None
 else :
  description += '\n\nDate: %s' % date
 I1ii1I1iiii = xbmcgui . ListItem ( name , iconImage = "DefaultVideo.png" , thumbnailImage = iconimage )
 I1ii1I1iiii . setInfo ( type = "Video" , infoLabels = { "Title" : name , "Plot" : description , "Genre" : genre , "dateadded" : date } )
 I1ii1I1iiii . setProperty ( "Fanart_Image" , fanart )
 if 10 - 10: O00OoOoo00 / i11iIiiIii - i1Ii + iI1 * IIiIiII11i
 if ( not II1OoooOo ) and not any ( x in url for x in Oo0Ooo ) :
  if regexs :
   if '$pyFunction:playmedia(' not in urllib . unquote_plus ( regexs ) and 'notplayable' not in urllib . unquote_plus ( regexs ) :
    if 94 - 94: IIiIiII11i + IIii1I / OOO0O0O0ooooo - II1 % O00OoOoo00
    I1ii1I1iiii . setProperty ( 'IsPlayable' , 'true' )
  else :
   I1ii1I1iiii . setProperty ( 'IsPlayable' , 'true' )
 else :
  o0O00oooo ( 'NOT setting isplayable' + url )
  if 64 - 64: I1 + Ooo00oOo00o
 if showcontext :
  OoOoooO000OO = [ ]
  if showcontext == 'fav' :
   OoOoooO000OO . append (
 ( 'Remove from Add-on Favorites' , 'XBMC.RunPlugin(%s?mode=6&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) ) )
 )
  elif not name in o0oOoO00o :
   IiIi11iiIIiI1 = (
 '%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=0'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) , urllib . quote_plus ( url ) , urllib . quote_plus ( iconimage ) , urllib . quote_plus ( fanart ) )
 )
   if playlist :
    IiIi11iiIIiI1 += 'playlist=' + urllib . quote_plus ( str ( playlist ) . replace ( ',' , '||' ) )
   if regexs :
    IiIi11iiIIiI1 += "&regexs=" + regexs
   OoOoooO000OO . append ( ( 'Add to Add-on Favorites' , 'XBMC.RunPlugin(%s)' % IiIi11iiIIiI1 ) )
  I1ii1I1iiii . addContextMenuItems ( OoOoooO000OO )
  if 6 - 6: ooO0O * II1 + ooiii11iII / i1Ii
 if not playlist is None :
  if I1IiI . getSetting ( 'add_playlist' ) == "false" :
   I1IiI1IIiI = name . split ( ') ' ) [ 1 ]
   ooooo0o0oo0Ooo = [
 ( 'Play ' + I1IiI1IIiI + ' PlayList' , 'XBMC.RunPlugin(%s?mode=13&name=%s&playlist=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( I1IiI1IIiI ) , urllib . quote_plus ( str ( playlist ) . replace ( ',' , '||' ) ) ) )
 ]
   I1ii1I1iiii . addContextMenuItems ( ooooo0o0oo0Ooo )
   if 12 - 12: O00OoOoo00 / i1Ii
   if 5 - 5: II1
 iiI = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = O00oo , listitem = I1ii1I1iiii , totalItems = total )
 if 18 - 18: IIiIiII11i % II1 - o00O00O0O0O . i11iIiiIii * IiIIi1I1Iiii % i1Ii
 return iiI
 if 12 - 12: O00ooooo00 / OoOooOOOO % O00OoO000O * ooO0O * OOO0O0O0ooooo * IIii1I
def OOOOoO ( url , name , iconimage , setresolved = True ) :
 if setresolved :
  I1ii1I1iiii = xbmcgui . ListItem ( name , iconImage = iconimage )
  I1ii1I1iiii . setInfo ( type = 'Video' , infoLabels = { 'Title' : name } )
  I1ii1I1iiii . setProperty ( "IsPlayable" , "true" )
  I1ii1I1iiii . setPath ( str ( url ) )
  xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , I1ii1I1iiii )
 else :
  xbmc . executebuiltin ( 'XBMC.RunPlugin(' + url + ')' )
  if 19 - 19: IIiIiII11i % i1Ii . ooO0O * O00OoO000O
  if 89 - 89: oo . OoOooOOOO
  if 7 - 7: iI1 % oo - IIiIiII11i + IiIIi1I1Iiii
  if 70 - 70: iIiiiI1IiI1I1 + ooiii11iII + i11iIiiIii - O00ooooo00 / ooO0O
def Ii ( link ) :
 Iiii = urllib . urlopen ( link )
 iI1IIiiIIIII = Iiii . read ( )
 Iiii . close ( )
 i1iIii = iI1IIiiIIIII . split ( "Jetzt" )
 o0O0ooooooo00 = i1iIii [ 1 ] . split ( 'programm/detail.php?const_id=' )
 I1111ii11IIII = o0O0ooooooo00 [ 1 ] . split ( '<br /><a href="/' )
 IiIi1II111I = I1111ii11IIII [ 0 ] [ 40 : len ( I1111ii11IIII [ 0 ] ) ]
 o00o = o0O0ooooooo00 [ 2 ] . split ( "</a></p></div>" )
 IIi1i1 = o00o [ 0 ] [ 17 : len ( o00o [ 0 ] ) ]
 IIi1i1 = IIi1i1 . encode ( 'utf-8' )
 return "  - " + IIi1i1 + " - " + IiIi1II111I
 if 84 - 84: OoOooOOOO + i1Ii + O0Oooo00
 if 33 - 33: i1Ii
def iii11i1IIII ( url , regex ) :
 I11i1 = Oo00OOOOO ( url )
 try :
  oOi11iI11iIiIi = re . findall ( regex , I11i1 ) [ 0 ]
  return oOi11iI11iIiIi
 except :
  o0O00oooo ( 'regex failed' )
  o0O00oooo ( regex )
  return
  if 93 - 93: O00OoO000O
  if 34 - 34: iI1 - O00OoO000O * IiIIi1I1Iiii / O0Oooo00
xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , 'movies' )
if 19 - 19: O00OoOoo00
try :
 xbmcplugin . addSortMethod ( int ( sys . argv [ 1 ] ) , xbmcplugin . SORT_METHOD_UNSORTED )
except :
 pass
try :
 xbmcplugin . addSortMethod ( int ( sys . argv [ 1 ] ) , xbmcplugin . SORT_METHOD_LABEL )
except :
 pass
try :
 xbmcplugin . addSortMethod ( int ( sys . argv [ 1 ] ) , xbmcplugin . SORT_METHOD_DATE )
except :
 pass
try :
 xbmcplugin . addSortMethod ( int ( sys . argv [ 1 ] ) , xbmcplugin . SORT_METHOD_GENRE )
except :
 pass
 if 46 - 46: IIii1I . i11iIiiIii - oo % OOO0O0O0ooooo / iIiiiI1IiI1I1 * O00ooooo00
O0OOOOOoo = iIi1i1iIi1Ii1 ( )
if 66 - 66: OOO0O0O0ooooo
Iiii = None
Iii1I1I11iiI1 = None
i11ii = None
oO0OO0 = None
o0o0O0O000 = None
O000oo0O = I1i1iiI1
oO0OO0 = None
oOooOOo00ooO = None
oOoO00O0 = None
if 71 - 71: ooiii11iII - O0Oooo00 - OoOooOOOO
try :
 Iiii = urllib . unquote_plus ( O0OOOOOoo [ "url" ] ) . decode ( 'utf-8' )
except :
 pass
try :
 Iii1I1I11iiI1 = urllib . unquote_plus ( O0OOOOOoo [ "name" ] )
except :
 pass
try :
 o0o0O0O000 = urllib . unquote_plus ( O0OOOOOoo [ "iconimage" ] )
except :
 pass
try :
 O000oo0O = urllib . unquote_plus ( O0OOOOOoo [ "fanart" ] )
except :
 pass
try :
 i11ii = int ( O0OOOOOoo [ "mode" ] )
except :
 pass
try :
 oO0OO0 = eval ( urllib . unquote_plus ( O0OOOOOoo [ "playlist" ] ) . replace ( '||' , ',' ) )
except :
 pass
try :
 oOooOOo00ooO = int ( O0OOOOOoo [ "fav_mode" ] )
except :
 pass
try :
 oOoO00O0 = O0OOOOOoo [ "regexs" ]
except :
 pass
 if 28 - 28: IIii1I
o0O00oooo ( "Mode: " + str ( i11ii ) )
if not Iiii is None :
 o0O00oooo ( "URL: " + str ( Iiii . encode ( 'utf-8' ) ) )
o0O00oooo ( "Name: " + str ( Iii1I1I11iiI1 ) )
if 7 - 7: O0Oooo00 % ooO0O * oo
if i11ii == None :
 o0O00oooo ( "Index" )
 iiIIII1i1i ( )
 if 58 - 58: ooO0O / I1 + iIiiiI1IiI1I1 % o00O00O0O0O - II1
elif i11ii == 1 :
 o0O00oooo ( "getData" )
 i11Iiii ( Iiii , O000oo0O )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 25 - 25: oo % II1 * IiIIi1I1Iiii - O00ooooo00 * iIiiiI1IiI1I1 * iI1
elif i11ii == 2 :
 o0O00oooo ( "getChannelItems" )
 I11iiii ( Iii1I1I11iiI1 , Iiii , O000oo0O )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 30 - 30: I1 % oo / O00OoOoo00 * OOO0O0O0ooooo * i1Ii . IIiIiII11i
elif i11ii == 3 :
 o0O00oooo ( "getSubChannelItems" )
 o0O ( Iii1I1I11iiI1 , Iiii , O000oo0O )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 46 - 46: oo - OOO0O0O0ooooo
elif i11ii == 4 :
 if not os . path . exists ( o00 ) :
  xbmcgui . Dialog ( ) . ok ( "[COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR]" , "You have currently have no saved favorites " , "Please Add a favourite to access this area. " )
  pass
 if os . path . exists ( o00 ) :
  o0O00oooo ( "getFavorites" )
  iiI1 ( '[COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR] [COLOR yellow]- FAVORITES[/COLOR]' , 'Favorites' , 0 , 'https://i.imgur.com/jOo0ut5.png' , I1i1iiI1 , '' , '' , '' , '' )
  iiI1 ( '[COLOR white]----------------------------------------[/COLOR]' , 'Favorites' , 0 , 'https://i.imgur.com/jOo0ut5.png' , I1i1iiI1 , '' , '' , '' , '' )
  ii1iII1iI111 ( )
  xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
  if 70 - 70: I1 + IiIIi1I1Iiii * IIii1I . IIiIiII11i * I1
elif i11ii == 5 :
 o0O00oooo ( "addFavorite" )
 try :
  Iii1I1I11iiI1 = Iii1I1I11iiI1 . split ( '\\ ' ) [ 1 ]
 except :
  pass
 try :
  Iii1I1I11iiI1 = Iii1I1I11iiI1 . split ( '  - ' ) [ 0 ]
 except :
  pass
 I1111III11 ( Iii1I1I11iiI1 , Iiii , o0o0O0O000 , O000oo0O , oOooOOo00ooO )
 if 49 - 49: O0Oooo00
elif i11ii == 6 :
 o0O00oooo ( "rmFavorite" )
 try :
  Iii1I1I11iiI1 = Iii1I1I11iiI1 . split ( '\\ ' ) [ 1 ]
 except :
  pass
 try :
  Iii1I1I11iiI1 = Iii1I1I11iiI1 . split ( '  - ' ) [ 0 ]
 except :
  pass
 O00OOo0oOOooO0o0O ( Iii1I1I11iiI1 )
 if 25 - 25: o00O00O0O0O . II1 * IIii1I . O0Oooo00 / OOO0O0O0ooooo + i1Ii
elif i11ii == 7 :
 o0O00oooo ( "addSource" )
 II1I ( Iiii )
 if 68 - 68: IiIIi1I1Iiii
elif i11ii == 8 :
 o0O00oooo ( "rmSource" )
 o0OoOO000ooO0 ( Iii1I1I11iiI1 )
 if 22 - 22: OoOooOOOO
elif i11ii == 9 :
 o0O00oooo ( "download_file" )
 iIiI1Iii1 ( Iii1I1I11iiI1 , Iiii )
 if 22 - 22: o00O00O0O0O * I1 - IiIIi1I1Iiii * OOO0O0O0ooooo / i11iIiiIii
elif i11ii == 10 :
 o0O00oooo ( "getCommunitySources" )
 Oo0oO00o ( )
 if 78 - 78: IiIIi1I1Iiii * OOO0O0O0ooooo / O00OoO000O + II1 + OoOooOOOO
elif i11ii == 11 :
 o0O00oooo ( "addSource" )
 II1I ( Iiii )
 if 23 - 23: o00O00O0O0O % II1 / IIii1I + O00OoOoo00 / O00ooooo00 / O0Oooo00
elif i11ii == 12 :
 o0O00oooo ( "setResolvedUrl" )
 if not Iiii . startswith ( "plugin://plugin" ) or not any ( x in Iiii for x in Oo0Ooo ) :
  oOi11iI11iIiIi = xbmcgui . ListItem ( path = Iiii )
  xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , oOi11iI11iIiIi )
 else :
  print 'Not setting setResolvedUrl'
  xbmc . executebuiltin ( 'XBMC.RunPlugin(' + Iiii + ')' )
  if 94 - 94: O00ooooo00
  if 36 - 36: IIiIiII11i + IiIIi1I1Iiii
elif i11ii == 13 :
 o0O00oooo ( "play_playlist" )
 Iii1iiIi1II1 ( Iii1I1I11iiI1 , oO0OO0 )
 if 46 - 46: o00O00O0O0O
elif i11ii == 14 :
 o0O00oooo ( "get_xml_database" )
 Ooo ( Iiii )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 65 - 65: O00ooooo00 . O00OoOoo00 / O00OoO000O
elif i11ii == 15 :
 o0O00oooo ( "browse_xml_database" )
 Ooo ( Iiii , True )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 11 - 11: ooO0O * O00OoO000O / O00OoO000O - OoOooOOOO
elif i11ii == 16 :
 o0O00oooo ( "browse_community" )
 Oo0oO00o ( True )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 68 - 68: IIiIiII11i % ooO0O - ooO0O / IIiIiII11i + O00OoOoo00 - IiIIi1I1Iiii
elif i11ii == 17 :
 o0O00oooo ( "getRegexParsed" )
 Iiii , Ooo0oo = OOO00O0oOOo ( oOoO00O0 , Iiii )
 if Iiii :
  OOOOoO ( Iiii , Iii1I1I11iiI1 , o0o0O0O000 , Ooo0oo )
 else :
  xbmc . executebuiltin ( "XBMC.Notification([COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR] ,Failed to extract regex. - " + "this" + ",4000," + O0oo0OO0 + ")" )
elif i11ii == 18 :
 o0O00oooo ( "youtubedl" )
 try :
  import youtubedl
 except Exception :
  xbmc . executebuiltin ( "XBMC.Notification([COLOR red][B]BOOM[/COLOR][COLOR yellow]![/B][/COLOR],Please [COLOR yellow]install the Youtube Addon[/COLOR] module ,10000," ")" )
 i1I1i111Ii = youtubedl . single_YD ( Iiii )
 OOOOoO ( i1I1i111Ii , Iii1I1I11iiI1 , o0o0O0O000 )
elif i11ii == 19 :
 o0O00oooo ( "Genesiscommonresolvers" )
 OOOOoO ( oOIIiIi ( Iiii ) , Iii1I1I11iiI1 , o0o0O0O000 , True )
 if 65 - 65: O00OoO000O - O00ooooo00
elif i11ii == 21 :
 o0O00oooo ( "download current file using youtube-dl service" )
 ii1oOoO0ooO0000 ( '' , Iii1I1I11iiI1 , 'video' )
elif i11ii == 23 :
 o0O00oooo ( "get info then download" )
 ii1oOoO0ooO0000 ( Iiii , Iii1I1I11iiI1 , 'video' )
elif i11ii == 24 :
 o0O00oooo ( "Audio only youtube download" )
 ii1oOoO0ooO0000 ( Iiii , Iii1I1I11iiI1 , 'audio' )
elif i11ii == 25 :
 o0O00oooo ( "YouTube/DMotion" )
 Iiii1 ( Iiii )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
elif i11ii == 26 :
 o0O00oooo ( "YouTube/DMotion From Search History" )
 Iii1I1I11iiI1 = Iii1I1I11iiI1 . split ( ':' )
 Iiii1 ( Iiii , search_term = Iii1I1I11iiI1 [ 1 ] )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
elif i11ii == 27 :
 o0O00oooo ( "Using IMDB id to play in Pulsar" )
 O00Ooiii = Iiii1 ( Iiii )
 xbmc . Player ( ) . play ( O00Ooiii )
elif i11ii == 30 :
 oOOoo0000O0o0 ( Iii1I1I11iiI1 , Iiii , o0o0O0O000 , O000oo0O )
 if 93 - 93: I1 * iIiiiI1IiI1I1 / i1Ii - O0Oooo00
elif i11ii == 40 :
 iiI11i1II ( )
 Oo0OO ( )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 98 - 98: i11iIiiIii / IIiIiII11i * O0Oooo00 / ooiii11iII
elif i11ii == 53 :
 o0O00oooo ( "Requesting JSON-RPC Items" )
 iiIiii ( Iiii )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) ) 
