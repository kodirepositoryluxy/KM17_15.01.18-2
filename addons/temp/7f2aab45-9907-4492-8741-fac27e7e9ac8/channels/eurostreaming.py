# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale  per eurostreaming.tv
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import urlparse

from core import config, httptools, scrapertools, servertools
from core.item import Item
from core.tmdb import infoSod
from platformcode import logger
from servers.decrypters import expurl

__channel__ = "eurostreaming"

host = "https://eurostreaming.club"


def mainlist(item):
    logger.info("streamondemand.eurostreaming mainlist")
    itemlist = [
        Item(
            channel=__channel__,
            title="[COLOR azure]Serie TV[/COLOR]",
            action="serietv",
            extra='serie',
            url="%s/category/serie-tv-archive/" % host,
            thumbnail=
            "http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"
        ),
        Item(
            channel=__channel__,
            title="[COLOR azure]Anime / Cartoni[/COLOR]",
            action="serietv",
            extra='serie',
            url="%s/category/anime-cartoni-animati/" % host,
            thumbnail=
            "http://orig09.deviantart.net/df5a/f/2014/169/2/a/fist_of_the_north_star_folder_icon_by_minacsky_saya-d7mq8c8.png"
        ),
        Item(
            channel=__channel__,
            title="[COLOR yellow]Cerca...[/COLOR]",
            action="search",
            extra='serie',
            thumbnail=
            "http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")
    ]

    return itemlist


def serietv(item):
    logger.info("streamondemand.eurostreaming peliculas")
    itemlist = []

    # Carica la pagina
    data = httptools.downloadpage(item.url).data

    # Estrae i contenuti
    patron = '<div class="post-thumb">\s*<a href="([^"]+)" title="([^"]+)">\s*<img src="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("Streaming", ""))
        if scrapedtitle.startswith("Link to "):
            scrapedtitle = scrapedtitle[8:]
        num = scrapertools.find_single_match(scrapedurl, '(-\d+/)')
        if num:
            scrapedurl = scrapedurl.replace(num, "-episodi/")
        itemlist.append(
            infoSod(
                Item(
                    channel=__channel__,
                    action="episodios",
                    fulltitle=scrapedtitle,
                    show=scrapedtitle,
                    title=scrapedtitle,
                    url=scrapedurl,
                    thumbnail=scrapedthumbnail,
                    plot=scrapedplot,
                    extra=item.extra,
                    folder=True),
                tipo='tv'))

    # Paginazione
    patronvideos = '<a class="next page-numbers" href="?([^>"]+)">Avanti &raquo;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(
                channel=__channel__,
                action="HomePage",
                title="[COLOR yellow]Torna Home[/COLOR]",
                folder=True)),
        itemlist.append(
            Item(
                channel=__channel__,
                action="serietv",
                title="[COLOR orange]Successivo >>[/COLOR]",
                url=scrapedurl,
                thumbnail=
                "http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                extra=item.extra,
                folder=True))

    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")


def search(item, texto):
    logger.info("[eurostreaming.py] " + item.url + " search " + texto)
    item.url = "%s/?s=%s" % (host, texto)
    try:
        return serietv(item)
    # Continua la ricerca in caso di errore
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def episodios(item):
    def load_episodios():
        for data in match.split('<br />'):
            ## Estrae i contenuti
            end = data.find('<a ')
            if end > 0:
                scrapedtitle = scrapertools.find_single_match(data[:end], '\d+[^\d]+\d+')
                scrapedtitle = scrapedtitle.replace('×', 'x')
                itemlist.append(
                    Item(
                        channel=__channel__,
                        action="findvideos",
                        contentType="episode",
                        title=scrapedtitle + " (" + lang_title + ")",
                        url=data,
                        thumbnail=item.thumbnail,
                        extra=item.extra,
                        fulltitle=scrapedtitle + " (" + lang_title + ")" + ' - ' + item.show,
                        show=item.show))

    logger.info("[eurostreaming.py] episodios")

    itemlist = []

    ## Carica la pagina
    data = httptools.downloadpage(item.url).data

    patron = r"onclick=\"top.location=atob\('([^']+)'\)\""
    b64_link = scrapertools.find_single_match(data, patron)
    if b64_link != '':
        import base64
        data = httptools.downloadpage(base64.b64decode(b64_link)).data

    patron = r'<a href="(%s/\?p=\d+)">' % host
    link = scrapertools.find_single_match(data, patron)
    if link != '':
        data = httptools.downloadpage(link).data

    data = scrapertools.decodeHtmlentities(data)

    patron = '</span>([^<]+)</div><div class="su-spoiler-content su-clearfix" style="display:none">(.+?)</div></div></div>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for lang_title, match in matches:
        lang_title = 'SUB ITA' if 'SUB' in lang_title.upper() else 'ITA'
        load_episodios()

    patron = '<li><span style="[^"]+"><a onclick="[^"]+" href="[^"]+">([^<]+)</a>(?:</span>\s*<span style="[^"]+"><strong>([^<]+)</strong>)?</span>(.*?)</div>\s*</li>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for lang_title1, lang_title2, match in matches:
        lang_title = 'SUB ITA' if 'SUB' in (
            lang_title1 + lang_title2).upper() else 'ITA'
        load_episodios()

    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(
                channel=__channel__,
                title="Aggiungi alla libreria",
                url=item.url,
                action="add_serie_to_library",
                extra="episodios" + "###" + item.extra,
                show=item.show))

    return itemlist


def findvideos(item):
    logger.info("streamondemand.eurostreaming findvideos")
    itemlist = []

    patron = '<a href="([^"]+)" target=[^>]+>(.*?)<'
    #patron = '<a href="(.*?)" target="_blank"[^>]+>(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(item.url)

    for scrapedurl, scrapedserver in matches:

        if scrapedserver.startswith(("DeltaBit")):
            continue

        itemlist.append(
            Item(
                channel=__channel__,
                action="play",
                fulltitle=item.scrapedtitle,
                show=item.scrapedtitle,
                title="[COLOR blue]" + item.title + "[/COLOR][COLOR orange]" + scrapedserver + "[/COLOR]",
                url=scrapedurl,
                thumbnail=item.scrapedthumbnail,
                plot=item.scrapedplot,
                folder=True))

    return itemlist


def play(item):
    itemlist = []

    data = item.url
    while 'vcrypt' in data or 'linkup' in data and 'cryptmango' not in data:
        data = httptools.downloadpage(data, only_headers=True, follow_redirects=False).headers.get("location", "")

    data = expurl.expand_url(data)

    while 'vcrypt' in data or 'linkup' in data and 'cryptmango' not in data:
        data = httptools.downloadpage(data, only_headers=True, follow_redirects=False).headers.get("location", "")

    if 'cryptmango' in data:
        data = httptools.downloadpage(data).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
