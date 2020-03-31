'''
    Author: Lily Jim
    Date of last modification: 3-7-2020
    Description: This creates the graphical user interface
    References:
        On Deck Development Team's Project 1 interface.py file
        Tkinter ComboBox: https://www.delftstack.com/tutorial/tkinter-tutorial/tkinter-combobox/
        Tkinter Grid: https://www.tutorialspoint.com/python/tk_grid.htm
        Tkinter Button: https://www.tutorialspoint.com/python/tk_button.htm
        Tkinter Button Config Options: https://effbot.org/tkinterbook/button.htm
        Tkinter Button Text Config: https://pythonexamples.org/python-tkinter-button-change-font/
        Tkinter variable: https://www.geeksforgeeks.org/python-setting-and-retrieving-values-of-tkinter-variable/
        Tkinter wait_variable: http://www.scoberlin.de/content/media/http/informatik/tkinter/x8996-event-processing.htm and https://stackoverflow.com/questions/44790449/making-tkinter-wait-untill-button-is-pressed
        Tkinter columnspan: https://stackoverflow.com/questions/21009232/how-to-make-tkinter-columns-of-equal-width-when-widgets-span-multiple-columns-p
        Tkinter Underline Text: https://stackoverflow.com/questions/3655449/underline-text-in-tkinter-label-widget
        Tkinter Scrollbar: https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid
        List methods: https://www.geeksforgeeks.org/python-list/ and https://www.programiz.com/python-programming/methods/list/index
        Dictionary methods: https://www.geeksforgeeks.org/iterate-over-a-dictionary-in-python/ and https://www.geeksforgeeks.org/get-method-dictionaries-python/
        Button with args: https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

import importlib
from functools import partial

import input
import output
import exportSummary
import raPreferences as raPrefs
import shiftAssignments as sa


class OnCallViewer:
    def __init__(self):
        '''
            None -> None
            This initializes an instance of OnCallViewer
            The variables track information displayed in the different windows or the windows themselves
        '''
        # Windows:
        self.root = tk.Tk()
        self.preferences = None
        self.schedule = None
        self.settings = None
        self.prefEdit = None
        self.schedEdit = None
        
        # RA Preferences Tracker:
        self.raIDs = None
        self.raNames = None
        self.delRaDropdown = None
        self.raSelectedToDelete = None
        
        # RA Preference Edit Tracker:
        self.weekdayOptions = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
        self.weekdayDropdown = None
        self.weekdayChoice = None
        self.weekendOptions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.weekendDropdown = None
        self.weekendChoice = None
        
        # Schedule Edit Tracker:
        self.scheduleNames = None
        self.changeRaDropdown = None
        self.changeRaChoice = None
        
        # Preference Settings Tracker:
        self.settingsSaved = False
        self.settingsClosed = tk.BooleanVar(self.root, True)
        self.settingsIDs = None
        self.settingsNames = None
        self.tiebreakerOptions = ['Random', 'Alphabetical Order (Last Name)', 'Numerical Order (ID Number)']
        # Dropdown menus
        self.goldStarDropdown = None
        self.tiebreakerDropdown = None
        self.pairingDropdown1 = None
        self.pairingDropdown2 = None
        self.pairingDropdown3 = None
        self.pairingDropdown4 = None
        # Selected in dropdowns
        self.goldStarChoice = None
        self.tiebreakerChoice = None
        self.pairingChoice1 = None
        self.pairingChoice2 = None
        self.pairingChoice3 = None
        self.pairingChoice4 = None
        return None
    
    
    
    
    
    ''' The following function is for the Main window and runs the whole application '''
    def home(self):
        '''
            None -> None
            This acts as the main function for the user interface
            This creates the home screen
        '''
        # Setup home window:
        root = self.root
        root.title('On Call - Home')
        root.geometry('400x200+200+100') # width x height + x_offset + y_offset
        root.minsize(400, 200)
        
        # Create buttons:
        prefButton = tk.Button(root, text='RA Preferences', command=self.preferencesView)
        prefButton.pack(padx=50, side=tk.LEFT) # Place buttons side by side horizontally
        
        scheduleButton = tk.Button(root, text='Schedule', command=self.scheduleView)
        scheduleButton.pack(padx=50, side=tk.LEFT)
        
        # Start screen:
        root.mainloop() # This window always exists, once closed the application will
        return None
    
    
    
    
    
    ''' The following functions are for the RA Preferences window '''
    def preferencesView(self):
        '''
            None -> None
            This creates the RA Preferences screen
        '''
        if(self.preferences != None):
            self.preferences.lift() # Bring current window to front
            return None # Only allow one preferences view at a time
        
        importlib.reload(raPrefs) # Make sure raPrefs is the most recent information
        numRAs = len(raPrefs.raPreferences)
        
        # Setup preferences window:
        self.preferences = tk.Toplevel()
        pref = self.preferences
        pref.title('On Call - RA Preferences')
        if(numRAs == 0): # No RAs is a special window with just a message and single button
            pref.geometry('225x125+250+150') # width x height + x_offset + y_offset
            pref.minsize(225, 125)
        elif(numRAs > 18): # Once you have more than 18 RAs, the window needs to be bigger
            pref.geometry('800x750+0+0') # width x height + x_offset + y_offset
            pref.minsize(600, 750)
        else: # This is the "standard" window
            pref.geometry('800x600+250+150') # width x height + x_offset + y_offset
            pref.minsize(600, 600)
        
        if(numRAs != 0): # If there are RAs in the system
            # Create undo button
            undoButton = tk.Button(pref, text='Undo', command=self.undoPreferences)
            undoButton.grid(column=0, row=0)
            if(len(input.inputUpdates) == 0):
                undoButton.configure(state='disabled') # If there is nothing to undo, button is not clickable
        
            # Display 'headers' for the preferences
            raNameLabel = tk.Label(pref, text='RA Name')
            raNameLabel.grid(column=0, row=1)
            weekdayLabel = tk.Label(pref, text='Weekday Preferences')
            weekdayLabel.grid(column=1, row=1, columnspan=3)
            weekendLabel = tk.Label(pref, text='Weekend Off Requests')
            weekendLabel.grid(column=4, row=1, columnspan=3)
            # Set 'header' font
            underline = tk.font.Font(raNameLabel, raNameLabel.cget("font"))
            underline.configure(size=14, underline=True)
            raNameLabel.configure(font=underline)
            weekdayLabel.configure(font=underline)
            weekendLabel.configure(font=underline)
        
            # Display current RAs in the system
            index = 0
            self.raIDs = []
            self.raNames = []
            for ra in raPrefs.raPreferences:
                if(ra != '1' and ra != '2' and ra != '3'):
                    self.raIDs.append(ra)
                    self.raNames.append(raPrefs.raPreferences.get(ra)[0])

                    # Show RA name
                    nameLabel = tk.Label(pref, text=raPrefs.raPreferences.get(ra)[0])
                    nameLabel.grid(column=0, row=index+2)

                    # Show weekday preferences
                    pref1 = tk.Button(pref, text=raPrefs.raPreferences.get(ra)[1], command=partial(self.editRA, index, 1))
                    pref1.grid(column=1, row=index+2)
                    pref2 = tk.Button(pref, text=raPrefs.raPreferences.get(ra)[2], command=partial(self.editRA, index, 2))
                    pref2.grid(column=2, row=index+2)
                    pref3 = tk.Button(pref, text=raPrefs.raPreferences.get(ra)[3], command=partial(self.editRA, index, 3))
                    pref3.grid(column=3, row=index+2)

                    # Show weekend off requests
                    pref4 = tk.Button(pref, text=raPrefs.raPreferences.get(ra)[4], command=partial(self.editRA, index, 4))
                    pref4.grid(column=4, row=index+2)
                    pref5 = tk.Button(pref, text=raPrefs.raPreferences.get(ra)[5], command=partial(self.editRA, index, 5))
                    pref5.grid(column=5, row=index+2)
                    pref6 = tk.Button(pref, text=raPrefs.raPreferences.get(ra)[6], command=partial(self.editRA, index, 6))
                    pref6.grid(column=6, row=index+2)

                    # Increase counter for widget placement
                    index += 1
        
        # Create import button:
        importPrefs = tk.Button(pref, text='Import Preferences', command=self.importPreferences)
        
        if(numRAs != 0):
            # Add import button:
            importPrefs.grid(column=1, row=numRAs+2, pady=25, columnspan=2)
            
            # Create RA deletion section:
            # Create Delete RA label
            delRaLabel = tk.Label(pref, text='Delete RA:')
            delRaLabel.grid(column=0, row=numRAs+3, padx=10)
            # Create dropdown menu
            self.delRaDropdown = tk.ttk.Combobox(pref, values=self.raNames, state='readonly')
            self.delRaDropdown.grid(column=1, row=numRAs+3, columnspan=2)
            self.delRaDropdown.bind('<<ComboboxSelected>>', self.updateDeletionChoice)
            # Create deletion save button:
            saveDeletion = tk.Button(pref, text='Delete', command=self.deleteRA)
            saveDeletion.grid(column=3, row=numRAs+3, padx=10)
            
            # Create delete all button
            delAll = tk.Button(pref, text='Delete All', command=self.deleteAllRAs)
            delAll.grid(column=4, row=numRAs+3, columnspan=3)
            
        else:
            # Show message that there are no RAs in the system 
            noRaLabel = tk.Label(pref, text='No Existing RAs\nPlease Import Preferences')
            noRaLabel.grid(column=0, row=0, pady=15)
            # Add import button:
            importPrefs.grid(column=0, row=1)
            # Center horizontally
            pref.grid_columnconfigure(0, weight=1)
        
        # Start screen:
        pref.protocol('WM_DELETE_WINDOW', self.closePreferences)
        pref.update() # use update, not mainloop so other functions can still run
        return None
    
    def undoPreferences(self):
        '''
            None -> None
            Calls input.py's undo function
        '''
        input.Preferences.undo()
        self.closePreferences()
        return None
    
    def importPreferences(self):
        '''
            None -> None
            Asks user for csv file name
            Calls input.py's importFile function
        '''
        importlib.reload(raPrefs)
        if(len(raPrefs.raPreferences) == 25): # User can't import a file if already at the RA limit
            tk.messagebox.showerror(message='The maximum limit of RAs has been reached. Please remove an RA before importing a new file.')
            return None
        continueYes = True # Track if the user clicks ok or cancel
        if(len(raPrefs.raPreferences) == 0):
            continueYes = tk.messagebox.askokcancel(message='You can import either a single RA or several RAs in the same file.\nContinue?')
        else:
            continueYes = tk.messagebox.askokcancel(message='New RAs will be added to the current list. Existing RAs will be permanently updated.\nContinue?')
        if(continueYes): # Only open file dialog if the user said ok
            files = [('CSV Files', '*.csv')]
            fileName = tk.filedialog.askopenfilename(filetypes = files)
            if(fileName != ''): # An empty fileName means the user clicked cancel on the file dialog window
                error = input.Preferences.importFile(fileName)
                if(error == 1): # This means there was at least one of many things wrong with the file
                    tk.messagebox.showerror(message='Invalid file.\nPlease check the following:\nID numbers are correct.\nAll preferences are filled out with valid choices.\nThe same weekday preference is not chosen multiple times per RA.')
                elif(error == 2): # This means the number of RAs in the file would cause the total number of RAs to exceed the system limit
                    tk.messagebox.showerror(message='The RA team is too large.\nA maximum of 25 RAs are allowed.')
                else:
                    self.closePreferences()
        return None
    
    def deleteRA(self):
        '''
            None -> None
            This calls input.py's function to delete the selected RA
        '''
        if(self.raSelectedToDelete != None):
            if(tk.messagebox.askokcancel(message='This will permanently delete %s.\nContinue?' % self.raSelectedToDelete)): # Check that the user really wants to delete the selected RA
                pos = self.raNames.index(self.raSelectedToDelete) # Match the name with their list position
                studentID = self.raIDs[pos] # Using the list position get the RA's ID number
                input.Preferences.deletePreferences(studentID) # Send ID number to input's function
                self.closePreferences() # terminates preferences window forcing the user to reopen it, refreshing the information
        else:
            tk.messagebox.showerror(message='No RA selected.\nPlease select an RA to delete.') # Can't delete an RA if no one is selected
        return None
    
    def deleteAllRAs(self):
        '''
            None -> None
            This calls input.py's function to clear all the RAs in the system
        '''
        if(tk.messagebox.askokcancel(message='This will permanently delete all of the RAs in the system.\nContinue?')):
            input.Preferences.resetPreferences()
            self.closePreferences()
        return None
    
    def closePreferences(self):
        '''
            None -> None
            This closes the preferences window
            It resets the RA Preferences Tracker variables
        '''
        if(self.prefEdit != None):
            self.closeEditRA() # Close the edit window if the main preference window is closed
        self.preferences.destroy()
        self.preferences = None
        self.raIDs = None
        self.raNames = None
        self.delRaDropdown = None
        self.raSelectedToDelete = None
        return None
    
    
    
    
    
    ''' The following functions are for the Edit RA Preference window '''
    def editRA(self, ra, field):
        '''
            int, int -> None
            This opens a new window and allows the user to input a new preference for an RA
        '''
        if(self.prefEdit != None):
            self.prefEdit.lift() # Bring the current edit window to the front
            return None # Only allow one RA to be edited at a time
        
        # Setup RA edit window:
        self.prefEdit = tk.Toplevel()
        prefEdit = self.prefEdit
        prefEdit.title('On Call - Edit RA Preference')
        prefEdit.geometry('400x200+400+300') # width x height + x_offset + y_offset
        prefEdit.minsize(400, 200)
        
        # Create label with RA's name:
        nameLabel = tk.Label(prefEdit, text=self.raNames[ra])
        nameLabel.grid(column=0, row=0, padx=10, pady=10)
        
        # Create label and dropdown menu for new preference:
        if(field <= 3): # Edit window for a weekday preference
            prefLabel = tk.Label(prefEdit, text=('Weekday Preference #%d:' % (field)))
            prefLabel.grid(column=0, row=1, padx=10, pady=10)
            self.weekdayDropdown = tk.ttk.Combobox(prefEdit, values=self.weekdayOptions, state='readonly')
            self.weekdayDropdown.grid(column=0, row=2, padx=10, pady=10)
            self.weekdayDropdown.bind('<<ComboboxSelected>>', self.updateWeekdayChoice)
        else: # Edit window for a weekend preference
            prefLabel = tk.Label(prefEdit, text=('Weekend Off Preference #%d:' % (field - 3)))
            prefLabel.grid(column=0, row=1, padx=10, pady=10)
            self.weekendDropdown = tk.ttk.Combobox(prefEdit, values=self.weekendOptions, state='readonly')
            self.weekendDropdown.grid(column=0, row=2, padx=10, pady=10)
            self.weekendDropdown.bind('<<ComboboxSelected>>', self.updateWeekendChoice)
        
        # Create save button:
        savePref = tk.Button(prefEdit, text='Save', command=partial(self.updateRA, ra, field))
        savePref.grid(column=0, row=3, padx=10, pady=10, columnspan=2)
        
        prefEdit.grid_columnconfigure(0, weight=1) # center everything in the window
        
        prefEdit.protocol('WM_DELETE_WINDOW', self.closeEditRA) # Ensures variables are reset
        prefEdit.update()
        
        return None
    
    def updateRA(self, ra, field):
        '''
            int, int -> None
            This updates an RA's preference to the selected choice in the dropdown menu
            When the user clicks save when updating an RA's preference field, this function will get called
            This calls input's updatePreferences function
        '''
        if(self.weekdayChoice == None and self.weekendChoice == None):
            tk.messagebox.showerror(message='No preference selected.\nPlease make a selection.')
        else:
            if(field <= 3): # Use weekdayChoice
                if(raPrefs.raPreferences.get(self.raIDs[ra])[field] != self.weekdayChoice):
                    # only call update if it is a new choice
                    input.Preferences.updatePreferences(self.raIDs[ra], field, self.weekdayChoice)
            else: # Use weekendChoice
                if(raPrefs.raPreferences.get(self.raIDs[ra])[field] != self.weekendChoice):
                    # only call update if it is a new choice
                    input.Preferences.updatePreferences(self.raIDs[ra], field, self.weekendChoice)
            self.closeEditRA() # Reset variables
            self.closePreferences() # Reset variables
        return None
    
    def closeEditRA(self):
        '''
            None -> None
            This closes the Edit RA Preferences window
            It resets the RA Preference Edit Tracker variables
        '''
        self.prefEdit.destroy()
        self.prefEdit = None
        self.weekdayDropdown = None
        self.weekdayChoice = None
        self.weekendDropdown = None
        self.weekendChoice = None
        return None
    
    
    
    
    
    ''' The following functions are for the Schedule window '''
    def scheduleView(self):
        '''
            None -> None
            This creates the schedule screen
        '''
        if(self.schedule != None):
            self.schedule.lift() # Bring current schedule window to front
            return None # Only allow one schedule view at a time
        
        importlib.reload(sa)
        numShifts = len(sa.shiftAssignments)
        
        # Setup schedule window:
        self.schedule = tk.Toplevel()
        sched = self.schedule
        sched.title('On Call - Schedule')
        if(numShifts == 0):
            sched.geometry('225x125+250+150') # width x height + x_offset + y_offset
            sched.minsize(225, 125)
        else:
            sched.geometry('1225x700+0+0') # width x height + x_offset + y_offset
            sched.minsize(1200, 700)
        
        # Only show schedule if there is a schedule
        if(numShifts != 0):
            # Create undo button
            undoButton = tk.Button(sched, text='Undo', command=self.undoShiftChange)
            undoButton.grid(column=0, row=0, columnspan=2) # center button across two columns
            if(len(output.outputUpdates) == 0):
                undoButton.configure(state='disabled') # If there is nothing to undo, button is not clickable
            
            # Display 'headers' for the schedule
            underline = tk.font.Font(undoButton, undoButton.cget("font"))
            underline.configure(size=14, underline=True)
            sundayDay = tk.Label(sched, text='Sunday Day')
            sundayDay.grid(column=2, row=1)
            sundayDay.configure(font=underline)
            sundayNight = tk.Label(sched, text='Sunday Night')
            sundayNight.grid(column=3, row=1)
            sundayNight.configure(font=underline)
            monday = tk.Label(sched, text='Monday')
            monday.grid(column=4, row=1)
            monday.configure(font=underline)
            tuesday = tk.Label(sched, text='Tuesday')
            tuesday.grid(column=5, row=1)
            tuesday.configure(font=underline)
            wednesday = tk.Label(sched, text='Wednesday')
            wednesday.grid(column=6, row=1)
            wednesday.configure(font=underline)
            thursday = tk.Label(sched, text='Thursday')
            thursday.grid(column=7, row=1)
            thursday.configure(font=underline)
            friday = tk.Label(sched, text='Friday')
            friday.grid(column=8, row=1)
            friday.configure(font=underline)
            saturdayDay = tk.Label(sched, text='Saturday Day')
            saturdayDay.grid(column=9, row=1)
            saturdayDay.configure(font=underline)
            saturdayNight = tk.Label(sched, text='Saturday Night')
            saturdayNight.grid(column=10, row=1)
            saturdayNight.configure(font=underline)
            
            # Display current schedule in the system
            weekNumFont = tk.font.Font(undoButton, undoButton.cget("font"))
            weekNumFont.configure(size=14)
            for week in sa.shiftAssignments:
                # Primary RA row
                weekNumLabel = tk.Label(sched, text='Week %d' % (week)) # Week number goes in first column
                weekNumLabel.grid(column=0, row=(week*2))
                weekNumLabel.configure(font=weekNumFont)
                primaryLabel = tk.Label(sched, text=('Primary')) # Primary/Secondary goes in second column
                primaryLabel.grid(column=1, row=(week*2))
                primaryLabel.configure(font=weekNumFont)
                slot1 = tk.Button(sched, text=sa.shiftAssignments[week][0][0], command=partial(self.editSchedule, week, 0, 0))
                slot1.grid(column=2, row=(week*2))
                slot2 = tk.Button(sched, text=sa.shiftAssignments[week][0][1], command=partial(self.editSchedule, week, 0, 1))
                slot2.grid(column=3, row=(week*2))
                slot3 = tk.Button(sched, text=sa.shiftAssignments[week][0][2], command=partial(self.editSchedule, week, 0, 2))
                slot3.grid(column=4, row=(week*2))
                slot4 = tk.Button(sched, text=sa.shiftAssignments[week][0][3], command=partial(self.editSchedule, week, 0, 3))
                slot4.grid(column=5, row=(week*2))
                slot5 = tk.Button(sched, text=sa.shiftAssignments[week][0][4], command=partial(self.editSchedule, week, 0, 4))
                slot5.grid(column=6, row=(week*2))
                slot6 = tk.Button(sched, text=sa.shiftAssignments[week][0][5], command=partial(self.editSchedule, week, 0, 5))
                slot6.grid(column=7, row=(week*2))
                slot7 = tk.Button(sched, text=sa.shiftAssignments[week][0][6], command=partial(self.editSchedule, week, 0, 6))
                slot7.grid(column=8, row=(week*2))
                slot8 = tk.Button(sched, text=sa.shiftAssignments[week][0][7], command=partial(self.editSchedule, week, 0, 7))
                slot8.grid(column=9, row=(week*2))
                slot9 = tk.Button(sched, text=sa.shiftAssignments[week][0][8], command=partial(self.editSchedule, week, 0, 8))
                slot9.grid(column=10, row=(week*2))
                # Secondary RA row
                secondaryLabel = tk.Label(sched, text=('Secondary'))
                secondaryLabel.grid(column=1, row=(week*2)+1)
                secondaryLabel.configure(font=weekNumFont)
                slot11 = tk.Button(sched, text=sa.shiftAssignments[week][1][0], command=partial(self.editSchedule, week, 1, 0))
                slot11.grid(column=2, row=(week*2)+1)
                slot12 = tk.Button(sched, text=sa.shiftAssignments[week][1][1], command=partial(self.editSchedule, week, 1, 1))
                slot12.grid(column=3, row=(week*2)+1)
                slot13 = tk.Button(sched, text=sa.shiftAssignments[week][1][2], command=partial(self.editSchedule, week, 1, 2))
                slot13.grid(column=4, row=(week*2)+1)
                slot14 = tk.Button(sched, text=sa.shiftAssignments[week][1][3], command=partial(self.editSchedule, week, 1, 3))
                slot14.grid(column=5, row=(week*2)+1)
                slot15 = tk.Button(sched, text=sa.shiftAssignments[week][1][4], command=partial(self.editSchedule, week, 1, 4))
                slot15.grid(column=6, row=(week*2)+1)
                slot16 = tk.Button(sched, text=sa.shiftAssignments[week][1][5], command=partial(self.editSchedule, week, 1, 5))
                slot16.grid(column=7, row=(week*2)+1)
                slot17 = tk.Button(sched, text=sa.shiftAssignments[week][1][6], command=partial(self.editSchedule, week, 1, 6))
                slot17.grid(column=8, row=(week*2)+1)
                slot18 = tk.Button(sched, text=sa.shiftAssignments[week][1][7], command=partial(self.editSchedule, week, 1, 7))
                slot18.grid(column=9, row=(week*2)+1)
                slot19 = tk.Button(sched, text=sa.shiftAssignments[week][1][8], command=partial(self.editSchedule, week, 1, 8))
                slot19.grid(column=10, row=(week*2)+1)
        else:
            # Show message that there is not a schedule in the system
            noSchedLabel = tk.Label(sched, text='No Existing Schedule\nPlease Generate New Schedule')
            noSchedLabel.grid(column=0, row=0, pady=20)
            sched.grid_columnconfigure(0, weight=1)
        
        # Create Generate button:
        generateSched = tk.Button(sched, text='Generate New Schedule', command=self.generateNewSchedule)
        
        if(numShifts != 0):
            # Add generate button to screen
            generateSched.grid(column=2, row=22, columnspan=2)
            
            # Create export schedule button:
            exportSched = tk.Button(sched, text='Export Schedule', command=self.exportSchedule)
            exportSched.grid(column=4, row=22, pady=50, columnspan=2)
            
            # Create export summary button:
            exportSum = tk.Button(sched, text='Export Summary', command=self.exportSummary)
            exportSum.grid(column=6, row=22, columnspan=2)
            
            # Create clear button:
            clearSched = tk.Button(sched, text='Clear Schedule', command=self.clearSchedule)
            clearSched.grid(column=8, row=22, columnspan=2)
        else:
            # Add generate button to screen
            generateSched.grid(column=0, row=22, columnspan=2)
        
        # Start screen:
        sched.protocol('WM_DELETE_WINDOW', self.closeSchedule)
        sched.update() # use update, not mainloop so other functions can still run
        return None
    
    def undoShiftChange(self):
        '''
            None -> None
            This calls output.py's undo function
        '''
        output.undo()
        self.closeSchedule() # Close window to refresh it
        return None
    
    def generateNewSchedule(self):
        '''
            None -> None
            This opens the preference's settings screen
            This calls output.py's generateSchedule function
        '''
        if(self.settings != None):
            self.settings.lift()
            return None # Only allow one generate screen at a time
        
        inputGood = input.Preferences.generateCheck() # Check to make sure the preferences are okay before running generate
        if(inputGood == 0):
            continueYes = True
            if(len(sa.shiftAssignments) != 0): # If there is already a schedule in the system as if okay to override
                continueYes = tk.messagebox.askokcancel(message='This will overwrite the current schedule.\nContinue?')
            if(continueYes): # If everything is good open settings
                self.settingsSaved = False # Make sure variable is reset before opening
                self.settingsClosed.set(False) # Make sure variable is reset before opening
                self.settingsView() # Open settings
                self.root.wait_variable(self.settingsClosed) # Don't continue until the settings window is closed
                if(self.settingsSaved):
                    error = output.generateSchedule() # If the settings were saved, run generate
                    if(error == 1): # Tell user generic fail message
                        tk.messagebox.showerror(message='An error occured.\nA schedule cannot be generated.')
        elif(inputGood == 1): # Not enough RAs
            tk.messagebox.showerror(message='A schedule cannot be generated:\nA minimum of 10 RAs are needed.')
        elif(inputGood == 2): # Weekend requests need changing
            tk.messagebox.showerror(message='A schedule cannot be generated:\nMore than half the RA team has requested the same weekend off.')
        elif(inputGood ==3): # Weekday requests need changing
            tk.messagebox.showerror(message='A schedule cannot be generated:\nAn RA has the same preference for multiple weekdays.')
        return None
    
    def exportSchedule(self):
        '''
            None -> None
            Asks user for csv file name
            Calls output.py's exportFile function
        '''
        importlib.reload(sa)
        if(len(sa.shiftAssignments) != 0): # If there is a schedule in the system
            files = [('CSV Files', '*.csv')]
            fileName = tk.filedialog.asksaveasfilename(filetypes = files) # Ask user to choose file name and location
            if(fileName != ''): # fileName will be empty if user clicks cancel on file dialog
                error = output.exportFile(fileName)
                if(error == 1):
                    tk.messagebox.showerror(message='An error occured.\nThe schedule could not be exported.')
        else: # If there is no schedule
            tk.messagebox.showerror(message='No schedule to export. Please generate a schedule first.')
        return None
    
    def exportSummary(self):
        '''
            None -> None
            Asks user for text file name
            Calls exportSummary.py's exportShiftInfo function
        '''
        importlib.reload(sa)
        if(len(sa.shiftAssignments) != 0): # If there is a schedule in the system
            files = [('Text Files', '*.txt')]
            fileName = tk.filedialog.asksaveasfilename(filetypes = files) # Ask user to choose file name and location
            if(fileName != ''): # fileName will be empty if user clicks cancel on file dialog
                exportSummary.exportShiftInfo(fileName)
        else: # If there is no schedule
            tk.messagebox.showerror(message='No schedule to export summary of. Please generate a schedule first.')
        return None
    
    def clearSchedule(self):
        '''
            None -> None
            This calls output.py's function to delete the schedule in the system
        '''
        if(tk.messagebox.askokcancel(message='This will permanently delete the schedule in the system.\nContinue?')):
            output.resetAssignments()
            self.closeSchedule() # Close window to refresh
        return None
    
    def closeSchedule(self):
        '''
            None -> None
            This closes the schedule window
        '''
        if(self.schedEdit != None):
            self.closeEditSchedule() # Close edit window if open
        if(self.settings != None):
            self.closeSettings() # Close settings window if open
        self.schedule.destroy() # Close actual schedule window
        self.schedule = None
        return None
    
    
    
    
    
    ''' The following functions are for the Edit Schedule window '''
    def editSchedule(self, weekNum, secondary, index):
        '''
            int, int, int -> None
            This creates the screen to update a shift in the schedule
        '''
        if(self.schedEdit != None):
            self.schedEdit.lift() # Bring current edit window to front
            return None # Only allow one shift to be edited at a time
        
        # Setup schedule edit window:
        self.schedEdit = tk.Toplevel()
        schedEdit = self.schedEdit
        schedEdit.title('On Call - Edit Schedule')
        schedEdit.geometry('400x150+400+300') # width x height + x_offset + y_offset
        schedEdit.minsize(400, 150)
        
        # Get RA info for dropdown menu:
        importlib.reload(raPrefs)
        self.scheduleNames = []
        for ra in raPrefs.raPreferences:
            if(ra != '1' and ra != '2' and ra != '3'):
                self.scheduleNames.append(raPrefs.raPreferences.get(ra)[0])
        
        # Create label with shift getting changed:
        shifts = ['Sunday Day', 'Sunday Night', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday Day', 'Saturday Night']
        primaryLabel = 'Primary'
        if(secondary):
            primaryLabel = 'Secondary'
        changeShiftLabel = tk.Label(schedEdit, text=('Change %s Week %d %s Shift:' % (shifts[index], weekNum, primaryLabel)))
        changeShiftLabel.grid(column=0, row=0, padx=10, pady=10)
        
        # Create dropdown menu for new shift assignment:
        self.changeRaDropdown = tk.ttk.Combobox(schedEdit, values=self.scheduleNames, state='readonly')
        self.changeRaDropdown.grid(column=0, row=1, padx=10, pady=10)
        self.changeRaDropdown.bind('<<ComboboxSelected>>', self.updateChangeRaChoice)
        
        # Create save button:
        saveChange = tk.Button(schedEdit, text='Save', command=partial(self.updateShift, weekNum, secondary, index))
        saveChange.grid(column=0, row=2, padx=10, pady=10)
        
        schedEdit.grid_columnconfigure(0, weight=1)
        
        schedEdit.protocol('WM_DELETE_WINDOW', self.closeEditSchedule) # Make sure to reset variables when closing
        schedEdit.update()
        return None
    
    def updateShift(self, weekNum, secondary, index):
        '''
            int, int, int -> None
            This updates the chosen field in the schedule
            This calls output's function
        '''
        if(self.changeRaChoice == None):
            tk.messagebox.showerror(message='No RA selected.\nPlease select an RA.')
        else:
            if(sa.shiftAssignments[weekNum][secondary][index] != self.changeRaChoice):
                # only call update if it is a new choice
                output.updateSchedule(weekNum, secondary, index, self.changeRaChoice)
            self.closeEditSchedule()
            self.closeSchedule()
        return None
    
    def closeEditSchedule(self):
        '''
            None -> None
            This closes the Edit Schedule window
            It resets the Schedule Edit Tracker variables
        '''
        self.schedEdit.destroy()
        self.schedEdit = None
        self.scheduleNames = None
        self.changeRaDropdown = None
        self.changeRaChoice = None
        return None
    
    
    
    
    
    ''' The following functions are for the generate schedule settings window '''
    def settingsView(self):
        '''
            None -> None
            This creates the preference's settings screen
        '''
        # Setup settings window:
        self.settings = tk.Toplevel()
        settings = self.settings
        settings.title('On Call - Generate Schedule Settings')
        settings.geometry('900x300+300+200') # width x height + x_offset + y_offset
        settings.minsize(900, 300)
        
        # Get RA info for dropdown menus:
        importlib.reload(raPrefs)
        self.settingsIDs = [0]
        self.settingsNames = ['None']
        for ra in raPrefs.raPreferences:
            if(ra != '1' and ra != '2' and ra != '3'):
                self.settingsIDs.append(ra)
                self.settingsNames.append(raPrefs.raPreferences.get(ra)[0])
        names = self.settingsNames
        
        # Create Gold Star label:
        goldStarLabel = tk.Label(settings, text='Gold Star RA:')
        goldStarLabel.grid(column=0, row=0, padx=10, pady=10)
        # Create Gold Star dropdown menu:
        self.goldStarDropdown = tk.ttk.Combobox(settings, values=names, state='readonly')
        self.goldStarDropdown.grid(column=1, row=0, padx=10, pady=10)
        self.goldStarDropdown.current(0)
        self.goldStarChoice = self.goldStarDropdown.get()
        self.goldStarDropdown.bind('<<ComboboxSelected>>', self.updateGoldStarChoice)
        
        # Create tiebreaker label:
        tiebreakerLabel = tk.Label(settings, text='Preference Tiebreaker:')
        tiebreakerLabel.grid(column=0, row=1, padx=10, pady=10)
        # Create tiebreaker dropdown menu:
        self.tiebreakerDropdown = tk.ttk.Combobox(settings, values=self.tiebreakerOptions, state='readonly')
        self.tiebreakerDropdown.grid(column=1, row=1, padx=10, pady=10)
        self.tiebreakerDropdown.current(0)
        self.tiebreakerChoice = self.tiebreakerDropdown.get()
        self.tiebreakerDropdown.bind('<<ComboboxSelected>>', self.updateTiebreakerChoice)
        
        # Create first dis-allowed pairing label:
        pairingLabel1 = tk.Label(settings, text='RAs who cannot share a shift:')
        pairingLabel1.grid(column=0, row=2, padx=10, pady=10)
        # Create first dis-allowed pairing first RA dropdown menu:
        self.pairingDropdown1 = tk.ttk.Combobox(settings, values=names, state='readonly')
        self.pairingDropdown1.grid(column=1, row=2, padx=10, pady=10)
        self.pairingDropdown1.bind('<<ComboboxSelected>>', self.updatePairingOne)
        self.pairingDropdown1.current(0)
        self.paringChoice1 = self.pairingDropdown1.get()
        # Create first dis-allowed pairing label:
        pairingLabel2 = tk.Label(settings, text='and')
        pairingLabel2.grid(column=2, row=2, padx=10, pady=10)
        # Create first dis-allowed pairing first RA dropdown menu:
        self.pairingDropdown2 = tk.ttk.Combobox(settings, values=names, state='readonly')
        self.pairingDropdown2.grid(column=3, row=2, padx=10, pady=10)
        self.pairingDropdown2.bind('<<ComboboxSelected>>', self.updatePairingTwo)
        self.pairingDropdown2.current(0)
        self.paringChoice2 = self.pairingDropdown2.get()
        
        # Create second dis-allowed pairing label:
        pairingLabel1 = tk.Label(settings, text='Second pair of RAs who cannot share a shift:')
        pairingLabel1.grid(column=0, row=3, padx=10, pady=10)
        # Create first dis-allowed pairing first RA dropdown menu:
        self.pairingDropdown3 = tk.ttk.Combobox(settings, values=names, state='readonly')
        self.pairingDropdown3.grid(column=1, row=3, padx=10, pady=10)
        self.pairingDropdown3.bind('<<ComboboxSelected>>', self.updatePairingThree)
        self.pairingDropdown3.current(0)
        self.paringChoice3 = self.pairingDropdown3.get()
        # Create second dis-allowed pairing label:
        pairingLabel2 = tk.Label(settings, text='and')
        pairingLabel2.grid(column=2, row=3, padx=10, pady=10)
        # Create first dis-allowed pairing first RA dropdown menu:
        self.pairingDropdown4 = tk.ttk.Combobox(settings, values=names, state='readonly')
        self.pairingDropdown4.grid(column=3, row=3, padx=10, pady=10)
        self.pairingDropdown4.bind('<<ComboboxSelected>>', self.updatePairingFour)
        self.pairingDropdown4.current(0)
        self.paringChoice4 = self.pairingDropdown4.get()
        
        # Create save button:
        saveSettings = tk.Button(settings, text='Save', command=self.saveSettingsChoices)
        saveSettings.grid(column=1, row=4, padx=10, pady=10)
        
        # Start screen:
        settings.protocol('WM_DELETE_WINDOW', self.closeSettings)
        settings.update()
        return None
    
    def saveSettingsChoices(self):
        '''
            None -> None
            This calls input.py's function to save the settings
            This also closes the settings window
        '''
        # Handle gold star choice
        nameIndex = self.settingsNames.index(self.goldStarChoice)
        input.Preferences.setGoldStar(self.settingsIDs[nameIndex])
        
        # Handle tiebreaker choice
        tiebreakerIndex = self.tiebreakerOptions.index(self.tiebreakerChoice)
        input.Preferences.setTiebreaker(tiebreakerIndex)
        
        # Handle bad pairing choices
        p1 = 0 # Default is None, which is passed as 0
        p2 = 0
        p3 = 0
        p4 = 0
        # First bad pairing
        if(self.pairingChoice1 != None and self.pairingChoice2 != None): # Only set bad pairing if both dropdown menus select an RA
            if(self.pairingChoice1 == self.pairingChoice2): # Can't select the same RA in both dropdown menus
                tk.messagebox.showerror(message='An RA was selected to not share a shift with themselves.\nThis is impossible.\nPlease update pairings.')
                return None
            pairingIndex1 = self.settingsNames.index(self.pairingChoice1)
            pairingIndex2 = self.settingsNames.index(self.pairingChoice2)
            p1 = self.settingsIDs[pairingIndex1] # Get actual ID number, not name
            p2 = self.settingsIDs[pairingIndex2]
        # Second bad pairing
        if(self.pairingChoice3 != None and self.pairingChoice4 != None): # Only set bad pairing if both dropdown menus select an RA
            if(self.pairingChoice3 == self.pairingChoice4): # Can't select the same RA in both dropdown menus
                tk.messagebox.showerror(message='An RA was selected to not share a shift with themselves.\nThis is impossible.\nPlease update pairings.')
                return None
            pairingIndex3 = self.settingsNames.index(self.pairingChoice3)
            pairingIndex4 = self.settingsNames.index(self.pairingChoice4)
            p3 = self.settingsIDs[pairingIndex3] # Get actual ID number, not name
            p4 = self.settingsIDs[pairingIndex4]
        input.Preferences.setBadPairings(p1, p2, p3, p4)
        
        # Close window
        self.settingsSaved = True
        self.closeSettings() # Settings window should close when someone clicks save
        self.closeSchedule() # Close schedule window to force a refresh
        return None
    
    def closeSettings(self):
        '''
            None -> None
            This closes the settings window
            It resets the Preference Settings Tracker variables
        '''
        self.settings.destroy()
        self.settings = None
        self.settingsIDs = None
        self.settingsNames = None
        self.settingsClosed.set(True)
        # Dropdown menus
        self.goldStarDropdown = None
        self.tiebreakerDropdown = None
        self.pairingDropdown1 = None
        self.pairingDropdown2 = None
        self.pairingDropdown3 = None
        self.pairingDropdown4 = None
        # Selected in dropdowns
        self.goldStarChoice = None
        self.tiebreakerChoice = None
        self.pairingChoice1 = None
        self.pairingChoice2 = None
        self.pairingChoice3 = None
        self.pairingChoice4 = None
        return None
    
    
    
    
    
    ''' The following functions are for testing '''
    def testButton(self):
        '''
            None -> None
            This function is used to test the pressing of buttons
        '''
        print('Button Pressed') # Prints to terminal
        return None
    
    def testRaEdit(self, ra, field):
        '''
            int -> None
            This function was created to test how the edit RA preferences button works
        '''
        print(ra, field) # Prints to terminal
        return None
    
    def testSchedEdit(self, week, secondary, index):
        '''
            int, int, int -> None
            This function was created to test how the edit schedule button works
        '''
        print(week, secondary, index) # Prints to terminal
        return None
    
    
    
    
    
    ''' The following functions are for tracking dropdown menus '''
    def updateDeletionChoice(self, event):
        '''
            This updates the selected RA to delete in the dropdown menu
            Dropdown menu is in Preferences window
        '''
        self.raSelectedToDelete = self.delRaDropdown.get()
        return None
    
    def updateWeekdayChoice(self, event):
        '''
            This updates the selected weekday choice in the dropdown menu
            Dropdown menu is in Edit RA Preference window
        '''
        self.weekdayChoice = self.weekdayDropdown.get()
        return None
    
    def updateWeekendChoice(self, event):
        '''
            This updates the selected weekend choice in the dropdown menu
            Dropdown menu is in Edit RA Preference window
        '''
        self.weekendChoice = self.weekendDropdown.get()
        return None
    
    def updateChangeRaChoice(self, event):
        '''
            This updates the selected RA in the dropdown menu
            Dropdown menu is in Edit Schedule window
        '''
        self.changeRaChoice = self.changeRaDropdown.get()
        return None
    
    def updateGoldStarChoice(self, event):
        '''
            This updates the selected RA in the gold star dropdown menu
            Dropdown menu is in Settings window
        '''
        self.goldStarChoice = self.goldStarDropdown.get()
        return None
    
    def updateTiebreakerChoice(self, event):
        '''
            This updates the selected tiebreaker choice in the dropdown menu
            Dropdown menu is in Settings window
        '''
        self.tiebreakerChoice = self.tiebreakerDropdown.get()
        return None
    
    def updatePairingOne(self, event):
        '''
            This updates the selected RA in the first dropdown menu for the first dis-allowed pair
            Dropdown menu is in Settings window
        '''
        self.pairingChoice1 = self.pairingDropdown1.get()
        return None
    
    def updatePairingTwo(self, event):
        '''
            This updates the selected RA in the second dropdown menu for the first dis-allowed pair
            Dropdown menu is in Settings window
        '''
        self.pairingChoice2 = self.pairingDropdown2.get()
        return None
    
    def updatePairingThree(self, event):
        '''
            This updates the selected RA in the first dropdown menu for the second dis-allowed pair
            Dropdown menu is in Settings window
        '''
        self.pairingChoice3 = self.pairingDropdown3.get()
        return None
    
    def updatePairingFour(self, event):
        '''
            This updates the selected RA in the second dropdown menu for the second dis-allowed pair
            Dropdown menu is in Settings window
        '''
        self.pairingChoice4 = self.pairingDropdown4.get()
        return None



if __name__ == "__main__":
    screen = OnCallViewer()
    screen.home()
    
    
'''Alternate Code

