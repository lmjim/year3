'''
	Author: Max Terry
	Date Last Modified: January 30, 2020
	Description: The queue class is used to maintain a list of "On Deck" names for cold-calling.
	It will both keep track of the names, increment flag/called counters, as well as randomize the queue.
'''

import random
import roster as r
from datetime import date

class Queue:

	def __init__(self, roster = r.Roster()):  # roster should be a Roster with student information
		self.roster = roster
		self.activeRoster = [] # this will be filled with ID numbers of the students. The full information for a student can be found in roster
		self.passiveRoster = [] # once students are cold-called they will be removed from the first list and added to this one. Once it is full it will be randomized
		self.numberStudents = 0
		self.studentSelected = 0 # when key inputs are received, this number is updated to know which element in the dictionary to remove
		rosterKeys = list(roster.student_dict.keys())
		random.shuffle(rosterKeys)
		for key in rosterKeys:
			self.activeRoster.append([key,self.roster.student_dict[key][2] + " " + self.roster.student_dict[key][3]])

		self.numberStudents = len(self.activeRoster)
		return None

	def removeStudent(self, testing=False):			#this would get called when the instructor presses "ctrl+up" to remove a student from the queue
		
		removedStudent = self.activeRoster.pop(self.studentSelected)
		# print(removedStudent[0])
		todays_date = str(date.today())

		if(testing == False):
			self.roster.increment_called(removedStudent[0], todays_date)	#student has been called on

		self.passiveRoster.append(removedStudent)
		self.checkQueue()
		return removedStudent

	def checkQueue(self):				
		if(len(self.activeRoster) < 4):			#if there are fewer than 4 students left, more students need to be filled in
			random.shuffle(self.passiveRoster)	#reshuffle the passive roster

			for student in self.passiveRoster:
				self.activeRoster.append(student)

			self.passiveRoster = []
		
		return None

	def flagStudent(self):				#when instructor presses "ctrl+down" this will set a special flag on the student
		removedStudent = self.removeStudent()
		self.roster.increment_flagged(removedStudent[0])
		return None

	def getOnDeck(self):
		names = []
		for student in self.activeRoster:
			studentName = self.roster.student_dict[student[0]][2] + " " + self.roster.student_dict[student[0]][3]
			names.append(studentName)
		return names[0:4]

	''' these functions were removed as they were abstracted out into other functions. Leaving them here to reflect progress.
	
		def randomizeQueue(self):			#to be called from checkQueue if the queue is to be reset.
		self.activeRoster = self.passiveRoster
		self.passiveRoster = []
		random.shuffle(self.activeRoster)
		return None

	def updateStudent(self, keyPressed):			#updates which student is currently being selected. This would be called when key inputs are registered??
		#if(keyPressed == "Left" && studentSelected > 0):
		#	studentSelected -= 1
		#else if(keyPressed == "Right" && studentSelected < 3):
		#	studentSelected += 1
		return None

	'''	


#The below code was used for testing the Queue class.
'''
def main():
	roster = r.Roster()
	myQueue = Queue(roster)
	print(myQueue.passiveRoster)
	print(myQueue.activeRoster)
	print(myQueue.getOnDeck())
	myQueue.updateStudent(1)
	print()
	myQueue.studentSelected = 0
	myQueue.removeStudent()
	print(myQueue.passiveRoster)
	print(myQueue.activeRoster)
	print(myQueue.getOnDeck())
	print()
	myQueue.flagStudent()
	print(myQueue.passiveRoster)
	print(myQueue.activeRoster)
	print(myQueue.getOnDeck())


if __name__ == "__main__":
	main()
'''
