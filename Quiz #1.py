fn = r'Rivers.shp'
layer = QgsVectorLayer(fn, '', 'ogr')

# გამოთვლა მ და კმ

pv = layer.dataProvider()
pv.addAttributes([QgsField('length', QVariant.Double), QgsField('lengthKM', QVariant.Double)])
layer.updateFields()

expr1 = QgsExpression('$length')
expr2 = QgsExpression('"length"/1000')

cntx = QgsExpressionContext()
cntx.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

with edit(layer):
    for i in layer.getFeatures():
        cntx.setFeature(i)
        i['length'] = expr1.evaluate(cntx)
        layer.updateFeature(i)
with edit(layer):
    for i in layer.getFeatures():
        cntx.setFeature(i)
        i['lengthKM'] = expr2.evaluate(cntx)
        layer.updateFeature(i)
        

# გატანა 55 - 155

fn1 = 'NewRivers.shp'
layer.selectByExpression('lengthKM < 55 and lengthKM > 155')
writer = QgsVectorFileWriter.writeAsVectorFormat(layer, fn1, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)

layer1 = iface.addVectorLayer(fn1, '', 'ogr')
del(writer)