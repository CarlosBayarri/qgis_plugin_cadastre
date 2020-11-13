#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from qgis.core import (
    QgsProject, QgsComposition, QgsApplication, QgsProviderRegistry)
from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from PyQt4.QtCore import QFileInfo
from PyQt4.QtXml import QDomDocument
from PyQt4.QtGui import QPrinter
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import QPainter, QColor, QPolygonF, QFont
from PyQt4.QtCore import QSizeF, QPointF, QRectF
from qgis.gui import QgsHighlight
import time
from PyQt4 import Qt
import urllib
from processing import * 

from PyQt4.QtXml import *
import lxml.etree as etree

import requests
import json
from osgeo import osr
from osgeo import ogr
import os

proyecto = QgsProject.instance()
pathProject = proyecto.readPath("")
myFile = r'./plantilla.qpt'
#myFile = r'plantilla.qpt'
registro = QgsMapLayerRegistry.instance()
capas = registro.mapLayers()
campos = ["MUNICIPIO","MASA","HOJA","TIPO","PARCELA","COORX","COORY","VIA","NUMERO","NUMERODUP","NUMSYMBOL","AREA","FECHAALTA","FECHABAJA","NINTERNO","PCAT1","PCAT2","EJERCICIO","NUM_EXP","CONTROL","REFCAT"]
valores = []
mCanvas = iface.mapCanvas()
mLegend = iface.legendInterface()
mCanvas.zoomToSelected()
mCanvas.zoomScale(1000)
mCanvas.setCanvasColor(QColor("white"))
mCanvas.enableAntiAliasing(True)
mCanvas.setSelectionColor( QColor("red") )
mCanvas.refresh() 

registro = QgsMapLayerRegistry.instance()
# CAPAS
#parcelas = QgsVectorLayer(r'./catastro_urbano/PARCELA/PARCELA.SHP','parcelitas','ogr')
parcelas = QgsVectorLayer(pathProject + '/PARCELA.SHP','PARCELA','ogr')
registro.addMapLayer(parcelas)
police = QgsVectorLayer(r'./layers/police_point.shp','police','ogr')
#registro.addMapLayer(police)
#iface.addRasterLayer("crs=EPSG:25830&layers=OI.OrthoimageCoverage&styles=&format=image/png&url=http://www.ign.es/wms-inspire/pnoa-ma?","pnoa","wms")
mem_layer = QgsVectorLayer("Polygon?crs=epsg:25830&field=id:integer&index=yes","Parcela seleccionada","memory")
registro.addMapLayer(mem_layer)

