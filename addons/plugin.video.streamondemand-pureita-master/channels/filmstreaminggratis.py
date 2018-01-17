# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale FilmStreamingGratis
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# By MrTruth
# ------------------------------------------------------------

import re

from core import logger
from core import servertools
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmstreaminggratis"
__category__ = "F"
__type__ = "generic"
__title__ = "FilmStreamingGratis"
__language__ = "IT"

host = "http://www.filmstreaminggratis.org"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]

def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand-pureita.filmstreaminggratis mainlist")
    itemlist = [Item(channel=__channel__,
                     action="ultimifilm",
                     title="[COLOR azure]Film [COLOR orange]Novità[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     action="categorie",
                     title="[COLOR azure]Film [COLOR orange]Categorie[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     action="loadfilms",
                     title="[COLOR azure]Film [COLOR orange]Lista[/COLOR]",
                     url="%s/blog/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title=color("Cerca film ...", "orange"),
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")
                ]

    return itemlist

# ==============================================================================================================================================================================

def search(item, texto):
    logger.info("streamondemand-pureita.filmstreaminggratis search")
    item.url = host + "/?s=" + texto
    try:
        return loadfilms(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


# ==============================================================================================================================================================================

def ultimifilm(item):
    logger.info("streamondemand-pureita.filmstreaminggratis ultimifilm")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers=headers)
    blocco = scrapertools.get_match(data, '<div class="es-carousel">(.*?)</div></li></ul>')
    patron = '<h5><a href="(.*?)".*?>(.*?)</a></h5>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra="movie",
                 thumbnail=item.thumbnail,
                 folder=True), tipo="movie"))

    return itemlist

# ==============================================================================================================================================================================

def categorie(item):
    logger.info("streamondemand-pureita.filmstreaminggratis categorie")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers=headers)
    blocco = scrapertools.get_match(data, '<div class="list styled custom-list"><ul>(.*?)</ul></div>')
    patron = '<li><a href="([^"]+)" title=".*?" >(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        if "Serie TV" not in scrapedtitle: # Il sito non ha una buona gestione per le Serie TV
            itemlist.append(
                Item(channel=__channel__,
                     action="loadfilms",
                     title=scrapedtitle,
                     url=scrapedurl,
                     extra="movie",
                     thumbnail=item.thumbnail,
                     folder=True))

    return itemlist

# ==============================================================================================================================================================================

def loadfilms(item):
    logger.info("streamondemand-pureita.filmstreaminggratis loadfilms")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers=headers)

    patron = '<h2 class="post-title"><a href="(.*?)" title=".*?">'
    patron += '(.*?)</a></h2>[^>]+>[^>]+>[^>]+><.*?data-src="(.*?)"'
    patron += '[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>\s+?(.*?)</div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedplot in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot.strip())
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 plot=scrapedplot,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo=item.extra))

    patronvideos = '<link rel="next" href="(.*?)" />'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title=color("Torna Home", "yellow"),
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="loadfilms",
                 title=color("Successivo >>", "orange"),
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def findvideos(item):
    logger.info("streamondemand-pureita.filmstreaminggratis findvideos")
    itemlist = []
	
    data = scrapertools.anti_cloudflare(item.url, headers)

    blocco = scrapertools.get_match(data, r'<br/>(.*?)</div></div>')
    patron = r'.*?src="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl in matches:
        data = scrapertools.anti_cloudflare(scrapedurl, headers)
        videos = servertools.find_video_items(data=data)
        for video in videos:
            itemlist.append(video)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join(["[%s] " % color(server, 'orange'), item.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__
		
    return itemlist

# ==============================================================================================================================================================================

def color(text, color):
    return "[COLOR "+color+"]"+text+"[/COLOR]"

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")


