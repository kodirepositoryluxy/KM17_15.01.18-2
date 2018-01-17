# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale per http://redanimedatabase.forumcommunity.net/
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# By DrZ3r0
# ------------------------------------------------------------

import re
import urlparse

from core import httptools, scrapertools, servertools
from core.item import Item
from lib.fuzzywuzzy import fuzz
from servers.decrypters import expurl
from platformcode import logger

__channel__ = "redanimedatabase"

host = "http://redanimedatabase.forumcommunity.net"

headers = [['Referer', host]]


# ----------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info("[RedAnimeDatabase.py]==> mainlist")
    itemlist = [
        Item(
            channel=__channel__,
            action="lista_anime",
            title=color("Lista Anime", "azure"),
            url="%s/?t=53406771" % host,
            thumbnail="http://static.europosters.cz/image/750/poster/street-fighter-anime-i4817.jpg"),
        Item(
            channel=__channel__,
            title="[COLOR yellow]Cerca...[/COLOR]",
            action="search",
            thumbnail=
            "http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")
    ]

    return itemlist


# ================================================================================================================


# ----------------------------------------------------------------------------------------------------------------
def search(item, texto):
    logger.info("[RedAnimeDatabase.py]==> " + item.url + " search " + texto)

    item.url = "%s/?t=53406771" % host

    try:
        itemlist = []

        data = httptools.downloadpage(item.url, headers=headers).data

        patron = r'<a\s*href="(\?t=\d+)"[^>]*?><span[^>]*?><b>([^>]+)</b></span></a>'
        matches = re.compile(patron, re.DOTALL).findall(data)

        for scrapedurl, scrapedtitle in matches:
            scrapedtitle = scrapertools.decodeHtmlentities(
                scrapedtitle.strip())
            # Clean up a bit the returned title to improve the fuzzy matching
            title_search = re.sub(r'\(.*\)', '',
                                  scrapedtitle)  # Anything within ()
            title_search = re.sub(r'\[.*\]', '',
                                  title_search)  # Anything within []

            # Check if the found title fuzzy matches the searched one
            if fuzz.WRatio(texto, title_search) > 85:

                scrapedurl = urlparse.urljoin(item.url, scrapedurl)
                itemlist.append(
                    Item(
                        channel=__channel__,
                        action="episodios",
                        title=scrapedtitle,
                        fulltitle=scrapedtitle,
                        url=scrapedurl,
                        thumbnail="",
                        show=scrapedtitle,
                        folder=True))

        return itemlist

    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


# ================================================================================================================


# ----------------------------------------------------------------------------------------------------------------
def lista_anime(item):
    logger.info("[RedAnimeDatabase.py]==> lista_anime")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = r'<a\s*href="(\?t=\d+)"[^>]*?><span[^>]*?><b>([^>]+)</b></span></a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.strip())
        scrapedurl = urlparse.urljoin(item.url, scrapedurl)
        itemlist.append(
            Item(
                channel=__channel__,
                action="episodios",
                title=scrapedtitle,
                fulltitle=scrapedtitle,
                url=scrapedurl,
                thumbnail="",
                show=scrapedtitle,
                folder=True))

    return itemlist


# ================================================================================================================


# ----------------------------------------------------------------------------------------------------------------
def episodios(item):
    logger.info("[RedAnimeDatabase.py]==> episodi")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    for blocco in scrapertools.find_multiple_matches(
            data,
            r'</div>\s*<td class="right Item" width="\d+%">(.*?)</table>'):

        patron = r'(<a href="[^"]+" target="_blank">)(?:<span[^>]*?>)?((?:Episodio|Streaming)\s*[0-9\.]*).*?(?:</span>)?</a>'
        matches = re.compile(patron, re.DOTALL).findall(blocco)

        for scrapedhtml, scrapedtitle in matches:
            if "animeliberoita.forumfree.it/?t=" in scrapedhtml:
                # vado di ricorsione su animeliberoita
                item.url = scrapertools.find_single_match(scrapedhtml, r'href="([^"]+)"')
                return episodios(item)
            if "Movie" in scrapedtitle or "Special" in scrapedtitle or "OAV" in scrapedtitle:
                continue  # Salto gli OAV e i movies
            if len(itemlist) > 0 and "Streaming" in scrapedtitle:
                # Se c'è un link alternativo dello stesso episodio unisco la sua parte HTML con quella dell'item precedente e continuo senza aggiungere l'item
                itemlist[-1].url += scrapedhtml
            else:
                itemlist.append(
                    Item(
                        channel=__channel__,
                        action="findvideos",
                        title=scrapedtitle,
                        fulltitle=scrapedtitle,
                        contentType="episode",
                        url=scrapedhtml,
                        thumbnail=item.thumbnail,
                        folder=True))
    return itemlist


# ================================================================================================================


# ----------------------------------------------------------------------------------------------------------------
def findvideos(item):
    logger.info("[RedAnimeDatabase.py]==> findvideos")

    for url in scrapertools.find_multiple_matches(item.url, r'href="([^"]+)'):
        item.url += '\n' + expurl.expand_url(url)

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        server = re.sub(r'[-\[\]\s]+', '', videoitem.title)
        videoitem.title = "".join(
            ["[%s] " % color(server, 'orange'), item.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__
    return itemlist


# ================================================================================================================


# ----------------------------------------------------------------------------------------------------------------
def color(text, color):
    return "[COLOR " + color + "]" + text + "[/COLOR]"


def HomePage(item):
    import xbmc
    xbmc.executebuiltin(
        "ReplaceWindow(10024,plugin://plugin.video.streamondemand)")


# ================================================================================================================
