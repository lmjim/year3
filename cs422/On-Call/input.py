'''
Author: Alyssa Huque
Date of last modification: 3-03-2020
Description: This produces the functionality of the RA Preferences module
References:
	On Deck Development Team's Project 1 fileInput.py file
    https://www.geeksforgeeks.org/python-add-new-keys-to-a-dictionary/
    https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-34.php
    https://stackoverflow.com/questions/2212433/counting-the-number-of-keywords-in-a-dictionary-in-python
    https://stackoverflow.com/questions/29334276/capitalize-first-letter-of-the-first-word-in-a-list-in-python
'''

import ast
inputUpdates = [] # global dictionary used for keep track of actions in a session

class Input:
	# all of these are Alyssa's internal functions
	def __init__(self):
		pass

	def inputPreferences(filename):
		'''file -> dictionary
		parses the file of RA preferences and adds to raPreferences dictionary.
		Also contains error checking for input file.
		1) checks that the first entry is a valid student ID
		2) checks that there is the correct number of fields
		3) checks that the given weekdays are valid weekday entries
		4) checks that the weekends requested off are valid (in the range of 0-10)
		5) checks the correct number of weekends have been provided
		6) checks that the weekdays provided are not repeats
		'''
		weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Sunday"] # list of weekdays
		with open(filename, "r") as file:
			try:
				contents = file.readlines()
			except:
				return 1
			for i in range(len(contents)):
				contents[i] = contents[i].strip('\n')
				contents[i] = contents[i].split(',')
			for j in range(len(contents)): # error checking
				contents[j][2:5] = [item.capitalize() for item in contents[j][2:5]] # will capitalize input for consistency
				if contents[j][0][:3] != "951": # 1) first field is not a student ID
					# print("error1")
					return 1
				# elif len(contents[j]) < 8 or len(contents[j]) > 8:
				elif len(contents[j]) != 8: # 2) checking the right number of fields
					# print("error2")
					return 1
				for item in contents[j][2:5]: # 3) checking the preference is a weekday
					if item not in weekdays:
						# print("error3")
						return 1
				for item in contents[j][5:]: # checking the preference is a valid weekend
					try:
						if int(item) > 10 or int(item) < 0: # 4) checking that the weekend input is valid
							# print("error4")
							return 1
					except ValueError: # 5) checking proper number weekends have been given
						# print("error5")
						return 1
				if contents[j][2] == contents[j][3] or contents[j][2] == contents[j][4] or contents[j][3] == contents[j][4]: # 6) no weekday preferences are the same
					# print("error6")
					return 1
				raPreferences = {j[0]: j[1:8] for j in contents} # write raPreferences dictionary
		file.close() # closes input file
		try:
			return raPreferences # returns dictionary
		except:
			return 1

	def readingDictPy(filename):
		'''file -> dictionary
		parses file with raPreferences dictionary
		'''
		with open(filename, "r") as file: # opens file
			contents = file.readlines() # reads lines
		for i in contents:
			raPreferences = i.strip("raPreferences = ") # stores only the dictionary and nothing more in roster_dict
		file.close()
		raPreferences = ast.literal_eval(raPreferences) # converts from string to dictionary
		return raPreferences

	def save(current_dictionary, idNum, index):
		''' str, int, int -> int (0)
		This function saves changes, is used for the undo functionality.
		'''
		old = current_dictionary[idNum][index] # tracks action and location of action
		# print(old)
		change = [idNum, index, old] # stores action
		# print(change)
		inputUpdates.append(change) # adds action to global dictionary of actions
		# print(inputUpdates)
		return 0

