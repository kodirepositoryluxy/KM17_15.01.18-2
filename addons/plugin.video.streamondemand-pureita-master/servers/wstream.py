# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para wstream.video
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# by DrZ3r0
# ------------------------------------------------------------

import re
import time
import urllib

from core import logger, httptools
from core import scrapertools

headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0']]


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[wstream.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    data = httptools.downloadpage(page_url, headers=headers).data

    time.sleep(9)

    try:
        post_url = re.findall('Form method="POST" action=\'(.*)\'', data)[0]
        post_selected = re.findall('Form method="POST" action=(.*)</Form>', data, re.DOTALL)[0]

        post_data = 'op=%s&usr_login=%s&id=%s&referer=%s&hash=%s&imhuman=Proceed+to+video' % (
            re.findall('input type="hidden" name="op" value="(.*)"', post_selected)[0],
            re.findall('input type="hidden" name="usr_login" value="(.*)"', post_selected)[0],
            re.findall('input type="hidden" name="id" value="(.*)"', post_selected)[0],
            re.findall('input type="hidden" name="referer" value="(.*)"', post_selected)[0],
            re.findall('input type="hidden" name="hash" value="(.*)"', post_selected)[0])

        headers.append(['Referer', post_url])
        data = httptools.downloadpage(post_url, post=post_data, headers=headers).data
    except:
        pass

    data_pack = scrapertools.find_single_match(data, "(eval.function.p,a,c,k,e,.*?)\s*</script>")

    if data_pack != "":
        from lib import jsunpack
        data = jsunpack.unpack(data_pack)

    video_url = scrapertools.find_single_match(data, 'file"?\s*:\s*"([^"]+)",')
    video_urls.append([".mp4 [wstream]", video_url + '|' + urllib.urlencode(dict(headers))])

    for video_url in video_urls:
        logger.info("[wstream.py] %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vìdeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = r"""wstream.video/(?:embed-)?([a-z0-9A-Z]+)"""
    logger.info("[wstream.py] find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[wstream]"
        url = 'http://wstream.video/%s' % match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'wstream'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
