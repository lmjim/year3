import arcpy
import getStats
def configText(years, wrkspc):
    for year in years:
        currentDataSet = "data" + str(year) 
        document = wrkspc + "\\" + str(year) + "\\" + currentDataSet + ".mxd" 
        totalDeaths = getStats.getTotal(wrkspc, currentDataSet, document) 
        maxDeaths = getStats.getMax(wrkspc, currentDataSet, document) 
        maxCrudeRate = getStats.getCrudeMax(wrkspc, currentDataSet, document) 
        mxd = arcpy.mapping.MapDocument(document)

        elemlist = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
        i = 0
        while i < 7:
            elemlist[0].clone()
            i = i + 1
        del elemlist
            
        # Modify text elements
        elemlist = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
        note = elemlist[0]
        note.name = "note"
        note.text = "* Crude Rate is per 100,000 based on state's population"
        analysis = elemlist[1]
        analysis.name = "analysis"
        analysis.text = maxDeaths[0] + " has the highest total number of deaths followed by " + maxDeaths[1] + ".\n" + maxCrudeRate[0] + " has the highest crude rate followed by " + maxCrudeRate[1] + "." 
        total = elemlist[2]
        total.name = "total"
        total.text = "Total Number of Deaths Caused by Firearms: " + str(totalDeaths)
        hawaii = elemlist[3]
        hawaii.name = "hawaiiLabel"
        hawaii.text = "Hawaii"
        alaska = elemlist[4]
        alaska.name = "alaskaLabel"
        alaska.text = "Alaska"
        contUS = elemlist[5]
        contUS.name = "contUSLabel"
        contUS.text = "Contiguous United States"
        sources = elemlist[6]
        sources.name = "sources"
        sources.text = "Sources: NYU Spatial Data Repository; United States Census Bureau; National Center for Injury Prevention and Control, CDC"
        author = elemlist[7]
        author.name = "author"
        author.text = "Created by: Lily Jim"
        title = elemlist[8]
        title.name = "title"
        title.text = "Deaths Caused by Firearms in " + str(year)

        # Note
        note.fontSize = 10.0
        note.elementHeight =  0.1552
        note.elementWidth = 3.447
        note.elementPositionX = 6.6765
        note.elementPositionY = 1.5
        # Analysis
        analysis.fontSize = 9.53
        analysis.elementHeight = 0.30
        analysis.elementWidth = 3.9645
        analysis.elementPositionX = 6.4178
        analysis.elementPositionY = 1.75
        # Total
        total.fontSize = 12.89
        total.elementHeight = 0.20
        total.elementWidth = 4.1882
        total.elementPositionX = 6.3059
        total.elementPositionY = 2.1
        # Hawaii
        hawaii.fontSize = 10.0
        hawaii.elementHeight = 0.150
        hawaii.elementWidth = 0.4028
        hawaii.elementPositionX = 3.7172
        hawaii.elementPositionY = 1.8
        # Alaska
        alaska.fontSize = 10.0
        alaska.elementHeight = 0.15
        alaska.elementWidth = 0.4028
        alaska.elementPositionX = 1.7172
        alaska.elementPositionY = 1.8
        # Contiguous US
        contUS.fontSize = 12.89
        contUS.elementHeight = 0.20
        contUS.elementWidth = 2.0296
        contUS.elementPositionX = 6.758
        contUS.elementPositionY = 2.8
        # Sources
        sources.fontSize = 9.67
        sources.elementHeight = 0.150
        sources.elementWidth = 7.484
        sources.elementPositionX = 2.516
        sources.elementPositionY = 7.3
        # Author
        author.fontSize = 9.66
        author.elementHeight = 0.150
        author.elementWidth = 1.1786
        author.elementPositionX = 1
        author.elementPositionY = 7.3
        # Title
        title.fontSize = 19.33
        title.elementHeight = 0.30
        title.elementWidth = 4.2979
        title.elementPositionX = 3.3511
        title.elementPositionY = 7.45

        mxd.save()
    return

def configScaleBar(years, wrkspc):
    for year in years:
        currentDataSet = "data" + str(year)
        document = wrkspc + "\\" + str(year) + "\\" + currentDataSet + ".mxd"
        mxd = arcpy.mapping.MapDocument(document)
        elemlist = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "Alternating Scale Bar")
        # Contiguous US
        contUS = elemlist[2]
        contUS.name = "contUSScale"
        contUS.elementHeight = 0.3156
        contUS.elementWidth = 2.5713
        contUS.elementPositionX = 6.6144
        contUS.elementPositionY = 2.4344
        # Hawaii
        hawaii = elemlist[1]
        hawaii.name = "hawaiiScale"
        hawaii.elementHeight = 0.2525
        hawaii.elementWidth = 1.320
        hawaii.elementPositionX = 3.2579
        hawaii.elementPositionY = 1.4975
        # Alaska
        alaska = elemlist[0]
        alaska.name = "alaskaScale"
        alaska.elementHeight = 0.2525
        alaska.elementWidth = 1.3214
        alaska.elementPositionX = 1.2579
        alaska.elementPositionY = 1.4975

        mxd.save()
    return

def configNorthArrow(years, wrkspc):
    for year in years:
        currentDataSet = "data" + str(year)
        document = wrkspc + "\\" + str(year) + "\\" + currentDataSet + ".mxd"
        mxd = arcpy.mapping.MapDocument(document)
        elemlist = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "North Arrow")
        # Contiguous US
        contUS = elemlist[2]
        contUS.name = "contUSArrow"
        contUS.elementHeight = 0.4
        contUS.elementWidth = 0.192
        contUS.elementPositionX = 9.304
        contUS.elementPositionY = 2.5
        # Hawaii
        hawaii = elemlist[1]
        hawaii.name = "hawaiiArrow"
        hawaii.elementHeight = 0.4
        hawaii.elementWidth = 0.192
        hawaii.elementPositionX = 4.6453
        hawaii.elementPositionY = 1.55
        # Alaska
        alaska = elemlist[0]
        alaska.name = "alaskaArrow"
        alaska.elementHeight = 0.4
        alaska.elementWidth = 0.192
        alaska.elementPositionX = 1.0
        alaska.elementPositionY = 1.55

        mxd.save()
    return

def configLegend(years, wrkspc):
    for year in years:
        currentDataSet = "data" + str(year)
        document = wrkspc + "\\" + str(year) + "\\" + currentDataSet + ".mxd"
        mxd = arcpy.mapping.MapDocument(document)
        legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
        # Legend
        legend.elementHeight = 1.6
        legend.elementWidth = 0.9857
        legend.elementPositionX = 5.2815
        legend.elementPositionY = 1.4

        mxd.save()
    return

