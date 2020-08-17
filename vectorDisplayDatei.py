#Import der nötigen Module, Funktionen und Klassen

import math
import pygame
#from sys import exit

from vector2Datei import vector2D
from vector3Datei import vector3D

#pygame module starten
pygame.init()
    
        
#Displayklasse enthält den Plotter und die restliche UI

class vectorDisplay():

    #Variablen (für jedes vectorDisplay gleich)
    __displaySize = (900,600)
    usedFont = pygame.font.SysFont("Courier", 30)
    usedFont2 = pygame.font.SysFont("Courier", 20)
    alphaBet = (
        "a", "b", "c", "d", "e", "f", "g", "h", "i",
        "j", "k", "l", "m", "n", "o", "p", "q", "r",
        "s", "t", "u", "v", "w", "x", "y", "z"
        )
    alphaCol = (
        (255,0,0), (0,255,0), (0,0,255),
        (200,200,0), (200,0,200), (0,200,200),
        (150,150,150)
        )#pygame benutzt drei Zahlen um Farben zu vergeben: (Rot, Grün, Blau)
    useMode = (
        "",#intMode 0
        "NewVector:",#intMode 1
        "Calculate:",#intMode 2
        "Edit Vector:",#intMode 3
        "Save:",#intMode4
        "Test:"#intMode5
        )
    
    #Funktionen
    
    def __init__(self):
        self.loadImages() 
        self.window = pygame.display.set_mode(
            vectorDisplay.__displaySize
            )
        pygame.display.set_caption("Vektorplotter") #Der Name des Vektorplotters wird angezeigt
        pygame.display.set_icon(imLogo) #Das Logo des Vektorplotter Programm wird angezeigt
        
        #interne Variablen Standardwerte
        self.__intMode = 0 #int; 0 bis 5 (siehe vectorDisplay.useMode)
        self.__intStatus = ""
        self.__intDimensionMode = 3 #möglich ist 3 oder 2
        self.__intCoordSize = "large" #mögl. "med", "large" oder "small"
        self.currentInput = []
        self.currentSpotInInput = 0
        
        #Variablen zur Festlegung, was refreshed werden soll
        #Funktuinen aktualisieren entsprechende Teile des Vektorplotters,
        #je nachdem welche Variablen True sind z.B. neue Anzeige
        self.sizeChange = True
        self.dimenChange = True
        self.listChange = True
        self.inputChange = True
        self.buttonChange = True
        self.saveOptions = False #Speichern hätte andere angezeigte Dinge...
        self.listPage = 1
        
        #starten des program-loops (letzter Schritt von __init__())
        self.__mainLoop()

    def loadImages(self): #Lädt die Bilder die benutzt werden
        
        global imCoordSys#Da die Variable innerhalb definiert wird, muss das deklariert werden
        imCoordSys = [#Bilder (600*400px)
            pygame.image.load("img/coords/small2.png"),
            pygame.image.load("img/coords/med2.png"),
            pygame.image.load("img/coords/large2.png"),
            pygame.image.load("img/coords/small3.png"),
            pygame.image.load("img/coords/med3.png"),
            pygame.image.load("img/coords/large3.png")
            ]#Bilder in Liste, damit sie einfach auszutauschen sind (fürs Anzeigen)

        global imKeyboardButtons
        imKeyboardButtons = [#Bilder 900*200px
            pygame.image.load("img/other/keyboardButtons.png"),
            pygame.image.load("img/other/saveOptions.png")
            ]

        global imDimensionSwitch
        imDimensionSwitch = [#Bilder 150*25px
            pygame.image.load("img/dimen/2d.png"),
            pygame.image.load("img/dimen/3d.png")
            ]

        global imSaveButton
        imSaveButton = pygame.image.load(
            "img/other/saveButton.png"#Bild 150*50px
            )

        global imLogo
        imLogo = pygame.image.load(
            "img/other/logo.png"#Bild 32*32px
            )

        global imVecPlace
        imVecPlace = pygame.image.load(
            "img/other/vectorplace.png"#Bild 300*50px
            )

        global imScroll
        imScroll = pygame.image.load(
            "img/other/scroll.png"#Bild 300*30px
            )
    
    def refreshPage(self): #Diese Funktion refresht nach jede beliebige Aktion die Seite
        if self.sizeChange:
            if self.__intDimensionMode == 3:
                numSys = 3
            else:
                numSys = 0
            if self.__intCoordSize == "small":
                numSys = numSys+1
            elif self.__intCoordSize == "med":
                numSys = numSys+2
            elif self.__intCoordSize == "large":
                numSys = numSys+3
            self.window.blit(imCoordSys[(numSys - 1)],(300,0))
            self.displayAllVec()
            pygame.display.flip()
            self.sizeChange = False
        if self.dimenChange:
            if self.__intDimensionMode == 3:
                numSys = 2
                numSys2 = 1
            else:
                numSys = 1
                numSys2 = 0
            if self.__intCoordSize == "small":
                numSys = numSys*1
            elif self.__intCoordSize == "med":
                numSys = numSys*2
            else:
                numSys = numSys*3
            self.window.blit(imCoordSys[(numSys - 1)],(300,0))
            self.window.blit(imDimensionSwitch[numSys2],(150,0))
            self.displayAllVec()
            pygame.display.flip()
            self.dimenChange = False
        if self.listChange:
            self.displayList(self.listPage)
            self.displayAllVec()
            pygame.display.flip()
            self.listChange = False
        if self.buttonChange:
            self.window.blit(imSaveButton,(0,0))
            if self.saveOptions:
                self.window.blit(imKeyboardButtons[1],(0,400))
            else:
                self.window.blit(imKeyboardButtons[0],(0,400))
            pygame.display.flip()
            self.buttonChange = False
        if self.inputChange:
            self.displayInputLine()
            pygame.display.flip()
        #pygame.display.flip()#Es flakert, wenn zu oft das Display geflipt wird...
        

    #displayFunktionen erstellen screens, welche dann an durch
    #   refreshPage zusammengesetzt werden
    def displayAllVec(self):
        vecidlist=vector3D.vecIdList()
        count = 0
        for element in vecidlist:
            self.displayVector(
                vecidlist[element-1],
                self.alphaCol[count]
                )
            count += 1
            if count == 7:
                count = 0
            #pygame.display.flip()
        
    def displayVector(self, iD, color=(0,0,0), transl=False):
        factor = 150
        veclist = vector3D.vecEntList()
        vecX = veclist[iD-1].x
        vecY = veclist[iD-1].y
        vecZ = veclist[iD-1].z
        prntX = 0
        prntY = 0
        if self.__intCoordSize == "small":
            factor = 150 #großes Koordinatensystem
        elif self.__intCoordSize == "med":
            factor = 15 #mittleres Koordinatensystem
        else:
            factor = 1.5 #kleines Koordinatensystem
        if self.__intDimensionMode == 2:
            if float(vecZ) != 0.0: #fragt ab ob Vektor nicht 3D ist 
                prntX = 600
                prntY = 200
            else:
                prntX = vecX*factor+600
                prntY = -vecY*factor+200 #weil die Koordinaten kleiner sein müssen
        if self.__intDimensionMode == 3:
            prntX = vecY*factor - 0.475*vecX*factor + 600#0.475 anstatt 0.5, da die 3D x-Achse schlech skaliert ist
            prntY = -vecZ*factor + 0.475*vecX*factor + 200#Diese Darstellung ahmt das Zeichnen von 3D objekten nach
        pygame.draw.line(
            self.window,
            color,
            (600,200),
            (int(prntX),int(prntY)),
            1
            )
        #pygame.display.flip()
        

    def displayList(self, page):
        count = 50
        count2 = 0
        veclist = vector3D.vecIdList()
        pagenum = self.usedFont.render("P"+str(page),False,(0,0,0))
        self.window.blit(imScroll, (0, 370))
        self.window.blit(pagenum, (220 ,370))
        for vec in  veclist:
            if (int(vec / 8)+1) == page:
                self.displayListEntry( #Erzeugt einen Balken in der Liste
                    (0,count),
                    vec,
                    True,
                    self.alphaCol[count2]
                    )
                count += 40
                count2 += 1
                if count2 == 7:
                    count2 = 0
            else:
                pass
        
    def displayListEntry(self, pos, posinlist, vis, col): #DisplayListEntry wird von displayList aufgerufen
        self.window.blit(imVecPlace, pos)
        veclist = vector3D.vecEntList()
        if posinlist >= 26:
            name = self.alphaBet[(posinlist//26)-1]+self.alphaBet[posinlist-1] 
            #Bei über 26 Vektoren wird der Name so zusammengesetzt: aa, ab, ac,...,ba,bb...
        else:
            name = self.alphaBet[posinlist-1]
        text1 = self.usedFont2.render(
            (name+"  "+str(veclist[posinlist-1])),False,col
            )
        self.window.blit(text1,((pos[0]+15),(pos[1]+10)))
        
    def displayInputLine(self):
        currentstring = ""
        currentstring += vectorDisplay.useMode[self.__intMode]+"  "
        spotincurrentstring = len(vectorDisplay.useMode[self.__intMode]+"  ")
        if self.__intMode == 5:
            for element in self.currentInput:
                currentstring += element
            currentstring = str(currentstring[:(spotincurrentstring+self.currentSpotInInput)]+"/"+currentstring[(spotincurrentstring+self.currentSpotInInput):])
        pygame.draw.rect(self.window,(255,255,255),(0,400,600,20))
        text = self.usedFont2.render(currentstring,False,(0,0,0))
        self.window.blit(text,(0,400))
        


        #interpretFunktionen nehmen die nutzereingabe und arbeiten damit
    def interpretKeydown(self,event):
            print(event.key)#Für Testzwecke
            print(event.unicode)
            if event.key == 113:#Q
                self.sizeChange = True
                if self.__intCoordSize == "med":
                    self.__intCoordSize = "small"
                elif self.__intCoordSize == "small":
                    self.__intCoordSize = "large"
                elif self.__intCoordSize == "large":
                    self.__intCoordSize = "med"
                self.buttonChange = True
            elif event.key == 119:#W
                self.dimenChange = True
                if self.__intDimensionMode == 2:
                    self.__intDimensionMode = 3
                else:
                    self.__intDimensionMode = 2
                self.buttonChange = True
            elif event.key == 101:#E
                pass
            elif event.key == 97:#A
                self.listChange = True
                if self.listPage > 1:
                    self.listPage += -1
            elif event.key == 115:#S
                vector3D.saveXML()
            elif event.key == 100:#D
                x = vector3D(input("x="),input("y="),input("z="))#Zwischenzeitlich hier...
            elif event.key == 122:#Y
                self.listChange = True
                self.listPage += 1
            elif event.key == 120:#X
                pass
            elif event.key == 99:#C
                pass#Hier sind auch noch unbenutze Tasten mit geplanter Funktion
            elif event.key == 116:#T
                self.__intMode = 5
                self.inputChange = True
            
    def interpretKeydownInput(self,event):
        if event.key == 13:#Enter
            return "Enter"
        elif event.key == 8:#Backspace
            if len(self.currentInput) != 0 and self.currentSpotInInput != 0:
                self.currentSpotInInput += -1
                self.currentInput.pop(self.currentSpotInInput)
        elif event.key == 276:#Left
            if len(self.currentInput) != 0 and self.currentSpotInInput != 0:
                self.currentSpotInInput += -1
        elif event.key == 275:#Right
            if len(self.currentInput) > self.currentSpotInInput:
                self.currentSpotInInput += 1
        else:
            var = event.unicode
            if var != "":
                self.currentInput.insert(self.currentSpotInInput,str(var))
                self.currentSpotInInput += 1
        print(self.currentInput)

    def interpretNumberInput(self,event):
        if event.key == 1:#wird z. Z. nicht benutzt... ist nur Muster für später
            self.currentInput += "1"
        elif event.key == 2:
            pass
    
    def __mainLoop(self): #MainLoop Funktion checkt was du bewegt hast und was mit der Maus angeklickt wurde
        looprun = True
        while looprun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    looprun = False
                elif event.type == pygame.KEYDOWN and self.__intMode == 0:
                    self.interpretKeydown(event)
                elif event.type == pygame.KEYDOWN and self.__intMode == 1:
                    self.interpretNumberInput(event)
                elif event.type == pygame.KEYDOWN and self.__intMode == 2:
                    self.interpretNumberInput(event)
                elif event.type == pygame.KEYDOWN and self.__intMode == 3:
                    self.interpretKeydownInput(event)
                elif event.type == pygame.KEYDOWN and self.__intMode == 4:
                    self.interpretKeydownInput(event)
                elif event.type == pygame.KEYDOWN and self.__intMode == 5:
                    if self.interpretKeydownInput(event) == "Enter":
                        self.currentInput = []
                        self.currentSpotInInput = 0
                        self.__intMode = 0
                else:
                    pass
            self.refreshPage()   
        pygame.quit()


#Beispielvektoren
##vector1 = vector3D(10,10,0)
##vector2 = vector3D(0,12,10)
##vector3 = vector3D(0.5,2)
##vector4 = vector3D(4,4,4)
##vector5 = vector3D(2,1,1)
##vector6 = vector3D(0.5,0.3,0)
##vector7 = vector3D(0.5,0.3,0.4)
##vector8 = vector3D(30,25,0)
##vector9 = vector3D(100,10,10)
#Viele Beispiele damit es sich lohnt die Liste zu scrollen

vector3D.importXML("20200605202500542087.xml")
print(str(vector3D.vecIdList()))

x = vectorDisplay()#Erstellen einer Entität vectorDisplay startet alles...

        
