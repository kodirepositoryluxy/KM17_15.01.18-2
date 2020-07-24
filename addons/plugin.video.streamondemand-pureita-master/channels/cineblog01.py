# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para cineblog01
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

import logging
import os

__channel__ = "cineblog01"
__category__ = "F,S"
__type__ = "generic"
__title__ = "CineBlog 01"
__language__ = "IT"

sito = "https://www.cb01.zone/"


headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', sito]
]

DEBUG = config.get_setting("debug")

def isGeneric():
    return True


def mainlist(item):
    logger.info("[cineblog01.py] mainlist")

    # Main options
    itemlist = [Item(channel=__channel__,
                     action="peliculas",
                     title="[COLOR azure]Cinema - Novita'[/COLOR]",
                     url=sito,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     action="peliculas",
                     title="[COLOR azure]Alta Definizione [HD][/COLOR]",
                     url="%s/tag/film-hd-altadefinizione/" % sito,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png"),
                Item(channel=__channel__,
                     action="menuhd",
                     title="[COLOR azure]Menù HD[/COLOR]",
                     url=sito,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/blueray_P.png"),
                Item(channel=__channel__,
                     action="menugeneros",
                     title="[COLOR azure]Per Genere[/COLOR]",
                     url=sito,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     action="menuanyos",
                     title="[COLOR azure]Per Anno[/COLOR]",
                     url=sito,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR yellow]Cerca Film[/COLOR]",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"),
                Item(channel=__channel__,
                     action="listserie",
                     title="[COLOR azure]Serie Tv - Novita'[/COLOR]",
                     url="%s/serietv/" % sito,
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR yellow]Cerca Serie Tv[/COLOR]",
                     extra="serie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist


def peliculas(item):
    logger.info("[cineblog01.py] peliculas")
    itemlist = []

    if item.url == "":
        item.url = sito

    # Descarga la página
    data = scrapertools.anti_cloudflare(item.url, headers)

    # Extrae las entradas (carpetas)
    patronvideos = '<div class="span4".*?<a.*?<p><img src="([^"]+)".*?'
    patronvideos += '<div class="span8">.*?<a href="([^"]+)"> <h1>([^"]+)</h1></a>.*?'
    patronvideos += '<strong>([^<]*)</strong>.*?<br />([^<+]+)'
    matches = re.compile(patronvideos, re.DOTALL).finditer(data)

    for match in matches:
        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedurl = urlparse.urljoin(item.url, match.group(2))
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(1))
        scrapedthumbnail = scrapedthumbnail.replace(" ", "%20")
        scrapedplot = scrapertools.unescape("[COLOR orange]" + match.group(4) + "[/COLOR]\n" + match.group(5).strip())
        scrapedplot = scrapertools.htmlclean(scrapedplot).strip()
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 viewmode="movie_with_plot"), tipo='movie'))

    # Next page mark
    try:
        bloque = scrapertools.get_match(data, "<div id='wp_page_numbers'>(.*?)</div>")
        patronvideos = '<a href="([^"]+)">></a></li>'
        matches = re.compile(patronvideos, re.DOTALL).findall(bloque)
        scrapertools.printMatches(matches)

        if len(matches) > 0:
            scrapedtitle = "[COLOR orange]Successivo>>[/COLOR]"
            scrapedurl = matches[0]
            scrapedthumbnail = ""
            scrapedplot = ""
            if (DEBUG): logger.info(
                "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
            itemlist.append(
                Item(channel=__channel__,
                     action="HomePage",
                     title="[COLOR yellow]Home[/COLOR]",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                     folder=True)),
            itemlist.append(
                Item(channel=__channel__,
                     action="peliculas",
                     title=scrapedtitle,
                     url=scrapedurl,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                     extra=item.extra,
                     plot=scrapedplot))
    except:
        pass

    return itemlist


def menugeneros(item):
    logger.info("[cineblog01.py] menugeneros")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data, '<select name="select2"(.*?)</select>')

    # The categories are the options for the combo  
    patron = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

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
                 extra=item.extra,
                 plot=scrapedplot))

    return itemlist


def menuhd(item):
    logger.info("[cineblog01.py] menuhd")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data, '<select name="select1"(.*?)</select>')

    # The categories are the options for the combo  
    patron = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

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
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/hd_movies_P.png",
                 extra=item.extra,
                 plot=scrapedplot))

    return itemlist


def menuanyos(item):
    logger.info("[cineblog01.py] menuvk")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data, '<select name="select3"(.*?)</select>')

    # The categories are the options for the combo  
    patron = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

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
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 extra=item.extra,
                 plot=scrapedplot))

    return itemlist


# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item, texto):
    logger.info("[cineblog01.py] " + item.url + " search " + texto)

    try:

        if item.extra == "movie":
            item.url = "https://www.cb01.uno/?s=" + texto
            return peliculas(item)
        if item.extra == "serie":
            item.url = "https://www.cb01.uno/serietv/?s=" + texto
            return listserie(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def listserie(item):
    logger.info("[cineblog01.py] listaserie")
    itemlist = []

    # Descarga la página
    data = scrapertools.anti_cloudflare(item.url, headers)

    # Extrae las entradas (carpetas)
    patronvideos = '<div class="span4">\s*<a href="([^"]+)"><img src="([^"]+)".*?<div class="span8">.*?<h1>([^<]+)</h1></a>(.*?)<br><a'
    matches = re.compile(patronvideos, re.DOTALL).finditer(data)

    for match in matches:
        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedurl = match.group(1)
        scrapedthumbnail = match.group(2)
        scrapedplot = scrapertools.unescape(match.group(4))
        scrapedplot = scrapertools.htmlclean(scrapedplot).strip()
        if scrapedtitle.startswith(("Aggiornamento Quotidiano Serie TV")):
            continue
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="season_serietv",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 extra=item.extra,
                 plot=scrapedplot), tipo='tv'))

    # Put the next page mark
    try:
        next_page = scrapertools.get_match(data, "<link rel='next' href='([^']+)'")
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="listserie",
                 title="[COLOR orange]Successivo>>[/COLOR]",
                 url=next_page,
                 extra=item.extra,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png", ))
    except:
        pass

    return itemlist

def season_serietv(item):
    def load_season_serietv(html, item, itemlist, season_title):
        if len(html) > 0 and len(season_title) > 0:
            itemlist.append(
                Item(channel=__channel__,
                    action="episodios",
                    title="[COLOR azure]%s[/COLOR]" % season_title,
                    contentType="episode",
                    url=html,
                    extra='serie',
                    show=item.show))
        
    itemlist = []

    # Descarga la página
    data = scrapertools.anti_cloudflare(item.url, headers)
    data = scrapertools.decodeHtmlentities(data)
    data = scrapertools.get_match(data, '<td bgcolor="#ECEAE1">(.*?)</table>')
    
#   for x in range(0, len(scrapedtitle)-1):
#        logger.debug('%x: %s - %s',x,ord(scrapedtitle[x]),chr(ord(scrapedtitle[x])))
    blkseparator=chr(32)+chr(226)+chr(128)+chr(147)+chr(32)
    data = data.replace(blkseparator,' - ')

    starts = []
    season_titles = []
    patron = '^(?:seri|stagion)[i|e].*$'
    matches = re.compile(patron, re.MULTILINE | re.IGNORECASE).finditer(data)
    for match in matches:
        if match.group()!= '':
            season_titles.append(match.group())
            starts.append(match.end())

    i = 1
    len_season_titles = len(season_titles)

    while i <= len_season_titles:
        inizio = starts[i - 1]
        fine = starts[i] if i < len_season_titles else -1

        html = data[inizio:fine]
        season_title = season_titles[i - 1]
        load_season_serietv(html, item, itemlist, season_title)
        i += 1

    return itemlist

def episodios(item):
    itemlist = []

    if item.extra == 'serie':
        itemlist.extend(episodios_serie_new(item))

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


def episodios_serie_new(item):
    def load_episodios(html, item, itemlist, lang_title):
        # for data in scrapertools.decodeHtmlentities(html).splitlines():
        patron = '((?:.*?<a href=".*?"[^=]+="_blank"[^>]+>.*?<\/a>)+)'
        matches = re.compile(patron).findall(html)        
        for data in matches:
            # Extrae las entradas
            scrapedtitle = data.split('<a ')[0]
            scrapedtitle = re.sub(r'<[^>]*>', '', scrapedtitle).strip()
            if scrapedtitle != 'Categorie':
                scrapedtitle = scrapedtitle.replace('&#215;', 'x')
                if scrapedtitle.find(' - ')>0:
                    scrapedtitle=scrapedtitle[0:scrapedtitle.find(' - ')]
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

    logger.info("[cineblog01.py] episodios")

    itemlist = []
    
    lang_title = item.title
    if lang_title.upper().find('SUB') >0:
        lang_title = 'SUB ITA' 
    else:
        lang_title = 'ITA'

    html=item.url
    load_episodios(html, item, itemlist, lang_title)
    
    return itemlist


