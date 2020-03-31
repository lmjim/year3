'''
	Author: Kiana Hosaka
	Date Last Modified: February 3, 2020
	Description: Increments values in the student roster dictionary.
	This class will directly increment files in the student dictionary that is
	contained inside of the file student.py
'''

# Importing the students.py file containing the student dictionary
import students as s

# Importing the fresh_roster.py file
import fresh_roster as fr

# Global variable that tracks which students got flagged on this day
flagged_list = []

# Global variable that tracks which students got called on this session
# Have this so there isn't repeated information if the instructor opens
# the software multiple times in one day.
session_list = []

# Global copy of the fresh_roster dictionary
test_dict = fr.students_dict

class Roster:
	def __init__(self, student_dict = s.students_dict):
		'''
			Initializes the student dict to be the dict from students.py
		'''
		self.flagged_list = []
		self.student_dict = student_dict

	def increment_called(self, student, date):
		'''
			(student's id number: str, date: str) -> None
			Increments the number of times a particular student was called on
			and appends the date to the list of days the student was called on.
			Will update the students.py data by overwriting with the
			updated dictionary from this class.
		'''
		self.student_dict[student][0] += 1 # Increment number called
		self.student_dict[student][7].append(date) # Append date
		session_list.append(student) # Append student to the current session list
		self.update_roster()
		return None

	def increment_flagged(self, student):
		'''
			(student's id number: str) -> None
			Increments the number of times a particular student was flagged
			and appends their name to the global flagged_list.
			Will update the students.py data by overwriting with the
			updated dictionary from this class.
		'''
		self.student_dict[student][1] += 1 # Increment number flagged
		flagged_list.append(student) # Append student to the flagged list
		self.update_roster()
		return None

	def update_roster(self):
		'''
			() -> None
			Updates the roster information by overwriting the current
			information in the students dictionary.
		'''
		new_roster = open("students.py", "w")
		new_roster.write("students_dict = %s\n" % (str(self.student_dict))) # Writes local dictionary
		new_roster.close()
		return None

	def increment_test_called(self, student):
		'''
			(student's id number: str) -> None
			For testing the randomization functionality.
			Increments the number of times a particular student was called on.
			Will update a copy of the students list.
		'''
		test_dict[student][0] += 1 # Increment the test dictionary with number called
		return None

	'''
	# Alternative Code
	def increment_test_flagged(self, student):
		pass
	'''	
