'''
	Authors: Lily Jim with additions from Max Terry
	Date Last Modified: February 3, 2020
	Description: The user interface for the On Deck application.
    
    For a more in depth description or explanations of functions, 
    please read the On Deck Technical Documentation.

	Image Sources:
    	Settings Icon: https://commons.wikimedia.org/wiki/File:Windows_Settings_app_icon.png
    	Testing Icon: https://freesvg.org/vector-clip-art-of-magnifying-glass-search-icon
    	Present Icon: https://www.kissclipart.com/teacher-icon-font-awesome-clipart-teacher-educatio-ywdgfs/
    	Roster Icon: https://commons.wikimedia.org/wiki/File:User_font_awesome.svg 
    	Application Icon: https://pixabay.com/illustrations/hands-raised-raised-hands-arms-up-1768845/ 
	
	Reference for layout: https://www.python-course.eu/tkinter_layout_management.php
	Reference for button images: https://www.geeksforgeeks.org/python-add-image-on-a-tkinter-button/ and https://www.tutorialspoint.com/python/tk_button.htm
	Reference for menubutton: https://www.javatpoint.com/python-tkinter-menubutton, http://effbot.org/tkinterbook/menu.htm, and https://www.tutorialspoint.com/python/tk_menubutton.htm
	Reference for opening new window: https://www.tutorialspoint.com/python/tk_toplevel.htm
	Reference for saving files: https://www.geeksforgeeks.org/python-asksaveasfile-function-in-tkinter/
	Reference for labels: https://www.tutorialspoint.com/python/tk_label.htm, https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop, and https://www.tutorialspoint.com/python/tk_relief.htm
	Reference for switch case in python: https://www.geeksforgeeks.org/switch-case-in-python-replacement/
	Reference for maintaining foreground: https://stackoverflow.com/questions/1892339/how-to-make-a-tkinter-window-jump-to-the-front
	Reference for messagebox: https://www.tutorialspoint.com/python/tk_messagebox.htm
	Reference for askokcancel: https://www.programcreek.com/python/example/88583/tkinter.messagebox.askokcancel
	Reference for running function on quit: https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
	Reference for clearing a file: https://www.tutorialspoint.com/python/file_truncate.htm
'''

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from datetime import date
import time
import ast
import importlib

# Our .py files:
import fileInput
import fileOutput
import fresh_roster
import queue
import queueState
import randomTester
import roster
import students

