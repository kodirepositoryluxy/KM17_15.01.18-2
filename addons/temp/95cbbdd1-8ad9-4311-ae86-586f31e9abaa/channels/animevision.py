# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale per http://animevision.altervista.org/
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# By costaplus
# ------------------------------------------------------------
import re

from core import httptools
from core import logger
from core import scrapertools
from core.item import Item

__channel__ = "animevision"

host = "http://www.animevision.it"


# -----------------------------------------------------------------
def mainlist(item):
    logger.info("streamondemand.animevision mainlist")

    itemlist = [Item(channel=__channel__,
                     action="lista_anime",
                     title="[COLOR azure]Anime [/COLOR]- [COLOR orange]Lista Completa[/COLOR]",
                     url=host + "/elenco.php",
                     thumbnail=CategoriaThumbnail,
                     fanart=CategoriaFanart)]

    return itemlist


# =================================================================

# -----------------------------------------------------------------
def lista_anime(item):
    logger.info("streamondemand.animevision lista_anime")

    itemlist = []

    data = httptools.downloadpage(item.url).data

    patron = "<div class='epContainer' >[^=]+='imgEp'[^<]+<a href='(.*?)'>[^>]+><img src='(.*?)'[^<]+<[^>]+>(.*?)</div>"
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedimg, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedimg = host + "/" + scrapedimg
        scrapedurl = host + "/" + scrapedurl

        itemlist.append(
            Item(channel=__channel__,
                 action="episodi",
                 title=scrapedtitle,
                 url=scrapedurl,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 thumbnail=scrapedimg,
                 fanart=scrapedimg,
                 viewmode="movie"))

    return itemlist


# =================================================================

# -----------------------------------------------------------------
def episodi(item):
    logger.info("streamondemand.animevision episodi")
    itemlist = []

    data = httptools.downloadpage(item.url).data

    patron = "epContainer'>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+><[^<]+<[^>]+>.*?href='(.*?)'[^>]+>(.*?)</a></div>"
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapedtitle.split(';')[1]
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedurl = host + "/" + scrapedurl

        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 thumbnail=item.thumbnail,
                 fanart=item.fanart))

    return itemlist


# =================================================================

# =================================================================
# riferimenti di servizio
# -----------------------------------------------------------------
CategoriaThumbnail = "http://static.europosters.cz/image/750/poster/street-fighter-anime-i4817.jpg"
CategoriaFanart = "https://i.ytimg.com/vi/IAlbvyBdYdY/maxresdefault.jpg"
