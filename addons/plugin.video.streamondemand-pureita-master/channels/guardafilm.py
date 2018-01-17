# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-PureITA / XBMC Plugin
# Canale GuardaFilm
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import re

from core import logger, httptools
from core.httptools import urllib
from core import servertools
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "guardafilm"
__category__ = "F"
__type__ = "generic"
__title__ = "GuardaFilm"
__language__ = "IT"

host = "http://www.guardafilm.site/"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]

def isGeneric():
    return True

# ==============================================================================================================================================================================
def mainlist(item):
    logger.info("streamondemand-pureita GuardaFilm.py mainlist")
    itemlist = [
        Item(channel=__channel__,
                     action="film",
                     title="Film [COLOR orange] - Novita [/COLOR]",
                     url="%s/movies/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png",),
        Item(channel=__channel__,
                     action="genere",
                     title="Film [COLOR orange] - Generi [/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png",),
        Item(channel=__channel__,
                     action="film",
                     title="Film [COLOR orange] - Alta Definizione [/COLOR]",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png",),
        Item(channel=__channel__,
                     action="search",
                     title=color("Cerca", "orange"),
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png",)]

    return itemlist

# ==============================================================================================================================================================================

def search(item, texto):
    logger.info("streamondemand-pureita GuardaFilm.py search")
    item.url = host + "/?s=" + texto
    item.extra = "movie"
    try:
        return film(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================

def genere(item):
    logger.info("streamondemand-pureita GuardaFilm.py pergenere")
    itemlist = []
    
    data = scrapertools.anti_cloudflare(item.url, headers=headers)

    patron = '<a href="([^"]+)">([^<]+)<\/a><\/li>'
    blocco = scrapertools.get_match(data, '<a>Scegli per Genere<\/a>([^+]+)<\/ul><\/div>')

    matches = re.compile(patron, re.DOTALL).findall(blocco)
    for scrapedurl, scrapedtitle in matches:
         itemlist.append(
             Item(channel=__channel__,
                 action="film",
                 title=color(scrapedtitle, "azure"),
                 url=scrapedurl,
                 extra="movie",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def film(item):
    logger.info("streamondemand-pureita GuardaFilm.py film")
    itemlist = []

    item.url = urllib.unquote_plus(item.url).replace("\\", "")

    data = scrapertools.anti_cloudflare(item.url, headers=headers)
    patron = '<div data-movie-id=".*?" class="ml-item">\s*<a href="([^"]+)" data-url="" class="ml-mask jt" data-hasqtip=".*?" oldtitle=".*?" title="">\s*'
    patron += '<img data-original="([^"]+)" class="lazy thumb mli-thumb" alt="([^<]+)">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedimg, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedimg,
                 extra=item.extra,
                 folder=True), tipo=item.extra))

    patron = "<li><a rel='nofollow' class='page larger' href='([^<]+)'>2</a></li>"
    matches = re.compile(patron, re.DOTALL).findall(data)


    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                action="film",
                title=color("Pagina 2 >>", "orange"),
                url=scrapedurl,
                thumbnail="",
                folder=True))
    patron = "<li><a rel='nofollow' class='page larger' href='([^<]+)'>3</a></li>"
    matches = re.compile(patron, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                action="film",
                title=color("Pagina 3 >>", "orange"),
                url=scrapedurl,
                thumbnail="",
                folder=True))

    return itemlist

# ==============================================================================================================================================================================

def findvideos(item):
    logger.info("streamondemand-pureita GuardaFilm.py findvideos")
    itemlist = []
	
    data = httptools.downloadpage(item.url, headers=headers).data 
    patron = 'src="([^"]+)" frameborder="0"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl in matches:
        if "dir?" in scrapedurl:
            data += httptools.downloadpage(scrapedurl).url
        else:
            data += httptools.downloadpage(scrapedurl).data

    for videoitem in servertools.find_video_items(data=data):
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__
        itemlist.append(videoitem)

    return itemlist

# ==============================================================================================================================================================================

def color(text, color):
    return "[COLOR "+color+"]"+text+"[/COLOR]"



