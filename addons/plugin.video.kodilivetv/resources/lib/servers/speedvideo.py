# -*- coding: utf-8 -*-

from core import httptools, logger, scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    return True, ""


def get_video_url(page_url,
                  premium=False,
                  user="",
                  password="",
                  video_password=""):
    logger.info("url=" + page_url)
    video_urls = []

    data = httptools.downloadpage(page_url).data

    media_url = scrapertools.find_single_match(data, 'linkfile ="([^"]+)"')

    media_url = scrapertools.getLocationHeaderFromResponse(media_url)

    video_urls.append(
        ["." + media_url.rsplit('.', 1)[1] + ' [speedvideo]', media_url])

    return video_urls
