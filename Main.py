'''
The TwentyFourGame class constructs the user interface for the game.

Created on Feb 23, 2019
@author: amosyu2000
'''
from FlashCard import FlashCard

from tkinter import *
import tkinter.ttk as ttk
from math import sqrt

class TwentyFourGame(FlashCard):
    
    def __init__(self, master):
        
        master.title('"24" Game')
        
        Grid.rowconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 0, weight=1)
        
        self.mainNumber = IntVar()
        self.mainNumber.set(24)
    
        self.amountCards = 4
        
        self.menu = Menu(master)
        self.menu.add_command(label="Settings", command=lambda: self.openSettings(master))
        self.menu.add_command(label="About", command=lambda: self.openAbout(master))
        master.config(menu=self.menu)
        
        self.title = Label(master, textvariable=self.mainNumber, font=("", 72, "bold"))
        self.title.grid(row=0, pady=10)
        
        self.description = Label(master, text=self.createDescription())
        self.description.grid(row=1, padx=100, pady=10)
        
        self.cardFrame = Frame(master)
        self.cardFrame.grid(row=2, pady=10)
        
        self.card = []
        for i in range(self.amountCards):
            self.card.append(FlashCard(self.cardFrame))
            
        self.shuffleButton = ttk.Button(master, text="New Deal", command=lambda: self.shuffleCards())  
        self.shuffleButton.grid(row=3, pady=10)
        
        self.inputFrame = Frame(master)
        self.inputFrame.grid(row=4, pady=10)
        
        self.inputLabel = Label(self.inputFrame, text="Answer")
        self.inputLabel.pack(side=LEFT)
        
        self.equation = StringVar()
        self.equation.trace('w', self.updateCardColors)
        
        self.inputField = ttk.Entry(self.inputFrame, textvariable = self.equation)
        self.inputField.pack(side=LEFT, padx=5)
        self.inputField.bind('<Return>', lambda event: self.openSubmit(master))
        self.inputField.focus()
        
        self.inputButton = ttk.Button(self.inputFrame, text="Submit", command=lambda: self.openSubmit(master))
        self.inputButton.pack(side=LEFT)
        
        self.credits = Label(master, text = 'v0.1 | Amos Yu | 2019', font=("", 8))
        self.credits.grid(row=6, sticky=E)

    def openSettings(self, master):
        window = Toplevel(master)
        window.title("Settings")
        window.grab_set()
        
        textFrame = Frame(window)
        textFrame.pack(side=TOP, padx=100, pady=10)
        
        Label(textFrame, text="Target Number ").grid(column=0, row=0, pady=5)
        Label(textFrame, text="Amount of Cards ").grid(column=0, row=1, pady=5)
        
        entry1 = ttk.Entry(textFrame)
        entry1.grid(column=1, row=0)
        entry1.insert(0, str(self.mainNumber.get()))
        entry1.bind('<Return>', lambda event: applyWindow())
        entry1.focus()
        
        entry2 = ttk.Entry(textFrame)
        entry2.grid(column=1, row=1)
        entry2.insert(0, str(self.amountCards))
        entry2.bind('<Return>', lambda event: applyWindow())
        
        buttonFrame = Frame(window)
        buttonFrame.pack(side=BOTTOM, padx=10, pady=10)
        
        okButton = ttk.Button(buttonFrame, text="Apply", command=lambda: applyWindow())
        okButton.pack(side=LEFT)
        
        cancelButton = ttk.Button(buttonFrame, text="Close", command=lambda: closeWindow())
        cancelButton.pack(side=LEFT)
        
        errorMessage = StringVar()
        errorLabel = Label(window, textvariable=errorMessage)
        errorLabel.pack(side=BOTTOM)
        
        def closeWindow():
            window.grab_release()
            window.destroy()
        
        def applyWindow():
            try:
                self.mainNumber.set(int(entry1.get()))
                self.description.config(text=self.createDescription())
                 
                try:
                    self.amountCards = int(entry2.get())
                    sqrt(self.amountCards)
                    self.shuffleCards()
                    closeWindow()
                except:
                    errorMessage.set('Please enter a positive integer value into "Amount of Cards"') 
            except:
                errorMessage.set('Please enter an integer value into "Target Number"')
    
    def openAbout(self, master):
        window = Toplevel(master)
        window.title('About "24" Game')
        window.grab_set()
        
        Label(window, text=" ".join(['"24" Game\nDeveloped February 2019\nBy Amos Yu\n \n',
                            'Written in Python 3.7\n \nRequired libraries\n',
                            'math\nrandom\ntkinter\nPillow\nos'])).grid(column=0, row=0, padx=100, pady=10)
        closeButton = ttk.Button(window, text="Close", command=lambda: closeWindow())
        closeButton.grid(column=0, row=1, pady=10)
        
        def closeWindow():
            window.grab_release()
            window.destroy()
   
    def shuffleCards(self):
        for card in self.card:
            card.destroy()
        self.card.clear()
        for i in range(self.amountCards):
            self.card.append(FlashCard(self.cardFrame))
        self.inputField.delete(0, END)
        self.inputField.focus()
    
    def createDescription(self):
        return "With only + - x / ^ ( ), use every card to make %s." % str(self.mainNumber.get())
    
    def updateCardColors(self, *dummy):    
        parsedEntry = list(self.equation.get())
        parsedEntry = ['**' if char=='^' else char for char in parsedEntry]  
        parsedEntry = ['*' if char=='x' else char for char in parsedEntry]
        
        i = 0
        while i + 1 < len(parsedEntry):
            if parsedEntry[i].isdigit() and parsedEntry[i+1].isdigit():
                parsedEntry[i:i+2] = [''.join(parsedEntry[i:i+2])]
            else: i += 1   
        
        numList = []
        for char in parsedEntry:
            if char.isdigit():
                numList.append(int(char))
        
        for card in self.card:
            card.setGreyScale(False) 
            try:
                numList.remove(card.value)
                card.setGreyScale()
            except: pass
    
    def openSubmit(self, master):
        
        window = Toplevel(master)   
        window.grab_set()
        
        Grid.rowconfigure(window, 0, weight=1)
        Grid.columnconfigure(window, 0, weight=1)
        
        buttonFrame = Frame(window)
        buttonFrame.pack(side=BOTTOM, pady=10)
        ttk.Button(buttonFrame, text="New Deal", command=lambda: newDeal()).pack(side=LEFT)
        ttk.Button(buttonFrame, text="Close", command=lambda: closeWindow()).pack(side=RIGHT)

        message = self.testEquation(self.equation.get())
        Label(window, text=message).pack(side=TOP, padx=100, pady=10)
        
        def newDeal():
            self.shuffleCards()
            window.grab_release()
            window.destroy()
        
        def closeWindow():
            window.grab_release()
            window.destroy()
            self.inputField.focus()

    def testEquation(self, entry):
        if entry == "":
            return "Please enter an equation into the text box."
        parsedEntry = list(entry)
        
        try:
            validChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', 'x', '/', '^', '(', ')', ' ']
            for char in parsedEntry:
                validChars.index(char)
        except: return "Invalid Entry.\n \nOnly use the operators\n+ - x / ^ and ()."
        
        parsedEntry = ['**' if char=='^' else char for char in parsedEntry]  
        parsedEntry = ['*' if char=='x' else char for char in parsedEntry]                    
        
        # Concatenate numbers
        i = 0
        while i + 1 < len(parsedEntry):
            if parsedEntry[i].isdigit() and parsedEntry[i+1].isdigit():
                parsedEntry[i:i+2] = [''.join(parsedEntry[i:i+2])]
            else: i += 1
        
        numList = []
        for char in parsedEntry:
            if char.isdigit():
                numList.append(int(char))
        
        cardValues = [card.value for card in self.card]
        
        try:
            for number in numList:
                cardValues.remove(number)
            if cardValues:
                return "Invalid Entry.\n \nMake sure to use every card in your equation."
        except: return "Invalid Entry.\n \nOnly use the numbers provided on the cards.\nEnsure you only use each card once."
        
        try: answer = eval(''.join(parsedEntry))
        except: return "I can't evaluate your equation.\n \nCheck that your equation is written properly."
        
        if answer == self.mainNumber.get():
            return "Congratulations!\n \nYou are correct!"
        else: return "Incorrect. Your equation evaluates to %s, not %s." % (str(answer), str(self.mainNumber.get()))
        
        return "Um...somehow you managed to break my code.\n \nGood job, I suppose."