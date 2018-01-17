# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale streamiblog
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import sys
import urlparse

from core import config, httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "streamblog"
__category__ = "F"
__type__ = "generic"
__title__ = "streamblog (IT)"
__language__ = "IT"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:39.0) Gecko/20100101 Firefox/39.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Connection', 'keep-alive']
]

DEBUG = config.get_setting("debug")

host = "https://www.streamblog.me/"


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.streamblog mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Novita'[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     extra="serie",
                     action="peliculas_tv",
                     url="%s/serie-tv/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Animazione[/COLOR]",
                     action="peliculas",
                     url="%s/animazione/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animated_movie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist


def categorias(item):
    logger.info("streamondemand.streamblog categorias")
    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)
    logger.info(data)

    # Narrow search by selecting only the combo
    patron = '<li class="drop"><a href="#" class="navlink">(.*?)<div class="bl_search">'
    bloque = scrapertools.get_match(data, patron)

    # The categories are the options for the combo
    patron = '<li><a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for url, titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url, url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 plot=scrapedplot))

    return itemlist


def search(item, texto):
    logger.info("[streamblog.py] " + item.url + " search " + texto)
    item.url = "%s/index.php?story=%s&do=search&subaction=search" % (host, texto)
    try:
        return results(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def results(item):
    logger.info("streamondemand.streamblog results")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '.*?<h2><a href="([^"]+)">(.*?)</a></h2>\s*'
    patron += '</div>\s*'
    patron += '<.*?img src="([^"]+)".*?/>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl, headers=headers)
        start = html.find("<div class=\"fstory_descr clear decor\">")
        end = html.find("<div class=\"fstory_treyler decor\">", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        # scrapedplot = ""
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="episodios" if item.extra == "serie" else "findvideos",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=host + scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True,
                 fanart=host + scrapedthumbnail))

    # Extrae el paginador
    patronvideos = '<div class="navigation".*?<span.*?/span>.*?<a href="([^"]+)">'
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
                 action="results",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

def peliculas(item):
    logger.info("streamondemand.streamblog peliculas")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = '<div class="blvideo">\s*<div class="poster"><a href="([^"]+)"><img src="([^"]+)" alt="(.*?)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedthumbnail = host + scrapedthumbnail
        scrapedplot = ""
        scrapetrailar = " Trailer"

        # Bypass fake links
        html = httptools.downloadpage(scrapedurl).data

        patron = '<div class="video-player-plugin">([\s\S]*)<div class="wrapper-plugin-video">'
        matches = re.compile(patron, re.DOTALL).findall(html)

        for url in matches:
            if "scrolling" in url:
                scrapedurl = scrapedurl
            else:
                scrapedtitle = scrapedtitle + scrapetrailar

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

    # Paginazione 
    patronvideos = '<div class="navigation">[^n]+n>[^<]+<\/span>[^<]+<a href="(.*?)">'
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

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")

def peliculas_tv(item):
    logger.info("streamondemand.streamblog peliculas")
    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = '<div class="blvideo">\s*<div class="poster"><a href="([^"]+)"[^<]+<img src="([^"]+)" alt="(.*?)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = host + scrapedthumbnail

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

    # Paginazione 
    patronvideos = '<div class="navigation">[^n]+n>[^<]+<\/span>[^<]+<a href="(.*?)">'
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
    def load_episodios(html, item, itemlist, lang_title):
        for data in scrapertools.decodeHtmlentities(html).split('<br />'):
            # Extrae las entradas
            end = data.find('<a ')
            if end > 0:
                scrapedtitle = re.sub(r'<[^>]*>', '', data[:end]).strip()
            else:
                scrapedtitle = ''
            title = scrapertools.find_single_match(scrapedtitle, '\d+[^\d]+\d+')
            if title == '':
                title = scrapedtitle
            if title != '':
                itemlist.append(
                    Item(channel=__channel__,
                         action="findvid_serie",
                         title=title + " (" + lang_title + ")",
                         url=item.url,
                         thumbnail=item.thumbnail,
                         extra=data,
                         fulltitle=item.fulltitle,
                         show=item.show))

    logger.info("streamondemand.streamblog episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)

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


def findvid_serie(item):
    logger.info("streamondemand.streamblog findvideos")

    # Descarga la página
    data = item.extra

    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist
