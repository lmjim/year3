'''
Author: Alex Archer
Date of last modification: 3-6-2020
Description: This determines the on call schedule for weekend shifts
References:
    https://stackoverflow.com/questions/13520876/how-can-i-make-multiple-empty-lists-in-python
'''

import random
import importlib
import raPreferences as raPrefs

def weekendShifts():
    '''
    None ->  [[], []] -- list of two-lists
    Reads the dictionary in raPreferences.py.
    This function acts like a main function specific to scheduling weekends and is called by output.py
    Returns a list of two-lists of the weekend shift schedule.
    '''
    importlib.reload(raPrefs)
    raPreferences =  raPrefs.raPreferences

    ra1 = raPreferences.get('3')[0][0] #ra 1 of bad pair 1
    ra2 = raPreferences.get('3')[0][1] 
    badPair1 = [ra1,ra2] 

    ra3 = raPreferences.get('3')[1][1] #ra 1 of bad pair 2
    ra4 = raPreferences.get('3')[1][1]
    badPair2 = [ra3,ra4]

    '''
    This loop strips the settings from the raPreferences dictonary, makes a copy in raDict
    and appends it with a new integer variable to count the number of shifts. 
    '''
    raDict = {}
    for key,val in raPreferences.items(): 
        if key not in ['1','2','3']:
            raDict[key] = val
            raDict[key].append(0) #add var to counts number of shifts
            raDict[key].append(0) #num primary
            raDict[key].append(0) #num secondary
            
    dictLen = len(list(raDict))
    avg = (78 / dictLen) #there are 78 slots to fill / #RAs. Used for number of shifts enforcement.
  
    '''
    Each Primary/Secondary is a List that corresponds to a weekend with 4 shifts.
    Each weekend is filled by a Primary and a Secondary RA  per shift.
    Week one is unique as there is no Sunday shift. 
    '''
    primary_1 = ["P1 Friday", "P1 Saturday Day", "P1 Saturday Night", "X"]
    secondary_1 = ["S1 Friday", "S1 Saturday Day", "S1 Saturday Night", "X"]

    #The remaining 9 weeks are assigned as empty lists of size 4. 
    primary_2, secondary_2, primary_3, secondary_3, primary_4, secondary_4, primary_5, secondary_5, primary_6,\
        secondary_6, primary_7, secondary_7, primary_8, secondary_8, primary_9, secondary_9, primary_10,\
        secondary_10 = ([None]*4 for i in range(18)) 
    
    #Final output schedule data structure is therefor a list of two-lists.
    schedule = [[primary_1, secondary_1], [primary_2, secondary_2], [primary_3, secondary_3], \
		[primary_4, secondary_4], [primary_5, secondary_5], [primary_6, secondary_6], \
		[primary_7, secondary_7], [primary_8, secondary_8], [primary_9, secondary_9], \
		[primary_10, secondary_10]]

    weekcount = 1

    ''' This loop assigns RAs to the first week's primary and secondary shifts. There is no sunday shift ''' 
    for day in range(3): #friday, saturday day, saturday night
        firstRa = random.choice(list(raDict)) #pick primary worker
        #make sure they don't have the week off
        while weekcount == raDict.get(firstRa)[4] or weekcount == raDict.get(firstRa)[5] or \
              weekcount == raDict.get(firstRa)[6]:
            firstRa = random.choice(list(raDict)) 
        raDict[firstRa][7] += 1 #increase shift counter
        raDict[firstRa][8] += 1 #increase primary
        secondRa = random.choice(list(raDict)) #pick secondary worker
        #make sure they don't have the week off, aren't a disallowed pair, the same person or have a shift already.
        while [firstRa,secondRa] == badPair1 or [secondRa,firstRa] == badPair1 or [firstRa,secondRa] == badPair2 or \
              [secondRa,firstRa] == badPair2 or firstRa == secondRa or weekcount == raDict.get(secondRa)[4] or \
              weekcount == raDict.get(secondRa)[5] or weekcount == raDict.get(secondRa)[6] or raDict.get(secondRa)[7] > 1 : 
            secondRa = random.choice(list(raDict)) 
        raDict[secondRa][7] += 1 #increase shift counter
        raDict[secondRa][9] += 1 #increase secondary counter
        #add each RA to the primary/secondary list for week one.
        primary_1[day] = raDict[firstRa][0]
        secondary_1[day] = raDict[secondRa][0]  
    weekcount += 1

    ''' This loop assigns RAs to Primary and Secondary shifts for weeks 2 through 10 '''
    for week in range(1,10): #weeks 2-10 
        for day in range(4): #friday, saturday day, saturday night, sunday day
            firstRa = random.choice(list(raDict)) #pick primary worker
            #make sure they dont have the week off or have more shifts than average or have more primary than secondary shifts.
            while weekcount == raDict.get(firstRa)[4] or weekcount == raDict.get(firstRa)[5] or \
                  weekcount == raDict.get(firstRa)[6] or raDict.get(firstRa)[8] > raDict.get(firstRa)[9] or raDict.get(firstRa)[7] > avg+1:
                firstRa = random.choice(list(raDict))
                    
            raDict[firstRa][7] += 1 #increase shift counter
            raDict[firstRa][8] += 1 
            secondRa = random.choice(list(raDict)) #pick secondary worker
            #make sure they don't have the week off, aren't a disallowed pair, or the same person, and have no more shifts than average and dont have more secondary than primary shifts.
            while [firstRa,secondRa] == badPair1 or [secondRa,firstRa] == badPair1 or [firstRa,secondRa] == badPair2 or \
                  [secondRa,firstRa] == badPair2 or firstRa == secondRa or weekcount == raDict.get(secondRa)[4] or \
                  weekcount == raDict.get(secondRa)[5] or weekcount == raDict.get(secondRa)[6] or raDict.get(secondRa)[9] > raDict.get(secondRa)[8] or raDict.get(secondRa)[7] > avg+1: 
                secondRa = random.choice(list(raDict))
            raDict[secondRa][7] += 1 #increase shift counter
            raDict[secondRa][9] += 1 
            #add each RA to the primary/secondary list for the particular week
            schedule[week][0][day] = raDict[firstRa][0]
            schedule[week][1][day] = raDict[secondRa][0]
        weekcount += 1

    return(schedule)    

