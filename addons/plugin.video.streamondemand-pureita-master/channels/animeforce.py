# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita.- XBMC Plugin
# Canale animeforce
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urllib
import urlparse

import xbmc

from core import config, httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod
from servers import adfly

__channel__ = "animeforce"
__category__ = "A"
__type__ = "generic"
__title__ = "AnimeForce"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.animeforce.org/"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]


def isGeneric():
    return True
PERPAGE = 20

# -----------------------------------------------------------------
def mainlist(item):
    log("mainlist", "mainlist")
    itemlist = [Item(channel=__channel__,
                     action="lista_anime",
                     title="[COLOR azure]Anime -[COLOR orange] Lista Completa[/COLOR]",
                     url=host + "/lista-anime/",
                     thumbnail=ThumbnailLista,
                     fanart=CategoriaFanart),
                Item(channel=__channel__,
                     action="animeaggiornati",
                     title="[COLOR azure]Anime -[COLOR orange] Episodi Aggiornati[/COLOR]",
                     url=host,
                     thumbnail=CategoriaThumbnail,
                     fanart=CategoriaFanart),
                Item(channel=__channel__,
                     action="ultimiep",
                     title="[COLOR azure]Anime -[COLOR orange] Ultimi Episodi[/COLOR]",
                     url=host,
                     thumbnail=ThumbnailNew,
                     fanart=CategoriaFanart),
                Item(channel=__channel__,
                     action="ultime_serie",
                     title="[COLOR azure]Anime -[COLOR orange] Ultime Serie[/COLOR]",
                     url=host + "/category/anime/articoli-principali/",
                     thumbnail=ThumbnailNew,
                     fanart=CategoriaFanart),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR yellow]Cerca ...[/COLOR]",
                     thumbnail=CercaThumbnail)]

    return itemlist


# =================================================================

# -----------------------------------------------------------------
def newest(categoria):
    log("newest", "newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "anime":
            item.url = "http://animeforce.org"
            item.action = "ultimiep"
            itemlist = ultimiep(item)

            if itemlist[-1].action == "ultimiep":
                itemlist.pop()
    # Se captura la excepción, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist

# =================================================================

# -----------------------------------------------------------------
def search(item, texto):
    log("search", "search")
    item.url = host + "/?s=" + texto
    try:
        return search_anime(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# =================================================================

# -----------------------------------------------------------------
def search_anime(item):
    log("search_anime", "search_anime")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<a href="([^"]+)"><img.*?src="([^"]+)".*?title="([^"]+)".*?/>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if "Sub Ita Download & Streaming" in scrapedtitle or "Sub Ita Streaming":
            itemlist.append(
                Item(channel=__channel__,
                    action="episodios",
                    title=scrapedtitle,
                    url=scrapedurl,
                    fulltitle=scrapedtitle,
                    show=scrapedtitle,
                    thumbnail=scrapedthumbnail))

    return itemlist


# =================================================================

# -----------------------------------------------------------------
def animeaggiornati(item):
    log("animeaggiornati", "animeaggiornati")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = r'<img.*?src="([^"]+)"[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if 'Streaming' in scrapedtitle:
            # Pulizia titolo
            cleantitle = scrapedtitle.replace("Streaming", "").replace("&", "")
            cleantitle = cleantitle.replace("Download", "")
            cleantitle = cleantitle.replace("Sub Ita", "")
            cleantitle = re.sub(r'Episodio?\s*\d+\s*(?:\(\d+\)|)\s*[\(OAV\)]*', '', cleantitle)
            # Creazione URL
            scrapedurl = re.sub(r'episodio?-?\d+-?(?:\d+-|)[oav]*', '', scrapedurl)
            itemlist.append(infoSod(
                Item(channel=__channel__,
                     action="episodios",
                     title=cleantitle,
                     url=scrapedurl,
                     fulltitle=cleantitle,
                     show=cleantitle,
                     thumbnail=scrapedthumbnail), tipo="tv"))

    return itemlist


# =================================================================

