# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita.- XBMC Plugin
# Canale per serietvu.
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# By MrTruth
# ------------------------------------------------------------

import re

from core import logger
from core import config
from core import servertools
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "serietvu"
__category__ = "S"
__type__ = "generic"
__title__ = "SerieTVU"
__language__ = "IT"

host = "http://www.serietvu.online/"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]

def isGeneric():
    return True

# ----------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info("[SerieTVU.py]==> mainlist")
    itemlist = [Item(channel=__channel__,
                     action="lista_serie",
                     title="[COLOR azure]Serie TV [/COLOR]- [COLOR yellow]Nuove[/COLOR]",
                     url="%s/category/serie-tv" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     action="latestep",
                     title="[COLOR azure]Episodi [/COLOR]- [COLOR yellow]Ultimi Aggiunti[/COLOR]",
                     url="%s/ultimi-episodi" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     action="lista_serie",
                     title="[COLOR azure]Serie TV [/COLOR]- [COLOR yellow]Aggiornate[/COLOR]",
                     url="%s/ultimi-episodi" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     action="categorie",
                     title=color("Categorie", "azure"),
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title=color("Cerca ...", "yellow"),
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def search(item, texto):
    logger.info("[SerieTVU.py]==> search")
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
def categorie(item):
    logger.info("[SerieTVU.py]==> categorie")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers=headers)
    blocco = scrapertools.get_match(data, '<h2>Sfoglia</h2>\s*<ul>(.*?)</ul>\s*</section>')
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_serie",
                 title=scrapedtitle,
                 contentType="tv",
                 url="%s%s" % (host, scrapedurl),
                 thumbnail=item.thumbnail,
                 folder=True))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def latestep(item):
    logger.info("[SerieTVU.py]==> latestep")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers=headers)

    patron = '<div class="item">\s*<a href="([^"]+)" data-original="([^"]+)" class="lazy inner">'
    patron += '[^>]+>[^>]+>[^>]+>[^>]+>([^<]+)<small>([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedimg, scrapedtitle, scrapedinfo in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title="%s %s" % (scrapedtitle, scrapedinfo),
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedimg,
                 show=scrapedtitle,
                 folder=True), tipo="tv"))
    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def lista_serie(item):
    logger.info("[SerieTVU.py]==> lista_serie")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers=headers)

    patron = '<div class="item">\s*<a href="([^"]+)" data-original="([^"]+)" class="lazy inner">'
    patron += '[^>]+>[^>]+>[^>]+>[^>]+>([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedimg, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedimg,
                 show=scrapedtitle,
                 folder=True), tipo="tv"))

    # Pagine
    patron = r'<li><a href="([^"]+)"\s*>Pagina'
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
def episodios(item):
    logger.info("[SerieTVU.py]==> episodios")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers=headers)

    patron = '<option value="(\d+)"[\sselected]*>.*?</option>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for value in matches:
        patron = '<div class="list [active]*" data-id="%s">(.*?)</div>\s*</div>' % value
        blocco = scrapertools.find_single_match(data, patron)

        patron = '(<a data-id="\d+.*?" data-href="([^"]+)" data-original="([^"]+)" class=".*?">)[^>]+>[^>]+>([^<]+)</div>'
        matches = re.compile(patron, re.DOTALL).findall(blocco)
        for scrapedextra, scrapedurl, scrapedimg, scrapedtitle in matches:
            scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("Episodio", "")).strip()
            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     title=value + "x" + scrapedtitle.zfill(2),
                     fulltitle=scrapedtitle,
                     contentType="episode",
                     url=scrapedurl,
                     thumbnail=scrapedimg,
                     extra=scrapedextra,
                     folder=True))
        
    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title="Aggiungi alla libreria",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios",
                 show=item.show))
        itemlist.append(
            Item(channel=__channel__,
                 title="Scarica tutti gli episodi della serie",
                 url=item.url,
                 action="download_all_episodes",
                 extra="episodios",
                 show=item.show))
    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def findvideos(item):
    logger.info("[SerieTVU.py]==> findvideos")
    itemlist = servertools.find_video_items(data=item.extra)

    # Non sono riuscito a trovare un modo migliore di questo, se qualcuno ha un metodo migliore di questo
    # per estrarre il video lo sistemi per favore.
    if len(itemlist) > 1:
        itemlist.remove(itemlist[1])
    server = re.sub(r'[-\[\]\s]+', '', itemlist[0].title)
    itemlist[0].title = "".join(["[%s] " % color(server, 'orange'), item.title])
    itemlist[0].fulltitle = item.fulltitle
    itemlist[0].show = item.show
    itemlist[0].thumbnail = item.thumbnail
    itemlist[0].channel = __channel__
    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-main/)")

def color(text, color):
    return "[COLOR "+color+"]"+text+"[/COLOR]"

# ================================================================================================================
