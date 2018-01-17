# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-PureITA / XBMC Plugin
# Canale  serietvonline
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config, httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "serietvonline"
host        = "https://serietvonline.com/"
headers     = [['Referer', host]]

# -----------------------------------------------------------------
def mainlist(item):
    logger.info("streamondemand.serietvonline mainlist")

    itemlist = [Item(channel=__channel__,
                     action="lista_novita",
                     title="[COLOR azure]Lista Novità[/COLOR]",
                     url=(host),
                     thumbnail=thumbnail_novita,
                     fanart=thumbnail_lista),
                Item(channel=__channel__,
                     action="lista_serie",
                     title="[COLOR azure]Lista Cartoni Animati e Anime[/COLOR]",
                     url=("%s/lista-cartoni-animati-e-anime/" % host),
                     thumbnail=thumbnail_animation,
                     fanart=thumbnail_lista),
                Item(channel=__channel__,
                     action="lista_serie",
                     title="[COLOR azure]Lista Documentari[/COLOR]",
                     url=("%s/lista-documentari/" % host),
                     thumbnail=thumbnail_doc,
                     fanart=thumbnail_lista),
                Item(channel=__channel__,
                     action="lista_serie",
                     title="[COLOR azure]Lista Serie Tv Anni 50 60 70 80[/COLOR]",
                     url=("%s/lista-serie-tv-anni-60-70-80/" % host),
                     thumbnail=thumbnail_classic,
                     fanart=thumbnail_lista),
                Item(channel=__channel__,
                     action="lista_serie",
                     title="[COLOR azure]Lista serie Alta Definizione[/COLOR]",
                     url=("%s/lista-serie-tv-in-altadefinizione/" % host),
                     thumbnail=thumbnail_lista,
                     fanart=thumbnail_lista),
                Item(channel=__channel__,
                     action="lista_serie",
                     title="[COLOR azure]Lista Serie Tv Italiane[/COLOR]",
                     url=("%s/lista-serie-tv-italiane/" % host),
                     thumbnail=thumbnail_lista,
                     fanart=thumbnail_lista),

                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra='serie',
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]
    return itemlist
# =================================================================

# -----------------------------------------------------------------
def search(item, texto):
    logger.info("streamondemand.serietvonline search " + texto)

    itemlist = []

    url = host + "/?s= " + texto

    data = httptools.downloadpage(url, headers=headers).data

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)"><span[^>]+><[^>]+><\/a>[^h]+h2>(.*?)<'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
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

    # Extrae el paginador
    patronvideos = '<div class="siguiente"><a href="([^"]+)">'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
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
# =================================================================

# -----------------------------------------------------------------
def lista_serie(item):
    logger.info("streamondemand.serietvonline novità")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    blocco = scrapertools.find_single_match(data, 'id="lcp_instance_0">(.*?)</ul>')
    patron='<li><a href="(.*?)" title=".*?">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(Item(channel=__channel__,
                                     action="episodios",
                                     title=scrapedtitle,
                                     fulltitle=scrapedtitle,
                                     url=scrapedurl,
                                     fanart=item.fanart if item.fanart != "" else item.scrapedthumbnail,
                                     show=item.fulltitle,
                                     folder=True),tipo='tv'))

    return itemlist
# =================================================================

# -----------------------------------------------------------------

def lista_novita(item):
    logger.info("streamondemand.serietvonline novità")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    blocco = scrapertools.find_single_match(data, '<div id="box_movies">(.*?)</span></div></div>')
    patron = '<a href="([^"]+)"><span class="player"></span></a>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>\s*<h2>(.*?)</h2>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(Item(channel=__channel__,
                                     action="episodios",
                                     title=scrapedtitle,
                                     fulltitle=scrapedtitle,
                                     url=scrapedurl,
                                     fanart=item.fanart if item.fanart != "" else item.scrapedthumbnail,
                                     show=item.fulltitle,
                                     folder=True),tipo='tv'))


									 
    patron = "<a rel='nofollow' class=previouspostslink href='(.*?)'><span class='icon-chevron-right2'>"
    next_page = scrapertools.find_single_match(data, patron)
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_novita",
                 title="[COLOR orange]Precedenti>>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png"))

    return itemlist

# =================================================================

# -----------------------------------------------------------------
def episodios(item):
    logger.info("streamondemand.serietvonline episodios")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    blocco = scrapertools.get_match(data, '<table>(.*?)</table>')
    #logger.debug(blocco)

    patron = '<tr><td>(.*?)</td><tr>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)
    scrapertools.printMatches(matches)

    for puntata in matches:
        puntata = "<td class=\"title\">"+puntata
        #logger.debug(puntata)
        scrapedtitle=scrapertools.find_single_match(puntata, '<td class="title">(.*?)</td>')
        scrapedtitle=scrapedtitle.replace(item.title,"")
        itemlist.append(
            Item(channel=__channel__,
                 action="episodios_all",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=puntata,
                 thumbnail=item.scrapedthumbnail,
                 plot=item.scrapedplot,
                 folder=True))
    return itemlist
# =================================================================

# -----------------------------------------------------------------
def episodios_all(item):
    logger.info("streamondemand.serietvonline episodios")
    itemlist = []

    patron = "<a href='(.*?)'[^>]+>[^>]+>(.*?)<\/a>"
    matches = re.compile(patron, re.DOTALL).findall(item.url)

    for scrapedurl,scrapedserver in matches:
        #logger.debug(scrapedurl)
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=item.scrapedtitle,
                 show=item.scrapedtitle,
                 title="[COLOR blue]" + item.title + "[/COLOR][COLOR orange]" + scrapedserver + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=item.scrapedthumbnail,
                 plot=item.scrapedplot,
                 folder=True))

    return itemlist
# =================================================================

# -----------------------------------------------------------------
def findvideos(item):
    itemlist=[]

    data = item.url
    while 'vcrypt' in item.url:
        item.url = httptools.downloadpage(item.url, only_headers=True, follow_redirects=False).headers.get("location")
        data = item.url

    logger.debug(data)

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
# =================================================================


# -----------------------------------------------------------------
def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")
# =================================================================


thumbnail_fanart="https://superrepo.org/static/images/fanart/original/script.artwork.downloader.jpg"
ThumbnailHome = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png"
thumbnail_novita="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"
thumbnail_animation="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/animation_P.png"
thumbnail_doc="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/documentary_P.png"
thumbnail_classic="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/classictv_P.png"
thumbnail_lista="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"
thumbnail_top="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"
thumbnail_cerca="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"
thumbnail_successivo="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png"
