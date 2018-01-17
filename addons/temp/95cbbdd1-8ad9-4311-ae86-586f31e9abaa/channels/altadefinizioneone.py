# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para altadefinizioneone
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import urlparse

from core import config, httptools
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "altadefinizioneone"

host = "http://www.altadefinizione.blog/"

headers = [['Referer', host]]


def mainlist(item):
    logger.info("streamondemand.altadefinizioneone mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Ultimi Film Inseriti[/COLOR]",
                     action="peliculas",
                     url="%s/novita-al-cinema/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film Per Categoria[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film per anno[/COLOR]",
                     action="byyear",
                     url=host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/Movie%20Year.png"),
                Item(channel=__channel__,
                     action="nazione",
                     title="[COLOR azure]Film Per Nazione[/COLOR]",
                     url=host,
                     thumbnail="http://i.imgur.com/RCkZdTz.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist

#disabled on global search

def newest(categoria):
    logger.info("[altadefinizioneone.py] newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "peliculas":
            item.url = "http://www.altadefinizione.blog/novita-al-cinema/"
            item.action = "peliculas"
            itemlist = peliculas(item)

            if itemlist[-1].action == "peliculas":
                itemlist.pop()

    # Se captura la excepción, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist

def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Narrow search by selecting only the in this list
    patron = '<div class="hidden-menu">(.*?)</div>'
    bloque = scrapertools.get_match(data, patron)

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for url, titulo in matches:
        scrapedtitle = titulo
        scrapedtitle = scrapedtitle.replace(" ", "")
        scrapedurl = urlparse.urljoin(item.url, url)
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot))

    return itemlist


def byyear(item):
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Narrow search by selecting only the in this list
    patron = '<a href="#" class="menu-link menu3">(.*?)</div>'
    bloque = scrapertools.get_match(data, patron)

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for url, titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url, url)
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot))

    return itemlist


def nazione(item):
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Narrow search by selecting only the in this list
    patron = '<a href="#" class="menu-link menu4">(.*?)</div>'
    bloque = scrapertools.get_match(data, patron)

    # Extrae las entradas (carpetas)
    patron = '<a[^h]+href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for url, titulo in matches:
        scrapedtitle = titulo
        scrapedtitle = scrapedtitle.replace(" ", "")
        scrapedurl = urlparse.urljoin(item.url, url)
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot))

    return itemlist


def search(item, texto):
    logger.info("[altadefinizioneone.py] " + item.url + " search " + texto)
    item.url = "%s/index.php?story=%s&do=search&subaction=search" % (host, texto)
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def peliculas(item):
    logger.info("streamondemand.altadefinizioneone peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<div class="tcarusel-item-title">\s*<a href="([^"]+)">(.*?)</a>\s*</div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">Avanti'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand/)")

