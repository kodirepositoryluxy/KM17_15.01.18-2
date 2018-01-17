# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: MuadDib

import re,urllib,urlparse,base64
import requests

from resources.lib.modules import client
from resources.lib.modules import log_utils

session = requests.Session()

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['www.bnwmovies.com']
        self.base_link = 'http://www.bnwmovies.com'
        self.search_link = '/?s='

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'title': title, 'year': year, 'imdb': imdb}
            return urllib.urlencode(url)

        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:

                    return url
        except:
            return
        return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources

            urldata = urlparse.parse_qs(url)
            urldata = dict((i, urldata[i][0]) for i in urldata)
            title = urldata['title']
            year = urldata['year']

            start_url=self.base_link+self.search_link+title.replace(' ','+')
            html = client.request(start_url)
            match = re.compile('<div class="post">.+?<h3>.+?href="(.+?)".+?rel="bookmark">(.+?)</a>',re.DOTALL).findall(html)
            for url,alt in match:
                if title.lower() == alt.lower():
                    html2 = client.request(url)

                    match = re.compile('<title >(.+?)</title>',re.DOTALL).findall(html2)
                    for rel in match:
                        if year in rel:
                            Link = re.compile('<source.+?src="(.+?)"',re.DOTALL).findall(html2)[-1] 
                            playlink = Link
                            sources.append({'source':'BNW','quality':'SD','language': 'en','url':playlink,'info':[],'direct':True,'debridonly':False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url