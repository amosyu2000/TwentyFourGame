'''
The FlashCard class creates cards.

Created on Feb 23, 2019
@author: amosyu2000
'''

from tkinter import *
import tkinter.ttk as ttk
import random
from PIL import ImageTk, Image
import os

class FlashCard:
    project_path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(project_path)

    skinList = os.listdir("CardSkins")[0:10]
    
    skinValueList = []
    for file in skinList:
        skinValueList.append(int(file[:2]))
    
    def createSkin(self, image):
        colourImage = Image.open("CardSkins/"+image)
        greyImage = Image.open("CardSkins/"+image)
        greyMask = Image.open("CardSkins/greyMask.png")
        greyImage.paste(greyMask, mask=greyMask)
        
        return ImageTk.PhotoImage(colourImage), ImageTk.PhotoImage(greyImage)
    
    def setGreyScale(self, boolean=True):
        if boolean:
            self.label.config(image=self.greySkin)
        else:
            self.label.config(image=self.skin)
            
    def destroy(self):
        self.frame.destroy()
    
    def __init__(self, master):
        randomIndex = random.randint(1,len(self.skinList)) - 1
        self.value = self.skinValueList[randomIndex]
        self.skin, self.greySkin = self.createSkin(self.skinList[randomIndex])
        
        self.frame = Frame(master)
        self.frame.pack(side=LEFT)
        
        self.label = Label(self.frame, image=self.skin)
        self.label.pack(padx=10)