class Preferences:
	def __init__(self):
		pass

	def importFile(filename):
		'''string -> int (0, 1, or 2)
		Receives the name of the file to import
		This function imports RA preference information.
		The file may contain one or several RAs. This function also accounts for an empty file.
		The file may contain RAs who are already in the system. These RAs have their preferences updated.
		Returns a 0 if no errors occured or a 1 if an error occured
		'''
		updated_dict = Input.inputPreferences(filename) #now i have a dictionary with the new information, I need to compare
		lastnames = []
		if(updated_dict == 1):
			# print("error7")
			return 1 # returns 1 for GUI warning
		original_dict = Input.readingDictPy("raPreferences.py")

		dictionary = original_dict.copy()

		# adding new RAs
		added_RAs = list(updated_dict.keys() - original_dict.keys())
		for i in range(len(added_RAs)):
			dictionary[added_RAs[i]] = updated_dict.get(added_RAs[i])

		# updating RA information
		for key in original_dict.keys() & updated_dict.keys():
			dictionary[key][1:7] = updated_dict[key][1:7]

		if len(dictionary.keys()) > 25:
			#print("A schedule cannot be generated: The RA team is too large. A maximum of 25 RAs are allowed. Likely, RAs from other buildings have been accidentally inputted.")
			return 2

		file = open("raPreferences.py", "w+") # writes file for Queue
		file.write("raPreferences = %s\n" % (str(dictionary)))
		file.close()
		return 0 # 0 if no errors occured or a 1 if an error occured

	def deletePreferences(student_id):
		'''string -> int (0)
		Receives the id number of the RA that needs to be deleted from
			the dictionary.
		This function removes the key/value pair of the given RA and
		rewrites the raPreferences dictionary.
		Returns a 0 if no errors occured or a 1 if an error occured
		'''
		current_dictionary = Input.readingDictPy("raPreferences.py")
		del current_dictionary[student_id]

		global inputUpdates # list with things that have been undone
		for i in range(len(inputUpdates)):
			if student_id == inputUpdates[i][0]: # if the student that has been deleted is in inputUpdates
				inputUpdates.pop(i) # remove deleted RA from inputUpdates if anything has been changed

		file = open("raPreferences.py", "w+")
		file.write("raPreferences = %s\n" % (str(current_dictionary)))
		file.close()
		return 0 # 0 if no errors occured or a 1 if an error occured

	def resetPreferences():
		'''None -> int (0)
		Resets the raPreferencesee dictionary.
		'''
		# current_dictionary = Input.readingDictPy("raPreferences.py") # obtains current raPreferences dictionary
		file = open("raPreferences.py", "w+") # opens the file containing raPrefernces dictionary
		file.write("raPreferences = {}") # writes an empty dictionary to raPreferences.py
		file.close()
		global inputUpdates
		inputUpdates = [] # cannot undo changes that do not exist anymore
		return 0

	def setGoldStar(student_id):
		'''string -> int (0)
		Accepts a student ID of the selected RA that will recieve they're preferred schedule.
		'''
		current_dictionary = Input.readingDictPy("raPreferences.py") # obtains current raPreferences dictionary
		current_dictionary['1'] = student_id # key 1, value is the student ID
		file = open("raPreferences.py", "w+") # opens the file containing raPreferences dictionary
		file.write("raPreferences = %s\n" % (str(current_dictionary))) # writes the new dictionary to raPreferences.py
		file.close()
		return 0

	def setTiebreaker(option):
		'''integer -> int (0)
		Accepts an integer 0, 1, or 2 to know which tiebreaker setting the
			user selected.
		0 is random.
		1 is alphabetical by last name.
		2 is numerical by student ID.
		'''
		current_dictionary = Input.readingDictPy("raPreferences.py") # obtains current raPreferences dictionary
		current_dictionary['2'] = option # key 2, value is the selected setting
		file = open("raPreferences.py", "w+") # opens the file containing raPreferences dictionary
		file.write("raPreferences = %s\n" % (str(current_dictionary))) # writes the new dictionary to raPreferences.py
		file.close()
		return 0

	def setBadPairings(student1, student2, student3, student4):
		'''string -> int (0)
		Accepts four student IDs.
		student1 and student2 cannot be paired together.
		student3 and student4 cannot be paired together.
		These inputs are written into the raPreferences dictionary in raPreferences.py
		'''
		current_dictionary = Input.readingDictPy("raPreferences.py")  # obtains current raPreferences dictionary
		current_dictionary['3'] = [[student1, student2], [student3, student4]] # key 3, value is the four student IDs as a list of pairs
		file = open("raPreferences.py", "w+") # opens the file containing the raPreferences dictionary
		file.write("raPreferences = %s\n" % (str(current_dictionary))) # writes the new dictionary to raPreferences.py
		file.close()
		return 0

	def exportRaPreferences(filename):
		'''string -> int (0)
		Recieves the name of a file and writes the current raPreferences
			dictionary to that file.
		'''
		current_dictionary = Input.readingDictPy("raPreferences.py") # obtains current raPreferences dictionary

		file = open(filename, "w+") # creates an empty file of given name
		try: # deletes keys that contain setting information so it is not written into file
			del current_dictionary["1"] # deletes gold star
			del current_dictionary["2"] # deletes tiebreaker
			del current_dictionary["3"] # deletes bad pairings
		except KeyError: # if those keys do not exist, continue
			pass
		for key in current_dictionary: # writes the dictionary into the new file
			file.write(key + ",")
			for i in range(len(current_dictionary.get(key))):
				file.write(str(current_dictionary.get(key)[i]) + ",")
			file.write("\n") # each key is on it's own line
		file.close()
		return 0

	def generateCheck():
		''' None -> int (0, 1, 2, or 3)
		The function checks that no more than half the RA team has requested the same weekend off.
		If more than half the RA team has requested the same weekend off, this is a violation of
			the RA contract and this function prints an error message and returns a 1.
		If all the RAs' weekends off do not create an issue this function returns a 0.
		'''

		current_dictionary = Input.readingDictPy("raPreferences.py") # obtains current raPreferences dictionary
		weekends_off = [0,0,0,0,0,0,0,0,0,0] # a list to tally the number of times each weekend has been requested off
		# weekends_off = [1,2,3,4,5,6,7,8,9,10] relevant indices as they are in terms of weeks

		try: # deletes keys that contain setting information so it is not written into file
			del current_dictionary["1"] # deletes gold star
			del current_dictionary["2"] # deletes tiebreaker
			del current_dictionary["3"] # deletes bad pairings
		except KeyError: # if those keys do not exist, continue
			pass

		requests = [] # a list to keep track of each RA's weekend off requests
		key_list = list(current_dictionary.keys()) # list of each RA's student's IDs

		if len(key_list) < 10: # checks that the team is the minimum size necessary to generate the schedule
			#print("A schedule cannot be generated: The RA team is too small. A minimum of 10 RAs are needed. Likely, not all the RAs have been uploaded.")
			return 1

		for i in key_list:
			requests += current_dictionary[i][4:] # adds RA's weekend off requests to list
			if current_dictionary[i][1] == current_dictionary[i][2] or current_dictionary[i][1] == current_dictionary[i][3] or current_dictionary[i][2] == current_dictionary[i][3]:
				# print("An RA has been given multiple of the same weekday preference. Please resolve this issue before a schedule can be generated")
				return 3
		
		for j in requests:
			j = int(j) # converts string to integer
			if j == 0: # 0 means the RA has not requested any weekend off
				pass
			else: # adds to weekends_off, the list that maintains the tally
				weekends_off[j-1] += 1 # indices are offset by 1 since indices start at 0 but weeks start at 1

		if (len(key_list) % 2) == 1: # odd number of RAs
			for k in range(len(weekends_off)):
				if weekends_off[k] > ((len(key_list) // 2) + 1): # if the number of weekends at index k is greater than half the RA team
					#print("error")
					#print("More than half the RA team has request weekend {} off. Please discuss with your RAs alternatives.".format(k+1))
					return 2

		else: # even number of RAs
			for l in range(len(weekends_off)):
				if weekends_off[l] > (len(key_list) // 2): # if the number of weekends at index k is greater than half the RA team
					#print("error")
					#print("More than half the RA team has request weekend {} off. Please discuss with your RAs alternatives.".format(l+1))
					return 2
		return 0

	def updatePreferences(idNum, index, newPref):
		'''str, int, str -> int (0 or 1)
		This function allows for updates of individual fields of the dictionary to allow for updating preferences.
		'''
		current_dictionary = Input.readingDictPy("raPreferences.py") # obtains current raPreferences dictionary
		# print(current_dictionary[idNum][index])

		Input.save(current_dictionary, idNum, index) # adds action to global dictionary
		current_dictionary[idNum][index] = newPref # makes modifications

		file = open("raPreferences.py", "w+") # opens the file containing raPreferences dictionary
		file.write("raPreferences = %s\n" % (str(current_dictionary))) # writes the new dictionary to raPreferences.py
		file.close()
		return 0

	def undo():
		'''None -> int (0 or 1)
		The undo functionality. Pulls from the global list inputUpdates to revert to previous action.
		'''
		try:
			current_dictionary = Input.readingDictPy("raPreferences.py") # obtains current raPreferences dictionary
			previous = inputUpdates.pop() #[idNum, index, old]
			current_dictionary[previous[0]][previous[1]] = previous[2]
			file = open("raPreferences.py", "w+") # opens the file containing raPreferences dictionary
			file.write("raPreferences = %s\n" % (str(current_dictionary))) # writes the new dictionary to raPreferences.py
			file.close()
		except IndexError:
			# print("list is empty")
			return 1
		return 0

if __name__ == '__main__':
	Preferences.importFile("Example Input/All RAs.csv")
	# Preferences.updatePreferences("951545641", 2, "Thursday")
	# Preferences.undo()
	# Preferences.save("951545641", 1)
	# Preferences.save("951318175", 2)
	# Preferences.weekendsOffcheck()
	# Preferences.resetPreferences()
	# Preferences.setGoldStar("2")
	# Preferences.setTiebreaker("0")
	# Preferences.setBadPairings(1,2,3,4)
	# Preferences.importFile("Example Input/example5.csv")
	# Preferences.deletePreferences('1')
	# Preferences.deletePreferences('2')
	# Preferences.deletePreferences('3')
	# Preferences.exportRaPreferences("test.csv")
	# print(inputUpdates)
