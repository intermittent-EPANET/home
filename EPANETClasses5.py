#EPANETClasses2.py
#9/1/15
#sets up junction, tank, pipe, and coordinates classes

def AddWhiteSpaceColon(parsedRow,colonYN):

    #this adds back in enough white space to satisfy EPANET
    #handles any mix of ints or strs in the row

    try:
        spacedRow=parsedRow[0]
    except:                     #empty row, a new line will be added at the end
        spacedRow=parsedRow
        
    spacedRow=str(spacedRow)    #incase first addition is a number
    i=1
    while i< len(parsedRow):

        white="        \t"
        try:
            spacedRow+=white+parsedRow[i] #I tested the readability of this file without the spaces and it worked
        except:
            spacedRow+=white+str(parsedRow[i])

        i+=1
    if colonYN==True:
        spacedRow+=white+";\n"
    else:
        spacedRow+="\n"
        
    return spacedRow



class Junction(object):
    
    #define class to carry all of the EPANET junction data
    kind='Junction'

    def __init__ (self, ID, Elev, Demand, Pattern, Colon):

        self.ID = str(ID)
        self.Elev= float(Elev)
        self.Demand= float(Demand)
        self.Pattern= str(Pattern)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "ID= %s Elevation = %.1f Demand = %.4f Pattern = %s" %(self.ID,self.Elev,self.Demand,self.Pattern)

    def flatten(self):

        return AddWhiteSpaceColon([self.ID,self.Elev,self.Demand,self.Pattern],self.Colon)

    
class Tank(object):
    
    #define class to carry all of the EPANET junction data
    kind='Tank'

    def __init__ (self, ID, Elev, InitLvl, MinLvl, MaxLvl, Dia, MinVol, Colon):

        self.ID = str(ID)
        self.Elev= float(Elev)
        self.InitLvl= float(InitLvl)
        self.MinLvl= float(MinLvl)
        self.MaxLvl= float(MaxLvl)
        self.Dia= float(Dia)
        self.MinVol= float(MinVol)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "ID= %s Elev = %.1f InitLvl = %.2f MinLvl = %.2f MaxLvl = %.2f Dia = %.3f MinVol = %.3f" %(self.ID,self.Elev,self.InitLvl, self.MinLvl, self.MaxLvl, self.Dia, self.MinVol)

    def flatten(self):

        return AddWhiteSpaceColon([self.ID,self.Elev,self.InitLvl, self.MinLvl, self.MaxLvl, self.Dia, self.MinVol],self.Colon)

class Pipe(object):

    #define class to carry all of the EPANET junction data
    kind='Pipe'

    def __init__ (self, ID, Node1, Node2, Length, Dia, Rough, Loss, Status, Colon):

        self.ID = str(ID)
        self.Node1= str(Node1)
        self.Node2= str(Node2)
        self.Length= float(Length)
        self.Dia= float(Dia)
        self.Rough= int(Rough)
        self.Loss= float(Loss)
        self.Status= str(Status)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "ID= %s Node1 = %s Node2 = %s Length = %.4f Dia = %.1f Rough = %i Loss = %.1f Status = %2" %(self.ID,self.Node1,self.Node2, self.Length, self.Dia, self.Rough, self.Loss, self.Status)

    def flatten(self):

        return AddWhiteSpaceColon([self.ID,self.Node1,self.Node2, self.Length, self.Dia, self.Rough, self.Loss, self.Status],self.Colon)

class Coordinate(object):
    
    #define class to carry all of the EPANET junction data
    kind='Coordinates'

    def __init__ (self, Node, Xcord, Ycord,Colon):

        self.Node = str(Node)
        self.Xcord= float(Xcord)
        self.Ycord= float(Ycord)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "Node= %s Xcordation = %.2f Ycord = %.2f " %(self.Node,self.Xcord,self.Ycord)

    def flatten(self):

        return AddWhiteSpaceColon([self.Node,self.Xcord,self.Ycord],self.Colon)

class DemandSpec(object):
    
    #define class to carry all of the EPANET junction data
    kind='DemandSpec'

    def __init__ (self, ID, Demand, Pattern, Colon):

        self.ID = str(ID)
        self.Demand= float(Demand)
        self.Pattern= str(Pattern)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "ID= %s Demand = %.4f Pattern = %s Colon= %b" %(self.ID,self.Demand,self.Pattern,self.Colon)

    def flatten(self):

        return AddWhiteSpaceColon([self.ID,self.Demand,self.Pattern],self.Colon)

##For Reading .RPT Files
class Link(object):
    
    #define class to carry which two nodes it is connected to and their indexes
    kind='Link'

    def __init__ (self, Name, ID1, ID2,i1,i2,Length,Dia):

        self.Name= str(Name)
        self.ID1 = str(ID1)
        self.ID2 = str(ID2)
        self.Length=float(Length)
        self.Dia=float(Dia)
        self.i1=int(i1)
        self.i2=int(i2)
        self.P1=[]
        self.P2=[]
        
    def __repr__(self):
        
        return "INCOMPLETE REPR FNC. ID1= %s ID2 = %s " %(self.ID1,self.ID2)

    def addPressure(self,P1,P2):

        self.P1.append(float(P1))
        self.P2.append(float(P2))
        


    