class Interface:
    def __init__(self):
        # Windows
        self.root = tk.Tk()
        self.roster = None
        self.present = None
        self.settings = None
        
        # Labels for presenting
        self.pos1 = None
        self.pos2 = None
        self.pos3 = None
        self.pos4 = None
        
        # Variables for on deck names and selected
        self.firstOnDeck = tk.StringVar()
        self.secondOnDeck = tk.StringVar()
        self.thirdOnDeck = tk.StringVar()
        self.fourthOnDeck = tk.StringVar()
        self.highlight = 0
        
        # Instance of the queue
        self.studentQueue = None
        
        # Restart flags
        self.restartRequired = False
        self.restartRecommended = False
        
        # Export daily log flag
        self.exportDailyLog = False

    ''' The following functions are for testing '''
    # Test button functionality
    def testButton(self):
        print('Button Pressed') # Prints to terminal
    
    # Test updating on deck names and moving highlight:
    def testPresenting(self):
        time.sleep(1)
        self.updateHighlight(1)
        time.sleep(1)
        self.updateOnDeck(['Lily Jim', 'Alyssa Huque', 'Max Terry', 'Leonie Way'])
        time.sleep(1)
        self.updateHighlight(2)
        time.sleep(0.5)
        self.updateHighlight(3)
        time.sleep(1)
        self.updateOnDeck(['reallylongfirst andlastnames', 'evenlongerreallylongfirst andlastnames', 'reallylongfirst andevenlongerlastnames', 'evenlongerreallylongfirst andevenlongerreallylonglastnames'])
        return
        
    ''' The following functions are related to the queue - written by Max'''
    # Initialize the first instance of the queue, or whenever a new roster is loaded in
    def initiateNewQueue(self):
        contents = ''
        importlib.reload(students)
        with open('students.py', 'r') as file:
            contents = file.read()
        contents = contents.strip("students_dict = ")
        studentDict = ast.literal_eval(contents)
        self.studentQueue = queue.Queue(roster.Roster(studentDict))
        return
    
    # Load in the information from a saved queue
    def initiateSavedQueue(self):
        contents = ''
        with open('students.py', 'r') as file:
            contents = file.read()
        contents = contents.strip("students_dict = ")
        studentDict = ast.literal_eval(contents)
        self.studentQueue = queue.Queue(roster.Roster(studentDict))
        with open('queueState.py', 'r') as file:
            savedActiveRoster = file.readline().strip("activeRoster = ")
            savedPassiveRoster = file.readline().strip("passiveRoster = ")
            savedActiveRoster = ast.literal_eval(savedActiveRoster)
            savedPassiveRoster = ast.literal_eval(savedPassiveRoster)
            if(len(savedActiveRoster) > 0): #if it isn't zero, then there is a saved state.
                self.studentQueue.activeRoster = savedActiveRoster
                self.studentQueue.passiveRoster = savedPassiveRoster
        return

    # Define key input events
    def keyInputs(self, event):
        if(event.keysym == "Right" and self.highlight < 3):
            self.updateHighlight(self.highlight + 1)
            self.studentQueue.studentSelected += 1
        elif(event.keysym == "Left" and self.highlight > 0):
            self.updateHighlight(self.highlight - 1)
            self.studentQueue.studentSelected -= 1
        elif(event.keysym == "Up"):
            self.studentQueue.removeStudent()
            newNames = self.studentQueue.getOnDeck()
            self.updateOnDeck(newNames)
        elif(event.keysym == "Down"):
            self.studentQueue.flagStudent()
            newNames = self.studentQueue.getOnDeck()
            self.updateOnDeck(newNames)
        return
    
    ''' The following functions are for the roster window '''
    # Upload New Roster
    def newRoster(self):
        importlib.reload(students)
        if len(students.students_dict) != 0:
            if(tk.messagebox.askokcancel(message='This will override the current roster. The application will need to be restarted.')):
                files = [('TSV Files', '*.tsv')]
                fileName = tk.filedialog.askopenfilename(filetypes = files)
                if(fileName != ''):
                    self.restartRequired = True
                    error = fileInput.parser(fileName)
                    if(error):
                        tk.messagebox.showerror(message='Roster not formatted correctly. Nothing changed.')
                    else:
                        self.initiateNewQueue()
        else:
            files = [('TSV Files', '*.tsv')]
            fileName = tk.filedialog.askopenfilename(filetypes = files)
            if(fileName != ''):
                self.restartRecommended = True
                error = fileInput.parser(fileName)
                if(error):
                    tk.messagebox.showerror(message='Roster not formatted correctly. Nothing changed.')
                else:
                    self.initiateNewQueue()
        return
    
    # Upload Updated Roster
    def updateRoster(self):
        importlib.reload(students)
        if(len(students.students_dict) != 0):
            if(tk.messagebox.askokcancel(message='This will restart the ordering of the queue. The application will need to be restarted.')):
                files = [('TSV Files', '*.tsv')]
                fileName = tk.filedialog.askopenfilename(filetypes = files)
                if(fileName != ''):
                    self.restartRequired = True
                    error = fileInput.instructor_update_roster(fileName)
                    if(error):
                        tk.messagebox.showerror(message='Roster not formatted correctly. Nothing changed.')
                    else:
                        importlib.reload(students)
                        self.initiateNewQueue()
        else:
            tk.messagebox.showerror(message='No roster exists already. Please select Choose New Roster instead.')
        return
    
    # Download Current Roster
    def downloadRoster(self):
        if(len(students.students_dict) != 0):
            files = [('TSV Files', '*.tsv')]
            fileName = tk.filedialog.asksaveasfilename(filetypes = files)
            if(fileName != ''):
                fileInput.export_roster('fresh_roster.py', fileName)
        else:
            tk.messagebox.showerror('Error', 'No Roster')
        return
    
    # Download Performance Summary Report
    def exportSummary(self):
        if(len(students.students_dict) != 0):
            files = [('TSV Files', '*.tsv')]
            fileName = tk.filedialog.asksaveasfilename(filetypes = files)
            if(fileName != ''):
                importlib.reload(students)
                fileOutput.term_output(fileName)
        else:
            tk.messagebox.showerror('Error', 'No Roster')
        return
    
    # Roster Menu View
    def rosterMenu(self):
        self.roster = tk.Toplevel()
        roster = self.roster
        roster.title("On Deck - Roster")
        roster.geometry('250x250+250+150') # width x height + x_offset + y_offset
        roster.minsize(250, 250)
        
        newRoster = tk.Button(roster, text='Choose New Roster', command=self.newRoster)
        newRoster.pack(pady=20)
        
        downloadRoster = tk.Button(roster, text='Download Current Roster', command=self.downloadRoster)
        downloadRoster.pack(pady=20)
        
        updateRoster = tk.Button(roster, text='Update Current Roster', command=self.updateRoster)
        updateRoster.pack(pady=20)
        
        summary = tk.Button(roster, text='Performance Summary Report', command=self.exportSummary)
        summary.pack(pady=20)
        
        roster.mainloop()
    
    ''' The following functions are for the presentation window '''
    # Get Initial On Deck Names
    def getOnDeckNames(self):
        onDeck = self.studentQueue.getOnDeck()
        return onDeck
    
    # Update On Deck Names
    def updateOnDeck(self, names):
        self.firstOnDeck.set(names[0])
        self.secondOnDeck.set(names[1])
        self.thirdOnDeck.set(names[2])
        self.fourthOnDeck.set(names[3])
        self.present.update()
        return
    
    # Change Highlighted Name
    def updateHighlight(self, pos):
        position = {0: self.pos1, 1: self.pos2, 2: self.pos3, 3: self.pos4}
        old = position.get(self.highlight)
        old.configure(relief='flat', bg='white')
        self.highlight = pos
        new = position.get(self.highlight)
        new.configure(relief='raised', bg='yellow')
        self.present.update()
        return
    
    # Presentation View
    def presentationView(self):
        if(self.restartRequired == False):
            importlib.reload(students)
            if(len(students.students_dict) != 0):
                self.exportDailyLog = True
                self.present = tk.Toplevel()
                present = self.present
                present.deiconify()
                present.title("On Deck")
                present.geometry('650x50+100+50') # width x height + x_offset + y_offset
                present.minsize(180, 50)
                present.attributes('-topmost', True)

                names = self.getOnDeckNames()
                self.firstOnDeck.set(names[0])
                self.secondOnDeck.set(names[1])
                self.thirdOnDeck.set(names[2])
                self.fourthOnDeck.set(names[3])
                
                self.pos1 = tk.Label(present, textvariable=self.firstOnDeck)
                self.pos1.pack(padx=10, side=tk.LEFT)
                self.pos1.configure(width=15, wraplength=100, relief='raised', bg='yellow') # highlight the first name to start
                self.highlight = 0 # first name is highlighted to start
                self.studentQueue.studentSelected = 0

                self.pos2 = tk.Label(present, textvariable=self.secondOnDeck)
                self.pos2.pack(padx=10, side=tk.LEFT)
                self.pos2.configure(width=15,wraplength=100, relief='flat', bg='white')

                self.pos3 = tk.Label(present, textvariable=self.thirdOnDeck)
                self.pos3.pack(padx=10, side=tk.LEFT)
                self.pos3.configure(width=15,wraplength=100, relief='flat', bg='white')

                self.pos4 = tk.Label(present, textvariable=self.fourthOnDeck)
                self.pos4.pack(padx=10, side=tk.LEFT)
                self.pos4.configure(width=15,wraplength=100, relief='flat', bg='white')

                present.bind("<Right>", self.keyInputs) # key listeners will only work while in the main screen
                present.bind("<Left>", self.keyInputs)
                present.bind("<Up>", self.keyInputs)
                present.bind("<Down>", self.keyInputs)

                present.update() # use update, not mainloop so other functions can still run
            else:
                tk.messagebox.showerror('Error', 'No Roster')
        else:
            tk.messagebox.showerror('Error', 'Application Restart Required')
        return

    ''' The following functions are for the settings window '''
    # Start Testing Mode
    def testingMode(self):
        if(self.restartRequired == False):
            if(self.restartRecommended == False):
                importlib.reload(students)
                if(len(students.students_dict) != 0):
                    if(tk.messagebox.askokcancel(message='You are starting the randomizer test. You will find the results in testing_report.tsv. Continue?')):
                        randomTester.testRandomness(self.studentQueue)
                else:
                    tk.messagebox.showerror('Error', 'No Roster')
            else:
                tk.messagebox.showerror('Error', 'Application Restart Required')
        else:
            tk.messagebox.showerror('Error', 'Application Restart Required')
        return
    
    # Reset Everything (clear rosters and queue)
    def resetAll(self):
        if(tk.messagebox.askokcancel(message='Are you sure you want to clear all information?')):
            studentsFile = open('students.py', 'w')
            studentsFile.truncate()
            studentsFile.write('students_dict = {}')
            studentsFile.close()
            
            freshRosterFile = open('fresh_roster.py', 'w')
            freshRosterFile.truncate()
            freshRosterFile.write('students_dict = {}')
            freshRosterFile.close()
            
            queueStateFile = open('queueState.py', 'w')
            queueStateFile.truncate()
            queueStateFile.write('activeRoster = []\npassiveRoster = []')
            queueStateFile.close()
            
            dailyLogFile = open('daily_logs.tsv', 'w')
            dailyLogFile.truncate()
            dailyLogFile.close()
            
            testingReportFile = open('testing_report.tsv', 'w')
            testingReportFile.truncate()
            testingReportFile.close()
        return
    
    # Settings Menu View
    def settingsMenu(self):
        self.settings = tk.Toplevel()
        settings = self.settings
        settings.deiconify()
        settings.title("On Deck - Settings")
        settings.geometry('200x225+250+150') # width x height + x_offset + y_offset
        settings.minsize(200, 225)
        
        testingPhoto = tk.PhotoImage(file='./images/testing-icon.png')
        testingIcon = testingPhoto.subsample(3)
        
        testButton = tk.Button(settings, text='Test Randomizer', image=testingIcon, compound='top', command=self.testingMode)
        testButton.pack(pady=20)
        
        clearAllButton = tk.Button(settings, text='Reset Application', command=self.resetAll)
        clearAllButton.pack(pady=20)
        
        settings.mainloop()
        return

    ''' The following function is for the home window and runs the whole application '''
    # Output Daily Log Upon Quit
    def onClose(self):
        # Daily log
        if(self.exportDailyLog):
            importlib.reload(students)
            fileOutput.daily_output(str(date.today()))

        # Save queue state
        importlib.reload(students)
        if(len(students.students_dict) != 0):
            with open('queueState.py', 'w') as file:
                file.write("activeRoster = " + str(self.studentQueue.activeRoster) + "\n")
                file.write("passiveRoster = " + str(self.studentQueue.passiveRoster))

        self.root.destroy()
        return
    
    # Home View
    def start(self):
        if(len(students.students_dict) != 0):
            self.initiateSavedQueue()
        
        root = self.root
        root.title("On Deck - Home")
        root.geometry('580x200+200+100') # width x height + x_offset + y_offset
        root.minsize(580, 200)

        # Define Images:
        rosterPhoto = tk.PhotoImage(file='./images/roster-icon.png')
        rosterIcon = rosterPhoto.subsample(2)
        
        presentPhoto = tk.PhotoImage(file='./images/present-icon.png')
        presentIcon = presentPhoto.subsample(5)
        
        settingsPhoto = tk.PhotoImage(file='./images/settings-icon.png')
        settingsIcon = settingsPhoto.subsample(3)
        
        # Create Buttons:
        rosterButton = tk.Button(root, text='Roster\nInformation', image=rosterIcon, compound='top', command=self.rosterMenu)
        rosterButton.pack(padx=50, side=tk.LEFT)
        
        presentButton = tk.Button(root, text='Present', image=presentIcon, command=self.presentationView)
        presentButton.pack(padx=50, side=tk.LEFT)
        
        settingsButton = tk.Button(root, text='Settings', image=settingsIcon, compound='top', command=self.settingsMenu)
        settingsButton.pack(padx=50, side=tk.LEFT)
        
        # Start Screen:
        root.protocol('WM_DELETE_WINDOW', self.onClose)
        root.mainloop()
        return

# Test this file:
if __name__ == "__main__":
    screen = Interface()
    screen.start()
    
''' Alternative code '''
    # For the home buttons
        #rosterButton = tk.Menubutton(root, text='Roster Information', image=rosterIcon)
        #rosterButton.menu = tk.Menu(rosterButton)
        #rosterButton['menu'] = rosterButton.menu
        #rosterButton.menu.add_command(label='Add New Roster', command=self.testButton)
        
        #settingsButton = tk.Menubutton(root, text='Settings', image=settingsIcon)
        #settingsButton.menu = tk.Menu(settingsButton)
        #settingsButton['menu'] = settingsButton.menu
        #settingsButton.menu.add_command(label='Test Randomizer', image=testingIcon2, command=self.testButton)
