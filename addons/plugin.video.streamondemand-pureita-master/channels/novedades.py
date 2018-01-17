# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand PureITA / XBMC Plugin
# Canale Novita
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

from core import config
from core import logger
from core.item import Item

__channel__ = "novedades"
__category__ = "F"
__type__ = "generic"
__title__ = "Novedades"
__language__ = "IT"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item, preferred_thumbnail="squares"):
    logger.info("streamondemand.channels.novedades mainlist")

    itemlist = [Item(channel=__channel__,
                     action="peliculas",
                     title="Film",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/bannermenu/banner_movie_blueP2.png",
                     viewmode="movie"),
					 Item(channel=__channel__,
                     action="series",
                     title="Serie TV",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/bannermenu/banner_tvshow_blueP2.png",
                     viewmode="movie"),
                Item(channel=__channel__,
                     action="peliculas_infantiles",
                     title="Cartoni Animati",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/bannermenu/banner_bambini_blueP2.png",
                     viewmode="movie"),
                Item(channel=__channel__,
                     action="anime",
                     title="Anime",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/bannermenu/banner_anime_blueP2.png",
                     viewmode="movie"),
                Item(channel=__channel__,
                     action="documentales",
                     title="Documentari",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/bannermenu/banner_documentary_blueP2.png",
                     viewmode="movie")]

    return itemlist


def peliculas(item):
    logger.info("streamondemand.channels.novedades peliculas")

    itemlist = []

    from channels import cineblog01
    item.url = "https://www.cb01.uno/"
    itemlist.extend(cineblog01.peliculas(item))

    from channels import casacinema
    item.url = "http://www.casacinema.video/?s=%5BHD%5D"
    itemlist.extend(casacinema.peliculas(item))	
	
    from channels import italiafilm
    item.url = "http://www.italia-film.gratis/novita-streaming/"
    itemlist.extend(italiafilm.peliculas(item))

    #from channels import piratestreaming
    #item.url = "http://www.piratestreaming.black/film-aggiornamenti.php"
    #itemlist.extend(piratestreaming.peliculas(item))

    #from channels import itafilmtv
    #item.url = "http://www.italia-film.gratis"
    #itemlist.extend(itafilmtv.peliculas(item))





    sorted_itemlist = []

    for item in itemlist:

        if item.extra != "next_page" and not item.title.startswith(">>"):
            item.title = item.title + " [" + item.channel + "]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)

    return sorted_itemlist


def peliculas_infantiles(item):
    logger.info("streamondemand.channels.novedades peliculas_infantiles")

    itemlist = []

    import guardaserieonline
    item.url = "http://www.guardaserie.online//category/animazione/"
    itemlist.extend(guardaserieonline.lista_serie(item))
	
    import streaminglove
    item.url = "https://www.streaminglove.tv/genere/animazione/"
    itemlist.extend(streaminglove.peliculas(item))
	
    import serietvu
    item.url = "http://www.serietvu.online/category/animazione-e-bambini/"
    itemlist.extend(serietvu.latestep(item))

    sorted_itemlist = []

    for item in itemlist:

        if item.extra != "next_page" and not item.title.startswith(">>"):
            item.title = item.title + " [" + item.channel + "]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)

    return sorted_itemlist


def series(item):
    logger.info("streamondemand.channels.novedades series")

    itemlist = []
	


    #import serietvu
    #item.url = "http://www.serietvu.com/ultimi-episodi/"
    #itemlist.extend(serietvu.latestep(item))

    import italiaserie
    item.url = "http://www.italiaserie.co/"
    itemlist.extend(italiaserie.peliculas(item))
	
    import serietvsubita
    item.url = "http://serietvsubita.net"
    itemlist.extend(serietvsubita.episodios(item))
	
    import serietvonline
    item.url = "https://serietvonline.com/"
    itemlist.extend(serietvonline.lista_novita(item))

    sorted_itemlist = []

    for item in itemlist:

        if item.extra != "next_page" and not item.title.startswith(">>"):
            item.title = item.title + " [" + item.channel + "]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)

    return sorted_itemlist


def anime(item):
    logger.info("streamondemand.channels.novedades anime")

    itemlist = []

    import animesenzalimiti
    item.url = "http://www.animesenzalimiti.com/"
    itemlist.extend(animesenzalimiti.ultimiep(item))

    import animeforce
    item.url = "https://www.animeforce.org/"
    itemlist.extend(animeforce.ultimiep(item))

    sorted_itemlist = []

    for item in itemlist:

        if item.extra != "next_page" and not item.title.endswith(">>"):
            item.title = item.title + " [" + item.channel + "]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)

    return sorted_itemlist


def documentales(item):
    logger.info("streamondemand.channels.novedades documentales")

    itemlist = []

    import documentaristreamingdb
    item.url = "http://www.documentari-streaming-db.com/?searchtype=movie&post_type=movie&sl=lasts&s="
    itemlist.extend(documentaristreamingdb.peliculas(item))

    sorted_itemlist = []

    for item in itemlist:

        if item.extra != "next_page" and not item.title.startswith(">>"):
            item.title = item.title + " [" + item.channel + "]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)

    return sorted_itemlist
