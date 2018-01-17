# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale  per http://altadefinizionehd.com/
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# By MrTruth
# ------------------------------------------------------------

import re

from core import httptools
from core import scrapertools
from core import servertools
from core.httptools import urllib
from core.item import Item
from core.tmdb import infoSod
from platformcode import logger

__channel__ = "altadefinizionehd"

host = "https://altadefinizionehd.com"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]


# ----------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info("[AltadefinizioneHD.py]==> mainlist")
    itemlist = [
        Item(channel=__channel__,
             action="ultimifilm",
             title=color("Ultimi film", "azure"),
             url=host,
             thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png", ),
        Item(channel=__channel__,
             action="pergenere",
             title=color("Per Genere", "azure"),
             url=host,
             thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png", ),
        Item(channel=__channel__,
             action="search",
             title=color("Cerca", "yellow"),
             extra="movie",
             url=host,
             thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search", )
    ]

    return itemlist


# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def search(item, texto):
    logger.info("[AltadefinizioneHD.py]==> search")
    item.url = host + "/?s=" + texto
    item.extra = "movie"
    try:
        return ultimifilm(item)
    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def newest(categoria):
    logger.info("[AltadefinizioneHD.py]==> newest " + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "peliculas":
            item.url = host
            item.action = "ultimifilm"
            itemlist = ultimifilm(item)

            if itemlist[-1].action == "ultimifilm":
                itemlist.pop()

    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist


# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def pergenere(item):
    logger.info("[AltadefinizioneHD.py]==> pergenere")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    blocco = scrapertools.get_match(data, '<ul class="scrolling cat">(.*?)</ul>')
    patron = '<li class="cat-item cat-item-\d+"><a href="([^"]+)"(?: title=".*?"|\s)>([^<]+)</a>\s<span>\d+</span>\s</li>'

    matches = re.compile(patron, re.DOTALL).findall(blocco)
    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="ultimifilm",
                 title=color(scrapedtitle, "azure"),
                 url=scrapedurl,
                 extra="movie",
                 folder=True))

    return itemlist


# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def ultimifilm(item):
    logger.info("[AltadefinizioneHD.py]==> ultimifilm")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = 'class="item">\s*<a href="([^"]+)">\s*<div class="image">\s*<img src=[^=]+="(.*?)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedimg = ""
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

    patron = '<a href="(.*?)" >Successivo</a></div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title=color("Torna Home", "yellow"),
                 folder=True))
        itemlist.append(
            Item(channel=__channel__,
                 action="ultimifilm",
                 title=color("Successivo >>", "orange"),
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist


# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def findvideos(item):
    logger.info("[AltadefinizioneHD.py]==> findvideos")

    data = httptools.downloadpage(item.url, headers=headers).data
    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join(["[%s] " % color(server.capitalize(), 'orange'), item.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist


# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def color(text, color):
    return "[COLOR " + color + "]" + text + "[/COLOR]"


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")

# ================================================================================================================
