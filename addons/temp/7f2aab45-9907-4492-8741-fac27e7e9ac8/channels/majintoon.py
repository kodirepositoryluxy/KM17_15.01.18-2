# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale  per https://majintoon.wordpress.com/
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# By MrTruth
# ------------------------------------------------------------

import re

from core import config
from platformcode import logger
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
                     thumbnail="https://majintoon.files.wordpress.com/2017/03/anime-fight-mix.jpg"),
                Item(channel=__channel__,
                     title=color("Cartoni Animati", "azure"),
                     action="lista_anime",
                     url="%s/category/bambini/" % host,
                     thumbnail="https://majintoon.files.wordpress.com/2017/03/anime-fight-mix.jpg"),
                Item(channel=__channel__,
                     title=color("Anime", "azure"),
                     action="lista_anime",
                     url="%s/category/anime/" % host,
                     thumbnail="https://majintoon.files.wordpress.com/2017/03/anime-fight-mix.jpg"),
                Item(channel=__channel__,
                     title=color("Anime Sub-ITA", "azure"),
                     action="lista_anime",
                     url="%s/category/anime-sub-ita/" % host,
                     thumbnail="https://majintoon.files.wordpress.com/2017/03/anime-fight-mix.jpg"),
                Item(channel=__channel__,
                     title=color("Film animazione", "azure"),
                     action="lista_anime",
                     url="%s/category/film-animazione/" % host,
                     thumbnail="https://majintoon.files.wordpress.com/2017/03/anime-fight-mix.jpg"),
                Item(channel=__channel__,
                     title=color("Serie TV", "azure"),
                     action="lista_anime",
                     url="%s/category/serie-tv/" % host,
                     thumbnail="https://majintoon.files.wordpress.com/2017/03/anime-fight-mix.jpg"),
                Item(channel=__channel__,
                     title=color("Cerca ...", "yellow"),
                     action="search",
                     extra="anime",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def search(item, texto):
    logger.info()
    item.url = host + "/?s=" + texto
    try:
        return lista_anime(item)
    # Continua la ricerca in caso di errore 
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
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
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
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_anime",
                 title=color("Successivo >>", "orange"),
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def links(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = r'(?:<p>|)<span style="[^"]+">Links?\s*([^<]+)<\/span>(?:<\/p>\s*|<br\s*\/>)(.*?)<\/p>'
    blocchi = scrapertools.find_multiple_matches(data, patron)
    if not len(blocchi) > 0:
        patron = r'<a name="Links?\s*([^"]+)"><\/a>(.*?)<\/p>'
        blocchi = scrapertools.find_multiple_matches(data, patron)
    for scrapedtitle, blocco in blocchi:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
            Item(channel=__channel__,
                 action="episodi",
                 title=color("Guarda con " + scrapedtitle, "orange"),
                 url=blocco,
                 extra=scrapedtitle,
                 thumbnail=item.thumbnail,
                 folder=True))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def episodi(item):
    logger.info()
    itemlist = []
    patron = ''

    if 'openload' in item.extra.lower():
        patron = r'<a href="([^"]+)"[^>]+>(?:[^>]+>[^>]+>[^>]+>\s*<b>|)([^<]+)(?:</b>|</a>)'
    else:
        patron = r'<a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(item.url)
    
    for scrapedurl, scrapedtitle in matches:
        if 'wikipedia' in scrapedurl: continue
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
        videoitem.title = "".join(["[%s] " % color(server.capitalize(), 'orange'), item.title])
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
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")

# ================================================================================================================
