# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale per http://www.animesenzalimiti.com/
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# By MrTruth
# ------------------------------------------------------------

import re
import xbmc

from core import logger
from core import servertools
from core import httptools
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "animesenzalimiti"

host = "https://www.animesenzalimiti.org"

# ----------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info()
    itemlist = [Item(channel=__channel__,
                     action="lista_anime",
                     title=color("Film Anime", "azure"),
                     url="%s/category/film-anime/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     action="lista_anime",
                     title=color("Serie Anime", "azure"),
                     url="%s/category/serie-anime/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     action="lista_anime",
                     title=color("Anime in corso", "azure"),
                     url="%s/category/serie-anime-in-corso/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     action="categorie",
                     title=color("Categorie", "azure"),
                     url=host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     action="search",
                     title=color("Cerca anime ...", "yellow"),
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")
                ]

    return itemlist

# ================================================================================================================
'''
# ----------------------------------------------------------------------------------------------------------------
def newest(categoria):
    logger.info()
    itemlist = []
    item = Item()
    try:
        if categoria == "anime":
            item.url = "http://www.animesenzalimiti.com"
            item.action = "ultimiep"
            itemlist = ultimiep(item)

            if itemlist[-1].action == "ultimiep":
                itemlist.pop()
    # Se captura la excepción, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist

# ================================================================================================================
'''
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
    blocco = scrapertools.get_match(data, r'Cateogrie</span></h4>\s*<ul>(.*?)</ul>')
    patron = r'<li[^>]+><a href="([^"]+)"\s*>([^<]+)</a>\s*</li>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        if 'anime da vedere assolutamente' in scrapedtitle.lower(): continue
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
def ultimiep(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data

    blocco = scrapertools.get_match(data, r'<div class="mh-wrapper clearfix">(.*?)<div class="mh-loop-pagination clearfix">')

    patron = r'<a href="([^"]+)"><img.*?src="([^?]+)[^"]+"[^>]+>'
    patron += r'[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        # Pulizia titolo
        scrapedtitle = removestreaming(scrapedtitle).strip()
        cleantitle = re.sub(r'Episodio?\s*\d+\s*(?:\(\d+\)|)', '', scrapedtitle).strip()
        ep = scrapertools.find_single_match(scrapedtitle, r'\d+$').zfill(2)
        scrapedtitle = re.sub(r'\d+$', ep, scrapedtitle)
        # Creazione URL
        ep = scrapertools.find_single_match(scrapedtitle.lower(), r'episodio?\s*(\d+)')
        scrapedurl = re.sub(r'episodio?-?\d+-?(?:\d+-|)[oav]*', '', scrapedurl)

        if 'sub-ita' in scrapedurl:
            scrapedurl = re.sub(r'/$', '', scrapedurl).replace('-sub-ita', '') + "-sub-ita/"

        print "EPISODIO: " + ep + "\nTITLE: " + scrapedtitle + "\nURL: " + scrapedurl
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl + ep,
                 fulltitle=cleantitle,
                 show=re.sub(r'Episodio\s*', '', scrapedtitle),
                 thumbnail=scrapedthumbnail), tipo="tv"))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def lista_anime(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = r'<a class="[^"]+" href="([^"]+)" title="([^"]+)"><img[^s]+src="([^"]+)"[^>]+'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        scrapedtitle = removestreaming(scrapedtitle)
        if 'top 10 anime da vedere' in scrapedtitle.lower(): continue
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodi",
                 contentType="tv",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra="tv",
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="tv"))

    patronvideos = r'<a class="next page-numbers" href="([^"]+)">'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

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
def episodi(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.find_single_match(data, r'(?:<p style="text-align: left;">|<div class="pagination clearfix">\s*)(.*?)</span></a></div>')

    # Il primo episodio è la pagina stessa
    itemlist.append(
        Item(channel=__channel__,
             action="findvideos",
             contentType="tv",
             title="Episodio: 1",
             fulltitle="%s %s %s " % (color(item.title, "deepskyblue"), color("|", "azure"), color("1", "orange")),
             url=item.url,
             extra="tv",
             thumbnail=item.thumbnail,
             folder=True))
    if blocco != "":
        patron = r'<a href="([^"]+)"><span class="pagelink">(\d+)</span></a>'
        matches = re.compile(patron, re.DOTALL).findall(data)
        for scrapedurl, scrapednumber in matches:
            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     contentType="tv",
                     title="Episodio: %s" % scrapednumber,
                     fulltitle="%s %s %s " % (color(item.title, "deepskyblue"), color("|", "azure"), color(scrapednumber, "orange")),
                     url=scrapedurl,
                     extra="tv",
                     thumbnail=item.thumbnail,
                     folder=True))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def findvideos(item):
    logger.info()

    data = httptools.downloadpage(item.url).data
    itemlist = servertools.find_video_items(data=data)

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
def removestreaming(text):
    return re.sub("(?:SUB ITA|ITA|)\s*(?:Download|Streaming)\s*(?:e|&)\s*(?:Download|Streaming)\s*(?:SUB ITA|ITA|)", "", text)

def color(text, color):
    return "[COLOR "+color+"]"+text+"[/COLOR]"

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")

# ================================================================================================================
