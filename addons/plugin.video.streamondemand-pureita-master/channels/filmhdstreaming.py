# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canal per filmhdstreaming
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
#  By Costaplus
# ------------------------------------------------------------

#   Import  sono importanti per il funzionamento del canale
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmhdstreaming"
__category__ = "F"
__type__ = "generic"
__title__ = "filmhdstreaming (IT)"
__language__ = "IT"

# riferimento alla gestione del log
DEBUG = config.get_setting("debug")

host = "https://cb01.mobi/"

# -----------------------------------------------------------------
# Elenco inziale del canale
def mainlist(item):
    logger.info("filmhdstreaming mainlist")

    itemlist = []
    itemlist.append(Item(channel=item.channel, action="elenco", title="[COLOR azure]Film - [COLOR orange]Top[/COLOR]", url=host,thumbnail=TopThumbnail, fanart=fanart))
    itemlist.append(Item(channel=item.channel, action="elenco", title="[COLOR azure]Film - [COLOR orange]Aggiornati[/COLOR]", url=host+"/page/1.html",thumbnail=NovitaThumbnail, fanart=fanart))
    itemlist.append(Item(channel=item.channel, action="elenco_years", title="[COLOR azure]Film - [COLOR orange]per Anno[/COLOR]", url=host,thumbnail=AnnoThumbnail, fanart=fanart))
    itemlist.append(Item(channel=item.channel, action="elenco_genere", title="[COLOR azure]Film - [COLOR orange]per Categoria[/COLOR]", url=host,thumbnail=GenereThumbnail, fanart=fanart))
    itemlist.append(Item(channel=item.channel, action="search", title="[COLOR yellow]Cerca film...[/COLOR]", extra="movie",thumbnail=thumbcerca, fanart=fanart))

    return itemlist
# =================================================================

#------------------------------------------------------------------
def newest(categoria):
    logger.info("filmhdstreaming newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "peliculas":
            item.url = "http://filmhdstreaming.org/page/1.html"
            item.action = "elenco"
            itemlist = elenco(item)

            if itemlist[-1].action == "elenco":
                itemlist.pop()

    # Se captura la excepción, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist
# =================================================================

#------------------------------------------------------------------
# Funzione elenco top
def elenco_top(item):
    logger.info("filmhdstreaming elenco_top")

    itemlist = []

    data = scrapertools.cache_page(item.url)

    # metodo che utilizzo pee verificare cosa scarica nella chace
    # provate and andare nel log di kodi e controllate in fondo...
    # io uso notepad ++ che ha come vantaggio di auto aggiornarsi ad ogni cambiamento del file
    # per non stare ad aprire e chidere tutte le vole il file di log di kodi
    logger.info("ecco la pagina completa ->" + data)

    # nel patron in questo caso tutto ciò che è tra > e class= verrà preso in cosiderazione
    patron = 'id="box_movies1">(.*?)class="header_slider">'
    filtro_top = scrapertools.find_single_match(data, patron)

    # controllo log
    logger.info("filtrato ->" + filtro_top)

    patron = 'class="movie">[^>]+><a href="(.*?)"><img src="(.*?)".*?<h2>(.*?)<\/h2>'

    matches = scrapertools.find_multiple_matches(filtro_top, patron)

    for scrapedurl, scrapedimg, scrapedtitle in matches:
        # sempre per controllare il log
        logger.info("Url:" + scrapedurl + " thumbnail:" + scrapedimg + " title:" + scrapedtitle)
        title = scrapedtitle.split("(")[0]
        itemlist.append(infoSod(Item(channel=item.channel,
                             action="findvideos",
                             title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                             fulltitle=scrapedtitle,
                             url=scrapedurl,
                             thumbnail=scrapedimg,
                             fanart=""
                             )))

    return itemlist
# =================================================================

#------------------------------------------------------------------
# Funzione elenco top
def elenco(item):
    logger.info("filmhdstreaming elenco")

    itemlist = []
    data = scrapertools.cache_page(item.url)

    patron = r'<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.replace(" streaming ita", "")
        scrapedtitle = scrapedtitle.replace(" film streaming", "")
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = r'<a class="page dark gradient" href=["|\']+([^"]+)["|\']+>AVANTI'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(re.sub(r'\d+.html$', '', item.url), matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="elenco",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

# =================================================================

#------------------------------------------------------------------
# Funzione elenco genere
def elenco_genere(item):
    logger.info("filmhdstreaming elenco_genere")

    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    bloque = scrapertools.get_match(data, '<ul>(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<li><a href="(.*?)"><i class="fa fa-caret-right"></i> (.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapedtitle.replace("Film streaming ", "")
        if DEBUG: logger.info("title=[" + scrapedtitle + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="elenco",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

#==================================================================

#------------------------------------------------------------------
# Funzione elenco genere

def elenco_years(item):
    logger.info("filmhdstreaming elenco_genere")

    itemlist = []


    data = scrapertools.cache_page(item.url)
    bloque = scrapertools.get_match(data, '<label for="drop-2" class="toggle">.*?</label>(.*?)</ul>')


    patron = '<li><a href="(.*?)"><i class="fa fa-caret-right"></i> (.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapedtitle.replace("Film streaming ", "")
        if DEBUG: logger.info("title=[" + scrapedtitle + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="elenco",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png",
                 folder=True))

    return itemlist
#==================================================================


#------------------------------------------------------------------
def search(item, texto):
    logger.info("filmhdstreaming search " + texto)

    itemlist = []

    item.url = "http://hdcineblog01.com/search/" + texto

    try:
        return elenco(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

#------------------------------------------------------------------
def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")

########################################################################
# Riferimenti a immagini statiche
GenereThumbnail = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png"
NovitaThumbnail = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"
TopThumbnail = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movies_P.png"
AnnoThumbnail = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"
thumbcerca = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png"
fanart ="https://superrepo.org/static/images/fanart/original/script.artwork.downloader.jpg"
HomeTxt = "[COLOR yellow]Torna Home[/COLOR]"
AvantiTxt = "[COLOR orange]Successivo>>[/COLOR]"
AvantiImg = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png"
ThumbnailHome = "https://raw.githubusercontent.com/orione7/Pelis_images/master/thumb_folder.png"
thumbnovita = "https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"
