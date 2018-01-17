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


import re,urllib,urlparse,json


from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import control
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['allrls.pw']
        self.base_link = 'http://allrls.pw'
        self.search_link = '?s=%s+%s&go=Search'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            if debrid.status() == False: raise Exception()
            url = urlparse.urljoin(self.base_link, '%s-%s' % (cleantitle.geturl(title), year))
            url = client.request(url, output='geturl')
            if url == None: 
                url = urlparse.urljoin(self.base_link, '%s' % (cleantitle.geturl(title)))
                url = client.request(url, output='geturl')
            if url == None: raise Exception()
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status() == False: raise Exception()
        return tvshowtitle

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.urljoin(self.base_link, '%s-s%02de%02d' % (cleantitle.geturl(url), int(season), int(episode)))
            url = client.request(url, output='geturl')
            print url
            if url == None: raise Exception()
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources
      
            hostDict = hostprDict + hostDict

            r = client.request(url)           

            urls = client.parseDOM(r, 'a', ret = 'href')

            for url in urls:
                try:

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    
                    if any(x in url for x in ['.rar', '.zip', '.iso']): raise Exception()
                    
                    quality, infoo = source_utils.get_release_quality(url)
                    
                    info = []
                    
                    if any(x in url.upper() for x in ['HEVC', 'X265', 'H265']): info.append('HEVC')
                    
                    info.append('ALLRLS')
                    
                    info = ' | '.join(info)
                    
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                     
                except:
                    pass

            return sources
        except:
            return

    def resolve(self, url):
        return url
