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

__channel__ = "italiafilmvideohd"

host = "http://www.italiafilm.link"

headers = [['Referer', host]]


def mainlist(item):
    logger.info("[italiafilmvideohd.py] mainlist")

    itemlist = [
        Item(channel=__channel__,
             title="[COLOR azure]Al Cinema[/COLOR]",
             action="fichas",
             url=host + "/cinema/",
             thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Ultimi Film Inseriti[/COLOR]",
             action="fichas",
             url=host + "/film-hd/",
             thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film per Genere[/COLOR]",
             action="genere",
             url=host,
             thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"),
        Item(channel=__channel__,
             title="[COLOR orange]Cerca...[/COLOR]",
             action="search",
             extra="movie",
             thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist


def newest(categoria):
    logger.info("[italiafilmvideohd.py] newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "peliculas":
            item.url = host + "/cinema/"
            item.action = "fichas"
            itemlist = fichas(item)

            if itemlist[-1].action == "fichas":
                itemlist.pop()

    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist


def search(item, texto):
    logger.info("[italiafilmvideohd.py] " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return fichas(item)

    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def genere(item):
    logger.info("[italiafilmvideohd.py] genere")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<div class="sub_title">Genere</div>(.+?)</div>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li>.*?'
    patron += 'href="([^"]+)".*?'
    patron += '<i>([^"]+)</i>'

    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapedtitle.replace('&amp;', '-')
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 folder=True))

    return itemlist


def fichas(item):
    logger.info("[italiafilmvideohd.py] fichas")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    # fix - calidad

    patron = '<li class="item">.*?'
    patron += 'href="([^"]+)".*?'
    patron += 'title="([^"]+)".*?'
    patron += '<img src="([^"]+)".*?'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scraped_2, scrapedtitle, scrapedthumbnail in matches:
        scrapedurl = scraped_2

        title = scrapertools.decodeHtmlentities(scrapedtitle)
        # title += " (" + scrapedcalidad + ")

        # ------------------------------------------------
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        # ------------------------------------------------
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=scrapedtitle), tipo='movie'))

    itemlist.append(
        Item(channel=__channel__,
             action="HomePage",
             title="[COLOR yellow]Torna Home[/COLOR]",
             folder=True)),

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)"\s*><span aria-hidden="true">&raquo;')

    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist


def findvideos(item):
    logger.info("[italiafilmvideohd.py] findvideos")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data.replace('\n', '')

    patron = r'<iframe width=".+?" height=".+?" src="([^"]+)" allowfullscreen frameborder="0">'
    url = scrapertools.find_single_match(data, patron).replace("?italiafilm", "")

    if 'hdpass' in url:
        data = httptools.downloadpage(url, headers=headers).data

        start = data.find('<div class="row mobileRes">')
        end = data.find('<div id="playerFront">', start)
        data = data[start:end]

        patron_res = r'<div class="row mobileRes">([\s\S]*)<\/div>'
        patron_mir = r'<div class="row mobileMirrs">([\s\S]*)<\/div>'
        patron_media = r'<input type="hidden" name="urlEmbed" data-mirror="([^"]+)" id="urlEmbed" value="([^"]+)"[^>]+>'

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


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")
