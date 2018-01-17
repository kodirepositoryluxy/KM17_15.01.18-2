# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale altadefinizioneclick
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import base64
import re
import urlparse

from core import httptools
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod
from platformcode import logger

__channel__ = "altadefinizioneclick"

host = "http://altadefinizione.pink"

headers = [['Referer', host]]

def mainlist(item):
    logger.info("[altadefinizioneclick.py] mainlist")

    itemlist = [
        Item(channel=__channel__,
             title="[COLOR azure]Novita'[/COLOR]",
             action="fichas",
             url=host + "/nuove-uscite/",
             thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film per Genere[/COLOR]",
             action="genere",
             url=host,
             thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film per Anno[/COLOR]",
             action="anno",
             url=host,
             thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film Sub-Ita[/COLOR]",
             action="fichas",
             url=host + "/sub-ita/",
             thumbnail="http://i.imgur.com/qUENzxl.png"),
        Item(channel=__channel__,
             title="[COLOR orange]Cerca...[/COLOR]",
             action="search",
             extra="movie",
             thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist


def search(item, texto):
    logger.info("[altadefinizioneclick.py] " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return fichas_src(item)

    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def genere(item):
    logger.info("[altadefinizioneclick.py] genere")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<ul class="listSubCat" id="Film">(.*?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li><a href="(.*?)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 folder=True))

    return itemlist


def anno(item):
    logger.info("[altadefinizioneclick.py] genere")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<ul class="listSubCat" id="Anno">(.*?)</div>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 folder=True))

    return itemlist


def fichas(item):
    logger.info("[altadefinizioneclick.py] fichas")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<img width[^s]+src="([^"]+)"[^>]+><[^=]+="info">\s*<h[^=]+=[^=]+="([^"]+)">(.*?)<[^2]+2>\s*<[^I]+IMDB[^:]+:(.*?)<'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedurl, scrapedtitle, scrapedpuntuacion in matches:

        title = scrapertools.decodeHtmlentities(scrapedtitle)
        title += " (" + scrapedpuntuacion + ")"

        # ------------------------------------------------
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        # ------------------------------------------------

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 title="[COLOR azure]" + title + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title), tipo='movie'))

    # Pagination
    next_page = scrapertools.find_single_match(data, '<a class="next page-numbers" href="([^"]+)">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist

def fichas_src(item):
    logger.info("[altadefinizioneclick.py] fichas")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<a href="([^"]+)">\s*<div[^=]+=[^=]+=[^=]+=[^=]+=[^=]+="(.*?)"[^>]+>[^<]+<[^>]+>\s*<h[^=]+="titleFilm">(.*?)<'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:

        title = scrapertools.decodeHtmlentities(scrapedtitle)

        # ------------------------------------------------
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        # ------------------------------------------------

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 title="[COLOR azure]" + title + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title), tipo='movie'))

    # Pagination
    next_page = scrapertools.find_single_match(data, '<a class="next page-numbers" href="([^"]+)">')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas_src",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist

def findvideos(item):
    logger.info("[altadefinizioneclick.py] findvideos")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data.replace('\n', '')
    patron = r'<iframe id="[^"]+" width="[^"]+" height="[^"]+" src="([^"]+)"[^>]+><\/iframe>'
    url = scrapertools.find_single_match(data, patron).replace("?alta", "")
    url = url.replace("&download=1", "")

    if 'hdpass' in url:
        data = httptools.downloadpage(url, headers=headers).data

        start = data.find('<div class="row mobileRes">')
        end = data.find('<div id="playerFront">', start)
        data = data[start:end]

        patron_res = '<div class="row mobileRes">(.*?)</div>'
        patron_mir = '<div class="row mobileMirrs">(.*?)</div>'
        patron_media = r'<input type="hidden" name="urlEmbed" data-mirror="([^"]+)" id="urlEmbed" value="([^"]+)"\s*/>'

        res = scrapertools.find_single_match(data, patron_res)

        urls = []
        for res_url, res_video in scrapertools.find_multiple_matches(res, '<option.*?value="([^"]+?)">([^<]+?)</option>'):

            data = httptools.downloadpage(urlparse.urljoin(url, res_url), headers=headers).data.replace('\n', '')

            mir = scrapertools.find_single_match(data, patron_mir)

            for mir_url in scrapertools.find_multiple_matches(mir, '<option.*?value="([^"]+?)">[^<]+?</value>'):

                data = httptools.downloadpage(urlparse.urljoin(url, mir_url), headers=headers).data.replace('\n', '')

                for media_label, media_url in re.compile(patron_media).findall(data):
                    urls.append(url_decode(media_url))

        itemlist = servertools.find_video_items(data='\n'.join(urls))
        for videoitem in itemlist:
            videoitem.title = item.title + videoitem.title
            videoitem.fulltitle = item.fulltitle
            videoitem.thumbnail = item.thumbnail
            videoitem.show = item.show
            videoitem.plot = item.plot
            videoitem.channel = __channel__

    return itemlist


def url_decode(url_enc):
    lenght = len(url_enc)
    if lenght % 2 == 0:
        len2 = lenght / 2
        first = url_enc[0:len2]
        last = url_enc[len2:lenght]
        url_enc = last + first
        reverse = url_enc[::-1]
        return base64.b64decode(reverse)

    last_car = url_enc[lenght - 1]
    url_enc[lenght - 1] = ' '
    url_enc = url_enc.strip()
    len1 = len(url_enc)
    len2 = len1 / 2
    first = url_enc[0:len2]
    last = url_enc[len2:len1]
    url_enc = last + first
    reverse = url_enc[::-1]
    reverse = reverse + last_car
    return base64.b64decode(reverse)
