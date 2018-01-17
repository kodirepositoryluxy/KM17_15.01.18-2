# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para itafilmtv
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
#  By Costaplus
# ------------------------------------------------------------
import re
import urlparse
import xbmc
from core import config, httptools
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "leserietv"
host = 'http://www.guardareserie.tv'
headers = [['Referer', host]]

# -----------------------------------------------------------------
def mainlist(item):
    logger.info("streamondemand.leserietv mainlist")
    itemlist = [Item(channel=__channel__,
                     action="novita",
                     title="[COLOR yellow]Novità[/COLOR]",
                     url=("%s/streaming/" % host),
                     thumbnail=thumbnail_novita,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     action="lista_serie",
                     title="[COLOR azure]Tutte le serie[/COLOR]",
                     url=("%s/streaming/" % host),
                     thumbnail=thumbnail_lista,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     title="[COLOR azure]Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail=thumbnail_categoria,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     action="top50",
                     title="[COLOR azure]Top 50[/COLOR]",
                     url=("%s/top50.html" % host),
                     thumbnail=thumbnail_top,
                     fanart=FilmFanart),
                Item(channel=__channel__,
                     extra="serie",
                     action="search",
                     title="[COLOR orange]Cerca...[/COLOR][I](minimo 3 caratteri)[/I]",
                     thumbnail=thumbnail_cerca,
                     fanart=FilmFanart)]
    return itemlist
# =================================================================


# -----------------------------------------------------------------
def novita(item):
    logger.info("streamondemand.leserietv novità")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<div class="video-item-cover"[^<]+<a href="(.*?)">[^<]+<img src="(.*?)" alt="(.*?)">'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedthumbnail = host + scrapedthumbnail
        logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle, viewmode="movie"), tipo='tv'))

    # Paginazione
    # ===========================================================
    patron = '<div class="pages">(.*?)</div>'
    paginazione = scrapertools.find_single_match(data, patron)
    patron = '<span>.*?</span>.*?href="([^"]+)".*?</a>'
    matches = re.compile(patron, re.DOTALL).findall(paginazione)
    scrapertools.printMatches(matches)
    # ===========================================================

    if len(matches) > 0:
        paginaurl = matches[0]
        itemlist.append(Item(channel=__channel__, action="novita"  , title="[COLOR orange]Successivo>>[/COLOR]", url=paginaurl, thumbnail=thumbnail_successivo, folder=True))
        itemlist.append(Item(channel=__channel__, action="HomePage", title="[COLOR yellow]Torna Home[/COLOR]"  ,thumbnail=ThumbnailHome, folder=True))

    return itemlist
# =================================================================

# -----------------------------------------------------------------
def lista_serie(item):
    logger.info("streamondemand.leserietv lista_serie")
    itemlist = []

    post = "dlenewssortby=title&dledirection=asc&set_new_sort=dle_sort_cat&set_direction_sort=dle_direction_cat"
    data = httptools.downloadpage(item.url, post=post, headers=headers).data
    patron = '<div class="video-item-cover"[^<]+<a href="(.*?)">[^<]+<img src="(.*?)" alt="(.*?)">'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedthumbnail = host + scrapedthumbnail
        logger.info(scrapedurl + " " + scrapedtitle + scrapedthumbnail)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle, viewmode="movie"), tipo='tv'))

    # Paginazione
    # ===========================================================
    patron = '<div class="pages">(.*?)</div>'
    paginazione = scrapertools.find_single_match(data, patron)
    patron = '<span>.*?</span>.*?href="([^"]+)".*?</a>'
    matches = re.compile(patron, re.DOTALL).findall(paginazione)
    scrapertools.printMatches(matches)
    # ===========================================================

    if len(matches) > 0:
        paginaurl = matches[0]
        itemlist.append(Item(channel=__channel__, action="novita", title="[COLOR orange]Successivo>>[/COLOR]", url=paginaurl,thumbnail=thumbnail_successivo, folder=True))
        itemlist.append(Item(channel=__channel__, action="HomePage", title="[COLOR yellow]Torna Home[/COLOR]", thumbnail=ThumbnailHome, folder=True))

    return itemlist
