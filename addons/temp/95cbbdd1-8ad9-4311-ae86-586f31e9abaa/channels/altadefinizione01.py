# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para altadefinizione01
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import urlparse

from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "altadefinizione01"

host = "http://www.altadefinizione01.one"

headers = [['Referer', host]]


def mainlist(item):
    logger.info("streamondemand.altadefinizione01 mainlist")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Ultimi film inseriti[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film Sub-Ita[/COLOR]",
                     action="peliculas",
                     url="%s/film-sub-ita/" % host,
                     thumbnail="http://i.imgur.com/qUENzxl.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Categorie film[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie-TV[/COLOR]",
                     action="peliculas_tv",
                     url="%s/serie-tv-streaming/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie-TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist


def newest(categoria):
    logger.info("streamondemand.altadefinizione01 newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "peliculas":
            item.url = host
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


def peliculas_tv(item):
    logger.info("streamondemand.altadefinizionezone peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<section class="main">(.*?)</section>'
    data = scrapertools.find_single_match(data, patron)

    # Extrae las entradas (carpetas)
    patron = '<h2 class="titleFilm"><a href="([^"]+)">(.*?)</a></h2>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="seasons",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = '<span>.*?</span>.*?href="(.*?)">'
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
                 action="peliculas_tv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist


def seasons(item):
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<li><a href="([^"]+)" data-toggle="tab">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedseason in matches:
        scrapedurl = item.url + scrapedurl
        scrapedtitle = item.title

        itemlist.append(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]" + " " + "Stagione " + scrapedseason,
                 url=scrapedurl,
                 thumbnail=item.scrapedthumbnail,
                 plot=item.scrapedplot,
                 folder=True))

    return itemlist


def episodios(item):
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = 'class="tab-pane fade" id="%s">(.*?)class="tab-pane fade"' % item.url.split('#')[1]
    bloque = scrapertools.find_single_match(data, patron)
    patron = 'class="text-muted">.*?<[^>]+>(.*?)<[^>]+>[^>]+>[^>][^>]+>[^<]+<a href="#" class="slink" id="megadrive-(.*?)" data-link="(.*?)"'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedtitle, scrapedepi, scrapedurl in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedepi = scrapedepi.split('_')[0] + "x" + scrapedepi.split('_')[1].zfill(2)
        scrapedtitle = scrapedepi + scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos_tv",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    return itemlist


def findvideos_tv(item):

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, '[COLOR green][B]' + videoitem.title + '[/B][/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist


def peliculas(item):
    logger.info("streamondemand.altadefinizione01 peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    start = data.find('<div id="dle-content">')
    end = data.find('<div class="row" id="preFooter">', start)
    bloque = data[start:end]

    # Extrae las entradas (carpetas)
    patron = r'<a href="([^"]+)"><img src="([^"]+)".*?alt="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("Streaming", ""))
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail), tipo="movie"))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">Avanti →</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(bloque)

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


def categorias(item):
    logger.info("streamondemand.altadefinizione01 categorias")
    itemlist = []

    # data = scrapertools.cache_page(item.url)
    data = httptools.downloadpage(item.url, headers=headers).data

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data, '<ul class="listSubCat" id="Film">(.*?)</ul>')

    # The categories are the options for the combo
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
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


def search(item, texto):
    logger.info("[altadefinizione01.py] " + item.url + " search " + texto)
    item.url = "%s/index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s" % (
        host, texto)
    try:
        if item.extra == "movie":
            return peliculas(item)
        if item.extra == "serie":
            return peliculas_tv(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def findvideos(item):
    logger.info("[altadefinizione01.py] findvideos")

    # Descarga la página
    data = httptools.downloadpage(item.url, headers=headers).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, '[COLOR green][B]' + videoitem.title + '[/B][/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
