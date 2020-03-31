import arcpy
def changeDisplay(years, wrkspc):
    statesSymbology = arcpy.mapping.Layer(wrkspc + "\\layout\\statesSymbology.lyr")
    naSymbology = arcpy.mapping.Layer(wrkspc + "\\layout\\naSymbology.lyr")
    for year in years:
        currentDataSet = "data" + str(year)
        document = wrkspc + "\\" + str(year) + "\\" + currentDataSet + ".mxd"
        mxd = arcpy.mapping.MapDocument(document)
        dfs = arcpy.mapping.ListDataFrames(mxd)
        for df in dfs:
            lyrs = arcpy.mapping.ListLayers(mxd, "", df)
            arcpy.mapping.UpdateLayer(df, lyrs[1], statesSymbology)
            arcpy.mapping.UpdateLayer(df, lyrs[2], naSymbology)
        mxd.save()
    return
