# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CargarCapas
                                 A QGIS plugin
 CargarCapas
                             -------------------
        begin                : 2018-06-09
        copyright            : (C) 2018 by CargarCapas
        email                : CargarCapas
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
    """Load CargarCapas class from file CargarCapas.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .CargarCapasModule import CargarCapas
    return CargarCapas(iface)
