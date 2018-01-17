# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale  streaminglove
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "streaminglove"
__category__ = "F,S,A"
__type__ = "generic"
__title__ = "streaminglove (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://streaminglove.tv"

headers = [
    ['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'],
    ['Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host],
    ['Cache-Control', 'max-age=0']
]

def isGeneric():
    return True


def mainlist(item):
    logger.info("pureita.streaminglove mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Ultimi Film Inseriti[/COLOR]",
                     action="peliculas",
                     url="%s/film/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film al Cinema[/COLOR]",
                     action="peliculas",
                     url="%s/genere/cinema/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film Per Categoria[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Film Sub Ita[/COLOR]",
                     action="peliculas",
                     url="%s/genere/sub-ita/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_sub_P.png"),               
               Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     action="serie",
                     url="%s/serietv/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
               Item(channel=__channel__,
                     title="[COLOR azure]Animazione[/COLOR]",
                     action="peliculas",
                     url="%s/genere/animazione/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_P.png"),
               Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist



def categorias(item):
    logger.info("pureita.streaminglove categorias")
    itemlist = []

    
    data = scrapertools.anti_cloudflare(item.url, headers)
    bloque = scrapertools.get_match(data, '<ul class="genres scrolling">.*?</ul>')

    
    patron = '</li>\s*<li class="[^>]+"><a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        logger.info("title=[" + scrapedtitle + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

def search(item, texto):
    logger.info("[streaminglove.py] " + item.url + " search " + texto)
    item.url = "http://www.streaminglove.tv/?s=" + texto

    try:
        return peliculas_src(item)

    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)

    return []

def peliculas_src(item):
    logger.info("pureita.streaminglove peliculas")
    itemlist = []

    
    data = scrapertools.anti_cloudflare(item.url, headers)

    patron = '<div class="thumbnail animation-2">\s*<a href="(.*?)">\s*<img src="(.*?)" alt="(.*?)" />\s*[^>]+>\s*(.*?) </span>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedtipo in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")

        if scrapedtipo=="TV":
            itemlist.append(infoSod(
                Item(channel=__channel__,
                     action="episodios",
                     fulltitle=scrapedtitle,
                     show=scrapedtitle,
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     folder=True), tipo='tv'))
        else:
            itemlist.append(infoSod(
                Item(channel=__channel__,
                     action="findvideos",
                     fulltitle=scrapedtitle,
                     show=scrapedtitle,
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     folder=True), tipo='movie'))

    return itemlist

def peliculas(item):
    logger.info("pureita.streaminglove peliculas")
    itemlist = []

    
    data = scrapertools.anti_cloudflare(item.url, headers)

    
    patron = '<a href="([^"]+)"><div class="see"></div></a>\s*</div>\s*<div class="data">\s*<h3>\s*'
    patron +='[^>]+></span>\s*<a href="(.*?)">([^"]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
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

    
    patronvideos = '<a href="([^"]+)"><span class="icon-chevron-right"></span></a>'
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
                 folder=True))

    return itemlist

def serie(item):
    logger.info("pureita.streaminglove peliculas")
    itemlist = []

    
    data = scrapertools.anti_cloudflare(item.url, headers)

    
    patron = '<a href="([^"]+)"><div class="see"></div></a>\s*</div>\s*<div class="data">\s*<h3>\s*<a href="(.*?)">([^"]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

   
    patronvideos = '<a href="([^"]+)"><span class="icon-chevron-right"></span></a>'
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
                 folder=True))

    return itemlist

def episodios(item):
    logger.info("pureita.streaminglove episodios")
    itemlist = []


    patron='<ul class="episodios">([^+]+)</ul>'

    data = scrapertools.anti_cloudflare(item.url, headers)
    matches = re.compile(patron, re.DOTALL).findall(data)

    for match in matches:

        patron='<li>\s*<div class="imagen"><a href="(.*?)">[^>]+>[^>]+>[^>]+>\s*<.*?numerando">(.*?)<[^>]+>[^>]+>[^>]+>(.*?)</a>'
        episodi = re.compile(patron, re.DOTALL).findall(match)

        for scrapedurl,scrapednumber,scrapedtitle in episodi:
            n0 = scrapednumber.replace(" ","")
            n1 = n0.replace("-","x")

            itemlist.append(Item(channel=__channel__,
                                 action="findvideos",
                                 fulltitle=n1 + " " + scrapedtitle,
                                 show=n1 + " " + scrapedtitle,
                                 title= n1 + " [COLOR orange] " + scrapedtitle + "[/COLOR]",
                                 url=scrapedurl,
                                 thumbnail=item.thumbnail,
                                 plot=item.plot,
                                 folder=True))

    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title=item.title + " [COLOR yellow] Aggiungi alla libreria [/COLOR]",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios",
                 show=item.show))
        itemlist.append(
            Item(channel=item.channel,
                 title="Scarica tutti gli episodi della serie",
                 url=item.url,
                 action="download_all_episodes",
                 extra="episodios",
                 show=item.show))

    return itemlist


def findvideos(item):
    logger.info("[streaminglove.py] play")

    data = scrapertools.anti_cloudflare(item.url, headers)

    patron = '<td><a class="link_a" href="(.*?)" target="_blank">'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for url in matches:
        html = scrapertools.cache_page(url, headers=headers)
        data += str(scrapertools.find_multiple_matches(html, 'window.location.href=\'(.*?)\''))

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")
