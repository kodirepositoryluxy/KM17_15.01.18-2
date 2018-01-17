# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita- XBMC Plugin
# Canale  fastsubita
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config, httptools
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "fastsubita"
__category__ = "S"
__type__ = "generic"
__title__ = "fastsubita"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://fastsubita.tk"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pureita.fastsubita mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Serie TV -  [COLOR orange]Elenco[/COLOR]",
                     action="serietv",
                     extra='serie',
                     url="%s/tutte-le-serie-tv/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_sub_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra='serie',
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

def serietv(item):
    logger.info("pureita.fastsubita peliculas")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    patron = '<h2 class="entry-title title-font"><a href="([^"]+)" rel="bookmark">(.*?)</a></h2>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = scrapedurl.replace ("//fastsubita.tk", host)
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png",
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True))

    patronvideos = '<a class="next page-numbers" href="([^"]+)">Successivi</a></div>'
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
                 action="serietv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 extra=item.extra,
                 folder=True))

    return itemlist

def elenco(item):
    logger.info("pureita.fastsubita peliculas")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    patron = '<a href="([^"]+)" title=[^>]+>([^>]+)</a></td>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedurl = "http:" + scrapedurl
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="serietv",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png",
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True))

    return itemlist

def search(item, texto):
    logger.info("[fastsubita.py] " + item.url + " search " + texto)
    item.url = "%s/?s=%s" % (host, texto)
    try:
        return serietv(item)
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")

