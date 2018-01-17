# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale piratestreaming
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import urlparse

from core import config, httptools
from platformcode import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "italiaserie"

host = "http://www.italiaserie.co"


def mainlist(item):
    logger.info("streamondemand.italiaserie mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Aggiornamenti Serie TV[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Ultimi Episodi[/COLOR]",
                     action="latestep",
                     url="%s/aggiornamento-episodi/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]
    return itemlist

def newest(categoria):
    logger.info("[italiaserie.py]==> newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "series":
            item.url = "%s/aggiornamento-episodi/" % host
            item.action = "latestep"
            itemlist = latestep(item)

            if itemlist[-1].action == "latestep":
                itemlist.pop()

    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist

def latestep(item):
    itemlist = []
    
    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.find_single_match(data, r'<div class="entry">\s*<h4><span style="color: #ffff00;">(.*?)<p>&nbsp;</p>')
    patron = r'<h\d+><a href="([^"]+)">([^<]+)</a>\s*\(([^)]+)\)</h\d+>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle, scrapedepandlang in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedepandlang = scrapertools.decodeHtmlentities(scrapedepandlang.replace('&#215;', 'x'))
        seasonandep = scrapertools.find_single_match(scrapedepandlang, r'(\d+x[0-9\-?]+)')
        lang = scrapedepandlang.replace(seasonandep, "").strip()
        extra = r'%s(.*?)<br\s*/>'
        
        # Multi Ep
        if '-' in scrapedepandlang:
            season = scrapertools.find_single_match(scrapedepandlang, r'(\d+x)')
            scrapedepandlang = scrapedepandlang.split('-')
            for ep in scrapedepandlang:
                ep = (season + ep if season not in ep else ep).replace(lang, "")
                completetitle = "%s (%s %s)" % (scrapedtitle, ep, lang)

                itemlist.append(infoSod(
                    Item(channel=__channel__,
                         action="findepvideos",
                         title=completetitle,
                         contentSerieName=completetitle,
                         fulltitle=scrapedtitle,
                         url=scrapedurl,
                         extra="%s (%s)" % (extra, (ep.replace('x', '×').replace(lang, '').strip())),
                         folder=True), tipo='tv'))
            continue
        
        # Ep singolo
        extra = extra % (scrapedepandlang.replace('x', '×').replace(lang, '').strip())
        completetitle = "%s (%s)" % (scrapedtitle, scrapedepandlang)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findepvideos",
                 title=completetitle,
                 contentSerieName=completetitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 extra=extra,
                 folder=True), tipo='tv'))

    return itemlist

def peliculas(item):
    logger.info("streamondemand.italiaserie peliculas")
    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data

    # Estrae i contenuti 
    patron = '<div class="post-thumb">\s*<a href="([^"]+)" title="([^"]+)">\s*<img src="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedurl = scrapedurl.replace("-1/", "-links/")

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
    patronvideos = '<a class="next page-numbers" href="(.*?)">'
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
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")


def search(item, texto):
    logger.info("[italiaserie.py] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        return peliculas(item)
    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def episodios(item):
    def load_episodios(html, item, itemlist, lang_title):
        patron = '((?:.*?<a[^h]+href="[^"]+"[^>]+>[^<][^<]+<(?:b|\/)[^>]+>)+)'
        matches = re.compile(patron).findall(html)
        for data in matches:
            # Estrazione
            scrapedtitle = data.split('<a ')[0]
            scrapedtitle = re.sub(r'<[^>]*>', '', scrapedtitle).strip()
            if scrapedtitle != 'Categorie':
                scrapedtitle = scrapedtitle.replace('&#215;', 'x')
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

    logger.info("[italiaserie.py] episodios")

    itemlist = []

    # Download pagina
    data = httptools.downloadpage(item.url).data
    data = scrapertools.decodeHtmlentities(data)
    if 'CLICCA QUI PER GUARDARE TUTTI GLI EPISODI' in data:
        item.url = re.sub('\-\d+', '-links', item.url)
        data = httptools.downloadpage(item.url).data
        data = scrapertools.decodeHtmlentities(data)
    data = scrapertools.get_match(data, '<div class="entry-content">(.*?)<!-- /.single-post -->')

    lang_titles = []
    starts = []
    patron = r"Stagione.*?ITA"
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
                 extra="episodios",
                 show=item.show))

    return itemlist


def findvideos(item):
    logger.info("streamondemand.italiaserie findvideos")

    # Carica la pagina 
    data = item.url

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist

def findepvideos(item):
    logger.info("streamondemand.italiaserie findepvideos")

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data
    
    if 'CLICCA QUI PER GUARDARE TUTTI GLI EPISODI' in data:
        item.url = re.sub('\-\d+', '-links', item.url)
        data = httptools.downloadpage(item.url).data
        data = scrapertools.decodeHtmlentities(data)

    data = scrapertools.find_single_match(data, item.extra)
    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join(["[%s] " % ("[COLOR orange]" + server.capitalize() + "[/COLOR]"), item.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
