# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA.- XBMC Plugin
# Canale AltadefinizioneZone
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "altadefinizionezone"
__category__ = "F,S"
__type__ = "generic"
__title__ = "altadefinizionezone (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://altadefinizione.live/"

headers = [
    ['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'],
    ['Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host],
    ['Cache-Control', 'max-age=0']
]


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand-pureita.altadefinizionezone mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Al Cinema[/COLOR]",
                     action="peliculas",
                     url="%s/film-streaming/del-cinema/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Ultimi Inseriti[/COLOR]",
                     action="peliculas",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Categoria[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR orange]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================

def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.find_single_match(data, '<ul class="listSubCat" id="Film">(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<li><a href="(.*?)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedurl = host + scrapedurl

        if DEBUG: logger.info("title=[" + scrapedtitle + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def list(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.find_single_match(data, '<ul class="listSubCat" id="Film">(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<li><a href="(.*?)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedurl = host + scrapedurl

        if DEBUG: logger.info("title=[" + scrapedtitle + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================
	
def search(item, texto):
    logger.info("[streamondemand-pureita.altadefinizionezone.py] " + item.url + " search " + texto)
    item.url = host + "/?do=search&subaction=search&story=" + texto
    try:
        if item.extra == "movie":
            return peliculas_search(item)
        if item.extra == "serie":
            return peliculas_search(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================

def peliculas_search(item):
    logger.info("streamondemand-pureita.altadefinizionezone peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="wrapperImage">[^>]+<span class=".*?">.*?</span>.*?<a href="(.*?)"><img src="(.*?)" class=".*?" alt="(.*?)" height=".*? width=".*?"></a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = host + scrapedthumbnail
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))


    return itemlist

# ==============================================================================================================================================================================

def peliculas(item):
    logger.info("streamondemand-pureita.altadefinizionezone peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="wrapperImage"><span class=".*?">.*?</span>.*?<a href="(.*?)">'
    patron += '<img src="(.*?)" class=".*?" alt="(.*?)" height=".*?" width=".*?"></a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = host + scrapedthumbnail
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">Succ →</a> </div>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def peliculas_tv(item):
    logger.info("streamondemand.altadefinizionezone peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    patron = '<div id="mainbar" class="container margin-b40">(.*?)<div class="margin-b20 accordion accordion-violet" >'
    data = scrapertools.find_single_match(data, patron)

    # Extrae las entradas (carpetas)
    patron = '<div class="short-images">\s*<a href="(.*?)"[^>]+>\s*<img src="(.*?)" alt="(.*?)" />'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = host + scrapedthumbnail
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="seasons",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = '<span>[^<]+</span> <a href="(.*?)">'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
            scrapedurl = urlparse.urljoin(item.url, matches[0])
            itemlist.append(
                 Item(channel=__channel__,
                   action="peliculas_tv",
                   title="[COLOR orange]Successivo >>[/COLOR]",
                   url=scrapedurl,
                   thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                   folder=True))

    return itemlist

# ==============================================================================================================================================================================

def seasons(item):
    logger.info("streamondemand-pureita.channels.altadefinizionezone seasons")

    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)

    patron = '<a href="([^"]+)" role="tab" data-toggle="tab">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedseason in matches:
        scrapedurl = item.url + scrapedurl
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = item.title 

        itemlist.append(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]" + " " + "Stagione" + scrapedseason,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def episodios(item):
    logger.info("streamondemand-pureita.channels.altadefinizionezone episodios")

    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)
    patron = '<div class="tab-pane fade" id="%s">(.*?)</ul>' % item.url.split('#')[1]
    bloque = scrapertools.find_single_match(data, patron)

    patron = '<div class="col"> <span class="episode-title"> <small class="epnum">(.*?)<\/span>[^>]+>\s*<div class="col">\s*<a href=[^=]+=[^=]+=[^=]+="([^"]+)">'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedtitle, scrapedurl in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedtitle = scrapedtitle.replace('</small>', '')

        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos_tv",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def findvideos_tv(item):
    itemlist = []
    data = scrapertools.cache_page(item.url)

    elemento = scrapertools.find_single_match(data, 'file: "(.*?)",')

    itemlist.append(Item(channel=__channel__,
                         action="play",
                         title=item.title,
                         url=elemento,
                         thumbnail=item.thumbnail,
                         fulltitle=item.fulltitle,
                         show=item.fulltitle))
    return itemlist


