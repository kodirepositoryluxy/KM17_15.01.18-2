# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale casacinema
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import re
import urlparse

from core import config, httptools
from platformcode import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "casacinema"

host = 'http://www.casacinema.video'

headers = [['Referer', '%s/genere/serie-tv' % host]]


def mainlist(item):
    logger.info("streamondemand.casacinema mainlist")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film - Novita'[/COLOR]",
                     action="peliculas",
                     extra="movie",
                     url="%s/genere/film" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film - HD[/COLOR]",
                     action="peliculas",
                     extra="movie",
                     url="%s/?s=[HD]" % host,
                     thumbnail="http://jcrent.com/apple%20tv%20final/HD.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Categorie[/COLOR]",
                     action="categorias",
                     extra="movie",
                     url="%s/genere/film" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film Sub - Ita[/COLOR]",
                     action="peliculas",
                     extra="movie",
                     url="%s/genere/sub-ita" % host,
                     thumbnail="http://i.imgur.com/qUENzxl.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     extra="serie",
                     action="peliculas_tv",
                     url="%s/genere/serie-tv" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist


def newest(categoria):
    logger.info("[casacinema.py] newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "peliculas":
            item.url = host + '/genere/film'
            item.extra = "movie"
            item.action = "peliculas"
            itemlist = peliculas(item)

            if itemlist[-1].action == "peliculas":
                itemlist.pop()

    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist


def search(item, texto):
    logger.info("[casacinema.py] " + item.url + " search " + texto)

    item.url = host + "?s=" + texto

    try:
        if item.extra == "serie":
            return peliculas_tv(item)
        if item.extra == "movie":
            return peliculas(item)
    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def peliculas(item):
    logger.info("streamondemand.casacinema peliculas")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = '<li><a href="([^"]+)"[^=]+="([^"]+)"><div>\s*<div[^>]+>(.*?)<'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios" if item.extra == "serie" else "findvideos",
                 contentType="movie",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='movie'))

    ## Paginación
    next_page = scrapertools.find_single_match(data, '<li><a href="([^"]+)" >Pagina')

    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 extra=item.extra,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist


def peliculas_tv(item):
    logger.info("streamondemand.casacinema peliculas")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = '<li><a href="([^"]+)"[^=]+="([^"]+)"><div>\s*<div[^>]+>(.*?)<'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios" if item.extra == "serie" else "findvideos",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='tv'))

    ## Paginación
    next_page = scrapertools.find_single_match(data, '<li><a href="([^"]+)" >Pagina')

    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_tv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 extra=item.extra,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")


def categorias(item):
    logger.info("streamondemand.casacinema categorias")

    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data, 'Categorie(.*?)</ul>')

    # The categories are the options for the combo
    patron = '<a href="(.*?)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 extra=item.extra,
                 url=urlparse.urljoin(host, scrapedurl)))

    return itemlist


def episodios(item):
    def load_episodios(html, item, itemlist, lang_title):
        patron = '.*?<a href="[^"]+"[^o]+ofollow[^>]+>[^<]+</a><(?:b|/)[^>]+>'
        matches = re.compile(patron).findall(html)
        for data in matches:
            # Estrae i contenuti 
            scrapedtitle = data.split('<a ')[0]
            scrapedtitle = re.sub(r'<[^>]*>', '', scrapedtitle).strip()
            if scrapedtitle != 'Categorie':
                scrapedtitle = scrapedtitle.replace('&#215;', 'x')
                scrapedtitle = scrapedtitle.replace('×', 'x')
                scrapedtitle = scrapedtitle.replace(';', '')
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

    logger.info("[casacinema.py] episodios")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data
    data = scrapertools.decodeHtmlentities(data)
    data = scrapertools.get_match(data, '<p>(?:<strong>|)(.*?)<div id="disqus_thread">')

    lang_titles = []
    starts = []
    patron = r"Stagione.*?(?:ITA|\d+)"
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
    logger.info("streamondemand.casacinema findvideos")

    data = item.url if item.extra == 'serie' else httptools.downloadpage(item.url, headers=headers).data

    html = httptools.downloadpage(data).data
    patron = '"http:\/\/shrink-service\.it\/[^\/]+\/[^\/]+\/([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(html)

    for url in matches:
        if url is not None:
            data = data
        else:
            continue

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

