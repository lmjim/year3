import arcpy
from arcpy import env
import datetime as dt

from createDocuments import setUp
from modifyElements import *
from createChoropleth import changeDisplay

wrkspc = r"D:\Users\Lily\Documents\ArcGISProjects\407Project"
env.workspace = wrkspc
env.overwriteOutput = True
years = [2005, 2010, 2015]
blankDocument = wrkspc + "\\layout\\Layout.mxd"
    
setUp(years, wrkspc, blankDocument)
print "Done with data frame setup"
    
configText(years, wrkspc)
print "Done with text configuration"

configScaleBar(years, wrkspc)
print "Done with scale bar configuration"
configNorthArrow(years, wrkspc)
print "Done with north arrow configuration"

changeDisplay(years, wrkspc)
print "Done with display changes"

configLegend(years, wrkspc)
print "Done with legend configuration"

for year in years:
    currentDataSet = "data" + str(year) 
    document = wrkspc + "\\" + str(year) + "\\" + currentDataSet + ".mxd"
    docPDF = wrkspc + "\\results\\" + currentDataSet + ".pdf"
    mxd = arcpy.mapping.MapDocument(document)
    arcpy.mapping.ExportToPDF(mxd, docPDF)
print "Done exporting to PDF"
