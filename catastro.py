#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jpalomav
#
# Created:     13/06/2018
# Copyright:   (c) jpalomav 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import urllib
server = 'https://www1.sedecatastro.gob.es/'
url = 'https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCListaBienes.aspx?del=46&muni=900&rc1=8718504&rc2=YJ2781H'
res = urllib.urlopen(url).read().split("\n")
for linea in res:
    for linea2 in linea.split('>'):
        if 'captcha' in linea2:
            fuente = linea2.split('src=')[1].split(' ')[0]
            path =  server+fuente[4:-1]
            print path
            break

