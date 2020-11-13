#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import urllib

server = 'https://www1.sedecatastro.gob.es/'
url = 'https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCListaBienes.aspx?del=46&muni=900&rc1=6033702&rc2=YJ2763C'
res = urllib.urlopen(url).read().split("\n")
#print urllib.urlopen(url).read().split("\n")
print ""
print ""
print ""
for linea in res:
    if "class='panel-heading amarillo'" in linea:
        #print linea
        for linea2 in linea.split('<'):
			#print linea2
			
            if "title='Tipo de parcela'" in linea2:
                for linea3 in linea2.split('>'):
                    if "(" in linea3:
						print linea3
            if "title='Superficie gráfica'" in linea2:
				for linea3 in linea2.split('>'):
					if len(linea3) < 65:
						print 'Superficie: '
						print linea3		
            if "title='Localización'" in linea2:
				for linea3 in linea2.split('>'):
					if len(linea3) < 65:
						print 'Localizacion: '
						print linea3
			
            if "title='Uso'" in linea2:
				for linea3 in linea2.split('>'):
					if len(linea3) < 55:
						print 'Uso: '
						print linea3
            if "title='Superficie construida'" in linea2:
				for linea3 in linea2.split('>'):
					if len(linea3) < 65:
						print 'Superficie construida: '
						print linea3
            if "title='Año construcción'" in linea2:
				for linea3 in linea2.split('>'):
					if len(linea3) < 65:
						print 'Año construcción: '
						print linea3
            if "title='Coeficiente de participación'" in linea2:
				for linea3 in linea2.split('>'):
					if len(linea3) < 65:
						print 'Coeficiente de participación: '
						print linea3
            if "javascript:CargarBien" in linea2:
                for linea3 in linea2.split('>'):
                    if len(linea3) < 25:
                        print linea3
for linea in res:
    for linea2 in linea.split('>'):
        if 'captcha' in linea2:
            try:
                fuente = linea2.split('src=')[1].split(' ')[0]
                path =  server+fuente[4:-1]
            except:
                path = '/media/natura/DATOS1/MASTER_GEOINFORMACION/2CUATRI/DAS/PROYECTO/no_foto.png'
            print path
            break
            
'''
res = urllib.urlopen(url).read().split("\n")
path = ''
for linea in res:
    #print linea
    if "title='Tipo de parcela'" in linea:
        print linea
    for linea2 in linea.split('>'):
        #print linea2
        if "VALENCIA" in linea2:
            print linea2
        if "PARCELA" in linea2:
            try:
                print linea2
                info0 = ''
            except:
                info0 = ''
        if 'captcha' in linea2:
            try:
                fuente = linea2.split('src=')[1].split(' ')[0]
                path =  server+fuente[4:-1]
            except:
                path = '/media/natura/DATOS1/MASTER_GEOINFORMACION/2CUATRI/DAS/PROYECTO/no_foto.png'
            #print path
            break
    '''