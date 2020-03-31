import tkinter
from tkinter import filedialog

myTkin = tkinter.Tk()
myTkin.title("On Deck")

def openFile():
	return tkinter.filedialog.askopenfilename()

fileButton = tkinter.Button(myTkin, text='Select File', width=25, command=openFile)
fileButton.pack()

exitButton = tkinter.Button(myTkin, text='Exit', width=25, command=myTkin.destroy) 
exitButton.pack()


#once widgets are added this will run the main program (and check for events and stuff)
myTkin.mainloop()
