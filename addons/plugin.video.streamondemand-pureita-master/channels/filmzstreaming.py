# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale  FilmZStreaming
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger, httptools
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmzstreaming"

DEBUG = config.get_setting("debug")

host = "https://filmzstreaming.pw/"

headers = [
    ['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]

def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand-pureita.FilmZStreaming mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Cinema[/COLOR]",
                     action="peliculas_new",
                     url="%s/film/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Novita'[/COLOR]",
                     action="peliculas",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Categoria[/COLOR]",
                     action="peliculas_genres",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film [COLOR orange]- Anno[/COLOR]",
                     action="peliculas_years",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_directors_P.png"),
               Item(channel=__channel__,
                     title="[COLOR orange]Cerca Film...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================

def peliculas_years(item):
    logger.info("streamondemand-pureita.FilmZStreaming peliculas_years")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, '<h2>Film Per Anno</h2>(.*?)</ul></nav></div>')

    # Extrae las entradas (carpetas)
    patron = '<a\s*href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).finditer(bloque)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="peliculas",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    return itemlist

	
# ==============================================================================================================================================================================

def peliculas_genres(item):
    logger.info("streamondemand-pureita.FilmZStreaming peliculas_genres")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, 'Categorie FILM</a>(.*?)DMCA</a></li>')


    # Extrae las entradas (carpetas)
    patron = '<li id=".*?" class=".*?"><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).finditer(bloque)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="peliculas",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    return itemlist


# ==============================================================================================================================================================================

def peliculas_new(item):
    logger.info("streamondemand-pureita.FilmZStreaming peliculas_new")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)
    patron = '<h1>Film</h1>(.*?)</div></aside>'
    data = scrapertools.find_single_match(data, patron)

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)[^>]+>\s*[^>]+>[^>]+></span>[^"]+</div>\s*[^>]+>\s*<[^>]+>[^>]+>[^>]+>\s*'
    patron += '<a href="([^"]+)"><div class="see"></div></a>\s*</div>\s*<div class="data">\s*<h3>\s*'
    patron += '<span class="flag" style="background-image[^h]+[^>]+[^>]+"></span>\s*<a href="[^"]+">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = scrapertools.unescape(match.group(1))
        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedurl = urlparse.urljoin(item.url, match.group(2))
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
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
    patronvideos = '<a class=[^>]+ href="([^"]+)"><i id=[^>]+></i>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_new",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================	
		
def search(item, texto):
    logger.info("[streamondemand-pureita.FilmZStreaming ] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        if item.extra == "movie":
            return peliculas_search(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================
		
def peliculas_search(item):
    logger.info("streamondemand-pureita.FilmZStreaming peliculas_search")
    itemlist = []
 
    data = httptools.downloadpage(item.url).data

    patron = '<div class="thumbnail animation-2">\s*<a href="([^"]+)">\s*<img src="([^"]+)" alt="(.*?)" />'
    matches = re.compile(patron, re.DOTALL).findall(data)

    scrapedplot = ""
    for scrapedurl, scrapedthumbnail, scrapedtitle, in matches:
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 contentType="movie",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    return itemlist
# ==============================================================================================================================================================================		
		
def peliculas(item):
    logger.info("streamondemand-pureita.FilmZStreaming peliculas")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    # Extrae las entradas (carpetas)
    patron = '<img src="([^"]+)[^>]+>\s*[^>]+>[^>]+><\/span>[^"]+<\/div>\s*[^>]+>\s*<[^>]+>[^>]+>[^>]+>\s*'
    patron += '<a href="([^"]+)"><div class="see"></div></a>\s*</div>\s*<div class="data">\s*<h3>\s*'
    patron += '<span class="flag" style="background-image[^h]+[^>]+[^>]+"></span>\s*<a href="[^"]+">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = scrapertools.unescape(match.group(1))
        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedurl = urlparse.urljoin(item.url, match.group(2))
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
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
    patronvideos = '<a class=[^>]+ href="([^"]+)"><i id=[^>]+></i>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png",
                 folder=True))
				 
    patronvideos = "<a href='([^>]+)' class=[^>]+>2</a>"
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]pagina 2[/COLOR]",
                 url=scrapedurl,
                 thumbnail="",
                 folder=True))
				 
    patronvideos = "<a href='([^>]+)' class=[^>]+>3</a>"
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]pagina 3[/COLOR]",
                 url=scrapedurl,
                 thumbnail="",
                 folder=True))
				 
    patronvideos = "<a href='([^>]+)' class=[^>]+>4</a>"
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]pagina 4[/COLOR]",
                 url=scrapedurl,
                 thumbnail="",
                 folder=True))
    return itemlist
# ==============================================================================================================================================================================

def findvideos(item):

    data = scrapertools.anti_cloudflare(item.url, headers)

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, '[COLOR orange][B]' + videoitem.title + '[/B][/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist


