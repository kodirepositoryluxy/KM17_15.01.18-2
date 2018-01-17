# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale per http://manganimenod.it
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# By MrTruth
# ------------------------------------------------------------

import re

from core import logger, httptools
from core import scrapertools
from core.item import Item

__channel__ = "animenod"

host = "http://manganimenod.it"

headers = [['Referer', host]]


# ----------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info("[AnimeNOD.py]==> mainlist")
    itemlist = [Item(channel=__channel__,
                     action="episodi",
                     title=color("One Piece", "orange"),
                     url="%s/episodi.php?a=ONEPIECEM" % host,
                     thumbnail="http://manganimenod.it/homepage/onepieceover.jpg"),
                Item(channel=__channel__,
                     action="episodi",
                     title=color("Dragon Ball", "orange"),
                     url="%s/episodi.php?a=DRAGONBALL1" % host,
                     thumbnail="http://manganimenod.it/homepage/dragonballover.jpg"),
                Item(channel=__channel__,
                     action="episodi",
                     title=color("Fairy Tail", "orange"),
                     url="%s/episodi.php?a=FAIRYTAIL" % host,
                     thumbnail="http://manganimenod.it/Anime/FAIRYTAIL/imgSeason/01.jpg"),
                Item(channel=__channel__,
                     action="episodi",
                     title=color("Bleach", "orange"),
                     url="%s/episodi.php?a=BLEACH" % host,
                     thumbnail="http://manganimenod.it/menu2/img/bigAltreSerie.png"),
                Item(channel=__channel__,
                     action="episodi",
                     title=color("Cavalieri dello zodiaco", "orange"),
                     url="%s/episodi.php?a=CDZ" % host,
                     thumbnail="http://manganimenod.it/Anime/CDZ/imgSeason/01.jpg"),
                Item(channel=__channel__,
                     action="episodi",
                     title=color("Hunter x Hunter", "orange"),
                     url="%s/episodi.php?a=HUNTERXHUNTER" % host,
                     thumbnail="http://manganimenod.it/Anime/HUNTERXHUNTER/imgSeason/01.jpg")]

    return itemlist


# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def episodi(item):
    logger.info("[AnimeNOD.py]==> episodi")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data

    patron = '<div class="ep"><a href="([^"]+)"><.*?url\(\'(.*?)\'\).*?>[^>]+>[^>]+>[^>]+>'
    patron += '[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+><a .*?title="([^"]+)">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedimg, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 contentType="episode",
                 url="%s/%s" % (host, scrapedurl),
                 thumbnail=scrapedimg,
                 extra=item.extra,
                 folder=True))
    return itemlist


# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def color(text, color):
    return "[COLOR " + color + "]" + text + "[/COLOR]"

# ================================================================================================================
