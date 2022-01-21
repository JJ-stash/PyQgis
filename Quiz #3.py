import processing

inp = r'Horizontals.shp'
out = r'Horizontals_Tin.tif'
asp = r'Quiz_3/ASP.tif'
slp = r'Quiz_3/SLP.tif'

processing.run("qgis:tininterpolation", {'INTERPOLATION_DATA':inp + '::~::0::~::1::~::1','METHOD':0, 'EXTENT':'203375.234400000,216405.989600000,4773417.596900000,4785390.016700000 [EPSG:32638]', 'PIXEL_SIZE':150,'OUTPUT':out})

processing.run('native:aspect',{'INPUT' : out, 'Z_FACTOR' : 1, 'OUTPUT' : asp})
iface.addRasterLayer(asp)

processing.run('native:slope',{'INPUT' : out, 'Z_FACTOR' : 1, 'OUTPUT' : slp})
iface.addRasterLayer(slp)