# -*- coding: utf-8 -*-
"""
/***************************************************************************
 informacionCatastral
                                 A QGIS plugin
 informacionCatastral
                             -------------------
        begin                : 2018-06-23
        copyright            : (C) 2018 by informacionCatastral
        email                : informacionCatastral
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
    """Load informacionCatastral class from file informacionCatastral.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .informacionCatastral import informacionCatastral
    return informacionCatastral(iface)
