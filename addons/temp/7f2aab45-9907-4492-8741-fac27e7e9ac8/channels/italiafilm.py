# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale italiafilm
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import time
import urlparse
from datetime import date

from core import config, httptools
from platformcode import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "italiafilm"

host = "http://www.italia-film.online"

headers = [['Referer', host]]


def mainlist(item):
    logger.info("[italiafilm.py] mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film - Novita'[/COLOR]",
                     action="peliculas",
                     extra="movie",
                     url="%s/category/film-streaming-%s/" % (host, date.today().year),
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film HD[/COLOR]",
                     action="peliculas",
                     extra="movie",
                     url="%s/category/film-hd/" % host,
                     thumbnail="http://i.imgur.com/3ED6lOP.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Categorie[/COLOR]",
                     action="categorias",
                     extra="movie",
                     url="%s/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     action="peliculas_tv",
                     extra="serie",
                     url="%s/category/serie-tv/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Ultime serie TV[/COLOR]",
                     action="pel_tv",
                     extra="serie",
                     url="%s/ultimi-telefilm-streaming/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Ultime Episodi[/COLOR]",
                     action="latestep",
                     extra="serie",
                     url="%s/ultime-serie-tv-streaming/" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]
    return itemlist


def newest(categoria):
    logger.info("[italiafilm.py] newest" + categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == "peliculas":
            item.url = "%s/category/film-streaming-%s/" % (host, date.today().year)
            item.action = "peliculas"
            item.extra = "movie"
            itemlist = peliculas(item)

            if itemlist[-1].action == "peliculas":
                itemlist.pop()
        elif categoria == "series":
            item.url = "%s/ultime-serie-tv-streaming/" % host
            item.action = "latestep"
            itemlist = latestep(item)

            if itemlist[-1].action == "series":
                itemlist.pop()

    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist


def categorias(item):
    logger.info("[italiafilm.py] categorias")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    data = scrapertools.find_single_match(data, '<a href=".">Categorie</a>(.*?)</div>')

    patron = '<li[^>]+><a href="([^"]+)">Film([^<]+)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for url, title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url, url)

        if scrapedtitle.startswith((" XXX")):
            continue

        scrapedplot = ""
        scrapedthumbnail = ""
        itemlist.append(
            Item(channel=__channel__,
                 action='peliculas',
                 extra=item.extra,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    return itemlist


def search(item, texto):
    logger.info("[italiafilm.py] search " + texto)
    item.url = host + "/?s=" + texto

    try:
        if item.extra == "movie":
            return peliculas(item)
        if item.extra == "serie":
            return peliculas_tv(item)
    # Se captura la excepcion, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

def latestep(item):
    logger.info("[italiafilm.py] latestep")
    itemlist = []

    data = httptools.downloadpage(item.url).data
    blocco = scrapertools.find_single_match(data, r'<li class="section_date">(.*?)<li class="section_date">')
    patron = r'<li class="[^"]+">\s*[^>]+>([^<|^(]+)[^>]+>\s*<a href="([^"]+)"'
    patron += r'[^>]+>[^>]+>[^>]+>(?:[^>]+>[^>]+>|)([^<]+)(?:[^>]+>[^>]+>|)</a>'
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedtitle, scrapedurl, scrapedepisode in matches:
        scrapedepisode = scrapertools.decodeHtmlentities(scrapedepisode)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        completetitle = "%s - %s" % (scrapedtitle, scrapedepisode)

        unsupportedeps = re.compile(r'\d+\-\d+', re.DOTALL).findall(scrapedepisode)
        if len(unsupportedeps) > 0:
            continue

        if 'completa' in scrapedtitle.lower():
            itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=completetitle,
                 contentSerieName=completetitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 folder=True), tipo='tv'))
        else:
            if 'episodio' not in scrapedepisode:
                replace = re.compile(r'(\d+)x(\d+)')
                ep_pattern = r'%s(.*?(?:<br\s*/>|</p>))' % replace.sub(r'\g<1>&#215;\g<2>', scrapedepisode)
            else:
                ep_pattern = r'%s(.*?(?:<br\s*/>|</p>))' % scrapedepisode

            itemlist.append(infoSod(
                Item(channel=__channel__,
                    action="findvideos_single_ep",
                    title=completetitle,
                    contentSerieName=completetitle,
                    fulltitle=scrapedtitle,
                    url=scrapedurl,
                    extra=ep_pattern,
                    folder=True), tipo='tv'))

    return itemlist

def peliculas(item):
    logger.info("[italiafilm.py] peliculas")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<article(.*?)</article>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for match in matches:
        title = scrapertools.find_single_match(match, '<h3[^<]+<a href="[^"]+"[^<]+>([^<]+)</a>')
        title = title.replace("Streaming", "")
        title = scrapertools.decodeHtmlentities(title).strip()
        url = scrapertools.find_single_match(match, '<h3[^<]+<a href="([^"]+)"')
        plot = ""
        thumbnail = scrapertools.find_single_match(match, 'data-echo="([^"]+)"')

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action='episodios' if item.extra == 'serie' else 'findvid',
                 contentType="movie",
                 fulltitle=title,
                 show=title,
                 title="[COLOR azure]" + title + "[/COLOR]",
                 url=url,
                 thumbnail=thumbnail,
                 plot=plot,
                 viewmode="movie_with_plot",
                 folder=True), tipo='movie'))

    # Siguiente
    try:
        pagina_siguiente = scrapertools.get_match(data, '<a class="next page-numbers" href="([^"]+)"')
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 extra=item.extra,
                 title="[COLOR orange]Successivo >> [/COLOR]",
                 url=pagina_siguiente,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))
    except:
        pass

    return itemlist


