'''
	Author: Max Terry
	Date Last Modified: January 28, 2020
	Description: Tests the randomization of the queue and outputs its results.
	
'''

import queue
import roster
import random
import fileOutput
import fresh_roster
import importlib

def testRandomness(studentQueue): #takes in a queue, outputs the randomness results for each person
	results = {}
	totalCalls = 1000
	roster = studentQueue.roster
	student_dict = roster.student_dict

	importlib.reload(fresh_roster)
	roster.test_dict = fresh_roster.students_dict

	originalStudentSelected = studentQueue.studentSelected

	for uoId in student_dict:
		name = student_dict[uoId][2] + " " + student_dict[uoId][3]
		if(name not in results.keys()):
			results[name] = 0

	for i in range(totalCalls):
		randomNumber = random.randint(0,3)
		studentQueue.studentSelected = randomNumber
		removedStudent = studentQueue.removeStudent(True)
		
		#results[removedStudent[1]] += 1
		roster.increment_test_called(removedStudent[0])

	fileOutput.testing_output(totalCalls)
	studentQueue.studentSelected = originalStudentSelected

	'''for key in results:
		percentCalled = (results[key]/totalCalls) * 100
		print(key + " was called " + str(results[key]) + " times out of a total of " + str(totalCalls) + " times. This represents  " + str(percentCalled) + "% of total calls")

'''
