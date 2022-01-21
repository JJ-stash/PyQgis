import processing
from qgis.PyQt import QtGui

inp = r'Horizontals.shp'
out = r'Horizontals_Tin.tif'

### out AKA Tin
processing.run("qgis:tininterpolation", {'INTERPOLATION_DATA':inp + '::~::0::~::1::~::1','METHOD':0,'EXTENT' : '592924.1634,602924.1634,4640845.6831,4650845.6831 [EPSG:32638]', 'PIXEL_SIZE':200,'OUTPUT':out})

### Statistics of out
tinlayer = iface.addRasterLayer(out)
stats = tinlayer.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
minVal = int(stats.minimumValue)
meanVal = int(stats.mean)
maxVal = int(stats.maximumValue)
sumOfVals = minVal+meanVal+maxVal
print("\nMin: " + str(minVal) + "\nMean: " +  str(meanVal) + "\nMax: " + str(maxVal) + "\nSum of em: " + str(sumOfVals))

### Add Statistics to out
lyr1 = QgsRasterLayer(out)
output = r'Horizontals_Tin_Calc.tif'
entries = []

ras = QgsRasterCalculatorEntry()
ras.ref = 'ras@1'
ras.raster = lyr1
ras.bandNumber = 1
entries.append(ras)

calc = QgsRasterCalculator('ras@1 + 4842', output, 'GTiff', lyr1.extent(), lyr1.width(), lyr1.height(), entries)
calc.processCalculation()

iface.addRasterLayer(output)

### Aspect & Slope of out
asp = r'ASP.tif'
processing.run('native:aspect',{'INPUT' : out, 'Z_FACTOR' : 1, 'OUTPUT' : asp})
iface.addRasterLayer(asp)

slp = r'SLP.tif'
processing.run('native:slope',{'INPUT' : out, 'Z_FACTOR' : 1, 'OUTPUT' : slp})
iface.addRasterLayer(slp)

### Reclassify of slp
reclass = r'Rec_SLP.tif'
processing.run("native:reclassifybytable", {'INPUT_RASTER': slp,'RASTER_BAND':1,'TABLE':['0','10','1','11','20','2','21','30','3','31','40','4','41','50','5'],'NO_DATA':0,'RANGE_BOUNDARIES':0,'NODATA_FOR_MISSING':False,'DATA_TYPE':5,'OUTPUT':reclass})
iface.addRasterLayer(reclass)

### Symbology of inp
#H = iface.addVectorLayer(inp, '', 'ogr')
#S = QgsLineSymbol.createSimple({'line_style' : 'dash', 'color' : 'green'})
#H.renderer().setSymbol(S)
#H.triggerRepaint()