''' These functions are for testing 
  # include **kwargs as function argument
    def clearshifts(): #clears shift counts, useful for resetting.
        for key in raDict.keys():
            raDict[key][7] = 0
            raDict[key][8] = 0
            raDict[key][9] = 0
         
    def shiftcount(): #counts shifts, useful for testing
        numshifts = 0
        for key in raDict.keys():
            numshifts += raDict[key][7]
            print(raDict[key][0], ' has ', raDict[key][7], " shifts. ", raDict[key][8], " primary shifts. ", raDict[key][9], " secondary shifts.") 
        print("numshifts: ", numshifts)
    if kwargs:
        shiftcount()
        clearshifts()
  
alternate code
def weekendShifts():
    raPreferences = input.Input.readingDictPy("raPreferences.py") #Alyssa's import function. makes a copy of read dictonary
    #if not raPreferences:
        #raPreferences = {951111111:	["Alex Archer",	"Tuesday",	"Thursday",	"Sunday", 3, 5, 8], 951111112: ["Kiana Hosaka", "Sunday", "Thursday", "Monday", 2, 6, 4], 951111113: ["Alyssa Huque", "Wednesday", "Monday", "Sunday", 0, 0, 0], 951111114: ["Lily Jim", "Thursday", "Sunday", "Tuesday", 5, 3, 9], 951111115: ["Max Terry", "Monday", "Sunday", "Thursday", 10, 5, 1], 951111116: ["Lucas Hyatt", "Wednesday", "Tuesday", "Monday", 5, 7, 2], 951111117: ["James Kang", "Tuesday", "Monday", "Sunday", 4, 8, 3], 951111118: ["Claire Kolln", "Thursday", "Wednesday", "Tuesday", 6, 9, 0], 951111119: ["Leonie Way", "Sunday", "Tuesday", "Thursday", 3, 2, 8], 951111121: ["Stefan Fields", "Wednesday", "Monday", "Sunday", 10, 1, 5], 951111122: ["Justin Becker", "Thursday", "Wednesday", "Monday", 5, 0, 9], 951111123: ["Cory Ingram", "Monday", "Sunday", "Tuesday", 10, 4, 3], 951111124: ["Samuel Lundquist", "Thursday", "Monday", "Wednesday", 3, 7, 10], 951111125: ["Olivia Pannell", "Monday", "Wednesday", "Thursday", 2, 4, 9], 951111126: ["Bethany Van Meter", "Sunday", "Thursday", "Tuesday", 9, 3, 8], 951111127: ["Ryan Gurnick", "Thursday", "Monday", "Wednesday", 0, 7, 10], 1: 951111116, 2: 2, 3: [[951111114, 951111127], [0, 0]]}
        #print("WeekdnScheduler: danger, Preference input has failed, switching to default values to avoid crash!")
        #in case input fails!
        
    #if raPreferences.get('3'): #setting key
    p1ra1 = raPreferences.get('3')[0][0] #student 1 of bad pair 1
    p1ra2 = raPreferences.get('3')[0][1] #student 2 of bad pair 1
    bad1 = [p1ra1,p1ra2] #bad pair 1.
        #if the student pair is passed as [0,0] meaning no student pair was selected
        #then dict.get() will turn it into a None.
        #S.T. comparison is made to None later and it doesn't matter
    p2ra1 = raPreferences.get('3')[1][1]  
    p2ra2 = raPreferences.get('3')[1][1]
    bad2 = [p2ra1,p2ra2]
    badpairs = [bad1,bad2]
    #else:
        #print("WeekdnScheduler: danger, setting 3 input has failed, bad pairings settings were not passed or defined.")
    radict = {}
    for key,val in raPreferences.items(): ##copy dictonary w/o preferences
        if key not in ['1','2','3']:
            radict[key] = val
            radict[key].append(0) #add var to counts number of shifts
    dictlen = len(list(radict))
    if dictlen != 0:
        avg = 78/dictlen#there are 78 slots to fill and the length of the list of keys is number of RAs. makes an average. used for number of shifts enforcement.
    else:
        print("WeekdnScheduler: danger, input has failed, there are 0 entries in rapreferences. swapping to default average")
        avg = 6
      
        #placeholders for week cuz Kiana requested a list of two-lists.
    primary_1 = ["P1 Friday", "P1 Saturday Day", "P1 Saturday Night", "X"]
    secondary_1 = ["S1 Friday", "S1 Saturday Day", "S1 Saturday Night", "X"]
    primary_2 = ["P2 Friday", "P2 Saturday Day", "P2 Saturday Night", "P2 Sunday Day"]
    secondary_2 = ["S2 Friday", "S2 Saturday Day", "S2 Saturday Night", "S2 Sunday Day"]
    primary_3 = ["P3 Friday", "P3 Saturday Day", "P3 Saturday Night", "P3 Sunday Day"]
    secondary_3 = ["S3 Friday", "S3 Saturday Day", "S3 Saturday Night", "S3 Sunday Day"]
    primary_4 = ["P4 Friday", "P4 Saturday Day", "P4 Saturday Night", "P4 Sunday Day"]
    secondary_4 = ["S4 Friday", "S4 Saturday Day", "S4 Saturday Night", "S4 Sunday Day"]
    primary_5 = ["P5 Friday", "P5 Saturday Day", "P5 Saturday Night", "P5 Sunday Day"]
    secondary_5 = ["S5 Friday", "S5 Saturday Day", "S5 Saturday Night", "S5 Sunday Day"]
    primary_6 = ["P6 Friday", "P6 Saturday Day", "P6 Saturday Night", "P6 Sunday Day"]
    secondary_6 = ["S6 Friday", "S6 Saturday Day", "S6 Saturday Night", "S6 Sunday Day"]
    primary_7 = ["P7 Friday", "P7 Saturday Day", "P7 Saturday Night", "P7 Sunday Day"]
    secondary_7 = ["S7 Friday", "S7 Saturday Day", "S7 Saturday Night", "S7 Sunday Day"]
    primary_8 = ["P8 Friday", "P8 Saturday Day", "P8 Saturday Night", "P8 Sunday Day"]
    secondary_8 = ["S8 Friday", "S8 Saturday Day", "S8 Saturday Night", "S8 Sunday Day"]
    primary_9 = ["P9 Friday", "P9 Saturday Day", "P9 Saturday Night", "P9 Sunday Day"]
    secondary_9 = ["S9 Friday", "S9 Saturday Day", "S9 Saturday Night", "S9 Sunday Day"]
    primary_10 = ["P10 Friday", "P10 Saturday Day", "P10 Saturday Night", "P10 Sunday Day"]
    secondary_10 = ["S10 Friday", "S10 Saturday Day", "S10 Saturday Night", "S10 Sunday Day"]
    #final output structure. list of two-lists.
    schedule = [[primary_1, secondary_1], [primary_2, secondary_2], [primary_3, secondary_3], \
		[primary_4, secondary_4], [primary_5, secondary_5], [primary_6, secondary_6], \
		[primary_7, secondary_7], [primary_8, secondary_8], [primary_9, secondary_9], \
		[primary_10, secondary_10]]
    weekcount = 1
    
    for i in range(3): #friday, saturday day, saturday night of week 1. Number of shifts are not considered.
        tmp = random.choice(list(radict)) #pick primary worker
        while weekcount == radict.get(tmp)[4] or weekcount == radict.get(tmp)[5] or weekcount == radict.get(tmp)[6]:
            tmp = random.choice(list(radict)) #make sure they dont have the week off
        radict[tmp][7] += 1 #increase shift counter
        tmp2 = random.choice(list(radict)) #pick secondary worker
        while [tmp,tmp2] == bad1 or [tmp2,tmp] == bad1 or [tmp,tmp2] == bad2 or [tmp2,tmp] == bad2 or tmp == tmp2 or weekcount == radict.get(tmp2)[4] or weekcount == radict.get(tmp2)[5]or weekcount == radict.get(tmp2)[6]: 
            tmp2 = random.choice(list(radict)) #make sure they arent the same person, a bad pair or have the week off.
        radict[tmp2][7] += 1 #increase shift counter
        primary_1[i] = radict[tmp][0]
        secondary_1[i] = radict[tmp2][0]    #update the week lists...
    weekcount += 1
    
    for x in range(1,10): #weeks 2-10 to be considered
        for i in range(4): #friday, saturday day, saturday night, sunday day
            tmp = random.choice(list(radict)) #pick primary worker
            while weekcount == radict.get(tmp)[4] or weekcount == radict.get(tmp)[5] or weekcount == radict.get(tmp)[6] or radict.get(tmp)[7] > avg:
                tmp = random.choice(list(radict)) #make sure they dont have the week off or have more shifts than average.
            radict[tmp][7] += 1 #increase shift counter
            tmp2 = random.choice(list(radict)) #pick secondary worker
            while [tmp,tmp2] == bad1 or [tmp2,tmp] == bad1 or [tmp,tmp2] == bad2 or [tmp2,tmp] == bad2 or tmp == tmp2 or weekcount == radict.get(tmp2)[4] or weekcount == radict.get(tmp2)[5] or weekcount == radict.get(tmp2)[6]or radict.get(tmp2)[7] > avg+1: 
                tmp2 = random.choice(list(radict)) #make sure they arent the same person, a bad pair or have the week off or have more shifts than average.
            radict[tmp2][7] += 1 #increase shift counter
            schedule[x][0][i] = radict[tmp][0]
            schedule[x][1][i] = radict[tmp2][0]    #update the week lists..
        weekcount += 1
    return(schedule)  
'''