def findvid(item):
    logger.info("streamondemand.italiafilm findvid")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti 
    patron = '<iframe style="border: 0;" src="([^"]+)" width="[^"]*" height="[^"]*" scrolling="[^"]*" allowfullscreen="[^"]*">'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl in matches:
        data += httptools.downloadpage(scrapedurl, headers=headers).data

    ### robalo fix obfuscator - start ####

    patron = 'href="(https?://www\.keeplinks\.eu/p16/([^"]+))"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for keeplinks, id in matches:
        headers.append(['Cookie', 'flag[' + id + ']=1; defaults=1; nopopatall=' + str(int(time.time()))])
        headers.append(['Referer', keeplinks])

        html = httptools.downloadpage(keeplinks, headers=headers).data
        data += str(scrapertools.find_multiple_matches(html, '<a href="([^"]+)" target="_blank"'))

    ### robalo fix obfuscator - end ####

    for videoitem in servertools.find_video_items(data=data):
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__
        itemlist.append(videoitem)

    return itemlist


def peliculas_tv(item):
    logger.info("[italiafilm.py] peliculas")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<article(.*?)</article>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for match in matches:
        title = scrapertools.find_single_match(match, '<h3[^<]+<a href="[^"]+"[^<]+>([^<]+)</a>')
        title = title.replace("Streaming", "")
        title = scrapertools.decodeHtmlentities(title).strip()
        show_title = re.sub('\(.*?\)', '', title.replace('Serie TV', ''))
        url = scrapertools.find_single_match(match, '<h3[^<]+<a href="([^"]+)"')
        plot = ""
        thumbnail = scrapertools.find_single_match(match, 'data-echo="([^"]+)"')

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action='episodios' if item.extra == 'serie' else 'findvideos',
                 fulltitle=title,
                 show=show_title,
                 title="[COLOR azure]" + title + "[/COLOR]",
                 url=url,
                 thumbnail=thumbnail,
                 plot=plot,
                 viewmode="movie_with_plot",
                 folder=True), tipo='tv'))

    # Siguiente
    try:
        pagina_siguiente = scrapertools.get_match(data, '<a class="next page-numbers" href="([^"]+)"')
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_tv",
                 extra=item.extra,
                 title="[COLOR orange]Successivo >> [/COLOR]",
                 url=pagina_siguiente,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))
    except:
        pass

    return itemlist


def pel_tv(item):
    logger.info("[italiafilm.py] peliculas")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<span class="tvseries_name">(.*?)</span>\s*<a href="([^"]+)"[^>]+><i class="icon-link"></i>(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scraptitle1, scrapedurl, scraptitle2 in matches:
        title = scraptitle1 + scraptitle2
        plot = ""
        thumbnail = ""
        url = scrapedurl

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action='episodios' if item.extra == 'serie' else 'findvideos',
                 fulltitle=title,
                 show=title,
                 title="[COLOR azure]" + title + "[/COLOR]",
                 url=url,
                 thumbnail=thumbnail,
                 plot=plot,
                 viewmode="movie_with_plot",
                 folder=True), tipo='tv'))

    # Siguiente
    try:
        pagina_siguiente = scrapertools.get_match(data, '<a class="next page-numbers" href="([^"]+)"')
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="pel_tv",
                 extra=item.extra,
                 title="[COLOR orange]Successivo >> [/COLOR]",
                 url=pagina_siguiente,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))
    except:
        pass

    return itemlist


def episodios(item):
    def load_episodios(html, item, itemlist, lang_title):
        for data in scrapertools.decodeHtmlentities(html).splitlines():
            # Estrae i contenuti 
            end = data.find('<a ')
            if end > 0:
                scrapedtitle = re.sub(r'<[^>]*>', '', data[:end]).strip()
            else:
                scrapedtitle = ''
            if scrapedtitle == '':
                patron = '<a\s*href="[^"]+"\s*target="_blank">([^<]+)</a>'
                scrapedtitle = scrapertools.find_single_match(data, patron).strip()
            title = scrapertools.find_single_match(scrapedtitle, '\d+[^\d]+\d+')
            if title == '':
                title = scrapedtitle
            if title != '':
                title = re.sub(r"(\d+)[^\d]+(\d+)", r"\1x\2", title)
                title += " (" + lang_title + ")"
                itemlist.append(
                    Item(channel=__channel__,
                         action="findvideos",
                         contentType="episode",
                         title=title,
                         url=data,
                         thumbnail=item.thumbnail,
                         extra=item.extra,
                         fulltitle=title + ' - ' + item.show,
                         show=item.show))

    logger.info("[italiafilm.py] episodios")

    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    start = data.find('id="pd_rating_holder')
    end = data.find('id="linkcorrotto-show"', start)

    data = data[start:end]

    lang_titles = []
    starts = []
    patron = r"STAGION[I|E](.*?ITA)?"
    matches = re.compile(patron, re.IGNORECASE).finditer(data)
    for match in matches:
        season_title = match.group()
        # if season_title != '':
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

    if len(itemlist) == 0:
        load_episodios(data, item, itemlist, 'ITA')

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
    logger.info("streamondemand.italiafilm findvideos")

    # Carica la pagina 
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

def findvideos_single_ep(item):
    logger.info("[italiafilm.py] findvideos_single_ep")
    
    data = httptools.downloadpage(item.url).data

    data = scrapertools.find_single_match(data, item.extra)

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join(["[[COLOR orange]%s[/COLOR]] " % server.capitalize(), item.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")