# -----------------------------------------------------------------
def ultimiep(item):
    log("ultimiep", "ultimiep")
    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)

    patron = r'<img.*?src="([^"]+)"[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if 'Streaming' in scrapedtitle:
            # Pulizia titolo
            scrapedtitle = scrapedtitle.replace("Streaming", "").replace("&", "")
            scrapedtitle = scrapedtitle.replace("Download", "")
            scrapedtitle = scrapedtitle.replace("Sub Ita", "").strip()
            cleantitle = re.sub(r'Episodio?\s*\d+\s*(?:\(\d+\)|)', '', scrapedtitle).strip()
            # Creazione URL
            episodio = scrapertools.find_single_match(scrapedtitle.lower(), r'episodio?\s*(\d+)')
            scrapedurl = re.sub(r'episodio?-?\d+-?(?:\d+-|)[oav]*', '', scrapedurl).replace('-fine', '')
            if 'download' not in scrapedurl:
                scrapedurl = scrapedurl.replace('-streaming', '-download-streaming')
            extra = "<tr>\s*<td[^>]+><strong>Episodio %s(?:[^>]+>[^>]+>|[^<]*)</strong></td>" % episodio
            print "EPISODIO: " + episodio + "\nTITLE: " + scrapedtitle + "\nExtra: " + extra + "\nURL: " + scrapedurl
            itemlist.append(infoSod(
                Item(channel=__channel__,
                    action="findvideos",
                    title=scrapedtitle,
                    url=scrapedurl,
                    fulltitle=cleantitle,
                    extra=extra,
                    show=re.sub(r'Episodio\s*', '', scrapedtitle),
                    thumbnail=scrapedthumbnail), tipo="tv"))

    return itemlist

# =================================================================

# -----------------------------------------------------------------

# =================================================================

# -----------------------------------------------------------------
def ultime_serie(item):
    log("ultimiep", "ultimiep")
    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)

    patron = r'<img.*?src="([^"]+)"[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if 'Streaming' in scrapedtitle:
            # Pulizia titolo
            scrapedtitle = scrapedtitle.replace("Streaming", "").replace("&", "")
            scrapedtitle = scrapedtitle.replace("Download", "")
            scrapedtitle = scrapedtitle.replace("Sub Ita", "").strip()
            cleantitle = re.sub(r'Episodio?\s*\d+\s*(?:\(\d+\)|)', '', scrapedtitle).strip()
            # Creazione URL
            episodio = scrapertools.find_single_match(scrapedtitle.lower(), r'episodio?\s*(\d+)')
            scrapedurl = re.sub(r'episodio?-?\d+-?(?:\d+-|)[oav]*', '', scrapedurl).replace('-fine', '')
            if 'download' not in scrapedurl:
                scrapedurl = scrapedurl.replace('-streaming', '-download-streaming')
            extra = "<tr>\s*<td[^>]+><strong>Episodio %s(?:[^>]+>[^>]+>|[^<]*)</strong></td>" % episodio
            print "EPISODIO: " + episodio + "\nTITLE: " + scrapedtitle + "\nExtra: " + extra + "\nURL: " + scrapedurl
            itemlist.append(infoSod(
                Item(channel=__channel__,
                    action="findvideos",
                    title=scrapedtitle,
                    url=scrapedurl,
                    fulltitle=cleantitle,
                    extra=extra,
                    show=re.sub(r'Episodio\s*', '', scrapedtitle),
                    thumbnail=scrapedthumbnail), tipo="tv"))

    return itemlist

# =================================================================
def lista_anime(item):
    log("lista_anime", "lista_anime")

    itemlist = []

    p = 1
    if '{}' in item.url:
        item.url, p = item.url.split('{}')
        p = int(p)

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data

    # Estrae i contenuti 
    patron = r'<li>\s*<strong>\s*<a\s*href="([^"]+?)">([^<]+?)</a>\s*</strong>\s*</li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    scrapedplot = ""
    scrapedthumbnail = ""
    for i, (scrapedurl, scrapedtitle) in enumerate(matches):
        if (p - 1) * PERPAGE > i: continue
        if i >= p * PERPAGE: break
        title = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodios",
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
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),

    if len(matches) >= p * PERPAGE:
        scrapedurl = item.url + '{}' + str(p + 1)
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="lista_anime",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist
# -----------------------------------------------------------------
def episodios(item):
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<td style="[^"]*?">\s*.*?<strong>(.*?)</strong>.*?\s*</td>\s*<td style="[^"]*?">\s*<a href="([^"]+?)"[^>]+>\s*<img.*?src="([^"]+?)".*?/>\s*</a>\s*</td>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl, scrapedimg in matches:
        if 'nodownload' in scrapedimg or 'nostreaming' in scrapedimg:
            continue

        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = re.sub(r'<[^>]*?>', '', scrapedtitle)
        scrapedtitle = '[COLOR azure][B]' + scrapedtitle + '[/B][/COLOR]'
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="episode",
                 title=scrapedtitle,
                 url=urlparse.urljoin(host, scrapedurl),
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 plot=item.plot,
                 fanart=item.thumbnail,
                 thumbnail=item.thumbnail))

    # Comandi di servizio
    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title="Aggiungi alla libreria",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios",
                 show=item.show))
        itemlist.append(
            Item(channel=__channel__,
                 title="Scarica tutti gli episodi della serie",
                 url=item.url,
                 action="download_all_episodes",
                 extra="episodios",
                 show=item.show))

    return itemlist


