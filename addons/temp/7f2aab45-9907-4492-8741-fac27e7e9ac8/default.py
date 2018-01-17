# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# XBMC entry point
# ------------------------------------------------------------
import os
import sys

import xbmc
import xbmcaddon
import xbmcgui
from core import config
from platformcode import logger
from platformcode import launcher

logger.info("init...")


__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')

line1 = "[COLOR yellow] ATTENZIONE:[/COLOR] sul tuo sistema è installato [COLOR red]streamondemand-pureita[/COLOR]"
line2 = "[COLOR azure]StreamOnDemand[/COLOR] non è compatibile con quell'addon"
line3 = "Se vuoi utilizzare [COLOR azure]StreamOnDemand[/COLOR] disinstalla [COLOR red]streamondemand-pureita[/COLOR]"

ROOT_DIR = config.get_runtime_path()

KILL_DIR = ROOT_DIR.replace('plugin.video.streamondemand', 'plugin.video.streamondemand-pureita-master')
kick = os.path.exists(KILL_DIR)

if kick == True:
    xbmcgui.Dialog().ok(__addonname__, line1, line2, line3)
    quit()

KILL_DIR = ROOT_DIR.replace('plugin.video.streamondemand', 'plugin.video.streamondemand-pureita')
kick = os.path.exists(KILL_DIR)

if kick == True:
    xbmcgui.Dialog().ok(__addonname__, line1, line2, line3)
    quit()

librerias = xbmc.translatePath(os.path.join(config.get_runtime_path(), 'lib'))
sys.path.append(librerias)


if sys.argv[2] == "":
    launcher.start()
    launcher.run()
else:
    launcher.run()
