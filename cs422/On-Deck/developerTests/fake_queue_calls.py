'''
	Author: Kiana Hosaka
	Date Last Modified: January 26, 2020
	Description: This file mimics the calls that Max will make from the Student 
	Selection System. Max - please just copy and paste this where the system determines if:
	- a student got called on
	- a student got flagged
	- a user requested daily and term log requests
'''
import roster as r
import fileOutput as output
from random import randrange # Just for testing purposes not sure if we are allowed to use this

def testing_day1(roster):
	'''
		Fake day 1 data for testing purposes.
		Alyssa (951641245) got called on.
		Lily (951548855) got called on.
	'''
	roster.increment_called("951123456", "20/01/01")
	roster.increment_called("951531642", "20/01/01")
	return None

def testing_day2(roster):
	'''
		Fake day 2 data for testing purposes.
		Kiana (951548858) got called on and flagged.
		Lily (951548855) got called on and flagged.
		Max (951548888) got called on.
	''' 
	roster.increment_called("951654321", "20/01/10")
	roster.increment_flagged("951654321")
	roster.increment_called("951531642", "20/01/10")
	roster.increment_flagged("951531642")
	roster.increment_called("951642531", "20/01/10")
	return None

def testing_day3(roster):
	'''
		Fake day 3 data for testing purposes.
		Max (951548888) got called on and flagged.
		Alyssa (951641245) got called on.
	'''
	roster.increment_called("951642531", "20/01/18")
	roster.increment_flagged("951642531")
	roster.increment_called("951123456", "20/01/18")
	return None

def testing_testing(roster, total_calls):
	'''
		Fake tests for testing system.
	'''
	# UO ID numbers
	test_list = ["951123456", "951654321", "951642531", "951531642"] 
	for i in range(total_calls):
		random_index = randrange(4)
		roster.increment_test_called(test_list[random_index])
	return None		

def main():
	roster = r.Roster()
	# Fake Day 1 test	
	today_date = "20/01/01"
	testing_day1(roster)
	output.daily_output(today_date)

	# Fake day 2 test
	testing_day2(roster)
	today_date = "20/01/10"
	output.daily_output(today_date)
	#output.term_output()

	# Fake day 3 test
	testing_day3(roster)
	today_date = "20/01/18"	
	output.daily_output(today_date)
	output.term_output("term_log.tsv")
	
	# Testing output with total calls as 7
	'''
	total_calls = 27
	testing_testing(roster, total_calls)
	output.testing_output(total_calls)
	'''


if __name__ == "__main__":
	main()
