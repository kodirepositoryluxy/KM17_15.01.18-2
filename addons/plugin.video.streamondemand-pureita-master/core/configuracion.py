# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# streamondemand-pureita-main - XBMC Plugin
# Configuraci�n
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand-pureita-master/
#------------------------------------------------------------

from core import downloadtools
from core import config
from core import logger

logger.info("[configuracion.py] init")

def mainlist(params,url,category):
    logger.info("[configuracion.py] mainlist")
    
    config.open_settings( )
