import qgis

## Getting TXT Data :
path = r'MidTerm.shp'
geo_dots = r'Country.txt'
layer = QgsFields()
layer.append(QgsField('Name', QVariant.String))
layer.append(QgsField('Population', QVariant.Int))

writer = QgsVectorFileWriter(path, 'UTF-8', layer, QgsWkbTypes.Point, QgsCoordinateReferenceSystem('EPSG:32638'), 'ESRI Shapefile')

file = open(geo_dots, "r")
text = file.read()
file.close()
lines = text.split("\n")

for i in lines[1:len(lines)-1]:
    line = i.split()
    fn = QgsFeature()
    fn.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(line[2]), float(line[3]))))
    fn.setAttributes([line[0], float(line[1])])
    writer.addFeature(fn)
    
del(writer)

## Pop Density :
layer1 = QgsVectorLayer(path, '', 'ogr')
pv = layer1.dataProvider()
pv.addAttributes([QgsField('Density', QVariant.Double)])
layer1.updateFields()

Density = QgsExpression('"Population"/100')

cntx = QgsExpressionContext()
cntx.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer1))

with edit(layer1):
    for i in layer1.getFeatures():
        cntx.setFeature(i)
        i['Density'] = Density.evaluate(cntx)
        layer1.updateFeature(i)

## Buffer Zones :
out = r'Buff.shp'
fields = layer1.fields()
feats = layer1.getFeatures()

for i in feats:
    if i['Density'] < 1200:
        processing.run('native:buffer', {'INPUT' : path, 'DISTANCE':1200, 'OUTPUT' : out})
    elif i['Density'] > 1200 and i['Density'] < 2000:
        processing.run('native:buffer', {'INPUT' : path, 'DISTANCE':2000, 'OUTPUT' : out})
    else:
        processing.run('native:buffer', {'INPUT' : path, 'DISTANCE':3000, 'OUTPUT' : out})
        
iface.addVectorLayer(out, '', 'ogr')