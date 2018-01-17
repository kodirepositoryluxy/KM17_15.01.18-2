# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale per cb01.io
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# Version: 201706200900
# By Errmax
# ------------------------------------------------------------
import re
import urlparse

from core import httptools, scrapertools, servertools
from core.item import Item
from core.tmdb import infoSod
from platformcode import logger

__channel__ = "cb01io"

host = "https://www.cb01.io"

headers = [['Referer', host]]


def mainlist(item):
    logger.info("[cineblog01.py] mainlist")

    # Main options
    itemlist = [
        Item(
            channel=__channel__,
            action="peliculas",
            title="[COLOR azure]Novità[/COLOR]",
            url=host,
            extra="movie",
            thumbnail=
            "http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"
        ),
        Item(
            channel=__channel__,
            action="menuhd",
            title="[COLOR azure]Menù HD[/COLOR]",
            url=host,
            extra="movie",
            thumbnail="http://jcrent.com/apple%20tv%20final/HD.png"),
        Item(
            channel=__channel__,
            action="menugenere",
            title="[COLOR azure]Per Genere[/COLOR]",
            url=host,
            extra="movie",
            thumbnail=
            "http://web.simmons.edu/~griffims/lis488/Genre%20Icons.jpg"),
        Item(
            channel=__channel__,
            action="menuanno",
            title="[COLOR azure]Per Anno[/COLOR]",
            url=host,
            extra="movie",
            thumbnail=
            "https://onlinefundraisingtoday2.files.wordpress.com/2011/10/end-of-year-crop.jpg?w=798"
        ),
        Item(
            channel=__channel__,
            action="menupaese",
            title="[COLOR azure]Per Paese[/COLOR]",
            url=host,
            extra="movie",
            thumbnail=
            "https://static1.squarespace.com/static/5009bba4e4b016a023bf6030/t/55819e7be4b040a431866acf/1434558079283/Country_Flags_Wallpaper_sz4qp.jpg?format=1500w"
        ),
        Item(
            channel=__channel__,
            action="search",
            title="[COLOR yellow]Cerca Film[/COLOR]",
            extra="movie",
            thumbnail=
            "https://lh3.googleusercontent.com/06iPDBYaBMSAufCp_MvFpfW-P7LMZSzYsFAyx_5Aw05RbLIhSjgGxpuHrzcRpPYG7U8=w300"
        )
    ]

    return itemlist


def peliculas(item):
    logger.info("[cineblog01.py] peliculas")
    itemlist = []

    if not item.url:
        item.url = host

    # Carica la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti
    patronvideos = 'class="filmbox".*?href="([^"]+)".*?src="([^"]+)".*?'
    patronvideos += '<h1>([^<]+)<.*?<h2.*?>([^<]+)<.*?<p>(.*?)<\/p>'
    matches = re.compile(patronvideos, re.DOTALL).finditer(data)

    for match in matches:
        scrapedurl = urlparse.urljoin(item.url, match.group(1))

        # Bypass fake links
        html = httptools.downloadpage(scrapedurl).data
        if '<h2>Streaming:</h2>' not in html: continue

        scrapedtitle = scrapertools.unescape(match.group(3))
        scrapedthumbnail = urlparse.urljoin(item.url, match.group(2))
        scrapedthumbnail = scrapedthumbnail.replace(" ", "%20")
        scrapedplot = scrapertools.unescape("[COLOR orange]" + match.group(4) + "[/COLOR]\n" + match.group(5).strip())
        scrapedplot = scrapertools.htmlclean(scrapedplot).strip()

        itemlist.append(
            infoSod(
                Item(
                    channel=__channel__,
                    action="findvid_film",
                    contentType="movie",
                    fulltitle=scrapedtitle,
                    show=scrapedtitle,
                    title=scrapedtitle,
                    url=scrapedurl,
                    thumbnail=scrapedthumbnail,
                    plot=scrapedplot,
                    extra=item.extra,
                    viewmode="movie_with_plot"),
                tipo='movie'))

    # Paginazione
    patronvideos = '<span>[^<]+</span> <a href="(.*?)">'
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
                extra=item.extra,
                action="peliculas",
                title="[COLOR orange]Successivo >>[/COLOR]",
                url=scrapedurl,
                thumbnail=
                "http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                folder=True))

    return itemlist