# ==================================================================

# -----------------------------------------------------------------
def findvideos(item):
    logger.info("streamondemand.animeforce findvideos")

    itemlist = []

    if item.extra:
        data = scrapertools.cache_page(item.url, headers=headers)

        blocco = scrapertools.get_match(data, r'%s(.*?)</tr>' % item.extra)
        scrapedurl = scrapertools.find_single_match(blocco, r'<a href="([^"]+)"[^>]+>')
        url = scrapedurl
    else:
        url = item.url

    if 'adf.ly' in url:
        url = adfly.get_long_url(url)
    elif 'bit.ly' in url:
        url = scrapertools.getLocationHeaderFromResponse(url)

    if 'animeforce' in url:
        headers.append(['Referer', item.url])
        data = scrapertools.cache_page(url, headers=headers)
        itemlist.extend(servertools.find_video_items(data=data))

        for videoitem in itemlist:
            videoitem.title = item.title + videoitem.title
            videoitem.fulltitle = item.fulltitle
            videoitem.show = item.show
            videoitem.thumbnail = item.thumbnail
            videoitem.channel = __channel__

        url = url.split('&')[0]
        data = scrapertools.cache_page(url, headers=headers)
        patron = """<source\s*src=(?:"|')([^"']+?)(?:"|')\s*type=(?:"|')video/mp4(?:"|')>"""
        matches = re.compile(patron, re.DOTALL).findall(data)
        headers.append(['Referer', url])
        for video in matches:
            itemlist.append(Item(channel=__channel__, action="play", title=item.title, url=video + '|' + urllib.urlencode(dict(headers)), folder=False))
    else:
        itemlist.extend(servertools.find_video_items(data=url))

        for videoitem in itemlist:
            videoitem.title = item.title + videoitem.title
            videoitem.fulltitle = item.fulltitle
            videoitem.show = item.show
            videoitem.thumbnail = item.thumbnail
            videoitem.channel = __channel__

    return itemlist


# ==================================================================

# =================================================================
# Funzioni di servizio
# -----------------------------------------------------------------
def scrapedAll(url="", patron=""):
    data = scrapertools.cache_page(url)
    if DEBUG: logger.info("data:" + data)
    MyPatron = patron
    matches = re.compile(MyPatron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    return matches


# =================================================================

# -----------------------------------------------------------------
def scrapedSingle(url="", single="", patron=""):
    data = scrapertools.cache_page(url)
    paginazione = scrapertools.find_single_match(data, single)
    matches = re.compile(patron, re.DOTALL).findall(paginazione)
    scrapertools.printMatches(matches)

    return matches


# =================================================================

# -----------------------------------------------------------------
def Crea_Url(pagina="1", azione="ricerca", categoria="", nome=""):
    # esempio
    # chiamate.php?azione=ricerca&cat=&nome=&pag=
    Stringa = host + "chiamate.php?azione=" + azione + "&cat=" + categoria + "&nome=" + nome + "&pag=" + pagina
    log("crea_Url", Stringa)
    return Stringa


# =================================================================

# -----------------------------------------------------------------
def log(funzione="", stringa="", canale=__channel__):
    if DEBUG: logger.info("[" + canale + "].[" + funzione + "] " + stringa)


# =================================================================

# -----------------------------------------------------------------
def HomePage(item):
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")


# =================================================================

# =================================================================
# riferimenti di servizio
# -----------------------------------------------------------------
AnimeThumbnail = "http://img15.deviantart.net/f81c/i/2011/173/7/6/cursed_candies_anime_poster_by_careko-d3jnzg9.jpg"
AnimeFanart = "https://i.ytimg.com/vi/IAlbvyBdYdY/maxresdefault.jpg"
ThumbnailNew = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_new_P.png"
ThumbnailLista = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_lista_P.png"
CategoriaThumbnail = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/anime_P.png"
CategoriaFanart = "https://i.ytimg.com/vi/IAlbvyBdYdY/maxresdefault.jpg"
CercaThumbnail = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"
CercaFanart = "https://i.ytimg.com/vi/IAlbvyBdYdY/maxresdefault.jpg"
HomeTxt = "[COLOR yellow]Torna Home[/COLOR]"
AvantiTxt = "[COLOR orange]Successivo>>[/COLOR]"
AvantiImg = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png"
