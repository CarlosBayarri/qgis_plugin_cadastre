import urllib2
from urllib2 import Request as request
from urllib2 import urlopen as open
import requests
import json
params = {'xmin': 39.298705113102244, 'ymin': -0.586395263671875,'xmax': 39.59828141820854, 'ymax': -0.0714111328125}
myOsmXmlUrlPath = ('http://overpass-api.de/api/interpreter?data=(node["building"="yes"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);way["building"="yes"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);relation["building"="yes"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s););(._;>;);out body;' % params)
# Note that osm json is NOT geojson!
#myOsmJsonUrlPath = = ('http://overpass-api.de/api/interpreter?data=[out:json];(node["amenity"="hospital"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);way["amenity"="hospital"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);relation["amenity"="hospital"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s););(._;>;);out body;' % params)
myOsmJsonUrlPath = ('http://overpass-api.de/api/interpreter?data=[out:json];(node["amenity"="hospital"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);way["amenity"="hospital"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);relation["amenity"="hospital"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s););(._;>;);out body;' % params)


#myOsmJsonUrlPath = ('http://overpass-api.de/api/interpreter?data=[out:json];(node["building"="yes"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);way["building"="yes"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s);relation["building"="yes"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s););(._;>;);out body;' % params)
myRequest = requests.get(myOsmJsonUrlPath)
#print dir(myRequest)
#print myRequest.text
data = myRequest.json()
#print json.dumps(data)

#data_string = json.dumps(data)

#decoded = json.loads(data_string)

print data['elements']
#{u'lat': 39.4782496, u'lon': -0.3641254, u'type': u'node', u'id': 60551624, u'tags': {u'amenity': u'hospital', u'name': u'Hospital Quir\xf3n', u'created_by': u'Potlatch 0.5c'}}