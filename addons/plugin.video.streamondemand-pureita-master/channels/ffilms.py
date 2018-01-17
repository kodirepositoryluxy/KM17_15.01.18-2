# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-PureITA / XBMC Plugin
# Canale ffilm
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# By MrTruth
# ------------------------------------------------------------

import re

from core import logger
from core import config
from core import servertools
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "ffilms"
__category__ = "F"
__type__ = "generic"
__title__ = "FFilms"
__language__ = "IT"

host = "https://ffilms.org/italiano/"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]

def isGeneric():
    return True

# ----------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info("[FFilms.py]==> mainlist")
    itemlist = [Item(channel=__channel__,
                     action="peliculas",
                     title=color("Film in primo piano", "azure"),
                     url=host,
                     extra=" Video in primo piano",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     action="peliculas",
                     title=color("Ultimi Film", "azure"),
                     url=host,
                     extra=" Ultimi video",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     action="peliculas",
                     title=color("Popolari", "azure"),
                     url=host,
                     extra=" Ordina per popolarità",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movies_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title=color("Cerca ...", "yellow"),
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def search(item, texto):
    logger.info("[FFilms.py]==> search")
    item.url = host + "/?s=" + texto
    try:
        return peliculas_search(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def peliculas_search(item):
    logger.info("[FFilms.py]==> peliculas_search")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers=headers)
    blocco = scrapertools.get_match(data, r'<h3>About \d+ (?:result|results)</h3>(.*?)</span>\s*</div>\s*</div>\s*</div>')
    patron = r'<a href="([^"]+)"><img.*?src="([^"]+)".*?/>[^>]+>[^>]+>[^>]+>'
    patron += r'[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>(.*?)</a></h3>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra="movie",
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="movie"))

    # Pagine
    patronvideos = '<a class="next page-numbers" href="([^"]+)">Next'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_search",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def peliculas(item):
    logger.info("[FFilms.py]==> peliculas")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers=headers)
    blocco = scrapertools.get_match(data, r'<h3><i class="fa fa-play"></i>%s</h3>(.*?)</div>\s*</div>\s*</div>' % item.extra)
    patron = r'<a title="([^"]+)" href="([^"]+)"><img.*?src="([^"]+)".*?/>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedtitle, scrapedurl, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra="movie",
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="movie"))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def findvideos(item):
    logger.info("[FFilms.py]==> findvideos")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    blocco = scrapertools.get_match(data, r'<div class="player player-small(.*?)(?:</li></ul>|\s*</iframe>\s*<div)')
    patron = r'<li(?: class="active"| )><a href="([^"]+)">\d+</a></li>'
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

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def color(text, color):
    return "[COLOR "+color+"]"+text+"[/COLOR]"
    
def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master/)")

# ================================================================================================================
