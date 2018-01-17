# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita- XBMC Plugin
# Canale seriehd
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import base64
import re
import urlparse

from core import config, httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "seriehd"

host = "http://www.seriehd.me"

headers = [['Referer', host]]


def mainlist(item):
    logger.info("[seriehd.py] mainlist")

    itemlist = [Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR azure]Serie TV[/COLOR]",
                     url=host + "/serie-tv-streaming/",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     action="sottomenu",
                     title="[COLOR orange]Categoria[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     action="search",
                     extra="serie",
                     title="[COLOR green]Cerca...[/COLOR]",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist


def search(item, texto):
    logger.info("[seriehd.py] search")

    item.url = host + "/?s=" + texto

    try:
        return fichas(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla.
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def sottomenu(item):
    logger.info("[seriehd.py] sottomenu")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<a href="([^"]+)">([^<]+)</a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png"))

    # Elimina 'Serie TV' de la lista de 'sottomenu'
    itemlist.pop(0)

    return itemlist


def fichas(item):
    logger.info("[seriehd.py] fichas")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<h2>(.*?)</h2>\s*'
    patron += '<img src="([^"]+)" alt="[^"]*" />\s*'
    patron += '<A HREF="([^"]+)">'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedthumbnail, scrapedurl in matches:
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 show=scrapedtitle,
                 thumbnail=scrapedthumbnail), tipo='tv'))

    patron = "<span class='current'>\d+</span><a rel='nofollow' class='page larger' href='([^']+)'>\d+</a>"
    next_page = scrapertools.find_single_match(data, patron)
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="fichas",
                 title="[COLOR orange]Successivo>>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png"))

    return itemlist


def episodios(item):
    logger.info("[seriehd.py] episodios")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = r'<iframe width=".+?" height=".+?" src="([^"]+)" allowfullscreen frameborder="0">'
    url = scrapertools.find_single_match(data, patron).replace("?seriehd", "")

    data = httptools.downloadpage(url).data.replace('\n', '').replace(' class="active"', '')


    section_stagione = scrapertools.find_single_match(data, '<h3>STAGIONE</h3><ul>(.*?)</ul>')
    patron = '<li[^>]+><a href="([^"]+)">(\d+)<'
    seasons = re.compile(patron, re.DOTALL).findall(section_stagione)

    for scrapedseason_url, scrapedseason in seasons:

        season_url = urlparse.urljoin(url, scrapedseason_url)
        data = httptools.downloadpage(season_url).data.replace('\n', '').replace(' class="active"', '')

        section_episodio = scrapertools.find_single_match(data, '<h3>EPISODIO</h3><ul>(.*?)</ul>')
        patron = '<li><a href="([^"]+)">(\d+)<'
        episodes = re.compile(patron, re.DOTALL).findall(section_episodio)

        for scrapedepisode_url, scrapedepisode in episodes:
            episode_url = urlparse.urljoin(url, scrapedepisode_url)

            title = scrapedseason + "x" + scrapedepisode.zfill(2)

            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     contentType="episode",
                     title=title,
                     url=episode_url,
                     fulltitle=title + ' - ' + item.show,
                     show=item.show,
                     thumbnail=item.thumbnail))

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
    logger.info("[seriehd.py] findvideos")

    itemlist = []

    # Descarga la página
    data = httptools.downloadpage(item.url, headers=headers).data.replace('\n', '')

    patron = r'<iframe id="iframeVid" width=".+?" height=".+?" src="([^"]+)" allowfullscreen'
    url = scrapertools.find_single_match(data, patron)

    if 'hdpass' in url:
        data = httptools.downloadpage(url, headers=headers).data

        start = data.find('<div class="row mobileRes">')
        end = data.find('<div id="playerFront">', start)
        data = data[start:end]

        patron_res = '<div class="row mobileRes">(.*?)</div>'
        patron_mir = '<div class="row mobileMirrs">(.*?)</div>'
        patron_media = r'<input type="hidden" name="urlEmbed" data-mirror="([^"]+)" id="urlEmbed" value="([^"]+)".*?>'

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
