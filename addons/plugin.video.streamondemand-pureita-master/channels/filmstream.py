# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale  http://film-stream.biz
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

__channel__ = "filmstream"
__category__ = "F"
__type__ = "generic"
__title__ = "Film-stream.org (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://film-stream.biz"


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.filmstream mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Ultimi Video Inseriti[/COLOR]",
                     extra="movie",
                     action="peliculas",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film Per Genere[/COLOR]",
                     extra="movie",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     extra="movie",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"),
                #Item(channel=__channel__,
                     #title="[COLOR azure]Serie TV[/COLOR]",
                     #extra="serie",
                     #action="peliculas_tv",
                     #url="%s/category/serie-tv/" % host,
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                #Item(channel=__channel__,
                     #title="[COLOR azure]Aggiornamento Serie TV[/COLOR]",
                     #extra="serie",
                     #action="aggiornamenti",
                     #url="%s/serietv/" % host,
                     #thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                #Item(channel=__channel__,
                     #title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     #action="search",
                     #extra="serie",
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]
    return itemlist


def categorias(item):
    logger.info("streamondemand.filmstream categorias")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data, '<ul class="mega-sub-menu">(.*?)</ul>')

    # The categories are the options for the combo
    patron = '<a class.*?href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = urlparse.urljoin(item.url, scrapedurl)
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedtitle = scrapedtitle.title()
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 extra=item.extra,
                 plot=scrapedplot))

    return itemlist


def search(item, texto):
    logger.info("[filmstream.py] " + item.url + " search " + texto)
    item.url = "%s/?s=%s&x=0&y=0" % (host, texto)
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



def aggiornamenti(item):
    logger.info("streamondemand.filmstream aggiornamenti")
    itemlist = []
    Day_List = []
    starts = []
    # Descarga la pagina
    data = scrapertools.cache_page("http://film-stream.cc/serietv/")

    # Extrae las entradas (carpetas)

    patron = '<span style="color: #ff6600;"><strong>[^<]+'
    matches = re.compile(patron, re.IGNORECASE).finditer(data)
    lista = list(matches)

    for match in lista:
        DAY = match.group(0)
        if DAY != '':
            matches = re.search('[^>]+$', DAY)
            DAY = matches.group(0)
            Day_List.append(DAY.upper())
            starts.append(match.end(0))

    i = 1
    len_Day_List = 10

    while i <= len_Day_List:
        inizio = starts[i - 1]
        fine = starts[i]

        html = data[inizio:fine]
        ToDay = Day_List[i - 1]

        itemlist.append(
            Item(channel=__channel__,
                 title="[COLOR yellow]" + ToDay + "[/COLOR]",
                 folder=True)),

        patron = '<p>[^<]{,10} <a href="http://film-stream.cc/[^<]+'
        matches = re.compile(patron, re.IGNORECASE).finditer(html)
        lista = list(matches)

        for match in lista:
            title = re.search('[^>]+$', match.group(0))
            title = scrapertools.decodeHtmlentities(title.group(0))
            link = re.search('"http://.*?"', match.group(0))

            if link is not None and title is not None:
                itemlist.append(infoSod(
                    Item(channel=__channel__,
                         action="episodios",
                         fulltitle=title,
                         show=title,
                         title="[COLOR azure]" + title + "[/COLOR]",
                         url=link.group(0)[1:-1],
                         extra=item.extra,
                         folder=True), tipo='tv'))
        i += 1
    return itemlist


def peliculas(item):
    logger.info("streamondemand.filmstream peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<div class="galleryitem".*?>\s*'
    patron += '<a href="?([^>"]+)"?.*?title="?([^>"]+)"?.*?<img.*?src="([^>"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl)
        start = html.find("</strong></p>")
        end = html.find("<p>&nbsp;</p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapedtitle.replace("Streaming", "")
        scrapedtitle = scrapedtitle.replace("(Serie Tv)", "{Serie Tv}")
        scrapedtitle = scrapedtitle.replace("(Serie TV)", "{Serie Tv}")
        scrapedtitle = scrapedtitle.replace("(Tv)", "{Tv}")
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("(Miniserie Tv)", "{Miniserie Tv}"))
        if scrapedtitle.startswith("Permanent Link to "):
            scrapedtitle = scrapedtitle[18:]
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
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

    # Extrae el paginador
    patronvideos = '<li><a href="([^"]+)">&gt;</a></li>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Home[/COLOR]",
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


def peliculas_tv(item):
    logger.info("streamondemand.filmstream peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<div class="galleryitem".*?>\s*'
    patron += '<a href="?([^>"]+)"?.*?title="?([^>"]+)"?.*?<img.*?src="([^>"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl)
        start = html.find("</strong></p>")
        end = html.find("<p>&nbsp;</p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapedtitle.replace("Streaming", "")
        scrapedtitle = scrapedtitle.replace("(Serie Tv)", "{Serie Tv}")
        scrapedtitle = scrapedtitle.replace("(Serie TV)", "{Serie Tv}")
        scrapedtitle = scrapedtitle.replace("(Tv)", "{Tv}")
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("(Miniserie Tv)", "{Miniserie Tv}"))
        if scrapedtitle.startswith("Permanent Link to "):
            scrapedtitle = scrapedtitle[18:]
        if (DEBUG): logger.info(
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
                 extra=item.extra,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = '<li><a href="([^"]+)">&gt;</a></li>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_tv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 extra=item.extra,
                 folder=True))

    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-main)")


def episodios(item):
    def load_episodios(html, item, itemlist, lang_title):
        patron = '(?:<strong>.*?<a href="[^"]+"[^_]+_blank[^>]+>[^<]+<\/a>[^>]+>.*?<\/strong>)'
        matches = re.compile(patron).findall(html)
        for data in matches:
            # Extrae las entradas
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

    logger.info("streamondemand.filmstream episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = scrapertools.decodeHtmlentities(data)
    data = scrapertools.get_match(data, '<div class="postcontent">(.*?)<div id="sidebar">')

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
        itemlist.append(
            Item(channel=__channel__,
                 title="Scarica tutti gli episodi della serie",
                 url=item.url,
                 action="download_all_episodes",
                 extra="episodios" + "###" + item.extra,
                 show=item.show))

    return itemlist


def findvideos(item):
    logger.info("streamondemand.filmstream findvideos")

    # Descarga la página
    data = item.url if item.extra == 'serie' else scrapertools.cache_page(item.url)

    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist
