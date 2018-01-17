# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale filmstream_biz
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import base64
import re
import urlparse


from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmstream_biz"

host = "http://filmstream.biz/"

headers = [
    ['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'],
    ['Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host],
    ['Cache-Control', 'max-age=0']
]


def isGeneric():
    return True

# ==============================================================================================================================================

def mainlist(item):
    logger.info("[pureita filmstream_biz] mainlist")

    itemlist = [
        Item(channel=__channel__,
             title="[COLOR azure]Film - [COLOR orange]Top 10[/COLOR]",
             action="top_10",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film - [COLOR orange]Per Genere[/COLOR]",
             action="genere",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film - [COLOR orange]Novita'[/COLOR]",
             action="peliculas",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film - [COLOR orange]Richiesti[/COLOR]",
             action="peliculas_new",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movies_P.png"),
        Item(channel=__channel__,
             title="[COLOR orange]Cerca...[/COLOR]",
             action="search",
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================

def search(item, texto):
    logger.info("[pureita filmstream_biz] " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return peliculas(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================		
		
def genere(item):
    logger.info("[pureita filmstream_biz] genere")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    patron = '<h3>CATEGORIE</h3>(.*?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li id=".*?" class=".*?"><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================

def top_10(item):
    logger.info("[pureita filmstream_biz] top_10")

    itemlist = []
	
    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
	
    patron = '<a href="([^"]+)"\s*class="tptn_link"><img src="([^"]+)" alt="[^>]+" title="([^<]+)" width[^>]+class=[^>]+>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle  in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        # ------------------------------------------------
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        # ------------------------------------------------
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='movie'))


    return itemlist

# ==============================================================================================================================================================================

def peliculas(item):
    logger.info("[pureita filmstream_biz] peliculas")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
	
	
    patron = '<header class="entry-header no-anim" data-url="(.*?\/(.*?))\/">\s*<img width=".*?" height=".*?" src="([^<]+)" class[^>]+>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if "serie-tv" in scrapedtitle:
		    continue
        scrapedtitle = scrapedtitle.replace("/", "")
        scrapedtitle = scrapedtitle.replace("filmstream.biz", "")
        scrapedtitle = scrapedtitle.replace("film-completo-online", "")
        scrapedtitle = scrapedtitle.replace("film-completi", "")
        scrapedtitle = scrapedtitle.replace("-streaming", "")
        scrapedtitle = scrapedtitle.replace("film-stream-biz", "")
        scrapedtitle = scrapedtitle.replace("film-altadefinizione", "")
        scrapedtitle = scrapedtitle.replace("alta-definizione", "")
        scrapedtitle = scrapedtitle.replace("online", "")
        scrapedtitle = scrapedtitle.replace("film", "")
        scrapedtitle = scrapedtitle.replace("gratis", "")
        scrapedtitle = scrapedtitle.replace("guarda-il", "")
        scrapedtitle = scrapedtitle.replace("stream", "")
        scrapedtitle = scrapedtitle.replace("netflix", "")
        scrapedtitle = scrapedtitle.replace("openload", "")
        scrapedtitle = scrapedtitle.replace("gratis-", "")
        scrapedtitle = scrapedtitle.replace("-hd", " [HD]")
        scrapedtitle = scrapedtitle.replace("-", " ")
        scrapedtitle = scrapedtitle.capitalize()

        # ------------------------------------------------
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        # ------------------------------------------------
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='movie'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<div class="nav-previous"><a href="([^"]+)" >Older posts</a></div>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist



	
# ==============================================================================================================================================================================

def peliculas_new(item):
    logger.info("[pureita filmstream_biz] peliculas_new")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<div class="nav-menu"></div>(.*?)<br /></div>')
	
	
    patron = '<header class="entry-header no-anim" data-url="(.*?\/(.*?))\/">\s*<img width=".*?" height=".*?" src="([^<]+)" class[^>]+>'

    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if "serie-tv" in scrapedtitle:
		    continue
        scrapedtitle = scrapedtitle.replace("/", "")
        scrapedtitle = scrapedtitle.replace("filmstream.biz", "")
        scrapedtitle = scrapedtitle.replace("film-completo-online", "")
        scrapedtitle = scrapedtitle.replace("film-completi", "")
        scrapedtitle = scrapedtitle.replace("-streaming", "")
        scrapedtitle = scrapedtitle.replace("film-stream-biz", "")
        scrapedtitle = scrapedtitle.replace("film-altadefinizione", "")
        scrapedtitle = scrapedtitle.replace("alta-definizione", "")
        scrapedtitle = scrapedtitle.replace("online", "")
        scrapedtitle = scrapedtitle.replace("film", "")
        scrapedtitle = scrapedtitle.replace("gratis", "")
        scrapedtitle = scrapedtitle.replace("guarda-il", "")
        scrapedtitle = scrapedtitle.replace("stream", "")
        scrapedtitle = scrapedtitle.replace("netflix", "")
        scrapedtitle = scrapedtitle.replace("openload", "")
        scrapedtitle = scrapedtitle.replace("gratis-", "")
        scrapedtitle = scrapedtitle.replace("-hd", " [HD]")
        scrapedtitle = scrapedtitle.replace("-", " ")
        scrapedtitle = scrapedtitle.capitalize()


        # ------------------------------------------------
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        # ------------------------------------------------
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='movie'))


    return itemlist	




