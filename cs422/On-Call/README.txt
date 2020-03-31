BRIEF DESCRIPTION OF THE SYSTEM: 'On Call' is a resident assistant (RA) scheduler software to assist RA coordinators in efficiently assigning shift assignments to produce a schedule of On Call shifts.

AUTHORS: Alex Archer (aa), Kiana Hosaka (kah), Alyssa Huque (ash), Lily Jim (lmj), Max Terry (mht)

DATE CREATED: 2-12-2020

CREATION PURPOSE: CIS 422 with Professor Anthony Hornof, Winter 2020, Project 2 assignment

HOW TO COMPILE SOURCE CODE: in terminal, type "python3.7 On-Call.py"

ADDITIONAL SET UP: none

DEPENDENCIES:
- Macintosh OSX 10.13 (High Sierra) or 10.15 (Catalina)
- python 3.7
- tkinter 8.6
- python standard libraries: ast, functools, importlib, and random
- existence of these files: raPreferences.py and shiftAssignments.py

DIRECTORY DESCRIPTION:
-On-Call (main): all files that are actively used/modified when the 'On Call' application is being used.
	-exportSummary.py
    -input.py
    -On-Call.py
	-onCallViewer.py
	-output.py
	-raPreferences.py
	-shiftAssignments.py
    -weekdayScheduler.py
	-weekendScheduler.py
-On-Call > developerTestFiles:
	-Makefile
	-originalExampleRaPreferences.py
	-test_end.py
	-test_week.py
-On-Call > testInputs:
	-16 RAs.csv
	-20 RAs.csv
	-25 RAs.csv
    -example.csv
	-example1.csv
	-example2.csv
	-example3.csv
	-example4.csv
	-example5.csv
	-RA 1.csv
	-RA 2.csv
	-RA 3.csv
	-RA 4.csv
	-RA 5.csv
	-RA 6.csv
	-RA 7.csv
	-RA 8.csv
	-RA 9.csv
	-RA 10.csv
	-RA 11.csv
	-RA 12.csv
	-RA 13.csv
	-RA 14.csv
	-RA 15.csv
	-RA 16.csv
    -Same weekday chosen.csv
	-Same Weekend Off.csv
	-updatedexample.csv
	