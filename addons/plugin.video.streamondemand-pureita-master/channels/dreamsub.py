# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita / XBMC Plugin
# Canale   dreamsub
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config, httptools, servertools
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "dreamsub"

host = "https://www.dreamsub.tv"


def mainlist(item):
    logger.info("streamondemand-pureita.dreamsub mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Anime / Cartoni[/COLOR]",
                     action="serietv",
                     extra='serie',
                     url="%s/anime" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animation_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Ultimi episodi Anime[/COLOR]",
                     action="ultimiep",
                     extra='anime',
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_new_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra='serie',
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist


def newest(categoria):
    logger.info("streamondemand-pureita.dreamsub newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "series":
            item.url = "https://www.dreamsub.tv"
            item.action = "ultimiep"
            item.extra = "serie"
            itemlist = ultimiep(item)

            if itemlist[-1].action == "ultimiep":
                itemlist.pop()

        if categoria == "anime":
            item.url = "https://www.dreamsub.tv"
            item.action = "ultimiep"
            item.extra = "anime"
            itemlist = ultimiep(item)

            if itemlist[-1].action == "ultimiep":
                itemlist.pop()
    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist


def serietv(item):
    logger.info("streamondemand-pureita.dreamsub peliculas")
    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data,'<input type="submit" value="Vai!" class="blueButton">(.*?)<div class="footer">')

    # Estrae i contenuti 
    patron = 'Lingua[^<]+<br>\s*<a href="([^"]+)" title="([^"]+)">'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host + scrapedurl
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapedtitle.replace("Streaming", "")
        scrapedtitle = scrapedtitle.replace("Lista episodi ", "")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='tv'))

    # Paginazione 
    patronvideos = '<li class="currentPage">[^>]+><li[^<]+<a href="([^"]+)">'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR orange]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="serietv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 extra=item.extra,
                 folder=True))

    return itemlist


def ultimiep(item):
    logger.info("streamondemand-pureita.dreamsub ultimiep")
    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data
    if 'anime' in item.extra:
        bloque = scrapertools.get_match(data, '<ul class="last" id="recentAddedEpisodesAnimeDDM">(.*?)</ul>')
    elif 'serie' in item.extra:
        bloque = scrapertools.get_match(data, '<ul class="last" id="recentAddedEpisodesTVDDM">(.*?)</ul>')

    # Estrae i contenuti 
    patron = '<li><a href="([^"]+)"[^>]+>([^<]+)<br>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        if 'anime' in item.extra:
            ep = scrapertools.find_single_match(scrapedtitle, r'\d+$').zfill(2)
            scrapedtitle = re.sub(r'\d+$', ep, scrapedtitle)
        scrapedurl = host + scrapedurl
        scrapedplot = ""
        scrapedthumbnail = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=(re.sub(r'\d*-?\d+$', '', scrapedtitle) if 'anime' in item.extra else re.sub(r'\d+x\d+$', '',
                                                                                                        scrapedtitle)).strip(),
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='tv'))
    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")


def search(item, texto):
    logger.info("[dreamsub.py] " + item.url + " search " + texto)
    item.url = "%s/search/%s" % (host, texto)
    try:
        return serietv(item)
    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def episodios(item):
    logger.info("streamondemand-pureita.channels.dreamsub episodios")

    itemlist = []

    data = httptools.downloadpage(item.url).data
    bloque = scrapertools.get_match(data, '<div class="seasonEp">(.*?)<div class="footer">')

    patron = '<li><a href="([^"]+)"[^<]+<b>(.*?)<\/b>[^>]+>([^<]+)<\/i>(.*?)<'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, title1, title2, title3 in matches:
        scrapedurl = host + scrapedurl
        scrapedtitle = title1 + " " + title2 + title3
        scrapedtitle = scrapedtitle.replace("Download", "")
        scrapedtitle = scrapedtitle.replace("Streaming", "")
        scrapedtitle = scrapedtitle.replace("& ", "")

        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=item.show,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 plot=item.plot,
                 folder=True))

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
    logger.info()

    print item.url
    data = httptools.downloadpage(item.url).data

    itemlist = servertools.find_video_items(data=data)
    if 'keepem.online' in data:
        urls = scrapertools.find_multiple_matches(data, r'(https://keepem\.online/f/[^"]+)"')
        for url in urls:
            url = httptools.downloadpage(url).url
            itemlist += servertools.find_video_items(data=url)
                
    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join(["[[COLOR orange]%s[/COLOR]] " % server.capitalize(), item.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
