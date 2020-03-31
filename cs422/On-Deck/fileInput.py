'''
	Author: Alyssa Huque
	Date of last modification: February 2, 2020
	Description:				
		- Parses file input
		- Exports current roster
		- Updates roster information
	Sources:
	https://stackoverflow.com/questions/9347419/python-strip-with-n
	https://stackoverflow.com/questions/4554130/fastest-way-to-swap-elements-in-python-list
	https://stackoverflow.com/questions/59915183/list-of-list-to-dictionary/59915243#59915243
	https://stackoverflow.com/questions/55402265/how-to-append-fields-values-in-python-list-and-ignore-none-value
	https://stackoverflow.com/questions/17911091/append-integer-to-beginning-of-list-in-python
	https://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops
	https://www.geeksforgeeks.org/get-method-dictionaries-python/
	https://www.programiz.com/python-programming/datetime/current-datetime
	https://chrisalbon.com/python/basics/compare_two_dictionaries/
	https://www.guru99.com/python-dictionary-beginners-tutorial.html
	https://www.geeksforgeeks.org/python-difference-in-keys-of-two-dictionaries/
	https://www.geeksforgeeks.org/python-list-copy-method/
	https://docs.python.org/3/tutorial/classes.html
'''

from datetime import datetime
import ast


class Parsing:
	def __init__(self): # restructured class, not utilized
		pass

	def reading_dict_py(filename):
		'''file -> dictionary
		Reads a python file that contains a dictionary
		filename can be...
		filename = students.py
		filename = fresh_roster.py'''
		with open(filename, "r") as file: # opens file
			contents = file.readlines() # reads lines
		for i in contents:
			roster_dict = i.strip("students_dict = ") # stores only the dictionary and nothing more in roster_dict
		file.close()
		roster_dict = ast.literal_eval(roster_dict) # converts from string to dictionary
		return roster_dict

	def reading_new_roster(filename):
		'''file -> dictionary
		filename is a tab-delimited roster'''
		with open(filename, "r") as file:
			contents = file.readlines()
			for i in range(len(contents)):
				# contents[i].split('\n')
				contents[i] = contents[i].strip('\n')
				contents[i] = contents[i].split('\t')
			for j in range(len(contents)): # number of students in roster
			# contents[j][1], contents[j][2] = contents[j][2], contents[j][1]
				if len(contents[j]) < 5: # prevents input files that will raise errors
					#print("Roster not formatted correctly")
					return 1 # returns 1 for GUI warning
				elif contents[j][2][:3] != "951": # prevents keys from being anything but student IDs
					#print("Roster not formatted correctly")
					return 1 # returns 1 for GUI warning
				contents[j].insert(5, []) # for the dates of participation
				contents[j].insert(0, 0) # for the participation count
				contents[j].insert(0, 0) # for the flags
				roster_dict = {j[4]: j[:8] for j in contents} # delete yes, LF in input
		file.close()
		return roster_dict


def parser(filename):
	'''str -> None
	parses input tab-delimited file formatted as <first_name> <tab> <last_name>
	<tab> <UO ID> <tab> <email_address> <tab> <phonetic_spelling>
	creates students.py (file with updating dictionary for queue) and fresh_roster.py
	(static version of dictionary meant for testing)'''
	roster_dict = Parsing.reading_new_roster(filename)
	if(roster_dict == 1):
		return 1 # returns 1 for GUI warning
        
	file1 = open("students.py", "w+") # writes file for Queue
	file1.write("students_dict = %s\n" % (str(roster_dict)))
	file1.close()

	file2 = open("fresh_roster.py", "w+") # writes file for Testing
	file2.write("students_dict = %s\n" % (str(roster_dict)))
	file2.close()
	return 0 # returns 0 for GUI, no errors occurred

def instructor_update_roster(updated_roster):
	'''str -> None
	3 cases of updating roster:
	1) adding students
	2) removing students
	3) changing information
	Allows instructor to update roster used in the cold calling system'''
	original_roster = Parsing.reading_dict_py("students.py")
	updated_roster = Parsing.reading_new_roster(updated_roster)
	if(updated_roster == 1):
		return 1 # returns 1 for GUI warning
        
	dictionary = original_roster.copy()

	# case 1) adding students
	added_students = list(updated_roster.keys() - original_roster.keys())
	for i in range(len(added_students)):
		dictionary[added_students[i]] = updated_roster.get(added_students[i])

	# case 2) removing students
	removed_students = list(original_roster.keys() - updated_roster.keys())
	for j in range(len(removed_students)):
		dictionary.pop(removed_students[j])

	# case 3) changing information
	for key in original_roster.keys() & updated_roster.keys():
		dictionary[key][2:6] = updated_roster[key][2:6]

	# updates file for queue
	with open("students.py", "w+") as file1:
		file1.write("students_dict = %s\n" % (str(dictionary)))
	file1.close()

	# updates file for testing
	with open("fresh_roster.py", "w+") as file2:
		file2.write("students_dict = %s\n" % (str(dictionary)))
	file2.close()
	
	return 0 # returns 0 for GUI, no errors occurred

def export_roster(filename, exportFile):
	'''str -> None
	Parses input file (fresh_roster.py) and prints to tab-delimited file. The
	functiton inherently names the file "exported_roster_TODAY'S DATE.tsv". Can be
	altered in GUI.'''
	roster_dict = Parsing.reading_dict_py(filename) # reads through dictionary

	fname = open(exportFile, "w+") # exportFile is the user given filename
	for key in roster_dict:
		fname.write(key + "\t") # writes as .tsv
		for i in range(len(roster_dict.get(key))):
			fname.write(str(roster_dict.get(key)[i]) + "\t") # writes .tsv
		fname.write("\n")
	fname.close()
	return None

'''
def oldparser(filename):
	# Practice parsing files and understanding how python parsers work
    with open(filename, "r") as fileob:
        contents = fileob.readlines()
        l = len(contents)
        print("lines:", l)
        count = 0
        for i in range(len(contents)):
            ch = len(contents[i])
            print("words:", len(contents[i]))
'''

'''
def parser(filename):
	# first attempt to create parser() function
	roster_dict = {}
	with open(filename, "r") as file:
		contents = file.readlines()
		# print(contents)
		# contents = contents.split('\t')
		for i in range(len(contents)):
			contents[i].split('\t')
			for j in range(1, len(contents)):
				roster_dict[contents[j]] = contents[i]
			print(roster_dictc)
			# print(contents)
'''

#if __name__ == '__main__':
	# print(Parsing.reading_new_roster("roster.tsv"))
	# parser("roster.tsv")
	# instructor_update_roster("update.tsv")
	# export_roster("students.py")
	# parser("errortest.tsv")
