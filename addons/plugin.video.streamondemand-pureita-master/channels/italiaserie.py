# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita / XBMC Plugin
# Canale italiaserie
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808.
# ------------------------------------------------------------
import re
import urlparse

from core import config, httptools
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod
from servers import servertools

__channel__ = "italiaserie"
__category__ = "S,A"
__type__ = "generic"
__title__ = "italiaserie"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.italiaserie.co"


def isGeneric():
    return True


def mainlist(item):
    logger.info("pureita.italiaserie mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Serie TV -[COLOR orange] Novita'[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV -[/COLOR][COLOR orange] Popolari[/COLOR]",
                     action="peliculas",
                     url="%s/genere/netflix/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV -[COLOR orange] Ultimi Episodi[/COLOR]",
                     action="episodios_ultimi",
                     url="%s/aggiornamento-episodi/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                #Item(channel=__channel__,
                     #title="[COLOR azure]Serie TV -[COLOR orange] Top 10[/COLOR]",
                     #action="top",
                     #url="%s/top-10/" % host,
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                #Item(channel=__channel__,
                     #title="[COLOR azure]Serie TV[/COLOR]",
                     #action="lista_tv",
                     #url="%s/lista-completa/" % host,
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
                #Item(channel=__channel__,
                     #title="[COLOR azure]Serie TV -[COLOR orange] Lista[/COLOR]",
                     #action="lista",
                     #url="%s/lista-completa/" % host,
                     #thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/a-z_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]
    return itemlist

	
#===============================================================================================================================================
	
def search(item, texto):
    logger.info("[italiaserie.py] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==============================================================================================================================================
		
def peliculas(item):
    logger.info("pureita.italiaserie peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<div class="post-thumb">\s*<a href="([^"]+)" title="([^"]+)">\s*<img src="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl)
        start = html.find("<div class=\"entry-content\">")
        end = html.find("</p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Extrae el paginador
    patronvideos = '<a class="next page-numbers" href="(.*?)">'
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
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist

# ==============================================================================================================================================
	
def episodios(item):
    def load_episodios(html, item, itemlist, lang_title):
        patron = '((?:.*?<a href="[^"]+"[^>]+>[^<][^<]+<(?:b|\/)[^>]+>)+)'
        matches = re.compile(patron).findall(html)
        for data in matches:


            # Extrae las entradas (carpetas)
            scrapedtitle = data.split('<a ')[0]
            scrapedtitle = re.sub(r'<[^>]*>', '', scrapedtitle).strip()
            if scrapedtitle.startswith(("Guarda L'ultimo Episodio:")):
                continue
            if scrapedtitle != 'Categorie':
                scrapedtitle = scrapedtitle.replace('&#215;', 'x')
                scrapedtitle = scrapedtitle.replace('×', 'x')
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

    logger.info("pureita.italiaserie episodios")

    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data
    data = scrapertools.decodeHtmlentities(data)
    if 'CLICCA QUI PER GUARDARE TUTTI GLI EPISODI' in data:
        item.url = re.sub('\-\d+', '-links', item.url)
        data = httptools.downloadpage(item.url).data
        data = scrapertools.decodeHtmlentities(data)
    data = scrapertools.get_match(data, '<div class="entry-content">(.*?)<!-- /.single-post -->')

    lang_titles = []
    starts = []
    patron = r"Stagione.*?ITA"
    matches = re.compile(patron, re.IGNORECASE).finditer(data)
    for match in matches:
        season_title = match.group()
        if season_title != '':
            lang_titles.append('SUB ITA' if 'SUB' in season_title.upper() else 'ITA')
            starts.append(match.end())

    i = 1
    len_lang_titles = len(lang_titles)

    while i <= len_lang_titles:
        inizio = starts[i - 1]
        fine = starts[i] if i < len_lang_titles else -1

        html = data[inizio:fine]
        lang_title = lang_titles[i - 1]

        load_episodios(html, item, itemlist, lang_title)

        i += 1

    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title="Aggiungi alla libreria",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios",
                 show=item.show))

    return itemlist

# ==============================================================================================================================================

def episodios_ultimi(item):
    itemlist = []
    
    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.find_single_match(data, r'<h1 class="entry-title">Aggiornamento Episodi</h1>([^+]+)<div class="clear"></div>')
    patron = r'<h4><a href="([^"]+)">([^<]+)</a>\s*\(([^)]+)\)</h4>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle, scrapedepandlang in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedepandlang = scrapertools.decodeHtmlentities(scrapedepandlang.replace('&#215;', 'x'))
        seasonandep = scrapertools.find_single_match(scrapedepandlang, r'(\d+x[0-9\-?]+)')
        lang = scrapedepandlang.replace(seasonandep, "").strip()
        extra = r'%s(.*?)<br\s*/>'

        # Multi Ep
        if '-' in scrapedepandlang:
            season = scrapertools.find_single_match(scrapedepandlang, r'(\d+x)')
            scrapedepandlang = scrapedepandlang.split('-')
            for ep in scrapedepandlang:
                ep = (season + ep if season not in ep else ep).replace(lang, "")
                itemlist.append(infoSod(
                    Item(channel=__channel__,
                         action="episodios",
                         title="%s (%s %s)" % (scrapedtitle, ep, lang),
                         fulltitle=scrapedtitle,
                         show=scrapedtitle,
                         url=scrapedurl,
                         extra="%s (%s)" % (extra, (ep.replace('x', '×').replace(lang, '').strip())),
                         folder=True), tipo='tv'))
            continue
        
        # Ep singolo
        extra = extra % (scrapedepandlang.replace('x', '×').replace(lang, '').strip())
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findepvideos",
                 title="%s (%s)" % (scrapedtitle, scrapedepandlang),
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 url=scrapedurl,
                 extra=extra,
                 folder=True), tipo='tv'))

    return itemlist

