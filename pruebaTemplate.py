import sys, os
from qgis.core import (
    QgsProject, QgsComposition, QgsApplication, QgsProviderRegistry)
from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from PyQt4.QtCore import QFileInfo
from PyQt4.QtXml import QDomDocument
from PyQt4.QtGui import QPrinter
from qgis.core import *
import sip
from qgis.gui import *
from PyQt4.QtGui import QPainter, QColor, QPolygonF
from PyQt4.QtCore import QSizeF, QPointF, QRectF
from qgis.gui import QgsHighlight
import time
from PyQt4 import Qt

from PyQt4.QtXml import *
import lxml.etree as etree

# --- INIT CHANGING THE TEMPLATE ---
with open(myFile, 'r') as f:
    tree  = etree.parse(f)
    #editing the title
    for elem in tree.iter(tag = 'ComposerLabel'):
            for child in elem:
                if child.tag == 'ComposerItem':
                    if child.attrib['id'] == "titulo":
                        print elem.attrib['labelText']
                        elem.attrib['labelText'] = 'Mapa'
    #save the edited composer as a new file
    #new_composer = os.path.join(xml_folder, mapname + "_composer.qpt")
    tree.write(myFile)
# ---  FINI CHANGING THE TEMPLATE ---

# Add all layers in map canvas to render
myMapRenderer = iface.mapCanvas().mapRenderer()
# Load template from file
myComposition = QgsComposition(myMapRenderer)
myFile = r'/media/natura/DATOS1/MASTER_GEOINFORMACION/2CUATRI/DAS/PROYECTO/plantilla.qpt'
myTemplateFile = file(myFile, 'rt')
myTemplateContent = myTemplateFile.read()

myDocument = QDomDocument()
myDocument.setContent(myTemplateContent)
myComposition.loadFromTemplate(myDocument)
'''
composerLabel = QgsComposerLabel(myComposition)
composerLabel.setText('TIIIII')
composerLabel.adjustSizeToText()
composerLabel.setItemPosition(myComposition.paperWidth() / 2,0,QgsComposerItem.UpperMiddle)
myComposition.addItem(composerLabel)
'''
'''
for item in myComposition.items():
    print item
    print dir(item)
'''
titulo = myComposition.getComposerItemById("titulo")
print titulo
print dir(titulo)
#open the composer template and edit it

#titulo.data("ggg")
    #print item
#rec = myComposition.getComposerItemById('rec')
#rec.setItemPosition(5,5)
#titulo = myComposition.getComposerItemById("titulo")
#print dir(titulo)
#print ditulo.AllProperties
#titulo.displayName('tiiiiiiii')

#print myComposition.getComposerItemById('rec')

myImagePath = r'/media/natura/DATOS1/MASTER_GEOINFORMACION/2CUATRI/DAS/PROYECTO/prueba.png'
myImage = myComposition.printPageAsRaster(0)
myImage.save(myImagePath)

myTemplateFile.close()
print 'Hecho'