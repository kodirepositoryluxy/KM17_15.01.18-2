# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita.- XBMC Plugin
# Canale vediserie - based on seriehd channel
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808.
# ------------------------------------------------------------
import re
import sys
import urllib2

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "vediserie"
__category__ = "S"
__type__ = "generic"
__title__ = "Vedi Serie"
__language__ = "IT"

headers = [['Upgrade-Insecure-Requests', '1'],
           ['User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36'],
           ['Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'],
           ['Accept-Encoding', 'gzip, deflate'],
           ['Accept-Language', 'en-US,en;q=0.8']]

host = "http://www.vediserie.tv/"


def isGeneric():
    return True

def mainlist(item):
    logger.info("[vediserie.py] mainlist")

    itemlist = [Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR azure]Serie TV [/COLOR]",
                     url="%s/category/serie-tv/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR azure]Serie TV - [COLOR orange]Aggiornamenti Odieni[/COLOR]",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR azure]Serie TV - [COLOR orange]Aggiornamenti Settimanali[/COLOR]",
                     url="%s/aggiornamenti-serie-tv/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),					 
                #Item(channel=__channel__,
                     #action="list_a_z",
                     #title="[COLOR azure]Serie TV - [COLOR orange]Ordine Alfabetico A-Z[/COLOR]",
                     #url="%s/lista-completa-serie-tv/" % host,
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist


def search(item, texto):
    logger.info("[vediserie.py] search")

    item.url = host + "/?s=" + texto

    try:
        return fichas(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla.
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


#def list_a_z(item):
    #logger.info("[vediserie.py] ordine alfabetico")
    #itemlist = []

    #data = anti_cloudflare(item.url)

    #patron = '<li><a href="([^"]+)" title="([^"]+)">.*?</a></li>'

    #matches = re.compile(patron, re.DOTALL).findall(data)

    #for scrapedurl, scrapedtitle in matches:
        #itemlist.append(
                #Item(channel=__channel__,
                     #action="episodios",
                     #title=scrapedtitle,
                     #url=scrapedurl))

    #return itemlist


def fichas(item):
    logger.info("[vediserie.py] fichas")
    itemlist = []

    data = scrapertools.anti_cloudflare(item.url, headers)

    # ------------------------------------------------
    cookies = ""
    matches = re.compile('(.vediserie.com.*?)\n', re.DOTALL).findall(config.get_cookie_data())
    for cookie in matches:
        name = cookie.split('\t')[5]
        value = cookie.split('\t')[6]
        cookies += name + "=" + value + ";"
    headers.append(['Cookie', cookies[:-1]])
    import urllib
    _headers = urllib.urlencode(dict(headers))
    # ------------------------------------------------

    patron = '<h2>[^>]+>\s*'
    patron += '<img[^=]+=[^=]+=[^=]+="([^"]+)"[^>]+>\s*'
    patron += '<A HREF=([^>]+)>[^>]+>[^>]+>[^>]+>\s*'
    patron += '[^>]+>[^>]+>(.*?)</[^>]+>[^>]+>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedurl, scrapedtitle in matches:
        scrapedthumbnail += "|" + _headers
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if scrapedtitle.startswith('<span class="year">'):
            scrapedtitle = scrapedtitle[19:]
        try:
           plot, fanart, poster, extrameta = info_tv(scrapedtitle)

           itemlist.append(
               Item(channel=__channel__,
                    thumbnail=poster,
                    fanart=fanart if fanart != "" else poster,
                    extrameta=extrameta,
                    plot=str(plot),
                    action="episodios",
                    title=scrapedtitle,
                    url=scrapedurl.replace('"', ''),
                    fulltitle=scrapedtitle,
                    show=scrapedtitle,
                    folder=True))
        except:
           itemlist.append(
               Item(channel=__channel__,
                    action="episodios",
                    title=scrapedtitle,
                    fulltitle=scrapedtitle,
                    url=scrapedurl.replace('"', ''),
                    show=scrapedtitle,
                    thumbnail=scrapedthumbnail))

    patron = '<span class=\'current\'>[^<]+</span><a class="page larger" href="(.*?)">'
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
    logger.info("[vediserie.py] episodios")

    itemlist = []

    # Descarga la página
    data = anti_cloudflare(item.url)

    patron = r'<div class="list" data-stagione="([^"]+)">\s*'
    patron += r'<ul class="listEpis">\s*'
    patron += r'<li><a href="javascript:void\(0\)" data-link="([^"]+)" data-id="([^"]+)">'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for season, url, episode in matches:
        season = str(int(season) + 1)
        episode = str(int(episode) + 1)
        if len(episode) == 1: episode = "0" + episode
        title = season + "x" + episode
        itemlist.append(
            Item(channel=__channel__,
                 action="findvid_serie",
                 title=title,
                 url=item.url,
                 thumbnail=item.thumbnail,
                 extra=url,
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


def findvid_serie(item):
    logger.info("[vediserie.py] findvideos")

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

def anti_cloudflare(url):
    # global headers

    try:
        resp_headers = scrapertools.get_headers_from_response(url, headers=headers)
        resp_headers = dict(resp_headers)
    except urllib2.HTTPError, e:
        resp_headers = e.headers

    if 'refresh' in resp_headers:
        time.sleep(int(resp_headers['refresh'][:1]))

        urlsplit = urlparse.urlsplit(url)
        h = urlsplit.netloc
        s = urlsplit.scheme
        scrapertools.get_headers_from_response(s + '://' + h + "/" + resp_headers['refresh'][7:], headers=headers)

    return scrapertools.cache_page(url, headers=headers)

def info_tv(title):
    logger.info("streamondemand.vediserie info")
    try:
        from core.tmdb import Tmdb
        oTmdb= Tmdb(texto_buscado=title, tipo= "tv", include_adult="true", idioma_busqueda="it")
        count = 0
        if oTmdb.total_results > 0:
           extrameta = {}
           extrameta["Year"] = oTmdb.result["release_date"][:4]
           extrameta["Genre"] = ", ".join(oTmdb.result["genres"])
           extrameta["Rating"] = float(oTmdb.result["vote_average"])
           fanart=oTmdb.get_backdrop()
           poster=oTmdb.get_poster()
           plot=oTmdb.get_sinopsis()
           return plot, fanart, poster, extrameta
    except:
        pass	

