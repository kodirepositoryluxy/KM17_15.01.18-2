# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale mondolunatico_new
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import httptools, logger, scrapertools, servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "mondolunatico_new"

host = "http://mondolunatico.org"

PERPAGE = 14

def mainlist(item):
    logger.info("streamondemand-pureita.mondolunatico_new mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film -[COLOR orange]Novita[/COLOR]",
                     action="peliculas",
                     url="%s/stream/movies/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film -[COLOR orange]Categorie[/COLOR]",
                     action="categorias",
                     url="%s/stream/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film -[COLOR orange]Anno[/COLOR]",
                     action="years",
                     url="%s/stream/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film -[COLOR orange]Attori[/COLOR]",
                     action="actors",
                     url="%s/stream/lista-registi-filmografie/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_directors_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist


# ==============================================================================================================================================================================
	
def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, '<h2>Film Per Genere</h2>(.*?)</li></ul></nav></div>')

    # Extrae las entradas
    patron = '<li[^>]+><a href="([^"]+)"[^>]>(.*?)<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
         
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================
	
def years(item):
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, '<h2>Release year</h2>(.*?)</li></ul></nav></div>')

    # Extrae las entradas 
    patron = '<li><a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
         
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================
	
def actors(item):
    itemlist = []

	
   # Descarga la pagina
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, '</strong></span></p><p><strong>(.*?)</ul></div></div></strong></p>')

   # Extrae las entradas 
    patron = '<li class="[^>]+"><a href="([^"]+)">(.*?)<\/a><\/li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
         
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_directors_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================


def search(item, texto):
    logger.info("[streamondemand-pureita.mondolunatico_new] " + item.url + " search " + texto)
    item.url = host + "/stream?s=" + texto
    try:
        if item.extra == "movie":
            return pelis_movie_src(item)
    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================================================
		
def pelis_movie_src(item):
    logger.info("streamondemand-pureita.mondolunatico_new peliculas")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data

    # Estrae i contenuti 
    patron = '<div class="thumbnail animation-2">\s*<a href="([^"]+)">\s*<img src="([^"]+)" alt="(.*?)" />'
    matches = re.compile(patron, re.DOTALL).findall(data)

    scrapedplot = ""
    for scrapedurl, scrapedthumbnail, scrapedtitle, in matches:
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 contentType="movie",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    return itemlist

# ==============================================================================================================================================================================

def peliculas(item):
    logger.info("streamondemand-pureita.mondolunatico_new peliculas")

    itemlist = []

    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data

    # Estrae i contenuti 
    patron = '</span><a href="([^"]+)">(.*?)</a></h3>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    scrapedplot = ""
    for i, (scrapedurl, scrapedtitle) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedthumbnail = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 contentType="movie",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))
				 


    # Paginazione 
    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================================================	
	
def findvideos_x(item):
    logger.info("streamondemand-pureita.mondolunatico_new findvideos")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = 'src="([^"]+)" frameborder="0"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl in matches:
        if "dir?" in scrapedurl:
            data += httptools.downloadpage(scrapedurl).url
        else:
            data += httptools.downloadpage(scrapedurl).data

    for videoitem in servertools.find_video_items(data=data):
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__
        itemlist.append(videoitem)

    return itemlist