global pcat1
global pcat2
for clave in capas:
    capa = capas[clave]
    if capa.name() == 'PARCELA':
        capaRenderer = capa.rendererV2()
        #print("Type:", capaRenderer.type())
        if (len(capa.selectedFeatures()) == 0):
            print "Selecciona una"
        elif (len(capa.selectedFeatures()) > 1):
            print "no"
        else: 
            feature = capa.selectedFeatures()[0]
            box = feature.geometry().boundingBox()
            xmin = box.xMinimum()
            xmax = box.xMaximum()
            ymin = box.yMinimum()
            ymax = box.yMaximum()
            xminOver = box.xMinimum()-1000
            xmaxOver = box.xMaximum()+1000
            yminOver = box.yMinimum()-1000
            ymaxOver = box.yMaximum()+1000
            source = osr.SpatialReference()
            source.ImportFromEPSG(25830)

            target = osr.SpatialReference()
            target.ImportFromEPSG(4326)

            transform = osr.CoordinateTransformation(source, target)

            point1Box = ogr.CreateGeometryFromWkt("POINT ("+str(xminOver)+" "+str(yminOver)+")")
            point1Box.Transform(transform)
            point2Box = ogr.CreateGeometryFromWkt("POINT ("+str(xmaxOver)+" "+str(ymaxOver)+")")
            point2Box.Transform(transform)

            xMinOver = point1Box.GetY()
            yMinOver = point1Box.GetX()
            xMaxOver = point2Box.GetY()
            yMaxOver = point2Box.GetX()
            params = {'xmin': xMinOver, 'ymin': yMinOver,'xmax': xMaxOver, 'ymax': yMaxOver}
            #print params
            hospitalOSM = ('http://overpass-api.de/api/interpreter?data=[out:json];(node["amenity"="hospital"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);way["amenity"="hospital"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);relation["amenity"="hospital"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s););(._;>;);out body;' % params)
            policeOSM = ('http://overpass-api.de/api/interpreter?data=[out:json];(node["amenity"="police"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);way["amenity"="police"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);relation["amenity"="police"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s););(._;>;);out body;' % params)
            supermarketOSM = ('http://overpass-api.de/api/interpreter?data=[out:json];(node["shop"="supermarket"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);way["shop"="supermarket"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);relation["shop"="supermarket"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s););(._;>;);out body;' % params)

            rec = QgsRectangle(xmin,ymin,xmax,ymax)
            rec2 = QgsRectangle(xmin-30,ymin-30,xmax+30,ymax+30)
            recOver = QgsRectangle(xminOver,yminOver,xmaxOver,ymaxOver)
            recOver2 = QgsRectangle(xminOver+500,yminOver+500,xmaxOver-500,ymaxOver-500)
            #print xmin
            mCanvas.setExtent(rec)
            for i in range(len(campos)):
                #print campos[i]
                if (campos[i] == 'PCAT1'):
                    #print campos[i]
                    pcat1 = feature.attribute(campos[i])
                    #print pcat1
                if (campos[i] == 'PCAT2'):
                    pcat2 = feature.attribute(campos[i])
                #print feature.attribute(campos[i])
                valores.append(feature.attribute(campos[i]))
                
            # --- INIT CHANGING THE TEMPLATE ---
            server = 'https://www1.sedecatastro.gob.es/'
            url = 'https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCListaBienes.aspx?del=46&muni=900&rc1='+str(pcat1)+'&rc2='+str(pcat2)+''
            res = urllib.urlopen(url).read().split("\n")
            path = ''
            localizacion = []
            uso = []
            superficie = []
            ano = []
            coeficiente = []
            refcat = []
            for linea in res:
                if "class='panel-heading amarillo'" in linea:
                    for linea2 in linea.split('<'):
                        #print linea2
                        if "title='Tipo de parcela'" in linea2:
                            for linea3 in linea2.split('>'):
                                if "(" in linea3:
                                    #print linea3
                                    descripcion = linea3
                        if "title='Superficie gráfica'" in linea2:
                            for linea3 in linea2.split('>'):
                                if len(linea3) < 65:
                                    superficieGrafica = linea3 + 'm2'
                                    #print 'Superficie: '
                                    #print linea3
                        if "title='Localización'" in linea2:
                            for linea3 in linea2.split('>'):
                                if len(linea3) < 65:
                                    #print 'Localizacion: '
                                    #print linea3
                                    localizacion.append(linea3)
                                    calle = linea3
                        
                        if "title='Uso'" in linea2:
                            for linea3 in linea2.split('>'):
                                if len(linea3) < 55:
                                    #print 'Uso: '
                                    #print linea3
                                    uso.append(linea3)
                        if "title='Superficie construida'" in linea2:
                            for linea3 in linea2.split('>'):
                                if len(linea3) < 65:
                                    #print 'Superficie construida: '
                                    #print linea3
                                    superficie.append(linea3)
                        if "title='Año construcción'" in linea2:
                            for linea3 in linea2.split('>'):
                                if len(linea3) < 65:
                                    #print 'Año construcción: '
                                    #print linea3
                                    ano.append(linea3)
                        if "title='Coeficiente de participación'" in linea2:
                            for linea3 in linea2.split('>'):
                                if len(linea3) < 65:
                                    #print 'Coeficiente de participación: '
                                    #print linea3
                                    coeficiente.append(linea3)
                        if "javascript:CargarBien" in linea2:
                            for linea3 in linea2.split('>'):
                                if len(linea3) < 25:
                                    #print linea3
                                    refcat.append(linea3)
            for linea in res:
                for linea2 in linea.split('>'):
                    if 'captcha' in linea2:
                        try:
                            fuente = linea2.split('src=')[1].split(' ')[0]
                            path =  server+fuente[4:-1]
                        except:
                            path = './no_foto.png'
                        #print path
                        break
            with open(myFile, 'r') as f:
                print 'Modificando plantilla...'
                tree  = etree.parse(f)
                # Editing the title
                for elem in tree.iter(tag = 'ComposerLabel'):
                    for child in elem:
                        if child.tag == 'ComposerItem':
                            if child.attrib['id'] == "titulo":
                                #print elem.attrib['labelText']
                                #print dir(elem.attrib)
                                #print 'Elemento: '+str(child.attrib['id'])
                                elem.attrib['labelText'] = 'INFORMACION CARTOGRAFICA CATASTRAL'
                                #print 'Texto: '+str(elem.attrib['labelText'])
                            if child.attrib['id'] == "info":
                                #print 'Elemento: '+str(child.attrib['id'])
                                #cadena = info0
                                '''
                                for j in range(len(valores)):
                                    print str(campos[j]) + ': ' + str(valores[j])
                                    if campos[j] == 'TIPO' or campos[j] == 'PARCELA' or campos[j] == 'AREA' or campos[j] == 'PARCELA' or campos[j] == 'REFCAT':
                                        cadena += str(campos[j]) + ': '+str(valores[j])+'   '
                                elem.attrib['labelText'] = cadena
                                '''
                                #print 'Texto: '+str(elem.attrib['labelText'])
                            if child.attrib['id'] == "tipoParcela":
                                #print 'Elemento: '+str(child.attrib['id'])
                                for j in range(len(valores)):
                                    #print str(campos[j]) + ': ' + str(valores[j])
                                    if campos[j] == 'TIPO':
                                        if valores[j] == 'U':
                                            cadena = ' Tipo : urbana'
                                        else: 
                                            cadena = ' Tipo : rustica'
                                elem.attrib['labelText'] = cadena
                            if child.attrib['id'] == "numeroParcela":
                                #print 'Elemento: '+str(child.attrib['id'])
                                for j in range(len(valores)):
                                    #print str(campos[j]) + ': ' + str(valores[j])
                                    if campos[j] == 'NUMERO': 
                                        cadena = '  Portal: '+str(valores[j])+''
                                elem.attrib['labelText'] = cadena
                            if child.attrib['id'] == "areaParcela":
                                #print 'Elemento: '+str(child.attrib['id'])
                                for j in range(len(valores)):
                                    #print str(campos[j]) + ': ' + str(valores[j])
                                    if campos[j] == 'AREA':
                                        cadena = ' Area: '+str(valores[j])+' m2'
                                elem.attrib['labelText'] = cadena
                            if child.attrib['id'] == "refcatParcela":
                                #print 'Elemento: '+str(child.attrib['id'])
                                for j in range(len(valores)):
                                    #print str(campos[j]) + ': ' + str(valores[j])
                                    if campos[j] == 'REFCAT':
                                        cadena = ' Referencia catastral: '+str(valores[j])+'   '
                                elem.attrib['labelText'] = cadena
                            if child.attrib['id'] == "descripcionParcela":
                                elem.attrib['labelText'] = ' ' + descripcion
                            if child.attrib['id'] == "calleParcela":
                                callex = calle.split()
                                k = 0
                                for l in callex:
                                    k += 1
                                    if len(l) < 2:
                                        l = int(l)
                                        o = k
                                        number = l
                                    #print type(l)
                                elem.attrib['labelText'] = 'CALLE: ' + str(calle.rsplit(str(number))[0])
                                
                                
                for elem in tree.iter(tag = 'ComposerPicture'):
                    for child in elem:
                        if child.tag == 'ComposerItem':
                            if child.attrib['id'] == "foto":
                                #print 'id: '+str(child.attrib['id'])
                                #print 'Path: '
                                #print path
                                #print dir(elem.attrib)
                                #print elem.attrib['labelText']
                                #for each in elem.attrib:
                                    #print each
                                elem.attrib['file'] = path
                            #if child.attrib['id'] == "norte":
                                #print 'id: '+str(child.attrib['id'])
                                
                                
                #save the edited composer as a new file
                #new_composer = os.path.join(xml_folder, mapname + "_composer.qpt")
                tree.write(myFile)
                
            # ---  FINI CHANGING THE TEMPLATE ---

            geometry = feature.geometry()
            geometry = geometry.asPolygon()
            poly_reproj = geometry
            crsSrc = QgsCoordinateReferenceSystem(25830)
            crsDest = QgsCoordinateReferenceSystem(25830)
            xform = QgsCoordinateTransform(crsSrc, crsDest)
            # capa.setLayerTransparency(35)
            # create a new symbol layer with default properties
            symbols = mem_layer.rendererV2().symbols()
            symbol = symbols[0]
            symbol.symbolLayer(0).setDataDefinedProperty('color', 'color_rgba(102,46,46,30)')
            symbol.symbolLayer(0).setDataDefinedProperty('color_border', 'color_rgb(255,255,255)')
            mLegend.refreshLayerSymbology(mem_layer)
            mCanvas.refresh() 
            
            for i, point in enumerate(geometry[0]):
                pt = xform.transform(point)
                poly_reproj[0][i] = pt
                #print pt
            
            prov = mem_layer.dataProvider()
            newFeature = QgsFeature()
            newFeature.setAttributes(valores)
            #print valores
            newFeature.setGeometry(QgsGeometry.fromPolygon(poly_reproj))
            #for j in range(len(campos)):
                #print campos[j]
                #newFeature.setFields(campos[j])
                #newFeature.setAttributes([j,""+campos[j]+""])
            #print newFeature.attribute("id")
            prov.addFeatures([newFeature])
            
            myRequest = requests.get(hospitalOSM)
            #print myRequest
            data = myRequest.json()
            if myRequest.status_code == 200:
                print 'Response OSM: OK'
            else:
                print 'Bad Response'
            
            elementos = data['elements']
            #print data['elements'][0]
            transform = osr.CoordinateTransformation(target,source)
            hospitalFeatureLayer = QgsVectorLayer("Point?crs=epsg:25830&field=id:integer&index=yes","Hospitales","memory")
            registro.addMapLayer(hospitalFeatureLayer)
            providerHospital = hospitalFeatureLayer.dataProvider()
            osmHospital = QgsFeature()
            for elem in elementos:
                if 'tags' in elem:
                    #print elem
                    if 'lat' in elem:
                        lat = elem['lat']
                        lon = elem['lon']
                        featureReprojected = ogr.CreateGeometryFromWkt("POINT ("+str(lon)+" "+str(lat)+")")
                        featureReprojected.Transform(transform)
                        #print featureReprojected.GetX()
                        newPoint = QgsPoint(featureReprojected.GetX(),featureReprojected.GetY())
                        osmFeatures.setGeometry(QgsGeometry.fromPoint(newPoint))
                        providerHospital.addFeatures([osmHospital])
            print 'Hospitales añadidos'
            myRequest = requests.get(policeOSM)
            #print myRequest
            data = myRequest.json()
            if myRequest.status_code == 200:
                print 'Response OSM: OK'
            else:
                print 'Bad Response'
            
            elementos = data['elements']
            #print data['elements'][0]
            transform = osr.CoordinateTransformation(target,source)
            policeFeatureLayer = QgsVectorLayer("Point?crs=epsg:25830&field=id:integer&index=yes","Policia","memory")
            registro.addMapLayer(policeFeatureLayer)
            providerPolice = policeFeatureLayer.dataProvider()
            policeFeatures = QgsFeature()
            for elem in elementos:
                if 'tags' in elem:
                    #print elem
                    if 'lat' in elem:
                        lat = elem['lat']
                        lon = elem['lon']
                        featureReprojected = ogr.CreateGeometryFromWkt("POINT ("+str(lon)+" "+str(lat)+")")
                        featureReprojected.Transform(transform)
                        #print featureReprojected.GetX()
                        newPoint = QgsPoint(featureReprojected.GetX(),featureReprojected.GetY())
                        osmFeatures.setGeometry(QgsGeometry.fromPoint(newPoint))
                        providerPolice.addFeatures([policeFeatures])
            print 'Policias añadidos'
            myRequest = requests.get(supermarketOSM)
            #print myRequest.status_code
            data = myRequest.json()
            if myRequest.status_code == 200:
                print 'Response OSM: OK'
            else:
                print 'Bad Response'
            
            elementos = data['elements']
            #print data['elements'][0]
            transform = osr.CoordinateTransformation(target,source)
            supermarketFeatureLayer = QgsVectorLayer("Point?crs=epsg:25830&field=id:integer&index=yes","Supermercado","memory")
            registro.addMapLayer(supermarketFeatureLayer)
            providerSupermarket = supermarketFeatureLayer.dataProvider()
            supermarketFeatures = QgsFeature()
            for elem in elementos:
                if 'tags' in elem:
                    #print elem
                    if 'lat' in elem:
                        lat = elem['lat']
                        lon = elem['lon']
                        featureReprojected = ogr.CreateGeometryFromWkt("POINT ("+str(lon)+" "+str(lat)+")")
                        featureReprojected.Transform(transform)
                        #print featureReprojected.GetX()
                        newPoint = QgsPoint(featureReprojected.GetX(),featureReprojected.GetY())
                        supermarketFeatures.setGeometry(QgsGeometry.fromPoint(newPoint))
                        providerSupermarket.addFeatures([supermarketFeatures])
            print 'Supermercados añadidos'
            #newFeature = QgsFeature()
            #newFeature.setGeometry(QgsGeometry.fromPolygon(poly_reproj))
            #prov.addFeatures([newFeature])
            
            
def createPDF():
    
    mapRenderer = mCanvas.mapRenderer()
    c = QgsComposition(mapRenderer)
    myTemplateFile = file(myFile, 'rt')
    myTemplateContent = myTemplateFile.read()
    myDocument = QDomDocument()
    myDocument.setContent(myTemplateContent)
    c.loadFromTemplate(myDocument)
    
    
    c.setPlotStyle(c.Print)
    x1, y1 = 20, 33
    x2, y2 = 230.05, 159.85
    w1, h1 = 203, 244.25
    w2, h2 = 169.5, 90.6
    composerMap1 = QgsComposerMap(c, x1 ,y1, w1, h1)
    composerMap1.zoomToExtent(rec2)
    composerMap1.setFrameEnabled(True)
    composerMap1.setFrameOutlineColor(QColor('black'))
    composerMap1.setFrameOutlineWidth(0.1)
     
    #Parametros de la Grid dentro del composerMap
    composerMap1.setGridEnabled(True)
    c.addItem(composerMap1)
    scale = QgsComposerScaleBar(c)
    scale.setItemPosition(190,265)
    scale.setStyle('Numeric') # optionally modify the style
    scale.setComposerMap(composerMap1)
    scale.applyDefaultSize()
    c.addItem(scale)
    scale = QgsComposerScaleBar(c)
    scale.setItemPosition(27.5,262.5)
    scale.setStyle('Line Ticks Up') # optionally modify the style
    scale.setComposerMap(composerMap1)
    scale.applyDefaultSize()
    c.addItem(scale)
    
    northarrowIcon = QgsComposerPicture(c)
    northarrowIcon.setSceneRect(QRectF(202.5,42.5,20,20))
    northarrowIcon.setPictureFile("/usr/share/qgis/svg/arrows/NorthArrow_04.svg")
    c.addItem(northarrowIcon)
    #print 'north added'
    composerMap2 = QgsComposerMap(c, x2 ,y2, w2, h2)
    composerMap2.zoomToExtent(recOver2)
    composerMap2.setFrameEnabled(True)
    composerMap2.setFrameOutlineColor(QColor('black'))
    composerMap2.setFrameOutlineWidth(0.1)
    c.addItem(composerMap2)
    
    
    # TEXT TO INFO SUBPARCELS
    string = ''
    i = 0
    #print refcat
    subparcel = QgsComposerLabel(c)
    subparcel.setText(' INFORMACION SUBPARCELARIA ')
    subparcel.setFont(QFont("Cambria",12))
    subparcel.setItemPosition(10,320)
    subparcel.setFrameEnabled(True)
    subparcel.setMarginX(161.25)
    subparcel.adjustSizeToText()
    c.addItem(subparcel) 
    
    subparcel = QgsComposerLabel(c)
    subparcel.setText(' Parcela ')
    subparcel.setFont(QFont("Cambria",12))
    subparcel.setItemPosition(12.5,329.5)
    subparcel.setFrameEnabled(True)
    subparcel.setMarginX(21)
    subparcel.adjustSizeToText()
    c.addItem(subparcel) 
    for i in range(len(refcat)):
        
        string = str(refcat[i])
        subparcel = QgsComposerLabel(c)
        subparcel.setText(string)
        subparcel.setFont(QFont("Cambria",10))
        subparcel.setItemPosition(15,337.75+5.75*i)
        subparcel.adjustSizeToText()
        c.addItem(subparcel) 
        i += 1
        if i == 50:
            break
    subparcel = QgsComposerLabel(c)
    subparcel.setText(' Uso ')
    subparcel.setFont(QFont("Cambria",12))
    subparcel.setItemPosition(85,329.5)
    subparcel.setFrameEnabled(True)
    subparcel.setMarginX(12.5)
    subparcel.adjustSizeToText()
    c.addItem(subparcel) 
    for i in range(len(uso)):
        string = str(uso[i])
        subparcel = QgsComposerLabel(c)
        subparcel.setText(string)
        subparcel.setFont(QFont("Cambria",10))
        subparcel.setItemPosition(87.5,337.75+5.75*i)
        subparcel.adjustSizeToText()
        c.addItem(subparcel) 
        if i == 50:
            break
    subparcel = QgsComposerLabel(c)
    subparcel.setText(' Ano ')
    subparcel.setFont(QFont("Cambria",12))
    subparcel.setItemPosition(128,329.5)
    subparcel.setFrameEnabled(True)
    subparcel.setMarginX(5)
    subparcel.adjustSizeToText()
    c.addItem(subparcel) 
    for i in range(len(ano)):
        string = str(ano[i])
        subparcel = QgsComposerLabel(c)
        subparcel.setText(string)
        subparcel.setFont(QFont("Cambria",10))
        subparcel.setItemPosition(132.5,337.75+5.75*i)
        subparcel.adjustSizeToText()
        c.addItem(subparcel) 
        if i == 50:
            break
    subparcel = QgsComposerLabel(c)
    subparcel.setText(' Superficie ')
    subparcel.setFont(QFont("Cambria",12))
    subparcel.setItemPosition(155,329.5)
    subparcel.setFrameEnabled(True)
    subparcel.setMarginX(7.5)
    subparcel.adjustSizeToText()
    c.addItem(subparcel) 
    for i in range(len(superficie)):
        string = str(superficie[i])
        subparcel = QgsComposerLabel(c)
        subparcel.setText(string)
        subparcel.setFont(QFont("Cambria",10))
        subparcel.setItemPosition(155.5,337.75+5.75*i)
        subparcel.adjustSizeToText()
        c.addItem(subparcel) 
        if i == 50:
            break
    subparcel = QgsComposerLabel(c)
    subparcel.setText(' Coeficiente de participacion ')
    subparcel.setFont(QFont("Cambria",12))
    subparcel.setItemPosition(200,329.5)
    subparcel.setFrameEnabled(True)
    subparcel.setMarginX(7.5)
    subparcel.adjustSizeToText()
    c.addItem(subparcel) 
    for i in range(len(coeficiente)):
        string = str(coeficiente[i])
        subparcel = QgsComposerLabel(c)
        subparcel.setText(string)
        subparcel.setFont(QFont("Cambria",10))
        subparcel.setItemPosition(220,337.75+5.75*i)
        subparcel.adjustSizeToText()
        c.addItem(subparcel) 
        if i == 50:
            break
    subparcel = QgsComposerLabel(c)
    subparcel.setText(' Localizacion ')
    subparcel.setFont(QFont("Cambria",12))
    subparcel.setItemPosition(282.5,329.5)
    subparcel.setFrameEnabled(True)
    subparcel.setMarginX(45)
    subparcel.adjustSizeToText()
    c.addItem(subparcel) 
    for i in range(len(localizacion)):
        string = str(localizacion[i])
        subparcel = QgsComposerLabel(c)
        subparcel.setText(string)
        subparcel.setFont(QFont("Cambria",10))
        subparcel.setItemPosition(285,337.75+5.75*i)
        subparcel.adjustSizeToText()
        c.addItem(subparcel) 
        if i == 50:
            break

    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    
    print pathProject

    printer.setOutputFileName(pathProject + '/out.pdf')

    printer.setPaperSize(QSizeF(c.paperWidth(), c.paperHeight()), QPrinter.Millimeter)
    printer.setFullPage(True)
    printer.setColorMode(QPrinter.Color)
    printer.setResolution(c.printResolution())

    pdfPainter = QPainter(printer)
  
    c.doPrint(printer, pdfPainter)
    pdfPainter.end()
    print 'Removing memory layers...'
    QgsMapLayerRegistry.instance().removeMapLayer(hospitalFeatureLayer)
    QgsMapLayerRegistry.instance().removeMapLayer(policeFeatureLayer)
    QgsMapLayerRegistry.instance().removeMapLayer(supermarketFeatureLayer)
    QgsMapLayerRegistry.instance().removeMapLayer(mem_layer)
    print "hecho"

createPDF()

