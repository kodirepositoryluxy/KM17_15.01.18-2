# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale per https://majintoon.wordpress.com/
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# By MrTruth
# ------------------------------------------------------------

import re

from core import config
from core import logger
from core import servertools
from core import httptools
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "majintoon"

host = "https://majintoon.wordpress.com"


# ----------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info()
    itemlist = [Item(channel=__channel__,
                     action="categorie",
                     title=color("Categorie", "azure"),
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_genre_P.png"),
                Item(channel=__channel__,
                     title=color("Anime", "azure"),
                     action="lista_anime",
                     url=host + "/category/anime/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_P.png"),
                Item(channel=__channel__,
                     title=color("Anime Sub-ITA", "azure"),
                     action="lista_anime",
                     url=host + "/category/anime-sub-ita/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_sub_P.png"),
                Item(channel=__channel__,
                     title=color("Film animazione", "azure"),
                     action="lista_anime",
                     url="%s/category/film-animazione/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animated_movie_P.png"),
                Item(channel=__channel__,
                     title=color("Serie TV", "azure"),
                     action="lista_anime",
                     url=host + "/category/serie-tv/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title=color("Cerca ...", "yellow"),
                     action="search",
                     extra="anime",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def search(item, texto):
    logger.info()
    item.url = host + "/?s=" + texto
    try:
        return lista_anime(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def categorie(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.get_match(data, r'Categorie</a>\s*<ul\s*class="sub-menu">(.*?)</ul>\s*</li>')
    patron = r'<li[^>]+><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
                Item(channel=__channel__,
                     action="lista_anime",
                     title=scrapedtitle,
                     url=scrapedurl,
                     extra="tv",
                     thumbnail=item.thumbnail,
                     folder=True))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def lista_anime(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data

    patron = r'<figure class="post-image">\s*<a title="([^"]+)" href="([^"]+)">'
    patron += r'\s*<img.*?src="([^"]*)".*?/>\s*</a>\s*</figure>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl, scrapedthumbnail in matches:
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="links",
                 contentType="tv",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 show=scrapedtitle,
                 extra="tv",
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="tv"))

    # Pagine
    patron = '<div class="nav-previous"><a href="([^"]+)" >'
    matches = re.compile(patron, re.DOTALL).findall(data)

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
                 action="lista_anime",
                 title=color("Successivo >>", "orange"),
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def links(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data

    blocchi = scrapertools.find_multiple_matches(data, r'(?:<p>|)<span style="[^"]+">Links?\s*([^<]+)</span>(?:</p>\s*|<br\s*/>)(.*?)</p>')
    for scrapedtitle, blocco in blocchi:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
            Item(channel=__channel__,
                 action="episodi",
                 title=color("Guarda con " + scrapedtitle, "orange"),
                 url=blocco,
                 thumbnail=item.thumbnail,
                 folder=True))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def episodi(item):
    logger.info()
    itemlist = []

    patron = r'<a href="([^"]+)" target="_blank"(?:\s*rel="[^"]+"|)>([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(item.url)

    for scrapedurl, scrapedtitle in matches:
        if 'wikipedia' not in scrapedurl:
            scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).replace("×", "x")
            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     contentType="tv",
                     title=color(scrapedtitle, "azure"),
                     fulltitle=scrapedtitle,
                     url=scrapedurl,
                     extra="tv",
                     show=item.show,
                     thumbnail=item.thumbnail,
                     folder=True))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def findvideos(item):
    logger.info()
    itemlist = servertools.find_video_items(data=item.url)
    
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
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")

# ================================================================================================================
