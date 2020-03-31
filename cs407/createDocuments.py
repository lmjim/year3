import arcpy
def setUp(years, wrkspc, blankDocument):
    for year in years:
        currentDataSet = "data" + str(year)
        untitled = arcpy.mapping.MapDocument(blankDocument)
        document = wrkspc + "\\" + str(year) + "\\" + currentDataSet + ".mxd"
        untitled.saveACopy(document)
        del untitled
    for year in years:
        currentDataSet = "data" + str(year)
        document = wrkspc + "\\" + str(year) + "\\" + currentDataSet + ".mxd"
        mxd = arcpy.mapping.MapDocument(document)
        df1 = arcpy.mapping.ListDataFrames(mxd)[0]
        df2 = arcpy.mapping.ListDataFrames(mxd)[1]
        df3 = arcpy.mapping.ListDataFrames(mxd)[2]
        legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
        legend.autoAdd = False
        
        arcpy.Copy_management("shapeFiles/US_states.shp", wrkspc + "\\" + str(year) + "\\US_states.shp")
        arcpy.AddField_management(wrkspc + "\\" + str(year) + "\\US_states.shp", "CRUDE_RATE", "DOUBLE")
        usStates = arcpy.mapping.Layer(wrkspc + "\\" + str(year) + "\\US_states.shp")
        na = arcpy.mapping.Layer("shapeFiles/North_America.shp")
        mainland = arcpy.mapping.Layer("shapeFiles/mainland.shp")
        hawaii = arcpy.mapping.Layer("shapeFiles/hawaii.shp")
        alaska = arcpy.mapping.Layer("shapeFiles/alaska.shp")
        
        table = "dataTables/" + currentDataSet + ".csv"
        arcpy.AddJoin_management(usStates, "NAME", table, "State")
        field = currentDataSet + ".csv.Crude Rate"
        arcpy.CalculateField_management(usStates, "CRUDE_RATE", "!" + field + "!", "PYTHON")
        
        df1.name = "mainland"
        mainland.visible = False
        arcpy.mapping.AddLayer(df1, mainland)
        legend.autoAdd = True
        arcpy.mapping.AddLayer(df1, usStates, "BOTTOM")
        legend.autoAdd = False
        arcpy.mapping.AddLayer(df1, na, "BOTTOM")

        df2.name = "hawaii"
        hawaii.visible = False
        arcpy.mapping.AddLayer(df2, hawaii)
        arcpy.mapping.AddLayer(df2, usStates, "BOTTOM")
        arcpy.mapping.AddLayer(df2, na, "BOTTOM")

        df3.name = "alaska"
        alaska.visible = False
        arcpy.mapping.AddLayer(df3, alaska)
        arcpy.mapping.AddLayer(df3, usStates, "BOTTOM")
        arcpy.mapping.AddLayer(df3, na, "BOTTOM")

        df1.elementHeight = 4.1538
        df1.elementWidth = 9
        df1.elementPositionX = 1
        df1.elementPositionY = 3.0962

        df2.elementHeight = 1.0
        df2.elementWidth = 1.8373
        df2.elementPositionX = 3.0
        df2.elementPositionY = 2.0

        df3.elementHeight = 1.0
        df3.elementWidth = 1.8372
        df3.elementPositionX = 1
        df3.elementPositionY = 2.0
        
        extent1 = df1.extent
        extent1.XMin = -125.654729593
        extent1.XMax = -65.757570507
        extent1.YMin = 23.357817783
        extent1.YMax = 51.002660438
        df1.extent = extent1

        extent2 = df2.extent
        extent2.XMin = -179.699756338
        extent2.XMax = -153.499628662
        extent2.YMin = 16.56082258
        extent2.YMax = 30.82190642 
        df2.extent = extent2

        extent3 = df3.extent
        extent3.XMin = -181.544314649
        extent3.XMax = -128.085270896
        extent3.YMin = 46.270878862
        extent3.YMax = 75.369359388
        df3.extent = extent3
            
        mxd.save()
    return