def findvideos(item):
    if item.extra == "movie":
        return findvid_film(item)
    if item.extra == 'serie':
        return findvid_serie(item)
    return []


def findvid_film(item):
    logger.info("[cineblog01.py] findvid_film")

    itemlist = []

    # Descarga la página
    data = scrapertools.anti_cloudflare(item.url, headers)
    data = scrapertools.decodeHtmlentities(data)

    # Extract the quality format
    patronvideos = '>([^<]+)</strong></div>'
    matches = re.compile(patronvideos, re.DOTALL).finditer(data)
    QualityStr = ""
    for match in matches:
        QualityStr = scrapertools.unescape(match.group(1))[6:]

    # STREAMANGO
    matches = []
    u = scrapertools.find_single_match(data, '(?://|\.)streamango\.com/(?:f/|embed/)?[0-9a-zA-Z]+')
    if u: matches.append((u, 'Streamango'))

    # Extrae las entradas
    streaming = scrapertools.find_single_match(data, '<strong>Streaming:</strong>(.*?)<table height="30">')
    patron = '<td><a[^h]href="([^"]+)"[^>]+>([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(streaming) + matches
    for scrapedurl, scrapedtitle in matches:
        logger.debug("##### findvideos Streaming ## %s ## %s ##" % (scrapedurl, scrapedtitle))
        title = "[COLOR orange]Streaming:[/COLOR] " + item.title + " [COLOR grey]" + QualityStr + "[/COLOR] [COLOR blue][" + scrapedtitle + "][/COLOR]"
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title=title,
                 url=scrapedurl,
                 fulltitle=item.fulltitle,
                 thumbnail=item.thumbnail,
                 show=item.show,
                 folder=False))

    streaming_hd = scrapertools.find_single_match(data, '<strong>Streaming HD[^<]+</strong>(.*?)<table height="30">')
    patron = '<td><a[^h]href="([^"]+)"[^>]+>([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(streaming_hd)
    for scrapedurl, scrapedtitle in matches:
        logger.debug("##### findvideos Streaming HD ## %s ## %s ##" % (scrapedurl, scrapedtitle))
        title = "[COLOR yellow]Streaming HD:[/COLOR] " + item.title + " [COLOR grey]" + QualityStr + "[/COLOR] [COLOR blue][" + scrapedtitle + "][/COLOR]"
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title=title,
                 url=scrapedurl,
                 fulltitle=item.fulltitle,
                 thumbnail=item.thumbnail,
                 show=item.show,
                 folder=False))

    streaming_3D = scrapertools.find_single_match(data, '<strong>Streaming 3D[^<]+</strong>(.*?)<table height="30">')
    patron = '<td><a[^h]href="([^"]+)"[^>]+>([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(streaming_3D)
    for scrapedurl, scrapedtitle in matches:
        logger.debug("##### findvideos Streaming 3D ## %s ## %s ##" % (scrapedurl, scrapedtitle))
        title = "[COLOR pink]Streaming 3D:[/COLOR] " + item.title + " [COLOR grey]" + QualityStr + "[/COLOR] [COLOR blue][" + scrapedtitle + "][/COLOR]"
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title=title,
                 url=scrapedurl,
                 fulltitle=item.fulltitle,
                 thumbnail=item.thumbnail,
                 show=item.show,
                 folder=False))

    download = scrapertools.find_single_match(data, '<strong>Download:</strong>(.*?)<table height="30">')
    patron = '<td><a[^h]href="([^"]+)"[^>]+>([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(download)
    for scrapedurl, scrapedtitle in matches:
        logger.debug("##### findvideos Download ## %s ## %s ##" % (scrapedurl, scrapedtitle))
        title = "[COLOR aqua]Download:[/COLOR] " + item.title + " [COLOR grey]" + QualityStr + "[/COLOR] [COLOR blue][" + scrapedtitle + "][/COLOR]"
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title=title,
                 url=scrapedurl,
                 fulltitle=item.fulltitle,
                 thumbnail=item.thumbnail,
                 show=item.show,
                 folder=False))

    download_hd = scrapertools.find_single_match(data, '<strong>Download HD[^<]+</strong>(.*?)<table width="100%" height="20">')
    patron = '<td><a[^h]href="([^"]+)"[^>]+>([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(download_hd)
    for scrapedurl, scrapedtitle in matches:
        logger.debug("##### findvideos Download HD ## %s ## %s ##" % (scrapedurl, scrapedtitle))
        title = "[COLOR azure]Download HD:[/COLOR] " + item.title + " [COLOR grey]" + QualityStr + "[/COLOR] [COLOR blue][" + scrapedtitle + "][/COLOR]"
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title=title,
                 url=scrapedurl,
                 fulltitle=item.fulltitle,
                 thumbnail=item.thumbnail,
                 show=item.show,
                 folder=False))

    if len(itemlist) == 0:
        itemlist = servertools.find_video_items(item=item)

    return itemlist


