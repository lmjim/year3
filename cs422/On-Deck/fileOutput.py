'''
	Author: Kiana Hosaka
	Date of Last Modification: February 3, 2020
	Description: Implements file output (smaller component of the larger Record System)
	Format of student dictionary: { UO ID: number of times called, number of times flagged,
		first name, last name, UO ID, email address, phonetic spelling, list of dates }

	References:
	- https://stackoverflow.com/questions/4454298/prepend-a-line-to-an-existing-file-in-python
		- This source allowed me to figure out how to prepend instead of append
		to the daily log files.
	- https://stackoverflow.com/questions/35807605/create-a-file-if-it-doesnt-exist
		- This source helped me make the prepending functionality work exactly as I wanted it to.
	- https://www.geeksforgeeks.org/reloading-modules-python/
		- This source helped me know what was causing a bug in our program. When we were
		trying to reference the dictionary that was being modified throughout the program,
		we had unexpected behavior and realized it was because we had to reload the data
		in the dictionary.
	- https://realpython.com/python-string-formatting/
		- Reminders of how string formatting works in Python.

'''
import importlib # For reloading functionality
import roster as r # Python file containing methods used to modify dictionary
import students as s # Python file containing dictionary from Alyssa


def daily_output(today_date):
	'''
		(today's date: str) -> None

		Method that outputs the daily log. Only displays the students that were
		cold called on that particular day/session  with information about their 
		flag status, name, and email.
	'''
	# If this file doesn't exist, make it	
	try:
		original = open("daily_logs.tsv", "r")
	except IOError:
		original = open("daily_logs.tsv", "w")
		original.close()

	# Save the data from the original file	
	# For prepending the daily log rather than prepending
	original = open("daily_logs.tsv", "r")
	data = original.read()

	# Open a daily_logs file to prepend daily information to
	output_file = open("daily_logs.tsv", "w")
	output_file.write("--- Daily log for %s ---\n" % (today_date))
	flagged = ""
	
	importlib.reload(s) # Reloads the student dictionary
	# Write each of the student's data that was cold called today and in this session
	for student in s.students_dict.keys():
		if ((today_date in s.students_dict[student][7]) and (student in r.session_list)):
			# "X" for students in flagged list from Roster.py
			# Empty string if not in flagged list
			if student in r.flagged_list:
				flagged = "X"
			else:
				flagged = ""

			# Outputs the flag, first name, last name, email
			output_file.write("%s\t%s %s <%s>\n" % (flagged, \
				s.students_dict[student][2], s.students_dict[student][3],  \
				s.students_dict[student][5]))

	output_file.write(data) # Writes the original data after the new data (prepending)
	output_file.write("\n")
	output_file.close()
	original.close()
	return None


def term_output(fileName):
	'''
		(name of output file: str) -> None
		Method that outputs the term log. Summarizes every student's participation
		for the	entire term.
	'''

	importlib.reload(s) # Reloads the student dictionary
	output_file = open(fileName, "w")
	output_file.write("--- Term Summary ---\n\n")
	output_file.write("Times Called\tTimes Flagged\tFirst Name\tLast Name\tUO ID\tEmail\tPhonetic Spelling\tList of Dates Called\n")

	# Writing each of the student's data
	for student in s.students_dict.keys():
		# Outputs the # times called, # times flagged, first name, last name, UO ID,
		# email, phonetic spelling, list of dates called
		output_file.write("%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n" % (s.students_dict[student][0], \
			s.students_dict[student][1], s.students_dict[student][2], \
			s.students_dict[student][3], s.students_dict[student][4], \
		 	s.students_dict[student][5], s.students_dict[student][6], \
			s.students_dict[student][7]))
		output_file.write("\n")

	output_file.close()
	return None


def testing_output(total_calls):
	'''
		(total number of calls: int) -> None

		Method that outputs the report of the testing mode. Summarizes every student's
		participation from the randomized queue. Evaluates the system performance.
	'''
	output_file = open("testing_report.tsv", "w")
	output_file.write("--- Testing System Report ---\n\n")
	output_file.write("Times Called\tFirst Name\tLast Name\tPercentage\n")
	
	# Writing each of the student's data
	for student in r.test_dict.keys():
		# Calculating percentage
		percent = (r.test_dict[student][0] / total_calls) * 100

		# Outputs the # times called, first name, last name, percent
		output_file.write("%d\t%s\t%s\t%.2f percent\n" % (r.test_dict[student][0], \
			r.test_dict[student][2], r.test_dict[student][3], percent))
		output_file.write("\n")

	output_file.close()
	return None
