# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale filmsenzalimiti
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re

from core import config, httptools
from platformcode import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmsenzalimiti"

host = "http://filmsenzalimiti.black"


def mainlist(item):
    logger.info("[filmsenzalimiti.py] mainlist")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film Del Cinema[/COLOR]",
                     action="novedades",
                     extra="movie",
                     url="%s/genere/film" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film HD[/COLOR]",
                     action="novedades",
                     extra="movie",
                     url="%s/?s=[HD]" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Categorie[/COLOR]",
                     action="categorias",
                     url="%s/genere/film" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     action="search",
                     extra="movie",
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     extra="serie",
                     action="novedades_tv",
                     url="%s/genere/serie-tv" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]
    return itemlist


def newest(categoria):
    logger.info("[filmsenzalimiti.py] newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "peliculas":
            item.url = host + "/genere/film"
            item.action = "novedades"
            itemlist = novedades(item)

            if itemlist[-1].action == "novedades":
                itemlist.pop()

    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist


def categorias(item):
    logger.info("[filmsenzalimiti.py] novedades")
    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data
    data = scrapertools.get_match(data, '<h3 class="widget-title">Categorie</h3>(.*?)</ul>')
    patron = '<li><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        if scrapedtitle.startswith(("PRIME")):
            continue
        if scrapedtitle.startswith(("ULTIME")):
            continue
        itemlist.append(
            Item(channel=__channel__,
                 action="novedades",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=host + scrapedurl,
                 thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png",
                 extra=item.extra,
                 folder=True))

    return itemlist


def search(item, texto):
    logger.info("[filmsenzalimiti.py] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        if item.extra == "movie":
            return novedades(item)
        if item.extra == "serie":
            return novedades_tv(item)
    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def novedades(item):
    logger.info("[filmsenzalimiti.py] novedades")
    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data

    patronvideos = '<li><a href="([^"]+)" data-thumbnail="([^"]+)"><div>\s*<div class="title">(.*?)<\/div>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
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
                 extra=item.extra,
                 folder=True), tipo='movie'))

    try:
        next_page = scrapertools.get_match(data, '<li><a href="([^"]+)" >Pagina successiva')
        itemlist.append(
            Item(channel=__channel__,
                 action="novedades",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 extra=item.extra,
                 folder=True))
    except:
        pass

    return itemlist


def novedades_tv(item):
    logger.info("[filmsenzalimiti.py] novedades")
    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data

    patronvideos = '<li><a href="([^"]+)" data-thumbnail="([^"]+)"><div>\s*<div class="title">(.*?)<\/div>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='tv'))

    try:
        next_page = scrapertools.get_match(data, '<li><a href="([^"]+)" >Pagina successiva')
        itemlist.append(
            Item(channel=__channel__,
                 action="novedades_tv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 extra=item.extra,
                 folder=True))
    except:
        pass

    return itemlist


def episodios(item):
    def load_episodios(html, item, itemlist, lang_title):
        patron = '((?:.*?<a href="[^"]+" target="_blank" rel="noopener" rel="nofollow">[^<]+<\/a>)+)'
        matches = re.compile(patron).findall(html)
        for data in matches:
            # Estrae i contenuti 
            scrapedtitle = data.split('<a ')[0]
            scrapedtitle = re.sub(r'<[^>]*>', '', scrapedtitle).strip()
            if scrapedtitle != 'Categorie':
                scrapedtitle = scrapedtitle.replace('×', 'x')
                itemlist.append(
                    Item(channel=__channel__,
                         action="findvideos",
                         contentType="episode",
                         title="[COLOR azure]%s[/COLOR]" % (scrapedtitle + " (" + lang_title + ")"),
                         url=data,
                         thumbnail=item.thumbnail,
                         extra=item.extra,
                         fulltitle=scrapedtitle + " (" + lang_title + ")" + ' - ' + item.show,
                         show=item.show))

    logger.info("[filmsenzalimiti.py] episodios")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data
    data = scrapertools.decodeHtmlentities(data)

    lang_titles = []
    starts = []
    patron = r"STAGIONE.*?ITA"
    matches = re.compile(patron, re.IGNORECASE).finditer(data)
    for match in matches:
        season_title = match.group()
        if season_title != '':
            lang_titles.append('SUB ITA' if 'SUB' in season_title.upper() else 'ITA')
            starts.append(match.end())

    i = 1
    len_lang_titles = len(lang_titles)

    while i <= len_lang_titles:
        inizio = starts[i - 1]
        fine = starts[i] if i < len_lang_titles else -1

        html = data[inizio:fine]
        lang_title = lang_titles[i - 1]

        load_episodios(html, item, itemlist, lang_title)

        i += 1

    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title="Aggiungi alla libreria",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios" + "###" + item.extra,
                 show=item.show))

    return itemlist


def findvideos(item):
    logger.info("[filmsenzalimiti.py] findvideos")

    # Carica la pagina 
    data = item.url if item.extra == 'serie' else httptools.downloadpage(item.url).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title).capitalize()
        videoitem.title = "".join(["[%s] " % color(server, 'orange'), item.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist

def color(text, color):
    return "[COLOR " + color + "]" + text + "[/COLOR]"

