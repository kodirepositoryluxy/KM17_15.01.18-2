# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# videotecadiclasse
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re

from core import httptools
from platformcode import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "videotecadiclasse"

host = "http://fetchrss.com"

PERPAGE = 10

def mainlist(item):
    logger.info("streamondemand.videotecadiclasse mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Aggiornamenti Film[/COLOR]",
                     action="peliculas",
                     url=host + "/generator/generate?url=https://www.facebook.com%2FVideotecaDiClasse%2F&provider=facebook",
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png")]

    return itemlist


def peliculas(item):
    logger.info("streamondemand.videotecadiclasse peliculas")
    itemlist = []

    # Download page
    data = httptools.downloadpage(item.url).data

    # Strip the data
    patron = 'This is an example of your RSS[^<]+<br>\s*<iframe src="([^"]+)"><\/iframe>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl in matches:
        scrapedthumbnail = "http://www.timeninjablog.com/wp-content/uploads/2015/12/RSS.jpg"
        scrapedtitle = "Genera RSS"
        scrapedurl = host + scrapedurl
        itemlist.append(Item(channel=__channel__,
                             action="peliculas_rss",
                             fulltitle=scrapedtitle,
                             show=scrapedtitle,
                             title=scrapedtitle,
                             url=scrapedurl,
                             thumbnail=scrapedthumbnail,
                             folder=True))
    return itemlist


def peliculas_rss(item):
    logger.info("streamondemand.videotecadiclass peliculas_rss")
    itemlist = []

    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Download page
    data = httptools.downloadpage(item.url).data

    # Strip data
    patron = '<div class="fetch-rss-content ">\s*(.*?)<\/div>\s*<a\s*href="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    scrapedplot = ""
    scrapedthumbnail = ""

    for i, (scrapedtitle, scrapedurl) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        title = scrapertools.decodeHtmlentities(scrapedtitle).strip()

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    if len(itemlist) > 0:
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),

    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas_rss",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist


def findvideos(item):
    logger.info("[videotecadiclasse.py] findvideos")
    itemlist = []

    data = httptools.downloadpage(item.url).data

    patron = 'LINK FILM STREAMING:[^<]+<a href="https://l[^=]+=([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl in matches:
        scrapedurl = scrapedurl.replace("&amp;", "&")
        scrapedurl = scrapedurl.replace("%2F", "/")
        scrapedurl = scrapedurl.replace("%3A", ":")
        #link = "openload"
        #if link not in scrapedurl: continue
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title=item.title,
                 fulltitle=item.fulltitle,
                 url=scrapedurl,
                 thumbnail=item.thumbnail))
    return itemlist


def play(item):
    logger.info("[videotecadiclasse.py] play")
    data = httptools.downloadpage(item.url).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.show
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
