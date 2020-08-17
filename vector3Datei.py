import math
import datetime

class vector3D():
    #Initialisierung der Variablen und Listen
    __totalVectorsActive = 0
    __totalVectorsInitiallized = 0
    __activeVectorList = []
    __activeVectorIDList = []
    #Allgemeine magische Methoden
    def __init__(self, x=0.0, y=0.0, z=0.0, iD=0):
        """Do not input iD - internal only for loading - might cause problems"""
        vector3D.__totalVectorsActive += 1
        vector3D.__totalVectorsInitiallized +=1
        self.__x = float(x)
        self.__y = float(y)
        self.__z = float(z)
        if iD == 0:
            self.__vecIndex = vector3D.__totalVectorsInitiallized
        else:
            self.__vecIndex = int(iD)
            print("jup")
        vector3D.__activeVectorList.append(self)
        vector3D.__activeVectorIDList.append(self.__vecIndex)
    def __del__(self):
        vector3D.__totalVectorsActive -= 1
        try: #Das ist ein try, da wenn __del__ durch ausführen von __removeVectorFromList (wodurch der Vektor zu __del__ freigegeben wird) aufgerufen wird,
            vector3D.__removeVectorFromList(self.__vecIndex)#er bereits in der Liste fehlt, was einen dieser Fehler hervorruft
        except ValueError:
            pass
        except IndexError:
            pass
    def __str__(self):
        if self.__z != 0:
            return "("+str(self.__x)+", "+str(self.__y)+", "+str(self.__z)+")"
        else:
            return "("+str(self.__x)+", "+str(self.__y)+")"
        
    #Interne/private Funktionen
    def __removeVectorFromList(vecID):
        """removes Vector from __activeVectorList based on private index; internal function - to remove use 'deleteVectorFromList()' function"""
        m = vector3D.__activeVectorIDList.index(vecID)
        vector3D.__activeVectorIDList.pop(m)
        vector3D.__activeVectorList.pop(m)
    def __getX(self):
        return self.__x
    def __getY(self):
        return self.__y
    def __getZ(self):
        return self.__z
    def __getTVA(self):
        return int(self.__totalVectorsActive)
    def __setX(self,x):
        self.__x = float(x)
    def __setY(self,y):
        self.__y = float(y)
    def __setZ(self,z):
        self.__z = float(z)
    def __methodAdd(self, other):
        """used internally for adding and subtracting""" #so kann ich das Programm Speicherplatzoptimieren und einfach __iadd__ oder __radd__ hinzufügen
        if type(other) == int or type(other) == float:#Aufgrund von jetzigen Anforderungen nicht bei Muliplikation und anderen Rechenarten (wo es z.Z. mehr Code wäre)
            return vector3D(self.__x+other,self.__y+other,self.__z+other)
        elif type(other) == vector3D:
            return vector3D(self.__x+other.__x,self.__y+other.__y,self.__z+other.__z)
        else:
            try:
                type(other) != vector2D() or type(other) != vector2Datei.vector2D#So, hier wirds speziell... Das Programm warf immer bei diesem abgleich, egal was versucht...
            except NameError:#einen solchen NameError aus... Deswegen testet das Programm hier nach diesem, und gibt wenn er kommt die Berechnung zurück...
                return vector3D(self.__x+other.__x,self.__y+other.__y,self.__z)#
            else:
                return vector3D(0.0,0.0,0.0)

    #Properties
    x = property(__getX, __setX)
    y = property(__getY, __setY)
    z = property(__getZ, __setZ)
    tva = property(__getTVA)
        
    #Magische Methoden fürs Rechnen
    def __abs__(self):
        return math.sqrt(self.__x**2+self.__y**2+self.__z**2)
    def __neg__(self):
        return vector3D(-self.__x,-self.__y,-self.__z)
    def __add__(self, other):
        return vector3D.__methodAdd(self,other)
    def __sub__(self, other):
        return vector3D.__methodAdd(self,-other)#Hierzu wird die Add Methode mit negiertem other verwendet
    def __mul__(self,other):
        if type(other) == int or type(other) == float:
            return vector3D(self.__x*other,self.__y*other,self.__z*other)
        elif type(other) == vector3D:
            x = ((self.__y * other.__z) - (self.__z * other.__y))
            y = ((self.__z * other.__x) - (self.__x * other.__z))
            z = ((self.__x * other.__y) - (self.__y * other.__x))
            return vector3D(x,y,z)
        else:
            try:
                type(other) != vector2Datei.vector2D or type(other) != vector2D
            except NameError:#siehe Zeile 61f für Erklärung
                x = - (self.__z * other.__y)
                y = (self.__z * other.__x)
                z = ((self.__x * other.__y) - (self.__y * other.__x))
                return vector3D(x,y,z)
            else:
                return vector3D(0.0,0.0,0.0) #alle anderen Rechenoptionen nicht möglich
    def __truediv__(self,other):
        if type(other) == int or type(other) == float:
            return vector3D(self.__x/other,self.__y/other,self.__z/other)
        else:
            return vector3D(0.0,0.0,0.0) #alle Anderen Rechenoptionen nicht möglich

    
    #Funktionen für erweiterte Möglichkeiten
    def printVectorList():
        """prints a list of all Vectors and their IDs"""
        count=0
        if 0 < len(vector3D.__activeVectorList):
            print("Alle Vektoren:")
            while count < len(vector3D.__activeVectorList):
                print(str(vector3D.__activeVectorList[count])+"\t\t ID: "+str(vector3D.__activeVectorIDList[count]))
                count+=1
        else:
            print("Keine Vektoren!")
    def deleteVectorFromList(iD):
        """deletes a Vector from the Vectorlist (based on ID)"""#öffentliche Methode leitete auf private weiter, die auch sonst intern benutzt wird
        vector3D.__removeVectorFromList(iD)
    def clearVectorList(aLL=0):#verrückte Schreibweisen mit Groß- und Kleinbuchstaben nur um sicherzugehen, dass wirklich nichts ausversehen den gleichen Namen hat...
        """clears the Vectorlist and the Vectors active and (if aLL != 0) the Vectors initiallised"""
        vector3D.__activeVectorList = []
        vector3D.__totalVectorsActive = 0
        vector3D.__activeVectorIDList = []
        if aLL != 0:
            vector3D.__totalVectorsInitiallized = 0
    def extractNumbersFromInput(iNPUT):
        """extracts Numbers from String/Input and returns them (ignores Floats)"""
        valForReturn =""
        x=0
        while x < len(iNPUT):
            i = iNPUT[x]
            try:
                i2=int(i)
            except ValueError:
                pass
            else: valForReturn += str(i)
            x+=1
        if valForReturn=="":
            return 0
        return int(valForReturn)
    def extractNumbersFromInput2(iNPUT):
        """extracts Numbers from String/Input and returns them as Float"""
        valForReturn =""
        x=0
        while x < len(iNPUT):
            i = iNPUT[x]
            if i == ".":
                valForReturn += "."
            else:
                try:
                    i2=int(i)
                except ValueError:
                    pass
                else:
                    valForReturn += str(i)
            x+=1
        print(valForReturn)
        if valForReturn=="":
            return 0.0
        return float(valForReturn)
    def vecIdList():
        vecidlist = list(vector3D.__activeVectorIDList)
        return vecidlist
    def vecEntList():
        vecentlist = list(vector3D.__activeVectorList)
        return vecentlist

    #XML utility
    def toXML(self):
        """converts given vector into xml format (string)"""
        local = "\t\t<vector>\n\t\t\t<ID>"+str(self.__vecIndex)+"</ID>\n\t\t\t<x>"+str(self.__x)+"</x>\n\t\t\t<y>"+str(self.__y)+"</y>\n\t\t\t<z>"+str(self.__x)+"</z>\n\t\t</vector>\n"
        return local
    def listXML():
        """produces a xml save-file of the vectorlist as a string"""
        count=0
        if 0 < len(vector3D.__activeVectorList):
            local = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<vectorspy>\n\t<date>"""+str(datetime.datetime.now())+"</date>\n\t<vectors>\n"
            while count < len(vector3D.__activeVectorList):
                local += str(vector3D.toXML(vector3D.__activeVectorList[count]))
                count+=1
            local+="\t</vectors>\n</vectorspy>"
        else:
            print("Keine Vektoren!")
        return local
    def saveXML(name=0):
        """saves a new xml-file containing the vectorlist (name=0 creates file with date as name; inputing name of already created file overwrites content)"""
        if name==0 or name==None or name=="":
            local = str(vector3D.extractNumbersFromInput(str(datetime.datetime.now())))+".xml"
        else:
            test = name[-4]+name[-3]+name[-2]+name[-1]
            if test == ".txt" or test ==".xml":
                local = str(name)
            else:
                local = str(name)+".xml"
        newSave = open(("saves/"+str(local)), "w")
        newSave.write(vector3D.listXML())
        newSave.close
    def importXML(docname):#Le Monstrume
        """Imports saved vectors from xml file (works with .xml and .txt with or without inputing ending)"""
        vector3D.clearVectorList()
        localName = "saves/"+str(docname)
        actualName = ""
        test = localName[-4]+localName[-3]+localName[-2]+localName[-1]
        if test == ".txt" or test ==".xml":
            #localName += test
            actualName=localName
            VecFile = open(str(localName), "r")
        else:
            #localName += test
            localName2 = str(localName)
            try:
                localName += ".xml"
                actualName = localName
                VecFile= open(str(localName), "r")
            except NameError:
                try:
                    localName2 += ".txt"
                    actualName = localName
                    VecFile=open(str(localName2), "r")
                except NameError:
                    print("Es gab leider ein Problem!")
                    actualName=None
                    return None
        localLength = sum(1 for line in VecFile)
        VecFile.close()
        VecFile = open(str(actualName), "r")
        if localLength%6 != 0:
            print("Datei ist nicht richtig Formatiert!")
            return None
        count=1
        altcount = 1
        while count < (localLength-4):
            actID = 0
            actX = 0
            actY = 0
            actZ = 0
            while altcount < 13:
                actLine = vector3D.extractNumbersFromInput2(VecFile.readline())
                if count == (localLength-2):
                    break
                elif altcount < 6:
                    pass
                elif altcount == 6:
                    actID = int(actLine)
                elif altcount == 7:
                    actX = float(actLine)
                elif altcount == 8:
                    actY = float(actLine)
                elif altcount == 9:
                    actZ = float(actLine)
                elif altcount == 10:
                    pass
                elif altcount == 11:
                    pass
                altcount+=1
                count+=1
                #print(str(count)+", "+str(altcount)) #troubleshooting
            #print(str(actID))#hier auch
            vector3D(actX, actY, actZ, actID)
            altcount=7
        VecFile.close()
        return actualName