# ==============================================================================================================================================

def lista(item):
    logger.info("pureita.italiaserie peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<li><a href="([^"]+)".*?>([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        if scrapedtitle.startswith("Link to "):
            scrapedtitle = scrapedtitle[8:]
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 plot=scrapedplot,
                 folder=True))




    return itemlist
	
# ==============================================================================================================================================	
def lista_tv(item):
    logger.info("pureita.italiaserie peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    blocco = scrapertools.find_single_match(data, r'<a href="[^"]+" title="Mini-serie">Mini-serie<\/a><ul>(.*?)<strong>Categoria:<\/strong>')

    # Extrae las entradas (carpetas)
    patron = '<li><a href="([^"]+)".*?>([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        scrapedplot = ""
        if scrapedtitle.startswith("Link to "):
            scrapedtitle = scrapedtitle[8:]
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 plot=scrapedplot,
                 folder=True))




    return itemlist
	
	
# ==============================================================================================================================================

def top(item):
    logger.info("pureita.italiaserie top")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<h3><a href="([^"]+)">(.*?)</a></h3>\s*<p><a href="[^"]+"><img class=".*? src="([^"]+)" alt="[^>]+" /></a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl)
        start = html.find("<div class=\"entry-content\">")
        end = html.find("</p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    return itemlist

# ==============================================================================================================================================

def findvideos(item):
    logger.info("pureita.italiaserie findvideos")

    # Descarga la página
    data = item.url

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist

# ==============================================================================================================================================

def findepvideos(item):
    logger.info("streamondemand.italiaserie findepvideos")

    # Carica la pagina 
    data = httptools.downloadpage(item.url).data
    
    if 'CLICCA QUI PER GUARDARE TUTTI GLI EPISODI' in data:
        item.url = re.sub('\-\d+', '-links', item.url)
        data = httptools.downloadpage(item.url).data
        data = scrapertools.decodeHtmlentities(data)

    data = scrapertools.find_single_match(data, item.extra)
    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join(["[%s] " % ("[COLOR orange]" + server.capitalize() + "[/COLOR]"), item.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist	

# ==============================================================================================================================================
	
def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")