def preferencesView(self):
        # Setup preferences window:
        self.preferences = tk.Toplevel()
        pref = self.preferences
        pref.title('On Call - RA Preferences')
        pref.geometry('700x400+250+150') # width x height + x_offset + y_offset
        pref.minsize(700, 400)
        pref.maxsize(700, 400)
        
        # Set up main frame
        prefMain = tk.Frame(pref)
        prefMain.grid(sticky='news') # Frame extends to north, east, west, and south of the window
        prefMain.grid_rowconfigure(0, weight=1)
        prefMain.grid_columnconfigure(0, weight=1)
        prefMain.grid_propagate(False)
        prefMain.config(width=700, height=400)
        # Create Canvas with scrollbar
        canvas = tk.Canvas(prefMain)
        canvas.grid(column=0, row=0, sticky='news')
        scroll = tk.Scrollbar(prefMain, orient="vertical", command=canvas.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=scroll.set)
        prefWidgets = tk.Frame(canvas)
        canvas.create_window((0, 0), window=prefWidgets, anchor='nw')
        
        importlib.reload(raPrefs)
        numRAs = len(raPrefs.raPreferences)
        
        if(numRAs != 0):
            # Create undo button
            undoButton = tk.Button(prefWidgets, text='Undo', command=self.undoPreferences)
            undoButton.grid(column=0, row=0)
            if(len(input.inputUpdates) == 0):
                undoButton.configure(state='disabled')
            
            # Create RA list frame
            #prefList = tk.Frame(prefMain)
            #prefList.grid(row=2, column=1, sticky='nw')
            #prefList.grid_rowconfigure(0, weight=1)
            #prefList.grid_columnconfigure(0, weight=1)
            #prefList.grid_propagate(False)
            #prefList.config(width=800, height=300)
            
            # Create canvas for the list frame
            #canvas = tk.Canvas(prefList)
            #canvas.grid(row=0, column=0, sticky="news")
            
            # Link a scrollbar to the canvas
            #scroll = tk.Scrollbar(prefList, orient="vertical", command=canvas.yview)
            #scroll.grid(row=0, column=1, sticky='ns')
            #canvas.configure(yscrollcommand=scroll.set)
            
            # Create a frame to contain the buttons
            #frameButtons = tk.Frame(canvas)
            #canvas.create_window((0, 0), window=frameButtons, anchor='nw')
            
            # Display current RAs in the system
            index = 0
            self.raIDs = []
            self.raNames = []
            for ra in raPrefs.raPreferences:
                if(ra != '1' and ra != '2' and ra != '3'):
                    self.raIDs.append(ra)
                    self.raNames.append(raPrefs.raPreferences.get(ra)[0])

                    # Show RA name
                    nameLabel = tk.Label(prefWidgets, text=raPrefs.raPreferences.get(ra)[0])
                    nameLabel.grid(column=0, row=index+1, sticky='news')

                    # Show weekday preferences
                    pref1 = tk.Button(prefWidgets, text=raPrefs.raPreferences.get(ra)[1], command=partial(self.editRA, index, 1))
                    pref1.grid(column=1, row=index+1, sticky='news')
                    pref2 = tk.Button(prefWidgets, text=raPrefs.raPreferences.get(ra)[2], command=partial(self.editRA, index, 2))
                    pref2.grid(column=2, row=index+1, sticky='news')
                    pref3 = tk.Button(prefWidgets, text=raPrefs.raPreferences.get(ra)[3], command=partial(self.editRA, index, 3))
                    pref3.grid(column=3, row=index+1, sticky='news')

                    # Show weekend off requests
                    pref4 = tk.Button(prefWidgets, text=raPrefs.raPreferences.get(ra)[4], command=partial(self.editRA, index, 4))
                    pref4.grid(column=4, row=index+1, sticky='news')
                    pref5 = tk.Button(prefWidgets, text=raPrefs.raPreferences.get(ra)[5], command=partial(self.editRA, index, 5))
                    pref5.grid(column=5, row=index+1, sticky='news')
                    pref6 = tk.Button(prefWidgets, text=raPrefs.raPreferences.get(ra)[6], command=partial(self.editRA, index, 6))
                    pref6.grid(column=6, row=index+1, sticky='news')

                    # Increase counter for widget placement
                    index += 1
            
            # Update buttons frames idle tasks to let tkinter calculate buttons sizes
            #frameButtons.update_idletasks()
            
            # Set the canvas scrolling region
            #canvas.config(scrollregion=canvas.bbox("all"))
        
        # Create import button:
        importPrefs = tk.Button(prefWidgets, text='Import Preferences', command=self.importPreferences)
        importPrefs.grid(column=1, row=numRAs+2, padx=50, pady=50)
        
        # Create RA deletion section:
        # Create Delete RA label
        delRaLabel = tk.Label(prefWidgets, text='Delete RA:')
        delRaLabel.grid(column=0, row=numRAs+3, padx=10, pady=10)
        # Create dropdown menu
        self.delRaDropdown = tk.ttk.Combobox(prefWidgets, values=self.raNames, state='readonly')
        self.delRaDropdown.grid(column=1, row=numRAs+3, padx=10, pady=10)
        self.delRaDropdown.bind('<<ComboboxSelected>>', self.updateDeletionChoice)
        # Create deletion save button:
        saveDeletion = tk.Button(prefWidgets, text='Save', command=self.deleteRA)
        saveDeletion.grid(column=2, row=numRAs+3, padx=10, pady=10)
        
        # Start screen:
        prefWidgets.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        pref.protocol('WM_DELETE_WINDOW', self.closePreferences)
        pref.update() # use update, not mainloop so other functions can still run
        return None
'''