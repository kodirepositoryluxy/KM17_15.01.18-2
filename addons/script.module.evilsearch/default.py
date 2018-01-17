# -*- coding: utf-8 -*-

'''
   Stefano Add-on
    Copyright (C) 2018 Stefano Addon family search For Evil Kong

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

   
'''


import urlparse,sys,re

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

content = params.get('content')

name = params.get('name')

url = params.get('url')

image = params.get('image')

fanart = params.get('fanart')


if action == None:
    from resources.lib.indexers import evilsearch
    evilsearch.indexer().root()



elif action == 'search':
    from resources.lib.indexers import evilsearch
    evilsearch.indexer().search(url=None)

elif action == 'addSearch':
    from resources.lib.indexers import evilsearch
    evilsearch.indexer().addSearch(url)

elif action == 'delSearch':
    from resources.lib.indexers import evilsearch
    evilsearch.indexer().delSearch()

elif action == 'play':
    from resources.lib.indexers import evilsearch
    evilsearch.player().play(url, content)
	
elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

else:
    if 'search' in action:
        url = action.split('search=')[1]
        url = url + '|SECTION|'
        from resources.lib.indexers import evilsearch
        evilsearch.indexer().search(url)
    else: quit()
