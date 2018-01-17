# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita-master - XBMC Plugin
# Canale filmontv - Fix by Orione7
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808/
# ------------------------------------------------------------

import Queue
import glob
import imp
import os
import re
import threading
import time
import urllib

from core import channeltools
from core import config
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod
from lib.fuzzywuzzy import fuzz

__channel__ = "filmontv"
__category__ = "F"
__type__ = "generic"
__title__ = "filmontv.tv (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.comingsoon.it"

TIMEOUT_TOTAL = 60


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.filmontv mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR red]IN ONDA ADESSO[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/Menu/Menu_ricerca_pureita/inondaadesso_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Mattina[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=mt" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/Menu/Menu_ricerca_pureita/mattino_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Pomeriggio[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=pm" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/Menu/Menu_ricerca_pureita/pomeriggio_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Preserale[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=pr" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/Menu/Menu_ricerca_pureita/preserale_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Prima serata[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=ps" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/Menu/Menu_ricerca_pureita/primaserata_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Seconda serata[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=ss" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/Menu/Menu_ricerca_pureita/secondaserata_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Notte[/COLOR]",
                     action="tvoggi",
                     url="%s/filmtv/?range=nt" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/Menu/Menu_ricerca_pureita/notte_P.png")]

    return itemlist


def tvoggi(item):
    logger.info("streamondemand.filmontv tvoggi")
    itemlist = []

    # Pagina di Download
    data = scrapertools.cache_page(item.url)

    # Estrazioni voci (Cartelle)
    patron = '<div class="col-xs-5 box-immagine">\s*<img src="([^"]+)"[^>]+>\s*</div>\s*[^>]+>[^>]+>\s*[^>]+>\s*[^>]+>(.*?)</div>\s*[^>]+>[^>]+>[^>]+>[^>]+>(.*?)</div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, scrapedtv in matches:
        scrapedurl = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        titolo = urllib.quote_plus(scrapedtitle)
        if (DEBUG): logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="do_search",
                 extra=titolo,
                 title=scrapedtitle + "[COLOR yellow]   " + scrapedtv + "[/COLOR]",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="movie"))

    return itemlist


# Questa e la funzione che esegue effettivamete la ricerca

def do_search(item):
    logger.info("streamondemand.channels.buscador do_search")

    tecleado = item.extra
    mostra = item.fulltitle

    itemlist = []

    channels_path = os.path.join(config.get_runtime_path(), "channels", '*.xml')
    logger.info("streamondemand.channels.buscador channels_path=" + channels_path)

    channel_language = config.get_setting("channel_language")
    logger.info("streamondemand.channels.buscador channel_language=" + channel_language)
    if channel_language == "":
        channel_language = "all"
        logger.info("streamondemand.channels.buscador channel_language=" + channel_language)

    if config.is_xbmc():
        show_dialog = True

    try:
        import xbmcgui
        progreso = xbmcgui.DialogProgressBG()
        progreso.create("Ricerca di " + mostra)
    except:
        show_dialog = False

    def worker(infile, queue):
        channel_result_itemlist = []
        try:
            basename_without_extension = os.path.basename(infile)[:-4]
            # http://docs.python.org/library/imp.html?highlight=imp#module-imp
            obj = imp.load_source(basename_without_extension, infile[:-4]+".py")
            logger.info("streamondemand.channels.buscador cargado " + basename_without_extension + " de " + infile)
            channel_result_itemlist.extend(obj.search(Item(extra='movie'), tecleado))
            for item in channel_result_itemlist:
                item.title = " [COLOR azure] " + item.title + " [/COLOR] [COLOR orange]su[/COLOR] [COLOR orange]" + basename_without_extension + "[/COLOR]"
                item.viewmode = "list"
        except:
            import traceback
            logger.error(traceback.format_exc())
        queue.put(channel_result_itemlist)

    channel_files = glob.glob(channels_path)

    channel_files_tmp = []
    for infile in channel_files:

        basename_without_extension = os.path.basename(infile)[:-4]

        channel_parameters = channeltools.get_channel_parameters(basename_without_extension)

        # Non cercare se il canale e inattivo
        if channel_parameters["active"] != "true":
            continue

        # Non Cercare se in canale e escluso dalla ricerca globale
        if channel_parameters["include_in_global_search"] != "true":
            continue

        # Non cercare se il canale e per adulti e se la modalita adulti e disabilitata
        if channel_parameters["adult"] == "true" and config.get_setting("adult_mode") == "false":
            continue

        # Non cercare se il canale e in una lingua filtrata
        if channel_language != "all" and channel_parameters["language"] != channel_language:
            continue

        channel_files_tmp.append(infile)

    channel_files = channel_files_tmp

    result = Queue.Queue()
    threads = [threading.Thread(target=worker, args=(infile, result)) for infile in channel_files]

    start_time = int(time.time())

    for t in threads:
        t.daemon = True  # NOTE: setting dameon to True allows the main thread to exit even if there are threads still running
        t.start()

    number_of_channels = len(channel_files)
    completed_channels = 0
    while completed_channels < number_of_channels:

        delta_time = int(time.time()) - start_time
        if len(itemlist) <= 0:
            timeout = None  # No result so far,lets the thread to continue working until a result is returned
        elif delta_time >= TIMEOUT_TOTAL:
            break  # At least a result matching the searched title has been found, lets stop the search
        else:
            timeout = TIMEOUT_TOTAL - delta_time  # Still time to gather other results

        if show_dialog:
            progreso.update(completed_channels * 100 / number_of_channels)

        try:
            result_itemlist = result.get(timeout=timeout)
            completed_channels += 1
        except:
            # Expired timeout raise an exception
            break

        for item in result_itemlist:
            title = item.fulltitle

            # Clean up a bit the returned title to improve the fuzzy matching
            title = re.sub(r'\(.*\)', '', title)  # Anything within ()
            title = re.sub(r'\[.*\]', '', title)  # Anything within []

            # Check if the found title fuzzy matches the searched one
            if fuzz.WRatio(mostra, title) > 85: itemlist.append(item)

    if show_dialog:
        progreso.close()

    itemlist = sorted(itemlist, key=lambda item: item.fulltitle)

    return itemlist
