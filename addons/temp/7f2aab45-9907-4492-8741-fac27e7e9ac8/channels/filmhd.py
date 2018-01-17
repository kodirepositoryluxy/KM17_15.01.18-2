# -*- coding: utf-8 -*-

from core import httptools, scrapertools
from core.item import Item
from core.tmdb import infoSod
from platformcode import logger

__channel__ = "filmhd"

host = "http://filmhd.me"


def mainlist(item):
    logger.info(" mainlist")

    itemlist = [
        Item(
            channel=__channel__,
            title="[COLOR azure]Film - Novita'[/COLOR]",
            action="movies",
            url=host,
            thumbnail=
            "http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"
        ),
        Item(
            channel=__channel__,
            title="[COLOR azure]Film - 3D[/COLOR]",
            action="movies",
            url="%s/genere/3d/" % host,
            thumbnail=
            "http://files.softicons.com/download/computer-icons/disks-icons-by-wil-nichols/png/256x256/Blu-Ray.png"
        ),
        Item(
            channel=__channel__,
            title="[COLOR azure]Film - Per Genere[/COLOR]",
            action="genre",
            url=host,
            thumbnail=
            "https://farm8.staticflickr.com/7562/15516589868_13689936d0_o.png"
        ),
        Item(
            channel=__channel__,
            title="[COLOR azure]Film - Per anno[/COLOR]",
            action="genre_years",
            url=host,
            thumbnail=
            "http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"
        ),
        Item(
            channel=__channel__,
            title="[COLOR azure]Film - Per Paese[/COLOR]",
            action="genre_country",
            url=host,
            thumbnail=
            "http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"
        ),
        Item(
            channel=__channel__,
            title="[COLOR azure]Film - A-Z[/COLOR]",
            action="genre_az",
            url=host,
            thumbnail=
            "http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"
        ),
        Item(
            channel=__channel__,
            title="[COLOR yellow]Cerca...[/COLOR]",
            action="search",
            extra="movie",
            thumbnail=
            "http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")
    ]

    return itemlist


def search(item, texto):
    logger.info(" " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return movies_search(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def movies_search(item):
    logger.info(" movies_search")

    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    patron = '<\/div>\s*<a href="([^"]+)">\s*<div class="movie-play">\s*'
    patron += '<i class="icon-controller-play"></i>\s*</div>\s*<img src="([^"]+)">[^>]+>[^>]+>[^>]+>[^>]+>([^<]+)</h2>'

    matches = scrapertools.find_multiple_matches(data, patron)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        # ------------------------------------------------
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        # ------------------------------------------------
        itemlist.append(
            infoSod(
                Item(
                    channel=__channel__,
                    action="findvideos",
                    title=scrapedtitle,
                    url=scrapedurl,
                    thumbnail=scrapedthumbnail,
                    fulltitle=scrapedtitle,
                    show=scrapedtitle),
                tipo='movie'))

    return itemlist


def genre(item):
    logger.info(" genre")
    itemlist = []

    data = httptools.downloadpage(item.url).data

    patron = '<li class="dropdown genre-filter">(.*?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<a href="([^"]+)">([^<]+)</a></label>'
    matches = scrapertools.find_multiple_matches(data, patron)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(
                channel=__channel__,
                action="movies",
                title=scrapedtitle,
                url=scrapedurl,
                thumbnail=
                "https://farm8.staticflickr.com/7562/15516589868_13689936d0_o.png",
                folder=True))

    return itemlist


def genre_years(item):
    logger.info(" genre_years")
    itemlist = []

    data = httptools.downloadpage(item.url).data

    patron = '<div class="dropdown-toggle" data-toggle="dropdown">Anno<i class="icon-chevron-down"></i></div>(.*?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = scrapertools.find_multiple_matches(data, patron)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(
                channel=__channel__,
                action="movies",
                title=scrapedtitle,
                url=scrapedurl,
                thumbnail=
                "http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png",
                folder=True))

    return itemlist


def genre_country(item):
    logger.info(" genre_country")
    itemlist = []

    data = httptools.downloadpage(item.url).data

    patron = '<div class="dropdown-toggle" data-toggle="dropdown">Nazione<i class="icon-chevron-down"></i></div>(.*?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li><a href="(.*?)\s*">([^<]+)</a></li>'
    matches = scrapertools.find_multiple_matches(data, patron)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(
                channel=__channel__,
                action="movies",
                title=scrapedtitle,
                url=scrapedurl,
                thumbnail=
                "http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png",
                folder=True))

    return itemlist


def genre_az(item):
    logger.info(" genre_az")
    itemlist = []

    data = httptools.downloadpage(item.url).data

    patron = '<li class="dropdown abc-filter">(.*?)</ul>'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li class="abc"><a href="([^"]+)">([^<]+)</a></li>'
    matches = scrapertools.find_multiple_matches(data, patron)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(
                channel=__channel__,
                action="movies",
                title=scrapedtitle,
                url=scrapedurl,
                thumbnail=
                "http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png",
                folder=True))

    return itemlist


def movies(item):
    logger.info(" movies")

    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url).data

    patron = '<a href="([^"]+)">\s*<div class="movie-play">\s*<i class="icon-controller-play"></i>\s*</div>\s*<img src="([^"]+)" alt="([^<]+)">'

    matches = scrapertools.find_multiple_matches(data, patron)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        # ------------------------------------------------
        scrapedthumbnail = httptools.get_url_headers(scrapedthumbnail)
        # ------------------------------------------------
        itemlist.append(
            infoSod(
                Item(
                    channel=__channel__,
                    action="findvideos",
                    title=scrapedtitle,
                    url=scrapedurl,
                    thumbnail=scrapedthumbnail,
                    fulltitle=scrapedtitle,
                    show=scrapedtitle),
                tipo='movie'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class="nextpostslink" href="([^"]+)">»</a>')
    if next_page:
        itemlist.append(
            Item(
                channel=__channel__,
                action="movies",
                title="[COLOR orange]Successivo >>[/COLOR]",
                url=next_page,
                thumbnail=
                "http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"
            ))

    return itemlist