def menu_list(item, opttxt):
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    # Narrow search by selecting only the combo
    bloque = re.search("<select.*?%s[^>]+>(.*?)<\/select" % opttxt, data,  re.S | re.I)

    if bloque:
        # The categories are the options for the combo
        patron = '<option value="([^"]+)">([^<]+)</option>'
        matches = re.compile(patron, re.DOTALL).findall(bloque.group(1))
        scrapertools.printMatches(matches)

        for url, titulo in matches:
            scrapedtitle = titulo
            scrapedurl = host + url
            scrapedthumbnail = ""
            scrapedplot = ""
            itemlist.append(
                Item(
                    channel=__channel__,
                    action="peliculas",
                    title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                    url=scrapedurl,
                    thumbnail=scrapedthumbnail,
                    extra=item.extra,
                    plot=scrapedplot))

    return itemlist


def menugenere(item):
    logger.info("[cineblog01.py] menugenere")
    return menu_list(item, "Film per Genere")


def menuhd(item):
    logger.info("[cineblog01.py] menuhd")
    return menu_list(item, "Film per Qualit")


def menuanno(item):
    logger.info("[cineblog01.py] menuanno")
    return menu_list(item, "Film per Anno")


def menupaese(item):
    logger.info("[cineblog01.py] menuanno")
    return menu_list(item, "Film per P..se")


# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item, texto):
    logger.info("[cineblog01.py] " + item.url + " search " + texto)

    try:

        item.url = host + "/?do=search&subaction=search&story=" + texto
        return peliculas(item)

    # Continua la ricerca in caso di errore
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def findvid_film(item):
    logger.info("[cineblog01.py] findvid_film")

    itemlist = []

    # Carica la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    data = scrapertools.decodeHtmlentities(data)

    # Extract the quality format
    patronvideos = 'Film per Qualit[^>]+>([^<]+)<'
    matches = re.compile(patronvideos, re.DOTALL).finditer(data)
    QualityStr = ""
    for match in matches:
        QualityStr = scrapertools.unescape(match.group(1))[6:]
    QualityStr = QualityStr.replace(" ", "")
    QualityStr = QualityStr.replace("\n", "")

    # Estrae i contenuti
    streaming = scrapertools.find_single_match(data, '<div class="box-link"(.*?)<\/div>')
    logger.info("streamin link block: %s" % streaming)
    patron = '<p><a href="([^"]+)".*?>([^<]+)<'
    matches = re.compile(patron, re.DOTALL).findall(streaming)
    for scrapedurl, scrapedtitle in matches:
        logger.debug("##### findvideos Streaming ## %s ## %s ##" % (scrapedurl, scrapedtitle))
        title = "[COLOR orange]Source:[/COLOR] [COLOR blue]" + scrapedtitle + "[/COLOR] [COLOR grey]" + QualityStr + "[/COLOR]"
        itemlist.append(
            Item(
                channel=__channel__,
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


def play(item):
    logger.info("[cineblog01.py] play")
    itemlist = []

    data = item.url
    logger.debug("##### play data ##%s##" % data)

    try:
        itemlist = servertools.find_video_items(data=data)

        for videoitem in itemlist:
            videoitem.title = item.show
            videoitem.fulltitle = item.fulltitle
            videoitem.show = item.show
            videoitem.thumbnail = item.thumbnail
            videoitem.channel = __channel__
    except AttributeError:
        logger.error("Error searching calling find_video_items")

    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")
