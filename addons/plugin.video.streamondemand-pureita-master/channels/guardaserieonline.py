# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita.- XBMC Plugin
# Canale guardaserieonline
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# By MrTruth
# ------------------------------------------------------------

import re
from core import httptools
from core import logger
from core import config
from core import servertools
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "guardaserieonline"
__category__ = "S, A"
__type__ = "generic"
__title__ = "GuardaSerie.online"
__language__ = "IT"

host = "http://www.guardaserie.online"

DEBUG = config.get_setting("debug")

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]

def isGeneric():
    return True

# ----------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info("[GuardaSerieOnline.py]==> mainlist")
    itemlist = [Item(channel=__channel__,
                     action="nuoveserie",
                     title="[COLOR azure]Serie TV - [COLOR orange]Nuove[/COLOR]",
                     url="%s/lista-serie-tv" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
               Item(channel=__channel__,
                     action="nuoveseriesub",
                     title="[COLOR azure]Serie TV - [COLOR orange]Inedite ([COLOR azure]Sub Ita[/COLOR])",
                     url="%s/lista-serie-tv" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_sub_P.png"),
               Item(channel=__channel__,
                     action="serietvaggiornate",
                     title="[COLOR azure]Serie TV - [COLOR orange]Aggiornate[/COLOR]",
                     url="%s/lista-serie-tv" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     action="categorie",
                     title="[COLOR azure]Serie TV - [COLOR orange]Categorie[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),                
               Item(channel=__channel__,
                     action="lista_serie",
                     title=color("Anime", "azure"),
                     url="%s/category/animazione/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animation_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title=color("Cerca ...", "yellow"),
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def newest(categoria):
    logger.info("[GuardaSerieOnline.py]==> newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "series":
            item.url = "%s/lista-serie-tv" % host
            item.action = "serietvaggiornate"
            itemlist = serietvaggiornate(item)

            if itemlist[-1].action == "serietvaggiornate":
                itemlist.pop()

    # Se captura la excepción, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def search(item, texto):
    logger.info("[GuardaSerieOnline.py]==> search")
    item.url = host + "/?s=" + texto
    try:
        return lista_serie(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def nuoveserie(item):
    logger.info("[GuardaSerieOnline.py]==> nuoveserie")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    blocco = scrapertools.get_match(data, '<div\s*class="container container-title-serie-new container-scheda" meta-slug="new">(.*?)</div></div><div')

    patron = r'<a\s*href="([^"]+)".*?>\s*<img\s*.*?src="([^"]+)" />[^>]+>[^>]+>[^>]+>[^>]+>'
    patron += r'[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>([^<]+)</p>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodi",
                 contentType="tv",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra="tv",
                 show=scrapedtitle,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="tv"))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def nuoveseriesub(item):
    logger.info("[GuardaSerieOnline.py]==> nuoveserie")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    blocco = scrapertools.get_match(data, '<div\s*class="container container-title-serie-ined container-scheda" meta-slug="ined">(.*?)</div></div><div')

    patron = r'<a\s*href="([^"]+)".*?>\s*<img\s*.*?src="([^"]+)" />[^>]+>[^>]+>[^>]+>[^>]+>'
    patron += r'[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>([^<]+)</p>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodi",
                 contentType="tv",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra="tv",
                 show=scrapedtitle,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="tv"))

    return itemlist

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------
def serietvaggiornate(item):
    logger.info("[GuardaSerieOnline.py]==> serietvaggiornate")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    blocco = scrapertools.get_match(data, r'<div\s*class="container container-title-serie-lastep  container-scheda" meta-slug="lastep">(.*?)</div></div><div')

    patron = r'<a\s*rel="nofollow" href="([^"]+)"[^>]+> <img\s*.*?src="([^"]+)"[^>]+>[^>]+>'
    patron += r'[^>]+>[^>]+>[^>]+>[^>]+>([^<]+)<[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>([^<]+)<[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedthumbnail, scrapedep, scrapedtitle in matches:
        episode = re.compile(r'^(\d+)x(\d+)', re.DOTALL).findall(scrapedep)  # Prendo stagione ed episodio
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        title = "%s %s" % (scrapedtitle, scrapedep)
        extra = r'<span\s*.*?meta-stag="%s" meta-ep="%s" meta-embed="([^"]+)">' % (
            episode[0][0], episode[0][1].lstrip("0"))
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="tv",
                 title=title,
                 show=title,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra=extra,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="tv"))
    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def categorie(item):
    logger.info("[GuardaSerieOnline.py]==> categorie")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    blocco = scrapertools.get_match(data, r'<ul\s*class="dropdown-menu category">(.*?)</ul>')
    patron = r'<li>\s*<a\s*href="([^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_serie",
                 title=scrapedtitle,
                 contentType="tv",
                 url="".join([host, scrapedurl]),
                 thumbnail='https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png',
                 extra="tv",
                 folder=True))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def lista_serie(item):
    logger.info("[GuardaSerieOnline.py]==> lista_serie")
    itemlist = []
    
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = r'<a\s*href="([^"]+)".*?>\s*<img\s*.*?src="([^"]+)" />[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>([^<]+)</p></div>'
    blocco = scrapertools.get_match(data, r'<div\s*class="col-xs-\d+ col-sm-\d+-\d+">(.*?)<div\s*class="container-fluid whitebg" style="">')
    matches = re.compile(patron, re.DOTALL).findall(blocco)
    
    for scrapedurl, scrapedimg, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodi",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedimg,
                 extra=item.extra,
                 show=scrapedtitle,
                 folder=True), tipo="tv"))


    patron = '<a\s*class="nextpostslink" rel="next" href="([^"]+)">&raquo;</a>'
    next_page = scrapertools.find_single_match(data, patron)
    if len(matches) > 0:
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_serie",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def episodi(item):
    logger.info("[GuardaSerieOnline.py]==> episodi")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = r'<img\s*.*?[meta-src|data-original]*="([^"]+)"\s*/>[^>]+>([^<]+)<[^>]+>[^>]+>[^>]+>'
    patron += r'[^>]+>[^>]+>([^<]+)*<[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>'
    patron += r'[^>]+>[^>]+>[^>]+>\s*<span\s*.*?(meta-embed="[^"]+">)'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedthumbnail, scrapedep, scrapedeptitle, scrapedextra in matches:
        scrapedeptitle = scrapertools.decodeHtmlentities(scrapedeptitle).strip()
        scrapedep = scrapertools.decodeHtmlentities(scrapedep).strip()
        scrapedtitle = "%s - %s" % (scrapedep, scrapedeptitle) if scrapedeptitle != "" else scrapedep
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url="",
                 contentType="episode",
                 extra=scrapedextra,
                 thumbnail=scrapedthumbnail,
                 folder=True))
    
    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title="Aggiungi alla libreria",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodi",
                 show=item.show))
        itemlist.append(
            Item(channel=__channel__,
                 title="Scarica tutti gli episodi della serie",
                 url=item.url,
                 action="download_all_episodes",
                 extra="episodi",
                 show=item.show))
    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def findvideos(item):
    logger.info("[GuardaSerieOnline.py]==> findvideos")

    if item.url:
        data = httptools.downloadpage(item.url, headers=headers).data
        data = scrapertools.find_single_match(data, item.extra)
        itemlist = servertools.find_video_items(data=data)
    else:
        itemlist = servertools.find_video_items(data=item.extra)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title).capitalize()
        videoitem.title = "".join(["[%s] " % color(server, 'orange'), item.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def color(text, color):
    return "[COLOR "+color+"]"+text+"[/COLOR]"

# ================================================================================================================
