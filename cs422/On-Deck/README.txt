BRIEF DESCRIPTION OF THE SYSTEM: 'On Deck' is a cold calling software to assist instructors in improving student engagement and learning in classroom settings.

AUTHORS: Kiana Hosaka (kah), Alyssa Huque (ash), Lily Jim (lmj), Max Terry (mht)

DATE STARTED: 1-10-2020
DATE FINISHED: 2-3-2020

CREATION PURPOSE: University of Oregon CIS 422 with Professor Anthony Hornof, Winter 2020, Project 1 assignment

HOW TO RUN THE CODE: in Terminal, type "python3 On-Deck.py"

ADDITIONAL SET UP: none

DEPENDENCIES:
- Macintosh OSX 10.13 (High Sierra) or 10.15 (Catalina)
- python 3.7.6 or 3.8.1
- tkinter 8.6
- python standard libraries: time, datetime, ast, importlib, and random
- existence of these files: daily_logs.tsv, fresh_roster.py, queueState.py, students.py, and testing_reports.tsv

DIRECTORY DESCRIPTION:
-On-Deck (main): all files that are actively used/modified when the 'On Deck' application is being used.
	-daily_logs.tsv
	-fileInput.py
	-fileOutput.py
	-fresh_roster.py
	-interface.py
	-On-Deck.py
	-queue.py
	-queueState.py
	-randomTester.py
	-roster.py
	-students.py
-On-Deck > developerTests: files intended only for software developers/maintainers to test code.
	-fake_queue_calls.py
    -Makefile
	-originalTkTest.py
-On-Deck > images: .png and .jpg images of the icons that are utilized by the GUI.
	-present-icon.png
	-raised-hands.jpg
	-roster-icon.png
	-settings-icon.png
	-testing-icon.png
-On Deck > roster: .tsv example roster files utilized for testing the application.
	-badRoster.tsv: for error catching
	-exampleRoster.tsv: small roster sample
	-roster.tsv: full CIS 422 roster sample
	-updatedRoster.tsv: full CIS 422 roster sample to test update capability
