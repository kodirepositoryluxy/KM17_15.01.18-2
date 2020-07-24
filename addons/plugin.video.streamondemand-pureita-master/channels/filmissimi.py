# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# By Costaplus
# ------------------------------------------------------------
import re

import xbmc

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmissimi"
__category__ = "F"
__type__ = "generic"
__title__ = "filmissimi.net"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.filmissimi.net"

headers = [
    ['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'],
    ['Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host],
    ['Cache-Control', 'max-age=0']
]

def isGeneric():
    return True

# -------------------------------------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info("[filmissimi.py] mainlist")
    itemlist = [Item(channel=__channel__,
                     action="elenco",
                     title="[COLOR yellow]Novita'[/COLOR]",
                     url=host,
                     thumbnail=NovitaThumbnail,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     action="elenco",
                     title="[COLOR azure]Film al Cinema[/COLOR]",
                     url=host + "/genere/cinema",
                     thumbnail=CinemaThumbnail,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     action="elenco",
                     title="[COLOR azure]Film Sub-Ita[/COLOR]",
                     url=host + "/genere/sub-ita",
                     thumbnail=SubThumbnail,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     action="elenco",
                     title="[COLOR azure]Film HD[/COLOR]",
                     url=host + "/genere/film-in-hd",
                     thumbnail=HDThumbnail,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     action="genere",
                     title="[COLOR azure]Genere[/COLOR]",
                     url=host,
                     thumbnail=GenereThumbnail,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     action="search",
                     extra="movie",
                     title="[COLOR orange]Cerca..[/COLOR]",
                     thumbnail=CercaThumbnail,
                     fanart=FilmFanart)]

    return itemlist


# ===========================================================================================================================================

# -------------------------------------------------------------------------------------------------------------------------------------------
def genere(item):
    logger.info("[filmissimi.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.get_match(data, '<ul id="menu-categorie-1" class="ge">(.*?)</div>')

    patron = '<li id=[^>]+><a href="(.*?)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
 
        if DEBUG: logger.info("title=[" + scrapedtitle + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="elenco",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist


# ===========================================================================================================================================

# -------------------------------------------------------------------------------------------------------------------------------------------
def elenco(item):
    logger.info("[filmissimi.py] elenco")
    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)

    elemento = scrapertools.find_single_match(data,'<div class="estre">(.*?)<div class="paginacion">')

    patron='<div class="item">[^<]+<a href="(.*?)"[^<]+<[^<]+<img.*?icon[^<]+<img src="(.*?)" alt="(.*?)"[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+</div>'
    matches = re.compile(patron, re.DOTALL).findall(elemento)

    for scrapedurl, scrapedthumbnail,scrapedtitle  in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.split("(")[0]
        logger.info("title=[" + scrapedtitle + "] url=[" + scrapedurl + "] thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail), tipo="movie"))

    # Paginazione
    # ===========================================================================================================================
    matches = scrapedSingle(item.url, '<div class="paginacion">(.*?)</div>',"current'>.*?<\/span><.*?href='(.*?)'>.*?</a>")
    if len(matches) > 0:
        paginaurl = matches[0]
        itemlist.append(
            Item(channel=__channel__, action="elenco", title=AvantiTxt, url=paginaurl, thumbnail=AvantiImg))
        itemlist.append(Item(channel=__channel__, action="HomePage", title=HomeTxt, folder=True))
    else:
        itemlist.append(Item(channel=__channel__, action="mainlist", title=ListTxt, folder=True))
    # ===========================================================================================================================
    return itemlist
# ===========================================================================================================================================


# -------------------------------------------------------------------------------------------------------------------------------------------
def search(item, texto):
    logger.info("[filmissimi.py] init texto=[" + texto + "]")
    itemlist = []
    url = "http://www.filmissimi.net/?s=" + texto

    data = scrapertools.cache_page(url, headers=headers)

    patron = 'class="s-img">[^<]+<.*?src="(.*?)"[^<]+<[^<]+<[^<]+</div>[^<]+<[^<]+<[^<]+<[^<]+</span>[^<]+</span>[^<]+<h3><a href="(.*?)">(.*?)</a></h3>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail,scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        log("elenco", "title=[" + scrapedtitle + "] url=[" + scrapedurl + "] thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail), tipo="movie"))

    # Paginazione
    # ===========================================================================================================================
    matches = scrapedSingle(url, '<div class="paginacion">(.*?)</div>',"current'>.*?<\/span><.*?href='(.*?)'>.*?</a>")

    if len(matches) > 0:
        paginaurl = matches[0]
        itemlist.append(Item(channel=__channel__, action="elenco", title=AvantiTxt, url=paginaurl, thumbnail=AvantiImg))
        itemlist.append(Item(channel=__channel__, action="HomePage", title=HomeTxt, folder=True))
    else:
        itemlist.append(Item(channel=__channel__, action="mainlist", title=ListTxt, folder=True))
    # ===========================================================================================================================
    return itemlist
# ===========================================================================================================================================

# =================================================================
# Funzioni di servizio
# -----------------------------------------------------------------
def scrapedAll(url="", patron=""):
    matches = []
    data = scrapertools.cache_page(url, headers=headers)
    log("data ->" + data)
    MyPatron = patron
    matches = re.compile(MyPatron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    return matches
# =================================================================

# -----------------------------------------------------------------
def scrapedSingle(url="", single="", patron=""):
    matches = []
    data = scrapertools.cache_page(url, headers=headers)
    elemento = scrapertools.find_single_match(data, single)
    matches = re.compile(patron, re.DOTALL).findall(elemento)
    scrapertools.printMatches(matches)

    return matches
# =================================================================

# -----------------------------------------------------------------
def HomePage(item):
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-main)")
# =================================================================

# =================================================================
# riferimenti di servizio
# ---------------------------------------------------------------------------------------------------------------------------------
NovitaThumbnail = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"
GenereThumbnail = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"
CinemaThumbnail= "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"
HDThumbnail= "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png"
SubThumbnail= "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_sub_P.png"
FilmFanart = "https://superrepo.org/static/images/fanart/original/script.artwork.downloader.jpg"
CercaThumbnail = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"
CercaFanart = "https://i.ytimg.com/vi/IAlbvyBdYdY/maxresdefault.jpg"
HomeTxt = "[COLOR yellow]Torna Home[/COLOR]"
ListTxt = "[COLOR orange]Torna a elenco principale [/COLOR]"
AvantiTxt = "[COLOR orange]Successivo>>[/COLOR]"
AvantiImg = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png"
thumbnail = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png"
# ----------------------------------------------------------------------------------------------------------------------------------#----------------------------------------------------------------------------------------------------------------------------------
