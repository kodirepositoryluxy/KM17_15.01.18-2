# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-PureITA.- XBMC Plugin
# Canale  animesenzalimiti
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
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

host = "https://animesenzalimiti.org/"

# ----------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info()
    itemlist = [Item(channel=__channel__,
                     action="ultimiep",
                     title="[COLOR azure]Anime [/COLOR]- [COLOR orange]Ultimi Episodi[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_new_P.png"),
                Item(channel=__channel__,
                     action="lista_anime",
                     title="[COLOR azure]Anime [/COLOR]- [COLOR orange]Film[/COLOR]",
                     url="%s/category/film-anime/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animated_movie_P.png"),
                Item(channel=__channel__,
                     action="lista_anime",
                     title="[COLOR azure]Anime [/COLOR]- [COLOR orange]Serie Speciali[/COLOR]",
                     url="%s/category/special-anime/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_P.png"),
                Item(channel=__channel__,
                     action="lista_anime",
                     title="[COLOR azure]Anime [/COLOR]- [COLOR orange]in Corso[/COLOR]",
                     url="%s/category/anime-in-corso/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animation_P.png"),
                Item(channel=__channel__,
                     action="categorie",
                     title="[COLOR azure]Anime [/COLOR]- [COLOR orange]Categorie[/COLOR]",
                     url="%s/category/anime-in-corso/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_genre_P.png"),
                Item(channel=__channel__,
                     action="cat_years",
                     title="[COLOR azure]Anime [/COLOR]- [COLOR orange]Archivio[/COLOR]",
                     url="%s/category/anime-in-corso/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title=color("Cerca anime ...", "orange"),
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ================================================================================================================category/anime-in-corso/
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

# ==============================================================================================================================================================================
'''
# ==============================================================================================================================================================================
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


# ==============================================================================================================================================================================

def categorie(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.get_match(data, r'<h2 class="screen-reader-text">Navigazione articoli</h2>([^+]+)</div>.*?</aside>.*?</div>')
    patron = r'<li class=".*?"><a href="([^"]+)" >([^<]+)</a>'

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

# ==============================================================================================================================================================================
def cat_years(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.get_match(data, r'<h2 class="screen-reader-text">Navigazione articoli</h2>([^+]+)</div>.*?</aside>.*?</div>')
    patron = r"<li><a href='([^>]+)'>([^<]+)</a></li>"
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
# ==============================================================================================================================================================================
'''
# ----------------------------------------------------------------------------------------------------------------
def animepopolari(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.get_match(data, r"<div class='widgets-grid-layout no-grav'>(.*?)</div>\s*</div>\s*</div>")
    patron = r'<a href="([^"]+)" title="([^"]+)"[^>]+>\s*<img.*?src="([^?]+)[^"]+"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        scrapedtitle = removestreaming(scrapedtitle)
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

    return itemlist
# ----------------------------------------------------------------------------------------------------------------
'''
# ==============================================================================================================================================================================

def ultimiep(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data

    blocco = scrapertools.get_match(data, r'<span class="mh-widget-title-inner">Ultimi Anime</span>(.*?)</article></div>')
    patron = r'<a class="[^>]+" href="([^"]+)" title="([^"]+)"><img width=".*?" height=".*?" src="([^"]+)"[^>]+>.*?</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        scrapedtitle = removestreaming(scrapedtitle)
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

    patronvideos = r'<a class="next page-numbers" href="([^"]+)">&raquo;</a></div>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

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

# ==============================================================================================================================================================================

def lista_anime(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = r'<a class="[^>]+" href="([^"]+)" title="([^"]+)"><img width=".*?" height=".*?" src="([^"]+)".*?'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        scrapedtitle = removestreaming(scrapedtitle)
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

    patron = r'<a class="next page-numbers" href="([^"]+)">&raquo;</a></div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = matches[0]
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_anime",
                 title=color("Successivo >>", "orange"),
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

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

# ==============================================================================================================================================================================

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

# ==============================================================================================================================================================================

def removestreaming(text):
    return re.sub("(?:SUB ITA|ITA|)\s*(?:Download|Streaming)\s*(?:e|&)\s*(?:Download|Streaming)\s*(?:SUB ITA|ITA|)", "", text)

def color(text, color):
    return "[COLOR "+color+"]"+text+"[/COLOR]"

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")

