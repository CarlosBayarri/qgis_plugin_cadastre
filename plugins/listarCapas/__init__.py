# -*- coding: utf-8 -*-
"""
/***************************************************************************
 listarCapas
                                 A QGIS plugin
 Visualiza un listado con las capas cargadas
                             -------------------
        begin                : 2018-05-30
        copyright            : (C) 2018 by ralugar
        email                : ralugar@email.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load listarCapas class from file listarCapas.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .listar_capas import listarCapas
    return listarCapas(iface)
