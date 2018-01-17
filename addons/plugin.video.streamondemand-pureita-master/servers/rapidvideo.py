# -*- coding: iso-8859-1 -*-
# ------------------------------------------------------------
# streamondemand-PureITA- XBMC Plugin
# Server rapidvideo
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import re
import urllib

from core import httptools
from core import jsunpack
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    try:
        response = httptools.downloadpage(page_url)
    except:
        pass

    if not response.data or "urlopen error [Errno 1]" in str(response.code):
        from platformcode import config
        if config.is_xbmc():
            return False, "[Rapidvideo] Questo connettore funziona solo con versione di Kodi 17 o successive"
        elif config.get_platform() == "plex":
            return False, "[Rapidvideo] Questo connettore non funziona con la tua versione di Plex, aggiornamento versione richiesto"
        elif config.get_platform() == "mediaserver":
            return False, "[Rapidvideo] Questo connettore richiede un aggiornamento di python alla versione 2.7.9 o superiore"

    if "Object not found" in response.data:
        return False, "[Rapidvideo] File inesistente o e stato cancellato"
    if response.code == 500:
        return False, "[Rapidvideo] Server error, riprova in seguito"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)
    video_urls = []
    data = httptools.downloadpage(page_url).data
    patron = 'https://www.rapidvideo.com/e/[^"]+'
    match = scrapertools.find_multiple_matches(data, patron)
    for url1 in match:
       res = scrapertools.find_single_match(url1, '=(\w+)')
       data = httptools.downloadpage(url1).data
       url = scrapertools.find_single_match(data, 'source src="([^"]+)')
       ext = scrapertools.get_filename_from_url(url)[-4:]
       video_urls.append(['%s %s [rapidvideo]' % (ext, res), url])

    return video_urls



# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.rapidvideo.org/ttsvqng2qp2v/Scooby-Doo_e_la_Maschera_di_Blue_Falcon_720p.mp4.html
    # http://www.rapidvideo.cool/3zed9xr3yeoo/The.Flash.1x01.Una.Citta.Di.Eroi.ITA.DLMux.x264-UBi.mkv.html
    patronvideos = 'rapidvideo.(?:org|com)/(?:\\?v=|e/|embed/|v/)([A-z0-9]+)'
    logger.info("[rapidvideo.py] find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for domain, match in matches:
        titulo = "[rapidvideo]"
        url = ("http://www.rapidvideo.%s/" + match) % domain
        d = scrapertools.cache_page(url)
        ma = scrapertools.find_single_match(d, '"fname" value="([^<]+)"')
        ma = titulo + " " + ma
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([ma, url, 'rapidvideo'])

            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve


def test():
    video_urls = get_video_url("http://www.rapidvideo.com/embed/sy6wen17")

    return len(video_urls) > 0
