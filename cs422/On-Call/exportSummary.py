'''
Author: Max Terry
Date of last modification: 3-5-2020
Description: Outputs a report of RA scheduling information in a separate file
'''

import shiftAssignments as sa
import importlib
import weekdayScheduler as week

def exportShiftInfo(fileName):
	'''
	string -> None
	Function will output information about each RA in the list.
	This includes the days the work, their total number of shifts, and total number of primary shifts.
	'''
	importlib.reload(sa)
	raInfo = week.WeekdayShifts().getRaInformation()[0]
	raDict = {}
	days = {0:"Sunday Day", 1:"Sunday Night", 2:"Monday", 3:"Tuesday",4:"Wednesday",5:"Thursday",6:"Friday", 7:"Saturday Day", 8:"Saturday Night"}

	for ra in raInfo:
		raDict[raInfo[ra][0]] = [[0,0],[0,0],[],[]]			#[[weekdayPrimary,weekdaySecondary], [weekendPrimary, weekendSecondary], [weekdays], [weekends]]

	for i in range(1,11):								#ten weeks
		primaryForWeek = sa.shiftAssignments[i][0]
		secondaryForWeek = sa.shiftAssignments[i][1]
		dayCounter = 0
		for ra in primaryForWeek:
			if ra in raDict.keys():
				if(dayCounter < 1 or dayCounter > 5):			#would mean its a weekend, so incremement primary weekend counter
					raDict[ra][1][0] += 1
					if(days[dayCounter] not in raDict[ra][3]):
						raDict[ra][3].append(days[dayCounter])	#adds weekend to weekend list
				else:
					raDict[ra][0][0] += 1
					if(days[dayCounter] not in raDict[ra][2]):
						raDict[ra][2].append(days[dayCounter])

			dayCounter += 1

		dayCounter = 0
		for ra in secondaryForWeek:
			if ra in raDict.keys():
				if(dayCounter < 1 or dayCounter > 5):			#would mean its a weekend, so increment secondary weekend counter
					raDict[ra][1][1] += 1
					if(days[dayCounter] not in raDict[ra][3]):
						raDict[ra][3].append(days[dayCounter])	#adds weekend to weekend list
				else:
					raDict[ra][0][1] += 1
					if(days[dayCounter] not in raDict[ra][2]):
						raDict[ra][2].append(days[dayCounter])
			dayCounter += 1

	try:
		output_file = open(fileName, 'w')
	except:
		return 1

	for ra in raDict:											#loop through each RA and write the necessary information to a txt file
		output_file.write(ra + '\n')
		output_file.write("Weekday Assigned: " + raDict[ra][2][0] + "\n")		#should only be one weekday here
		output_file.write("Total number of weekday shifts: " + str(sum(raDict[ra][0])) + "\n")
		output_file.write("Total number of primary weekday shifts: " + str(raDict[ra][0][0]) + "\n")
		output_file.write("Weekends Assigned: " + ", ".join(raDict[ra][3]) + "\n")
		output_file.write("Total number of weekend shifts: " + str(sum(raDict[ra][1])) + "\n")
		output_file.write("Total number of primary weekend shifts: " + str(raDict[ra][1][0]) + "\n")
		output_file.write("\n")

	output_file.close()

'''def exportShiftInfo(fileName):
	importlib.reload(sa)
	primaryInfo = {}
	secondaryInfo = {}
	cummulativeInfo = {}
	days = {0:"Sunday Day", 1:"Sunday Night", 2:"Monday",3:"Tuesday",4:"Wednesday",5:"Thursday",6:"Friday",7:"Saturday Day",8:"Saturday Night"}

	try:
		open(fileName, 'w')
	except:
		return 1

	for i in range(1,11):				#10 weeks
		primary = sa.shiftAssignments[i][0]
		secondary = sa.shiftAssignments[i][1]
		for ra in primary:
			day = primary.index(ra)
			if ra in primaryInfo.keys():
				primaryInfo[ra][0] += 1
				if day not in primaryInfo[ra][1]:
					primaryInfo[ra][1].append(days[day])
			else:
				primaryInfo[ra] = [1, [days[day]]]		#number of primary shifts

		for ra in secondary:
			day = secondary.index(ra)
			if ra in secondaryInfo.keys():
				secondaryInfo[ra][0] += 1
				if day not in secondaryInfo[ra][1]:
					secondaryInfo[ra][1].append(days[day])
			else:
				secondaryInfo[ra] = [1, [days[day]]]		#number of secondary shifts

	for ra in primaryInfo.keys():
		cummulativeInfo[ra] = [primaryInfo[ra], secondaryInfo[ra]]

	for ra in cummulativeInfo:
		print(ra, ' ', cummulativeInfo[ra][0], ' ', cummulativeInfo[ra][1])

	print(cummulativeInfo)

	#print(primaryInfo)
	#print(secondaryInfo)
'''