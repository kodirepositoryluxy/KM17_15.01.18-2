# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale  Filmgratis
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# By MrTruth
# ------------------------------------------------------------

import re
import urlparse

from core import logger
from core import httptools
from core import servertools
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmgratis"

host = "https://filmgratis.uno"

# ----------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info()
    itemlist = [Item(channel=__channel__,
                     action="peliculas",
                     title="[COLOR azure]Film [COLOR orange]- Novita[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     action="categorie",
                     title="[COLOR azure]Film [COLOR orange]- Categoria[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     action="peranno",
                     title="[COLOR azure]Film [COLOR orange]- per Anno[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                Item(channel=__channel__,
                     action="perpaese",
                     title="[COLOR azure]Film [COLOR orange]- per Paese[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR orange]Cerca Film...[/COLOR]",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================

def search(item, texto):
    logger.info("filmgratis.py Search ===> " + texto)
    item.url = "%s/index.php?story=%s&do=search&subaction=search" % (host, texto)
    try:
        return peliculas(item)
    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================

def newest(categoria):
    logger.info("filmgratis " + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "peliculas":
            item.url = host
            item.action = "peliculas"
            itemlist = peliculas(item)

            if itemlist[-1].action == "peliculas":
                itemlist.pop()

    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist

# ==============================================================================================================================================================================

def annoattuale(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.get_match(data, r'<div class="left-menu-main">(.*?)</div>')
    patron = r'<a href="([^"]+)">Film\s*\d{4}</a>'

    item.url = urlparse.urljoin(host, scrapertools.find_single_match(blocco, patron))
    return peliculas(item)

# ==============================================================================================================================================================================

def categorie(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.get_match(data, r'<div class="menu-janr-content">(.*?)</div>')
    patron = r'<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if 'film erotici' in scrapedtitle.lower(): continue
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url=urlparse.urljoin(host, scrapedurl),
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def peranno(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.get_match(data, r'<div class="sort-menu-title">\s*Anno di pubblicazione:\s*</div>(.*?)<div style="clear: both;"></div>')
    patron = r'<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url=urlparse.urljoin(host, scrapedurl),
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def perpaese(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.get_match(data, r'<div class="sort-menu-title">\s*Paesi di produzione:\s*</div>(.*?)</div>')
    patron = r'<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url=urlparse.urljoin(host, scrapedurl),
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_country_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def peliculas(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = r'<div class="main-news-image">\s*<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)".*?/></a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        year = scrapertools.find_single_match(scrapedtitle, r'\((\d{4})\)')
        scrapetrailar = " Trailer"

        # 
        html = httptools.downloadpage(scrapedurl).data

        patron = '<div class="video-player-plugin">([\s\S]*)<div class="wrapper-plugin-video">'
        matches = re.compile(patron, re.DOTALL).findall(html)
        for url in matches:
            if "scrolling" in url:
                scrapedurl = scrapedurl
            else:
                scrapedtitle = scrapedtitle + scrapetrailar

            itemlist.append(infoSod(
                Item(channel=__channel__,
                     action="findvideos",
                     contentType="movie",
                     title=scrapedtitle,
                     fulltitle=scrapedtitle,
                     url=scrapedurl,
                     extra="movie",
                     thumbnail=scrapedthumbnail,
                     folder=True), tipo="movie"))

    # Pagine
    patronvideos = r'<a href="([^"]+)">>'
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
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 extra=item.extra,
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def findvideos(item):
    logger.info()
    data = httptools.downloadpage(item.url).data
    
    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join([item.title, '[COLOR orange][B]' + ' ' + server + '[/B][/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__
    return itemlist

# ==============================================================================================================================================================================
    
def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita/)")

