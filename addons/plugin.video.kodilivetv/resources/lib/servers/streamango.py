# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para streamango
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# by DrZ3r0
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    if "We are unable to find the video" in data:
        return False, "[streamango] Il file non esiste o è stato cancellato"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data

    video_urls = []
    matches = scrapertools.find_multiple_matches(data, 'type:"video/([^"]+)",src:"([^"]+)",height:(\d+)')
    for ext, media_url, calidad in matches:
        if not media_url.startswith("http"):
            media_url = "http:" + media_url
        video_urls.append([".%s %sp [streamango]" % (ext, calidad), media_url])

    video_urls.reverse()
    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra videos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    patronvideos = '(?://|\.)streamango\.com/(?:f/|embed/)?([0-9a-zA-Z]+)'
    logger.info("find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[streamango]"
        url = "http://streamango.com/embed/%s" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'streamango'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
