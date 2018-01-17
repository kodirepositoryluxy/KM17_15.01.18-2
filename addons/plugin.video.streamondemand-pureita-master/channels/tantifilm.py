# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para piratestreaming
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod
from core import servertools

__channel__ = "tantifilm"
__category__ = "F"
__type__ = "generic"
__title__ = "Tantifilm.net (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.tantifilm.uno"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]

def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.tantifilm mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Categorie[/COLOR]",
                     action="categorias",
                     url=host+"/watch-genre/3d/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Al Cinema[/COLOR]",
                     action="peliculas",
                     url="%s/watch-genre/al-cinema/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),                     
                Item(channel=__channel__,
                     title="[COLOR azure]HD - Alta Definizione[/COLOR]",
                     action="peliculas",
                     url="%s/watch-genre/altadefinizione/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png"),
                Item(channel=__channel__,	 
                     title="[COLOR azure]Film - 3D[/COLOR]",
                     action="peliculas",
                     url=host+"/watch-genre/3d/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_3D_P.png"),
                Item(channel=__channel__,	 
                     title="[COLOR azure]Film - Raccomandati[/COLOR]",
                     action="peliculas",
                     url=host+"/watch-genre/featured/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png"),
               Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     extra="serie",
                     action="peliculas_tv",
                     url="%s/watch-genre/series-tv-featured/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV - Altadefinizione[/COLOR]",
                     extra="serie",
                     action="peliculas_tv",
                     url="%s/watch-genre/serie-altadefinizione/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist


def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.get_match(data,'<select class="select_join" onchange="location.href = this.value" size="1" name="linkIole2">(.*?)</select>')

    # Extrae las entradas (carpetas)
    patron = r'<option[^>]+><a href=\'([^\']+)\'>(.*?)</a></option>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist


def search(item, texto):
    logger.info("[tantifilm.py] " + item.url + " search " + texto)
    item.url = "%s/?s=%s" % (host, texto)

    try:
        if item.extra == "serie":
            return search_peliculas_tv(item)
        else:
            return search_peliculas(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def search_peliculas(item):
    logger.info("streamondemand.tantifilm search_peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)" title="([^"]+)" rel="[^"]+">\s*<img width="[^"]+" height="[^"]+" src="([^"]+)" class="[^"]+" alt="[^"]+" srcset="[^"]+" sizes="[^"]+" />'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl, headers=headers)
        start = html.find("<div class=\"content-left-film\">")
        end = html.find("</div>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.replace("streaming", "").replace("Permalink to ", "")
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="episodios" if item.extra == "serie" else "findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    return itemlist


def search_peliculas_tv(item):
    logger.info("streamondemand.tantifilm search_peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)" title="([^"]+)" rel="[^"]+">\s*<img width="[^"]+" height="[^"]+" src="([^"]+)" class="[^"]+" alt="[^"]+" srcset="[^"]+" sizes="[^"]+" />'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl, headers=headers)
        start = html.find("<div class=\"content-left-film\">")
        end = html.find("</div>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.replace("streaming", "").replace("Permalink to ", "")
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="episodios" if item.extra == "serie" else "findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    return itemlist


def peliculas(item):
    logger.info("streamondemand.tantifilm peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="media3">[^>]+><a href="([^"]+)"><img[^s]+src="([^"]+)"[^>]+></a><[^>]+><a[^>]+><p>(.*?)</p></a></div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        html = scrapertools.cache_page(scrapedurl, headers=headers)
        start = html.find("<div class=\"content-left-film\">")
        end = html.find("</div>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.replace("streaming", "")
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios" if item.extra == "serie" else "findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a class="nextpostslink" rel="next" href="([^"]+)">»</a>'
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
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 folder=True))

    return itemlist


