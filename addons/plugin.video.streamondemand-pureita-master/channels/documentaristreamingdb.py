# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita.- XBMC Plugin
# Canale  documentaristreamingdb
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "documentaristreamingdb"
__category__ = "D"
__type__ = "generic"
__title__ = "documentaristreamingdb (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.documentari-streaming-db.com"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'],
    ['Accept-Encoding', 'gzip, deflate']
]


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.documentaristreamingdb mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Aggiornamenti[/COLOR]",
                     action="peliculas",
                     url="http://www.documentari-streaming-db.com/?searchtype=movie&post_type=movie&sl=lasts&s=",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                #Item(channel=__channel__,
                     #title="[COLOR azure]Categorie[/COLOR]",
                     #action="categorias",
                     #url="http://www.documentari-streaming-db.com/documentari-streaming-database/",
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR orange]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist


def newest(categoria):
    logger.info("streamondemand.documentaristreamingdb newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "documentales":
            item.url = "http://www.documentari-streaming-db.com/?searchtype=movie&post_type=movie&sl=lasts&s="
            item.action = "peliculas"
            itemlist = peliculas(item)

            if itemlist[-1].action == "peliculas":
                itemlist.pop()

    # Se captura la excepción, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist

def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.get_match(data, '<ul role="menu" class="collapse collapse-1156 ">(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<a href="(.*?)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        if (DEBUG): logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")

        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("Documentari ", ""))
        if scrapedtitle.startswith("Tutte"):
            continue

        strip = scrapedtitle
        strip = strip.replace(" ", "")
        from unidecode import unidecode
        strip = unidecode(strip)
        url = host + "/?searchtype=movie&post_type=movie&sl=lasts&cat=" +  strip.encode("ascii").lower() + "&s="

        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=url,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist


def search(item, texto):
    logger.info("streamondemand.documentaristreamingdb " + item.url + " search " + texto)
    item.url = host + "/?searchtype=movie&post_type=movie&s=" + texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

def peliculas(item):
    logger.info("streamondemand.documentaristreamingdb peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="movie-poster">\s*<img[^=]+=[^=]+=[^=]+="([^"]+)"[^>]+>\s*<a[^=]+=[^=]+="([^"]+)">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedurl in matches:
        #html = scrapertools.cache_page(scrapedurl)
        #start = html.find("</div><h2>")
        #end = html.find("<p><strong>", start)
        #scrapedplot = html[start:end]
        #scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        #scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedplot = ""
        scrapedtitle = scrapedurl
        scrapedtitle = scrapedtitle.replace(host, "")
        scrapedtitle = scrapedtitle.replace("/", "")
        scrapedtitle = scrapedtitle.replace("-streaming", "")
        scrapedtitle = scrapedtitle.replace("-", " ")
        scrapedtitle = scrapedtitle.title()
        if DEBUG: logger.info(
            "url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 viewmode="movie_with_plot",
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    # Extrae el paginador
    patronvideos = '<a class="next page-numbers" href="(.*?)">'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        scrapedurl = scrapedurl.replace("&#038;", "&")
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/return_home2_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

def findvideos(item):
    logger.info("streamondemand.documentaristreamingdb findvideos")

    data = scrapertools.cache_page(item.url, headers=headers)
    
    links = []
    begin = data.find('<div class="moview-details-text">')
    if begin != -1:
        end = data.find('<!-- //movie-details -->', begin)
        mdiv = data[begin:end]
        
        items = [[m.end(), m.group(1)] for m in re.finditer('<b style="color:#333333;">(.*?)<\/b>', mdiv)]
        if items:
            for idx, val in enumerate(items):
                if idx == len(items)-1:
                    _data = mdiv[val[0]:-1]
                else:
                    _data = mdiv[val[0]:items[idx+1][0]]
                
                for link in re.findall('<a.*?href="([^"]+)"[^>]+>.*?<b>(.*?)<\/b><\/a>+', _data):
                    if not link[0].strip() in [l[1] for l in links]: links.append([val[1], link[0].strip(), link[1].strip()])
                    
        items = [[m.end(), m.group(1)] for m in re.finditer('<p><strong>(.*?)<\/strong><\/p>', mdiv)]
        if items:
            _title = ''
            for idx, val in enumerate(items):
                if idx == len(items)-1:
                    _data = mdiv[val[0]:-1]
                else:
                    _data = mdiv[val[0]:items[idx+1][0]]

                for link in re.findall('<a\s.*?href="([^"]+)".*?>(?:<span[^>]+>)*(?:<strong>)*([^<]+)', _data):
                    if not link[0].strip() in [l[1] for l in links]:
                        if not link[1].strip() in link[0]: _title = link[1].strip()
                        links.append([_title, link[0].strip(), 'unknown'])

        items = [[m.start(), m.group(1)] for m in re.finditer('<li><strong>([^<]+)<', mdiv)]
        if items:
            for idx, val in enumerate(items):
                if idx == len(items)-1:
                    _data = mdiv[val[0]:-1]
                else:
                    _data = mdiv[val[0]:items[idx+1][0]]

                for link in re.findall('<a\s.*?href="([^"]+)".*?>(?:<span[^>]+>)*(?:<strong>)*([^<]+)', _data):
                    if not link[0].strip() in [l[1] for l in links]: links.append([val[1], link[0].strip(), link[1].strip()])
                    
    itemlist = []
    if links:
        for l in links:
            title = unicode(l[0], 'utf8', 'ignore')
            title = title.replace(u'\xa0',' ').replace('Documentario ', '').replace(' doc ', ' ').replace(' streaming','').replace(' Streaming','')
            url = l[1]
            action = "play"
            server = "unknown"
            folder = False
            
            if url == '#' or not title: continue
            
            logger.info('server: %s' % l[2])
            if l[2] != 'unknown':
                server = unicode(l[2], 'utf8', 'ignore')
            else:
                logger.info(url)
                match = re.search('https?:\/\/(?:www\.)*([^\.]+)\.', url)
                if match:
                    server = match.group(1)
                    
                    if server == "documentari-streaming-db":
                        action = "findvideos"
                        folder = True
            logger.info('server: %s, action: %s' % (server, action))
            
            logger.info(title + ' - [COLOR blue]' + server + '[/COLOR]')
            
            itemlist.append( Item(
                channel=item.channel, 
                title=title + ' - [COLOR blue]' + server + '[/COLOR]',
                action=action, 
                server=server, #servertools.get_server_from_url(url), 
                url=url, 
                thumbnail=item.thumbnail, 
                fulltitle=title, 
                show=item.show, 
                plot=item.plot, 
                parentContent=item, 
                folder=folder) 
            )
    else:
        itemlist = servertools.find_video_items(data=data)

        for videoitem in itemlist:
            videoitem.title = "".join([item.title, '[COLOR orange][B]' + videoitem.title + '[/B][/COLOR]'])
            videoitem.fulltitle = item.fulltitle
            videoitem.show = item.show
            videoitem.thumbnail = item.thumbnail
            videoitem.channel = __channel__
        
    return itemlist

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")
