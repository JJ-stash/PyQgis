fn = r'Rivers.shp'
layer = QgsVectorLayer(fn, '', 'ogr')


# გამოთვლა მ და კმ + დამატება Code ფილდის

pv = layer.dataProvider()
pv.addAttributes([QgsField('lengthM', QVariant.Double), QgsField('lengthKM', QVariant.Double), QgsField('Code', QVariant.Int)])
layer.updateFields()

expr1 = QgsExpression('$lengthM')
expr2 = QgsExpression('"lengthM"/1000')

cntx = QgsExpressionContext()
cntx.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

with edit(layer):
    for i in layer.getFeatures():
        cntx.setFeature(i)
        i['lengthM'] = expr1.evaluate(cntx)
        layer.updateFeature(i)
with edit(layer):
    for i in layer.getFeatures():
        cntx.setFeature(i)
        i['lengthKM'] = expr2.evaluate(cntx)
        layer.updateFeature(i)


## Code ფილდში შეტანა 1,2 ან 3ის

with edit(layer):
    for i in layer.getFeatures():
        if i['lengthKM'] < 75:
            cntx.setFeature(i)
            i['Code'] = 1
            layer.updateFeature(i)
        elif i['lenghtKM'] > 75 and i['lenghtKM'] < 150:
            cntx.setFeature(i)
            i['Code'] = 2
            layer.updateFeature(i)
        elif i['lengthKM'] > 150:
            cntx.setFeature(i)
            i['Code'] = 3
            layer.updateFeature(i)


## Dissolve :

out = r'Rivers_Diss.shp'
fields = layer.fields()
feats = layer.getFeatures()

for i in feats:
    if i['Code'] == 1:
        processing.run('native:buffer', {'INPUT' : fn, 'DISTANCE' : 1000, 'DISSOLVE' : True, 'OUTPUT' : out})
    elif i['Code'] == 2:
        processing.run('native:buffer', {'INPUT' : fn, 'DISTANCE' : 2000, 'DISSOLVE' : True, 'OUTPUT' : out})
    elif i['Code'] == 3:
        processing.run('native:buffer', {'INPUT' : fn, 'DISTANCE' : 3000, 'DISSOLVE' : True, 'OUTPUT' : out})

iface.addVectorLayer(fn, '', 'ogr')
iface.addVectorLayer(out, '', 'ogr')