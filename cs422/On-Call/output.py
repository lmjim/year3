'''
	Author: Kiana Hosaka
	Date of Last Modification: March 1, 2020
	Description: File produces the functionality of the Shift Assignments Module.
	References:
	- Prepending to a list: https://kite.com/python/answers/how-to-prepend-to-a-list-in-python
	- Ensuring file could be opened: https://stackoverflow.com/questions/6825994/check-if-a-file-is-open-in-python

'''

import importlib
import shiftAssignments as sa
#import test_week as week # For testing
#import test_end as end # For testing
import weekdayScheduler as week
import weekendScheduler as end

# List of previous shiftAssignments dictionary states
outputUpdates = []

def generateSchedule():
	'''
		(None) -> int

		Calls the schedulers and saves their returned information into the shiftAssignments dictionary. 
		Returns 0 if no errors occured or 1 if an error occured.
	'''

	# For now, I am not "calling" the schedulers but I have created test files
	week_schedule = week.WeekdayShifts().weekdayShifts()
	end_schedule = end.weekendShifts() 

	# Dictionary that will get written to shiftAssignments.py
	assignments = {}
	
	# File containing shift assignment dictionary
	try:
		f = open("shiftAssignments.py", "w")
	except:
		return 1

	# Adding the WEEKDAYS to the dictionary
	for i in range(10): # 10 weeks in a term
		assignments.update({i+1: [week_schedule[i][0], week_schedule[i][1]]})

	# Adding the WEEKENDS to the dictionary
	for i in range(10): # 10 weeks in a term

		# Prepend Sunday Day
		assignments[i+1][0].insert(0, end_schedule[i][0][3]) # Prepending Primary Sunday Day
		assignments[i+1][1].insert(0, end_schedule[i][1][3]) # Prepending Secondary Sunday Day
		#assignments[i+1][0].insert(0, end.schedule[i][0][3]) # Using test file
		#assignments[i+1][1].insert(0, end.schedule[i][1][3]) # Using test file

		# Appending rest of weekend
		for j in range(3): # Friday, Saturday Day, Sunday Night
			assignments[i+1][0].append(end_schedule[i][0][j]) # Primary
			assignments[i+1][1].append(end_schedule[i][1][j]) # Secondary
			#assignments[i+1][0].append(end.schedule[i][0][j]) # Using test file
			#assignments[i+1][1].append(end.schedule[i][1][j]) # Using test file

	# Writing assignment dictionary to shiftAssignments.py
	f.write("shiftAssignments = %s\n" % (str(assignments)))

	f.close()
	return 0


def exportFile(fileName):
	'''
		(Name of file: str) -> int

		Receives the name of the file to export to.
		Exports the saved shift assignments to a specified CSV file. 
		Returns 0 if no errors occured or 1 if an error occured.
	'''
	
	importlib.reload(sa) # Reloading dictionary

	# Creating user inputted output file
	try:
		output_file = open(fileName, "w")
	except:
		return 1

	# Writing header
	output_file.write(",,,SUNDAY DAY,SUNDAY NIGHT,MONDAY,TUESDAY,WEDNESDAY,THURSDAY,"
				"FRIDAY,SATURDAY DAY,SATURDAY NIGHT\n")	

	# Go through the weeks of shiftAssignments dictionary and save into output file
	for week in sa.shiftAssignments:
		# Write week i's number
		output_file.write("Week %d,Primary" % (week))

		# Write week i's primary schedule
		output_file.write(",, %s, %s, %s, %s, %s, %s, %s, %s, %s \n" % \
				(sa.shiftAssignments[week][0][0], \
				sa.shiftAssignments[week][0][1], sa.shiftAssignments[week][0][2], \
				sa.shiftAssignments[week][0][3], sa.shiftAssignments[week][0][4], \
				sa.shiftAssignments[week][0][5], sa.shiftAssignments[week][0][6], \
				sa.shiftAssignments[week][0][7], sa.shiftAssignments[week][0][8]))

		# Write week i's secondary schedule		
		output_file.write(",Secondary,, %s, %s, %s, %s, %s, %s, %s, %s, %s \n" % \
				(sa.shiftAssignments[week][1][0], \
				sa.shiftAssignments[week][1][1], sa.shiftAssignments[week][1][2], \
				sa.shiftAssignments[week][1][3], sa.shiftAssignments[week][1][4], \
				sa.shiftAssignments[week][1][5], sa.shiftAssignments[week][1][6], \
				sa.shiftAssignments[week][1][7], sa.shiftAssignments[week][1][8]))

		output_file.write("\n")
			
	output_file.close()
	return 0

 
def rewriteSchedule(assignments):
	'''
		(Updated assignments: dict) -> None
		
		Recieves an updated assignments dictionary and rewrites the sa.shiftAssignments file.
		Called by updateScehdule(...) and undo().
		Returns 0 if no errors occured and 1 if an error occured.
	'''
	try:
		f = open("shiftAssignments.py", "w")
	except:
		return 1

	f.write("shiftAssignments = %s\n" % (str(assignments)))
	f.close()
	importlib.reload(sa) # Reloading dictionary

	return 0

def updateSchedule(weekNum, secondary, index, newName):
	'''
		(Term week: int, Secondary?: int, Index of old name: int, New RA: str) -> int

		Receives an int indicating the week number, 0 if the RA is the primary 
		for the shift or 1 if they are secondary, an int indicating the field 
		in the list that was changed, and a str of the new name for that field.
		This function updates a field in the shiftAssignmnets dictionary.
		Returns 0 if no errors occured or 1 if an error occured.
	'''
	# Save the current state
	save()

	# Copy of current shift assignments	
	importlib.reload(sa) # Reloading dictionary
	new_assignments = sa.shiftAssignments

	# Update new assignment 
	new_assignments[weekNum][secondary][index] = newName
	
	# Update shiftAssignments dictionary
	rewriteSchedule(new_assignments)

	return 0


		
def save():
	'''
		() -> int

		Saves the old states of shiftAssignments.
	'''
	# Copy of shift assignments
	last_state = sa.shiftAssignments

	# Append to outputUpdates
	outputUpdates.append(last_state)

	# print("outputUpdates:")
	# print(outputUpdates)

	return 0


def undo():
	'''
		() -> None
		
		Rewrites the sa.shiftAssignments with the previous state.
	'''
	# Getting the last state and removing from outputUpdates
	last_state = outputUpdates.pop()

	# Copy of current shift assignments
	importlib.reload(sa) # Reloading dictionary

	# Update shiftAssignments dictionary
	rewriteSchedule(last_state)

	return 0


def resetAssignments():
	'''
		() -> int

		Resets the shiftAssignments dictionary in shiftAssignments.py to be empty.	
	'''
	try:
		f = open("shiftAssignments.py", "w")
	except:
		return 1

	f.write("shiftAssignments = {}")
	f.close()
	importlib.reload(sa) # Reloading dictionary

	global outputUpdates
	outputUpdates = [] # if the schedule is cleared from the system, undos cannot be made

	return 0


'''
	Calling methods to test program functionality.
'''
#generateSchedule()
#updateSchedule(2, 0, 1, "ALOOOHHHHAAAAAAAA")
#updateSchedule(10, 0, 0, "HOSSSAAKKAAAA")
#print("From main:")
#print(sa.shiftAssignments)
#undo()
#print("After undo:")
#print(sa.shiftAssignments)
#exportFile("file_output.csv")
