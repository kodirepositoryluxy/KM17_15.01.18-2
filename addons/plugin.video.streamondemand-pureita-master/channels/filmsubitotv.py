# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-PureITA.- XBMC Plugin
# Canale per filmsubito.tv
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808.
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmsubitotv"
__category__ = "F,A,S"
__type__ = "generic"
__title__ = "FilmSubito.tv"
__language__ = "IT"

host = "https://www.cinemasubito.link/"

DEBUG = config.get_setting("debug")

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.filmsubitotv mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film - Novità[/COLOR]",
                     action="peliculas",
                     extra="movie",
                     url=host + "film-2016-streaming.html",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film per Genere[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film per Paese[/COLOR]",
                     action="genere",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country_P.png"),					 
                Item(channel=__channel__,
                     title="[COLOR azure]Film per Anno[/COLOR]",
                     action="anno",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Cartoni animati degli anni '80[/COLOR]",
                     action="cartoni80",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/cartoons_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
					 extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV ITA[/COLOR]",
                     action="peliculas_tv",
                     url="%s/serietv-streaming.html" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV Sub-ITA[/COLOR]",
                     action="peliculas_tv",
                     url="%s/serietv-streaming-sub-ita.html" % host,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_sub_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist


def search(item, texto):
    logger.info("streamondemand.filmsubitotv " + item.url + " search " + texto)
    item.url = host + "/search.php?keywords=" + texto
    try:
        if item.extra == "movie":
            return peliculas_movie_src(item)
        if item.extra == "serie":
            return peliculas_tv_src(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def peliculas(item):
    logger.info("streamondemand.filmsubitotv peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<h3 dir="ltr"><a href="([^"]+)"[^>]+>(.*?)</a></h3>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvid",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 plot=scrapedplot,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">&raquo;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 folder=True))

    return itemlist

def seasons(item):
    logger.info("streamondemand.channels.filmsubitotv episodios")

    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)

    patron = '<h3 dir="ltr"><a style=[^h]+href="([^"]+)" class=[^=]+="([^"]+)">(.*?)</a></h3>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedseason  in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapedtitle + scrapedseason

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    return itemlist

def episodios(item):
    logger.info("streamondemand.channels.cinemasubito episodios")

    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.get_match(data, 'Lista Episodi(.*?)</ul>')

    patron = '<li>\s*<a href="(.*?)">\s*(.*?)\s*<\/a>\s*<\/li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle  in matches:
        scrapedplot = ""
        scrapedthumbnail = ""

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
	
def peliculas_tv(item):
    logger.info("streamondemand.cinemasubito peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.anti_cloudflare(item.url, headers)

    # Extrae las entradas (carpetas)
    patron = '<h3 dir="ltr"><a href="([^"]+)" class=[^=]+="([^"]+)">'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
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
    patronvideos = '<a href="([^"]+)">&raquo;'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_tv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 folder=True))

    return itemlist

def peliculas_movie_src(item):
    logger.info("streamondemand.filmsubitotv peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.anti_cloudflare(item.url, headers)

    # Extrae las entradas (carpetas)
    patron = '<h3 dir="ltr"><a href="([^"]+)" class=[^=]+="([^"]+)">'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
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
    patronvideos = '<a href="([^"]+)">&raquo;'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_movie_src",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

def peliculas_tv_src(item):
    logger.info("streamondemand.filmsubitotv peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.anti_cloudflare(item.url, headers)

    # Extrae las entradas (carpetas)
    patron = '<h3 dir="ltr"><a href="([^"]+)" class=[^=]+="([^"]+)">'
    matches = re.compile(patron, re.DOTALL).finditer(data)

    for match in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.unescape(match.group(2))
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
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
    patronvideos = '<a href="([^"]+)">&raquo;'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_tv_src",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist
	
    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">&raquo;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="serietv80",
                 title="[COLOR orange]Successivo>>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 folder=True))

    return itemlist

def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, '<ul id=\'ul_categories\'>(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<a title="(.*?)" alt=[^=]+="(.*?)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedtitle, scrapedurl in matches:
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

def genere(item):
    logger.info("[filmsubitotv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<li class=".*?"><a title="([^"]+)" alt=".*?" href="([^"]+)" class="">.*?</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country_P.png",				 
                 folder=True))

    return itemlist


def serie80(item):
    logger.info("[filmsubitotv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    #    patron = '<a href="#" class="dropdown-toggle wide-nav-link" data-toggle="dropdown">Serie anni 80<b class="caret"></b></a>(.*?)<li class="dropdown">'
    #    data = scrapertools.find_single_match(data, patron)

    patron = '<li class=".*?" ><a title="([^"]+)" alt=".*?" href="([^"]+)">.*?</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(
            Item(channel=__channel__,
                 action="serietv80",
                 title=scrapedtitle,
                 url=scrapedurl,
                 folder=True))

    return itemlist


def anno(item):
    logger.info("[filmsubitotv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<a href="#" class="dropdown-toggle wide-nav-link" data-toggle="dropdown">Anno<b class="caret"></b></a>(.*?)<li class="dropdown">'
    data = scrapertools.find_single_match(data, patron)

    patron = '<a.*?href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country_P.png",				 
                 folder=True))

    return itemlist


def cartoni80(item):
    logger.info("[filmsubitotv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<a href="#" class="dropdown-toggle wide-nav-link" data-toggle="dropdown">Cartoni anni 80<b class="caret"></b></a>(.*?)<li class="dropdown">'
    data = scrapertools.find_single_match(data, patron)

    patron = '<a.*?href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(Item(channel=__channel__, action="peliculas", title=scrapedtitle, url=scrapedurl, folder=True))

    return itemlist


def serie(item):
    logger.info("streamondemand.filmsubitotv peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '</span>.*?<a href="([^"]+)" class="pm-thumb-fix pm-thumb-145">.*?"><img.*?src="([^"]+)" title="Young and Hungry " alt="([^"]+)" width="145">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 folder=True,
                 fanart=scrapedthumbnail))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">&raquo;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="serie",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 folder=True))

    return itemlist


def findvid(item):
    logger.info("[filmsubitotv.py] findvideos")

    # Descarga la página
    data = scrapertools.cache_page(item.url)

    # ---------------------------------------------------------------
    servers = {
        '2': 'http://embed.nowvideo.li/embed.php?v=%s',
        '3': 'http://speedvideo.net/embed-%s-607x360.html',
        '4': 'http://www.fastvideo.me/embed-%s-607x360.html',
        '5': 'http://www.rapidvideo.org/embed-%s-607x360.html',
        '11': 'https://openload.co/embed/%s/',
        '16': 'http://youwatch.org/embed-%s-640x360.html',
        '21': 'http://vidto.me/embed-%s',
        '22': 'http://www.exashare.com/embed-%s-700x400.html',
        '23': 'http://videomega.tv/cdn.php?ref=%s&width=700&height=430',
        '30': 'http://streamin.to/embed-%s-700x370.html'
    }

    patron = "=.setupNewPlayer.'([^']+)','(\d+)'"
    matches = re.compile(patron, re.DOTALL).findall(data)

    data = ""
    for video_id, i in matches:
        try:
            data += servers[i] % video_id + "\n"
        except:
            pass
    # ---------------------------------------------------------------

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, videoitem.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.channel = __channel__

    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")
