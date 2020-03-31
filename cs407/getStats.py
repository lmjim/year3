import arcpy
def getTotal(wrkspc, currentDataSet, document):
    # Total number of deaths
    mxd = arcpy.mapping.MapDocument(document)
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    intable = arcpy.mapping.ListLayers(mxd, "", df)[1]
    outtable = wrkspc + "\\sumstats"
    fieldName = currentDataSet + ".csv.Deaths"
    path = arcpy.Statistics_analysis(intable, outtable, [[fieldName, "SUM"]])
    fields = arcpy.ListFields(path)
    total = int([row[0] for row in arcpy.da.SearchCursor(path, [fields[3].name])][0])
    del mxd
    return total

def getMax(wrkspc, currentDataSet, document):
    # Top two states with highest death count
    mxd = arcpy.mapping.MapDocument(document)
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    layer = arcpy.mapping.ListLayers(mxd, "", df)[1]
    out = wrkspc + "\\sumstats"
    deathsField = currentDataSet + ".csv.Deaths"
    path = arcpy.Statistics_analysis(layer, out, [[deathsField, "MAX"]])
    fields = arcpy.ListFields(path)
    maximum = [row[0] for row in arcpy.da.SearchCursor(path, [fields[3].name])][0]
    second = 0 
    nameField = currentDataSet + ".csv.State" 
    state = "unknown"
    state2 = "unknown"
    cursor = arcpy.da.SearchCursor(layer, [nameField, deathsField], deathsField+" > 1000")
    for row in cursor:
        if row[1] == maximum:
            state = row[0]
        else:
            if row[1] > second:
                second = row[1]
                state2 = row[0]
    del mxd
    return [state, state2]

def getCrudeMax(wrkspc, currentDataSet, document):
    # Top two states with highest crude rate
    mxd = arcpy.mapping.MapDocument(document)
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    layer = arcpy.mapping.ListLayers(mxd, "", df)[1]
    out = wrkspc + "\\sumstats"
    rateField = "US_states.CRUDE_RATE"
    path = arcpy.Statistics_analysis(layer, out, [[rateField, "MAX"]])
    fields = arcpy.ListFields(path)
    maximum = [row[0] for row in arcpy.da.SearchCursor(path, [fields[3].name])][0]
    second = 0
    nameField = currentDataSet + ".csv.State"
    state = "unknown"
    state2 = "unknown"
    cursor = arcpy.da.SearchCursor(layer, [nameField, rateField], rateField + " > 15")
    for row in cursor:
        if row[1] == maximum:
            state = row[0]
        else: 
            if row[1] > second:
                second = row[1]
                state2 = row[0]
    del mxd
    return [state, state2]
