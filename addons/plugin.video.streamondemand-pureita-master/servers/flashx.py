# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# AlfaPureita - XBMC Plugin
# Conector para flashx
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import base64
import os
import re
import time
import urllib

from core import config
from core import httptools
from core import logger
from core import scrapertools
from lib import jsunpack


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url, cookies=False).data

    if 'File Not Found' in data or 'file was deleted' in data:
        return False, "[FlashX] File non presente"
    elif 'Video is processing now' in data:
        return False, "[FlashX] File in processo"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    page_url = page_url.replace("playvid-", "")

    headers = {'Host': 'www.flashx.tv',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
               'Cookie': ''}
    data = httptools.downloadpage(page_url, headers=headers, replace_headers=True).data
    flashx_id = scrapertools.find_single_match(data, 'name="id" value="([^"]+)"')
    fname = scrapertools.find_single_match(data, 'name="fname" value="([^"]+)"')
    hash_f = scrapertools.find_single_match(data, 'name="hash" value="([^"]+)"')
    post = 'op=download1&usr_login=&id=%s&fname=%s&referer=&hash=%s&imhuman=Proceed to the video' % (
        flashx_id, urllib.quote(fname), hash_f)
    wait_time = scrapertools.find_single_match(data, "<span id='xxc2'>(\d+)")

    headers['Referer'] = "https://www.flashx.tv/"
    headers['Accept'] = "*/*"
    headers['Host'] = "www.flashx.tv"

    coding_url = 'https://www.flashx.tv/flashx.php?fxfx=5'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    httptools.downloadpage(coding_url, headers=headers, replace_headers=True)

    try:
        time.sleep(int(wait_time) + 1)
    except:
        time.sleep(6)

    headers.pop('X-Requested-With')
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    data = httptools.downloadpage('https://www.flashx.tv/dl?playnow', post, headers, replace_headers=True).data

    matches = scrapertools.find_multiple_matches(data, "(eval\(function\(p,a,c,k.*?)\s+</script>")

    video_urls = []
    for match in matches:
        try:
            match = jsunpack.unpack(match)
            match = match.replace("\\'", "'")

            # {src:\'https://bigcdn.flashx1.tv/cdn25/5k7xmlcjfuvvjuw5lx6jnu2vt7gw4ab43yvy7gmkvhnocksv44krbtawabta/normal.mp4\',type:\'video/mp4\',label:\'SD\',res:360},
            media_urls = scrapertools.find_multiple_matches(match, "{src:'([^']+)'.*?,label:'([^']+)'")
            subtitle = ""
            for media_url, label in media_urls:
                if media_url.endswith(".srt") and label == "Spanish":
                    try:
                        from core import filetools
                        data = scrapertools.downloadpage(media_url)
                        subtitle = os.path.join(config.get_data_path(), 'sub_flashx.srt')
                        filetools.write(subtitle, data)
                    except:
                        import traceback
                        logger.info("Error al descargar el subtítulo: " + traceback.format_exc())

            for media_url, label in media_urls:
                if not media_url.endswith("png") and not media_url.endswith(".srt"):
                    video_urls.append(["." + media_url.rsplit('.', 1)[1] + " [flashx]", media_url, 0, subtitle])

            for video_url in video_urls:
                logger.info("%s - %s" % (video_url[0], video_url[1]))
        except:
            pass

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    # http://flashx.tv/z3nnqbspjyne
    # http://www.flashx.tv/embed-li5ydvxhg514.html
    patronvideos = 'flashx.(?:tv|pw|to)/(?:embed.php\?c=|embed-|playvid-|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[flashx]"
        url = "https://www.flashx.tv/playvid-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'flashx'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve

