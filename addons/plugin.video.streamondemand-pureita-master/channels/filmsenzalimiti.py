# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-PureITA / XBMC Plugin
# Canale filmsenzalimiti
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re

from core import config, httptools
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod
from servers import servertools

__channel__ = "filmsenzalimiti"
__category__ = "F"
__type__ = "generic"
__title__ = "Film Senza Limiti (IT)"
__language__ = "IT"
__creationdate__ = "20120605"

DEBUG = config.get_setting("debug")

host = "http://www.filmsenzalimiti.black"


def isGeneric():
    return True


def mainlist(item):
    logger.info("[filmsenzalimiti.py] mainlist")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]Al Cinema[/COLOR]",
                     action="novedades",
                     extra="film",
                     url="%s//prime-visioni/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange][HD][/COLOR]",
                     action="novedades",
                     extra="film",
                     url="%s/?s=HD" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - [COLOR orange]A-Z[/COLOR]",
                     action="novedades",
                     extra="film",
                     url="%s/genere/film/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/all_movies_P.png"),
                Item(channel=__channel__,
                     action="search",
                     extra="film",
                     title="[COLOR yellow]Cerca Film...[/COLOR]",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV - [COLOR orange]A-Z[/COLOR]",
                     extra="serie",
                     action="novedades_tv",
                     url="%s/genere/serie-tv" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV - [COLOR orange]Aggiornate[/COLOR]",
                     extra="serie",
                     action="novedades_tv",
                     url="%s/aggiornamenti-serie-tv/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]
    return itemlist

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

def categorias(item):
    logger.info("[filmsenzalimiti.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data, '<h3 class="widget-title">Categorie</h3>(.*?)</ul>')
    patron = '<li><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="novedades",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True))

    return itemlist

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

def search(item, texto):
    logger.info("[filmsenzalimiti.py] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        if item.extra == "film":
            return novedades(item)
        if item.extra == "serie":
            return novedades_tv(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

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
                 contentType="film",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='film'))

    try:
        next_page = scrapertools.get_match(data, '<li><a href="([^"]+)" >Pagina successiva')
        itemlist.append(
            Item(channel=__channel__,
                 action="novedades",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 extra=item.extra,
                 folder=True))
    except:
        pass

    return itemlist

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
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
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 extra=item.extra,
                 folder=True))
    except:
        pass

    return itemlist

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

def episodios(item):
    def load_episodios(html, item, itemlist, lang_title):
        patron = '((?:.*?<a href="[^"]+" target="_blank" rel="noopener" rel="nofollow">[^<]+<\/a>)+)'
        matches = re.compile(patron).findall(html)
        for data in matches:
            # Extrae las entradas
            scrapedtitle = data.split('<a ')[0]
            scrapedtitle = re.sub(r'<[^>]*>', '', scrapedtitle).strip()
            if scrapedtitle != 'Categorie':
                itemlist.append(
                    Item(channel=__channel__,
                         action="findvideos",
                         title="[COLOR azure]%s[/COLOR]" % (scrapedtitle + " (" + lang_title + ")"),
                         url=data,
                         thumbnail=item.thumbnail,
                         extra=item.extra,
                         fulltitle=scrapedtitle + " (" + lang_title + ")" + ' - ' + item.show,
                         show=item.show))

    logger.info("[filmsenzalimiti.py] episodios")

    itemlist = []

    # Descarga la página
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
                 title=item.title,
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios" + "###" + item.extra,
                 show=item.show))
        itemlist.append(
            Item(channel=__channel__,
                 title="Scarica tutti gli episodi della serie",
                 url=item.url,
                 action="download_all_episodes",
                 extra="episodios" + "###" + item.extra,
                 show=item.show))

    return itemlist

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------	

def findvideos(item):
    logger.info("[filmsenzalimiti.py] findvideos")

    data = item.url if item.extra == 'serie' else httptools.downloadpage(item.url).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist
