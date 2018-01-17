# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-PureITA / XBMC Plugin
# Canale filmperevolvere
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import urlparse

import lib.pyaes as aes
from core import config
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmperevolvere"
__category__ = "F,C"
__type__ = "generic"
__title__ = "filmperevolvere (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "https://filmperevolvere.it/"

headers = [
    ['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/54.0'],
    ['Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Accept-Language', 'en-US,en;q=0.5'],
    ['Referer', host],
    ['DNT', '1'],
    ['Upgrade-Insecure-Requests', '1'],
    ['Cache-Control', 'max-age=0']
]


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand-pureita.filmperevolvere mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Ultimi Film Inseriti[/COLOR]",
                     action="peliculas_film",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Categorie[/COLOR]",
                     action="categorie",
                     url="%s/indexes/3651-2/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

def search(item, texto):
    logger.info("[filmperevolvere.py] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto

    try:
        return peliculas_film(item)

    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)

    return []

# ------------------------------------------------------------------------------------------------------------------------------------

def categorie(item):
    itemlist = []

    c = get_test_cookie(item.url)
    if c: headers.append(['Cookie', c])

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.get_match(data, '<div class="page-title pad group">(.*?)</li> </div>')

    # Extrae las entradas (carpetas)
    patron = '<h3 class="ei-item-term"><a\s*href="([^"]+)">(.*?)<\/a><\/h3>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:

        if scrapedtitle.startswith(("HOME")):
            continue
        if scrapedtitle.startswith(("SERIE TV")):
            continue
        if scrapedtitle.startswith(("GENERI")):
            continue

        if (DEBUG): logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ------------------------------------------------------------------------------------------------------------------------------------	

def peliculas(item):
    logger.info("streamondemand-pureita.filmperevolvere peliculas")
    itemlist = []

    c = get_test_cookie(item.url)
    if c: headers.append(['Cookie', c])


    data = scrapertools.cache_page(item.url, headers=headers)


    patron = '<h4 class="ei-item-title"><a href="([^"]+)">(.*?)</a></h4> '
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapedtitle.title()
        txt = "Serie Tv"
        if txt in scrapedtitle: continue
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))


    patronvideos = '<li class="next right"><a href="([^"]+)"[^>]+>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/return_home2_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

# ------------------------------------------------------------------------------------------------------------------------------------	
	
def peliculas_film(item):
    logger.info("streamondemand-pureita.filmperevolvere peliculas_film")
    itemlist = []

    c = get_test_cookie(item.url)
    if c: headers.append(['Cookie', c])

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="post-thumbnail">\s*<a href="([^"]+)" title="([^"]+)">\s*<img width="520"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapedtitle.title()
        txt = "Serie Tv"
        if txt in scrapedtitle: continue
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<li class="next right"><a href="([^"]+)"[^>]+>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/return_home2_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_film",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist
	
# ------------------------------------------------------------------------------------------------------------------------------------

def findvideos(item):
    logger.info("streamondemand-pureita.filmperevolvere findvideos")

    c = get_test_cookie(item.url)
    if c: headers.append(['Cookie', c])

    # Descarga la página
    data = scrapertools.cache_page(item.url, headers=headers)

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, '[COLOR green][B]', videoitem.title, '[/B][/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist

# ------------------------------------------------------------------------------------------------------------------------------------

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")

# ------------------------------------------------------------------------------------------------------------------------------------

def get_test_cookie(url):
    data = scrapertools.cache_page(url, headers=headers)
    a = scrapertools.find_single_match(data, 'a=toNumbers\("([^"]+)"\)')
    if a:
        b = scrapertools.find_single_match(data, 'b=toNumbers\("([^"]+)"\)')
        if b:
            c = scrapertools.find_single_match(data, 'c=toNumbers\("([^"]+)"\)')
            if c:
                cookie = aes.AESModeOfOperationCBC(a.decode('hex'), iv=b.decode('hex')).decrypt(c.decode('hex'))
                return '__test=%s' % cookie.encode('hex')
    return ''
