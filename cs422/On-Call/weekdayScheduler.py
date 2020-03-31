'''
Author: Max Terry
Date of last modification: 3-5-2020
Description: This determines the on call schedule for weekday shifts
References:
    TODO
'''

import ast
import random
import raPreferences
import importlib

class WeekdayShifts:
    def __init__(self):
        '''
        None -> (None)
        Sets the initial values of class variables
        '''
        raInfo = self.getRaInformation()
        self.raPreferences = raInfo[0]
        self.settings = raInfo[1]
        return None

    def getRaInformation(self):
        '''
        None -> (dictionary,dictionary)
        Reads the dictionary in raPreferences.py.
        Returns a dictionary containing the preference information.
        '''
        importlib.reload(raPreferences)
        fileContents = ''
        tempRaPreferences = {}
        with open("raPreferences.py", "r") as prefFile:
            fileContents = prefFile.readlines()[0]
            tempRaPreferences = ast.literal_eval(fileContents.strip("raPreferences = "))

        finalReference = {}
        settings = {}
        for raId in tempRaPreferences:
            if raId not in ['1','2','3']:       #to save just the RA information
                finalReference[raId] = tempRaPreferences[raId][0:4]       #gets rid of weekend information
                finalReference[raId].append(0)           #to keep track of shift counter
                finalReference[raId].append(0)           #to keep track of number of primary shifts
            else:
                settings[raId] = tempRaPreferences[raId]

        return finalReference,settings

    def weekdayShifts(self):
        '''
        None -> (list)
        This function acts like a main function specific to scheduling weekdays and is called by output.py
        Returns a dictionary of the weekday shifts
        '''

        if(len(self.raPreferences) != 0):
            weekdays = self.assignDays()
            schedule = self.scheduleShifts(weekdays)
            return schedule
        else:
            print("Error in loading RA preferences")

    def assignDays(self):
        '''
        None -> dict
        assigns each RA to the weekday that they will be scheduled on for the term
        '''
        #schedule  this many per day at first, then fill in the last few later
        raPerDay = len(self.raPreferences) // 5
        leftOver = len(self.raPreferences) - (raPerDay * 5)
        weekdays = {"Sunday": [], "Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": []}
        raList = list(self.raPreferences.keys())
        
        #Gold star RA gets their first preference
        if(self.settings['1'] != 0):                    #Not necessarily a gold star RA
            goldStarRa = self.settings['1']
            goldStarInfo = self.raPreferences[goldStarRa]
            goldStarDay = goldStarInfo[1]
            weekdays[goldStarDay].append(goldStarRa)
            raList.remove(goldStarRa)

        rasToRemove = []
        random.shuffle(raList)          #so every ra has an equal chance of being scheduled first/last
        #first choice loop
        for ra in raList:
            firstPreference = self.raPreferences[ra][1]
            if(len(weekdays[firstPreference]) < raPerDay and self.badPairInDay(weekdays[firstPreference], ra) == False):
                weekdays[firstPreference].append(ra)
                rasToRemove.append(ra)
        raList = [ra for ra in raList if ra not in rasToRemove]     #removes the scheduled RAs so they are not considered later

        #second choice loop
        rasToRemove = []
        random.shuffle(raList)
        for ra in raList:
            secondPreference = self.raPreferences[ra][2]
            if(len(weekdays[secondPreference]) < raPerDay and self.badPairInDay(weekdays[secondPreference], ra) == False):
                weekdays[secondPreference].append(ra)
                rasToRemove.append(ra)
        raList = [ra for ra in raList if ra not in rasToRemove]

        #third choice loop
        rasToRemove = []
        random.shuffle(raList)
        for ra in raList:
            thirdPreference = self.raPreferences[ra][3]
            if(len(weekdays[thirdPreference]) < raPerDay and self.badPairInDay(weekdays[thirdPreference], ra) == False):
                weekdays[thirdPreference].append(ra)
                rasToRemove.append(ra)
        raList = [ra for ra in raList if ra not in rasToRemove]

        #make sure everyday has three people on it before assigning extra days
        tieSetting = self.settings['2']     #Decides how to break ties
        random.shuffle(raList)
        for day in weekdays:
            while(len(weekdays[day]) != raPerDay):
                raSelected = self.tiebreaker(tieSetting, raList)
                if(self.badPairInDay(weekdays[firstPreference], ra) == False):
                    weekdays[day].append(raSelected)       #adds the student selected by the tie breaker
                    raList.remove(raSelected)

        if(len(raList) != 0):
            #for leftover people
            rasToRemove = []
            random.shuffle(raList)
            for ra in raList:
                tempRaPreferences = self.raPreferences[ra][1:4]
                for i in range(3):                                  #preferences
                    day = tempRaPreferences[i]
                    if(len(weekdays[day]) < raPerDay + 1 and ra not in rasToRemove and self.badPairInDay(weekdays[day], ra) == False):
                        weekdays[day].append(ra)
                        rasToRemove.append(ra)
                if ra not in rasToRemove:                               #this would happen if an extra spot needs to be filled but it is not one of the ras preferences
                    for day in weekdays:
                        if(len(weekdays[day]) < raPerDay + 1 and ra not in rasToRemove and self.badPairInDay(weekdays[day], ra) == False):
                            weekdays[day].append(ra)
                            rasToRemove.append(ra)

            raList = [ra for ra in raList if ra not in rasToRemove]
        return weekdays

    def tiebreaker(self, tieSetting, raList):
        '''
        int,list -> string
        Returns an ra from a list of ras based on the user's tiebreaker setting.
        Tiebreaks will either be done randomly, alphabetically by last name, or numerically by student ID number
        '''
        if(tieSetting == 0):                    #for random tiebreakers
            randomRa = random.choice(raList)
            return randomRa
        elif(tieSetting == 1):                  #alphabetical by last name tiebreaker
            lastNames = []
            for ra in raList:
                lastNames.append([ra, self.raPreferences[ra][0].split()[1]])      #just want to keep track of last names
            minName = lastNames[0]
            for name in lastNames:
                if name[1] < minName[1]:
                    minName = name
            return minName[0]                 #alphabetically first by last name
        elif(tieSetting == 2):             #for numeric by student ID number
            idList = []
            for ra in raList:
                idList.append(int(ra))
            raToReturn = str(min(idList))
            return raToReturn

    def badPairInDay(self, weekday, ra):
        '''
        list,string -> boolean
        Checks to see if an RA can be scheduled based on the presence of a bad pair, defined by the user
        '''
        isBadPair = False
        badPairs = self.settings['3']
        for pair in badPairs:               #checks to see if the RA even has a bad pair in the first place
            if ra in pair:
                isBadPair = True

        if(isBadPair == False):                     #if the RA is in neither bad pair list, then the ra can be scheduled with anyone
            return False

        for studentNo in weekday:
            if((studentNo in badPairs[0] and ra in badPairs[0]) or (studentNo in badPairs[1] and ra in badPairs[1])): #if the
                return True
        return False                         #means an ra is in a bad pair, but that bad pair is not present on this day

    def scheduleShifts(self, initialWeekdays):
        '''
        dictionary -> list
        Once the ras are all assigned to a day, this function actually schedules them week by week
        '''
        weekdays = initialWeekdays.copy()       #to avoid aliasing
        finalShiftList = []

        for i in range(10):     #ten weeks
            weekList = []
            primaryList = []
            secondaryList = []
            for day in weekdays:  #5 shifts per week
                needShiftRas = []           #will save who has the fewest shifts
                minShifts = 1000            #start at a high number so the first RA will be lower
                
                for ra in weekdays[day]:     #go through the ras to see who needs more shifts 
                    numberShifts = self.raPreferences[ra][4]
                    if numberShifts < minShifts:
                        minShifts = numberShifts
                        needShiftRas = [ra]      #save the name in the list of fewest shifts
                    elif numberShifts == minShifts:
                        needShiftRas.append(ra)

                if(len(needShiftRas) < 2):          #if there is only one person with the minimum number of shifts
                    haveShiftRas = weekdays[day].copy()
                    haveShiftRas.remove(needShiftRas[0])    #have to get rid of this to avoid duplicates
                    needShiftRas.append(random.choice(haveShiftRas))

                minPrimaryShifts = 1000
                minRa = ''
                for ra in needShiftRas:
                    if(self.raPreferences[ra][5] < minPrimaryShifts):
                        minPrimaryShifts = self.raPreferences[ra][5]
                        minRa = ra

                primaryRa = minRa#random.choice(needShiftRas)
                needShiftRas.remove(primaryRa)              #so there isnt a repeat here
                self.raPreferences[primaryRa][4] += 1       #increment the shift counter
                self.raPreferences[primaryRa][5] += 1       #increment the primary RA counter

                secondaryRa = random.choice(needShiftRas)   #don't need to remove this one as the availableRa list resets anyways
                self.raPreferences[secondaryRa][4] += 1

                primaryList.append(self.raPreferences[primaryRa][0])            #want all primary/secondary ras for a week in separate lists
                secondaryList.append(self.raPreferences[secondaryRa][0])

            weekList.append(primaryList)
            weekList.append(secondaryList)
            finalShiftList.append(weekList)
        return finalShiftList