def peliculas_tv(item):
    logger.info("streamondemand.tantifilm peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="media3">[^>]+><a href="([^"]+)"><img[^s]+src="([^"]+)"[^>]+></a><[^>]+><a[^>]+><p>(.*?)</p></a></div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        html = scrapertools.cache_page(scrapedurl, headers=headers)
        start = html.find("<div class=\"content-left-film\">")
        end = html.find("</div>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.replace("streaming", "")
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios" if item.extra == "serie" else "findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = '<a class="nextpostslink" rel="next" href="([^"]+)">»</a>'
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
                 action="peliculas_tv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 folder=True))

    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")


def latest(item):
    logger.info("streamondemand.tantifilm peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="mediaWrap mediaWrapAlt">\s*'
    patron += '<a href="([^"]+)" title="([^"]+)" rel="bookmark">\s*'
    patron += '<img[^s]+src="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl, headers=headers)
        start = html.find("<div class=\"content-left-film\">")
        end = html.find("</div>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.replace("Permalink to ", "")
        scrapedtitle = scrapedtitle.replace("streaming", "")
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
    patronvideos = '<a class="nextpostslink" rel="next" href="([^"]+)">»</a>'
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
                 action="latest",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 folder=True))

    return itemlist


def episodios(item):
    def load_episodios(html, item, itemlist):
        for data in html.splitlines():
            # Extrae las entradas
            end = data.find('<a ')
            if end > 0:
                scrapedtitle = re.sub(r'<[^>]*>', '', data[:end]).strip()
            else:
                scrapedtitle = ''
            if scrapedtitle == '':
                patron = '<a\s*href="[^"]+"(?:\s*target="_blank")?>([^<]+)</a>'
                scrapedtitle = scrapertools.find_single_match(data, patron).strip()
            title = scrapertools.find_single_match(scrapedtitle, '\d+[^\d]+\d+')
            if title == '':
                title = scrapedtitle
            if title != '':
                itemlist.append(
                    Item(channel=__channel__,
                         action="findvideos",
                         title=title,
                         url=item.url,
                         thumbnail=item.thumbnail,
                         extra=data,
                         fulltitle=item.fulltitle,
                         show=item.show))

    logger.info("streamondemand.tantifilm episodios")

    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)
    data = scrapertools.decodeHtmlentities(data)

    start = data.find('<div class="sp-wrap sp-wrap-blue">')
    end = data.find('<div id="disqus_thread">', start)

    data_sub = data[start:end]

    starts = []
    patron = r".*?STAGIONE|MINISERIE|WEBSERIE|SERIE"
    matches = re.compile(patron, re.IGNORECASE).finditer(data_sub)
    for match in matches:
        season_title = match.group()
        if season_title != '':
            starts.append(match.end())

    i = 1
    len_starts = len(starts)

    while i <= len_starts:
        inizio = starts[i - 1]
        fine = starts[i] if i < len_starts else -1

        html = data_sub[inizio:fine]

        load_episodios(html, item, itemlist)

        i += 1

    if len(itemlist) == 0:
        patron = '<a href="(#wpwm-tabs-\d+)">([^<]+)</a></li>'
        seasons_episodes = re.compile(patron, re.DOTALL).findall(data)

        end = None
        for scrapedtag, scrapedtitle in seasons_episodes:
            start = data.find(scrapedtag, end)
            end = data.find('<div class="clearfix"></div>', start)
            html = data[start:end]

            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     title=scrapedtitle,
                     url=item.url,
                     thumbnail=item.thumbnail,
                     extra=html,
                     fulltitle=item.fulltitle,
                     show=item.show))

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


def findvideos(item):
    logger.info("streamondemand.tantifilm findvideos")

    # Descarga la página
    data = item.extra if item.extra != '' else scrapertools.cache_page(item.url, headers=headers)

    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    # Extrae las entradas
    patron = r'\{"file":"([^"]+)","type":"[^"]+","label":"([^"]+)"\}'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle in matches:
        title = item.title + " " + scrapedtitle + " quality"
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title=title,
                 url=scrapedurl.replace(r'\/', '/').replace('%3B', ';'),
                 thumbnail=item.thumbnail,
                 fulltitle=item.title,
                 show=item.title,
                 server='',
                 folder=False))

    return itemlist