# =================================================================

# -----------------------------------------------------------------
def categorias(item):
    logger.info("streamondemand.leserietv categorias")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<ul class="dropdown-menu cat-menu">(.*?)</ul>')
    patron = '<li ><a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = urlparse.urljoin(item.url, scrapedurl)
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append(
            Item(channel=__channel__,
                 action="lista_serie",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 plot=scrapedplot))

    return itemlist
# =================================================================

# -----------------------------------------------------------------
def search(item, texto):
    logger.info("streamondemand.leserietv " + host + " search " + texto)

    itemlist = []

    post = "do=search&subaction=search&story=" + texto
    data = httptools.downloadpage("http://www.guardareserie.tv", post=post, headers=headers).data

    patron = '<div class="video-item-cover"[^<]+<a href="(.*?)">[^<]+<img src="(.*?)" alt="(.*?)">'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedthumbnail = host + scrapedthumbnail
        logger.info(scrapedurl + " " + scrapedtitle + scrapedthumbnail)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle), tipo='tv'))

    return itemlist
# =================================================================

# -----------------------------------------------------------------
def top50(item):
    logger.info("streamondemand.leserietv top50")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = 'class="top50item">\s*<[^>]+>\s*<.*?="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle in matches:
        scrapedthumbnail = ""
        logger.debug(scrapedurl + " " + scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle, viewmode="movie"), tipo='tv'))

    return itemlist
# =================================================================

# -----------------------------------------------------------------
def episodios(item):
    logger.info("streamondemand.leserietv episodios")
    itemlist = []
    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<li id[^<]+<[^<]+<.*?class="serie-title">(.*?)</span>[^>]+>[^<]+<.*?megadrive-(.*?)".*?data-link="([^"]+)">Megadrive</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedlongtitle, scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapedtitle.split('_')[0] + "x" + scrapedtitle.split('_')[1].zfill(2)

        scrapedtitle = scrapedtitle + " [COLOR orange]" + scrapedlongtitle + "[/COLOR]"
        itemlist.append(Item(channel=__channel__,
                             action="findvideos",
                             title=scrapedtitle,
                             fulltitle=scrapedtitle,
                             url=scrapedurl,
                             thumbnail=item.thumbnail,
                             fanart=item.fanart if item.fanart != "" else item.scrapedthumbnail,
                             show=item.fulltitle))

    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title="Aggiungi alla libreria",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios",
                 contentType="episode",
                 show=item.show))

    return itemlist
# =================================================================

# ------------------------------------------------------------------
def findvideos(item):
    logger.info("streamondemand.leserietv findvideos "+item.url)
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    blocco = scrapertools.find_single_match(data, 'id="player_code">.*?</div>')

    data_pack = scrapertools.find_single_match(blocco, "(eval.function.p,a,c,k,e,.*?).s*</script>")
    if data_pack != "":
        from lib import jsunpack
        data_unpack = jsunpack.unpack(data_pack)
        data = data_unpack
    logger.debug(data_pack)

    elemento = scrapertools.find_single_match(data, 'file"?\s*:\s*"([^"]+)",')

    itemlist.append(Item(channel=__channel__,
                         action="play",
                         title=item.title,
                         url=elemento,
                         thumbnail=item.thumbnail,
                         fanart=item.fanart,
                         fulltitle=item.fulltitle,
                         show=item.fulltitle))
    return itemlist
# =================================================================

def HomePage(item):
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")


# =================================================================
FilmFanart = "https://superrepo.org/static/images/fanart/original/script.artwork.downloader.jpg"
ThumbnailHome = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png"
thumbnail_novita="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"
thumbnail_lista="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"
thumbnail_categoria="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"
thumbnail_top="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"
thumbnail_cerca="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"
thumbnail_successivo="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png"