def findvid_serie(item):
    def load_vid_series(html,item,itemlist,blktxt):
        if len(blktxt)>2:
            vtype=blktxt.strip()[:-1] + " - "
        else:
            vtype=''
        patron = '<a href="([^"]+)"[^=]+="_blank"[^>]+>(.*?)</a>'
        # Extrae las entradas
        matches = re.compile(patron, re.DOTALL).finditer(html)
        for match in matches:
            scrapedurl = match.group(1)
            scrapedtitle = match.group(2)
            title = item.title + " [COLOR blue][" + vtype + scrapedtitle +"][/COLOR]"
            itemlist.append(
                Item(channel=__channel__,
                     action="play",
                     title=title,
                     url=scrapedurl,
                     fulltitle=item.fulltitle,
                     show=item.show,
                     folder=False))
    
    
    logger.info("[cineblog01.py] findvid_serie")

    itemlist = []
    lnkblk = []
    lnkblkp = []

    data = item.url

    # First blocks of links
    if data[0:data.find('<a')].find(':')>0:
        lnkblk.append(data[data.find(' - ')+3:data[0:data.find('<a')].find(':')+1])
        lnkblkp.append(data.find(' - ')+3)
    else:
        lnkblk.append(' ')
        lnkblkp.append(data.find('<a'))

    # Find new blocks of links
    patron = '<a\s[^>]+>[^<]+</a>([^<]+)'
    matches = re.compile(patron, re.DOTALL).finditer(data)
    for match in matches:
        sep = match.group(1)
        if sep != ' - ':
            lnkblk.append(sep)
    
    i=0
    if len(lnkblk)>1:
        for lb in lnkblk[1:]:
            lnkblkp.append(data.find(lb,lnkblkp[i]+len(lnkblk[i])))
            i=i+1

    for i in range(0,len(lnkblk)):
        if i==len(lnkblk)-1:
            load_vid_series(data[lnkblkp[i]:],item,itemlist,lnkblk[i])
        else:
            load_vid_series(data[lnkblkp[i]:lnkblkp[i+1]],item,itemlist,lnkblk[i])

    return itemlist


def play(item):
    logger.info("[cineblog01.py] play")

    if '/goto/' in item.url:
        item.url = item.url.split('/goto/')[-1].decode('base64')

    item.url = item.url.replace('http://cineblog01.uno', 'http://k4pp4.pw')
    #import web_pdb; web_pdb.set_trace()

    logger.debug("##############################################################")
    if "go.php" in item.url:
        data = scrapertools.anti_cloudflare(item.url, headers)
        try:
            data = scrapertools.get_match(data, 'window.location.href = "([^"]+)";')
        except IndexError:
            try:
                # data = scrapertools.get_match(data, r'<a href="([^"]+)">clicca qui</a>')
                # In alternativa, dato che a volte compare "Clicca qui per proseguire":
                data = scrapertools.get_match(data, r'<a href="([^"]+)".*?class="btn-wrapper">.*?licca.*?</a>')
            except IndexError:
                data = scrapertools.get_header_from_response(item.url, headers=headers, header_to_get="Location")
        while 'vcrypt' in data:
            data = scrapertools.get_header_from_response(data, headers=headers, header_to_get="Location")
        logger.debug("##### play go.php data ##\n%s\n##" % data)
    elif "/link/" in item.url:
        data = scrapertools.anti_cloudflare(item.url, headers)
        from lib import jsunpack

        try:
            data = scrapertools.get_match(data, "(eval\(function\(p,a,c,k,e,d.*?)</script>")
            data = jsunpack.unpack(data)
            logger.debug("##### play /link/ unpack ##\n%s\n##" % data)
        except IndexError:
            logger.debug("##### The content is yet unpacked ##\n%s\n##" % data)

        data = scrapertools.find_single_match(data, 'var link(?:\s)?=(?:\s)?"([^"]+)";')
        while 'vcrypt' in data:
            data = scrapertools.get_header_from_response(data, headers=headers, header_to_get="Location")
        logger.debug("##### play /link/ data ##\n%s\n##" % data)
    else:
        data = item.url
        logger.debug("##### play else data ##\n%s\n##" % data)
    logger.debug("##############################################################")

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.show
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-main)")
