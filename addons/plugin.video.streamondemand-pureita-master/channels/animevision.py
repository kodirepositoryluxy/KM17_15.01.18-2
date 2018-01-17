# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamoOnDemand-PureITA / XBMC Plugin
# Canale animevision
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# By costaplus
# ------------------------------------------------------------
import re

from core import config
from core import logger
from core import scrapertools
from core.item import Item

__channel__ = "animevision"
__category__ = "A"
__type__ = "generic"
__title__ = "Animevision"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.animevision.it"

def isGeneric():
    return True


# -----------------------------------------------------------------
def mainlist(item):
    logger.info("streamondemand.animevision mainlist")

    itemlist = [Item(channel=__channel__,
                     action="lista_anime",
                     title="[COLOR azure]Anime [/COLOR]- [COLOR orange]Lista Completa[/COLOR]",
                     url=host + "/elenco.php",
                     thumbnail=CategoriaThumbnailList,
                     fanart=CategoriaFanart),
                Item(channel=__channel__,
                     action="lista_popolari",
                     title="[COLOR azure]Anime [/COLOR]- [COLOR orange]Episodi Popolari[/COLOR]",
                     url=host + "?ordine=like",
                     thumbnail=CategoriaThumbnail,
                     fanart=CategoriaFanart),
                Item(channel=__channel__,
                     action="lista_popolari",
                     title="[COLOR azure]Anime [/COLOR]- [COLOR orange]Episodi piu' Visti[/COLOR]",
                     url=host + "?ordine=view",
                     thumbnail=CategoriaThumbnail,
                     fanart=CategoriaFanart)]

    return itemlist
# =================================================================

# -----------------------------------------------------------------
def lista_anime(item):
    logger.info("streamondemand.animevision lista_anime")

    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = "<div class='epContainer' ><a class='falseLink' href='(.*?)'><div class='imgEp video-wrapper' id='.*?'><div class='immagine loading'>"
    patron += "<img data-src='(.*?)' src='.*?' class='img-fluid video-main b-lazy'>[^>]+>[^>]+></i></div>[^>]+>(.*?)</div>"
	
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl,scrapedimg, scrapedtitle in matches:
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
def lista_popolari(item):
    logger.info("streamondemand.animevision lista_anime")

    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = "<div class='epContainer'>\s*<a class='falseLink' href='(.*?)' style='.*?'>\s*<div class='imgEp video-wrapper loading' id='.*?'>\s*"
    patron += "<img style='pointer-events: none;' class='img-fluid video-main b-lazy' src='.*?' data-src='(.*?)' alt='.*?'>[^>]+>[^>]+></i></div>"
    patron += "[^>]+>\s*.*?</div>\s*[^>]+>\s*[^>]+><b>(.*?)</b>"
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl,scrapedimg, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedimg = host + "/" + scrapedimg
        scrapedurl = host + "/" + scrapedurl

        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
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
    itemlist=[]

    data = scrapertools.cache_page(item.url)

    patron="<a class='nodecoration text-white' href='([^<]+)'>(.*?)</a>"
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle  in matches:
        scrapedtitle=scrapedtitle.split(';')[1]
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
CategoriaThumbnailList = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_lista_P.png"
CategoriaThumbnail = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_P.png"
CategoriaFanart = "https://i.ytimg.com/vi/IAlbvyBdYdY/maxresdefault.jpg"
