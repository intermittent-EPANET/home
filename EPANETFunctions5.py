#EPANETFunctions.py
#9/1/15

from EPANETClasses5 import * #get all classes from EPANETClasses file
#now works for .RPT files also

def HeaderIndex(header,bigList):

    #returns the row number of the header. adds the required square brackets and /n chars
    fullheader="["+header+"]"+"\n"
    if bigList.count(fullheader)>1:

        print("warning! more than 1 header with that name")

    elif bigList.count(fullheader)<1:

        print("header not found!")

    return bigList.index(fullheader)

def FindEdges(header,bigList):

    #next find the index starting header
    startrow=HeaderIndex(header,bigList)
    
    startrow+=1 #advance past header
    while bigList[startrow][0]==';':
        #we have a comment (e.g. names of columns)
        startrow+=1
    #startrow now points at start of data

    #find end of data
    endrow=startrow
    while endrow<len(bigList) and bigList[endrow]!='\n':
        #we still in the section
        endrow+=1
    #print('finaledge',[bigList[endrow]])#will print -1, 0, +1
    endrow-=1 #cutoff the blank line
    #print('ADJfinaledge',[bigList[endrow]])#will print -1, 0, +1
    bounds=(startrow,endrow) #cuts off the title and headers, cuts off the /n row between sections
    return bounds
    
def CopySection(header,bigList):

    #calls find edeges. separated so that splice can also call find edges
    bounds=FindEdges(header,bigList)
    #print(header,bounds[0],bounds[1])
    #print(bigList[bounds[0]],bigList[bounds[1]:bounds[1]+5])
    return bigList[bounds[0]:bounds[1]+1] #because range is exclusive to teh last term

def Splice(header, bigList, smallList):

    #takes bigList and splices in smallList under the heading "header"
    #needs to be debugged!
    bounds=FindEdges(header,bigList)
    frontList=bigList[:bounds[0]] #range is exclusive of last term
    middleList=smallList
    endList=bigList[bounds[1]+1:] #range is inclusive of first term
    #print('warning changed this splicing line also')
    return frontList+middleList+endList
    
def SizeConversion (demand, householdDemand,dayPercent,pipeDia,lossCoef,tankHeight):

    #Demand in LPS
    #steps for fixing a junction:
        #1 convert demand to an equivalent number or people
        #2 convert people into an equivalent size of pipe and tank and loss coefficient
        #3 round floats
    ppl=demand/(householdDemand/24/3600)
    #print("SizeConversion ppl count is ", ppl)
    #step2
    newPipeDia=pipeDia*ppl**0.3799
    oldTankDia=(dayPercent*householdDemand/1000*4/3.141/tankHeight)**0.5
    newTankDia=oldTankDia*ppl**0.5
    newLossCoef=lossCoef/ppl**0.4804

    #round values to 2 decimal places
    newPipeDia=round(newPipeDia,2)
    newTankDia=round(newTankDia,3)
    newLossCoef=round(newLossCoef,2)
    return {'newPipeDia': newPipeDia, 'newTankDia': newTankDia, 'newLossCoeff':newLossCoef}

def Collate(featureList):

    #for pipes, tanks, etc. flatten the whole list
    flatList=[]
    for row in featureList:
        flatList.append(row.flatten())

    return flatList

def ReadEPANET(filename):

    #read
    f=open(filename,"r")
    fullcontentList=f.readlines()
    f.close()

    #separate
    junctionsList=CopySection("JUNCTIONS",fullcontentList)
    #print(junctionsList[-1])
    tanksList=CopySection("TANKS",fullcontentList)
    #print(tanksList)
    pipesList=CopySection("PIPES",fullcontentList)
    coordinatesList=CopySection("COORDINATES",fullcontentList)
    demandsList=CopySection("DEMANDS",fullcontentList)

    #convert to customized objects: Junctions, Tanks, Pipes, Coordinates
    junctions=[]
    i=0
    while i < len(junctionsList):
        splitjunction=junctionsList[i].split()
        numElem=len(splitjunction)
        if splitjunction[-1][-1]==';':
            colonYN=True
            numElem-=1
        else:
            colonYN=False
        if numElem>0:
            ID=splitjunction[0]
        else:
            print('error no ID specified')
        if numElem>1:
            Elev=splitjunction[1]
        else:
            Elev=0
            print('error no Elev specified')
        if numElem>2:
            Demand=splitjunction[2]
        else:
            Demand=0
        if numElem>3:
            Pattern=splitjunction[3]
        else:
            Pattern=""
        
        junctions.append(Junction(ID,Elev,Demand,Pattern,colonYN))
        i+=1

    tanks=[]
    i=0
    while i< len(tanksList):
        t=tanksList[i].split()
        numElem=len(t)
        if t[-1][-1]==';':
            colonYN=True
            numElem-=1
        else:
            colonYN=False
        if numElem>0:
            ID=t[0]
        else:
            print('error no ID specified')
        if numElem>1:
            Elev=t[1]
        else:
            Elev=0
        if numElem>2:
            InitLvl=t[2]
        else:
            InitLvl=0
        if numElem>3:
            MinLvl=t[3]
        else:
            MinLvl=0
        if numElem>4:
            MaxLvl=t[4]
        else:
            MaxLvl=0
        if numElem>5:
            Dia=t[5]
        else:
            print('error no diameter specified',t)
        if numElem>6:
            MinVol=t[6]
        else:
            MinVol=0
        tanks.append(Tank(ID, Elev, InitLvl, MinLvl, MaxLvl, Dia, MinVol, colonYN))
        i+=1

    pipes=[]
    i=0
    while i< len(pipesList):
        p=pipesList[i].split()
        numElem=len(p)
        if p[-1][-1]==';':
            colonYN=True
            numElem-=1
        else:
            colonYN=False
            
        if numElem>0:
            ID=p[0]
        else:
            print('error no ID specified')
        if numElem>1:
            Node1=p[1]
        else:
            print('error no Node1 ID specified')
        if numElem>2:
            Node2=p[2]
        else:
            print('error no Node2 ID specified')
        if numElem>3:
            Length=p[3]
        else:
            print('error no length specified')
        if numElem>4:
            Dia=p[4]
        else:
            print('error no dia specified')
        if numElem>5:
            Rough=p[5]
        else:
            print('error no rough specified')
        if numElem>6:
            Loss=p[6]
        else:
            Loss=0
            print('warning using default loss value')
        if numElem>7:
            Status=p[7]
        else:
            Status='Open'
            
        pipes.append(Pipe(ID, Node1, Node2, Length, Dia, Rough, Loss, Status, colonYN))
        i+=1

    coordinates=[]
    i=0
    while i< len(coordinatesList):
        c=coordinatesList[i].split()
        if c[-1][-1]==';':
            colonYN=True
        else:
            colonYN=False
        coordinates.append(Coordinate(c[0],c[1],c[2],colonYN))
        i+=1

    demands=[]
    i=0
    while i< len(demandsList):
        d=demandsList[i].split()
        numElem=len(d)
        #print('demand',d, d[0],d[1])
        if d[-1][-1]==';':
            colonYN=True
            numElem-=1
            print('warning if ; is not separated by a space, data loss may occur')
        else:
            colonYN=False
        if numElem>2:
            Pattern=d[2]
        else:
            Pattern="0"
        #print(Pattern)
        demands.append(DemandSpec(d[0],d[1],Pattern,colonYN))
        i+=1
        
    return {'FullContent':fullcontentList,'Junctions':junctions,'Tanks':tanks,'Pipes':pipes,'Coordinates':coordinates,'Demands':demands}

def WriteEPANET(filenameFIX, junctionsFIX, tanksFIX, pipesFIX, coordinatesFIX, demandsFIX, fullcontentListFIX):
    #protect input variables
    filename=filenameFIX
    junctions=junctionsFIX
    tanks=tanksFIX
    pipes=pipesFIX
    coordinates=coordinatesFIX
    demands=demandsFIX
    fullcontentList=fullcontentListFIX
    
    ##############Flatten Lists #######
    junctionsList_adj=Collate(junctions)
    tanksList_adj=Collate(tanks)
    pipesList_adj=Collate(pipes)
    coordinatesList_adj=Collate(coordinates)
    demandsList_adj=Collate(demands)

    
    ###############Reassemble###############

    fullcontentList=Splice("JUNCTIONS",fullcontentList,junctionsList_adj)
    fullcontentList=Splice("TANKS",fullcontentList,tanksList_adj)
    fullcontentList=Splice("PIPES",fullcontentList,pipesList_adj)
    fullcontentList=Splice("COORDINATES",fullcontentList,coordinatesList_adj)
    fullcontentList=Splice("DEMANDS",fullcontentList,demandsList_adj)

    ###SAVE IT####

    file = open(filename, "w")  #used to be filename[:-4]+"_new.inp"
    for row in fullcontentList:
        file.write(row)
    file.close()

def ShiftTanks(tanks,shift):
    
    #Shift B-tanks
    for t in tanks:
        if t.ID[:2]=="TB":
            t.Elev+=shift
    return tanks

def RoundKeyValues(junctions,tanks,pipes):
    
    for junc in junctions:
        junc.Elev=round(junc.Elev,2)

    for t in tanks:
        t.Elev=round(t.Elev,2)

    for p in pipes:
        p.Length=round(p.Length,2)

    return (junctions,tanks,pipes)

#def MakeSumps(junctions,tanks,pipes,coordinates):
#    
#    #########################################
#    #                                       #
#    #                                       #
#    #   SUMP MAKING CONSTANTS ARE HERE!!!   #
#    #                                       #
#    #########################################
#
#    #account for semicolon usage; if one of the categories doesn't have any entries, use the colon value from others
#    jcolon=junctions[0].Colon
#
#    if len(tanks):
#        tcolon=tanks[0].Colon
#    else:
#        tcolon=jcolon
#
#    pcolon=pipes[0].Colon
#    ccolon=coordinates[0].Colon
#    
#    householdDemand=800 #was using 600 now use 175*5= #LPD; used to determine how many HH's are clumped at a junction
#
#    #pipe between the water main and the HH
#    pipeLengthHH=10 #m avg length between water main and HH's sump, meter or equivalent
#    pipeRoughHH=110 #avg roughness factor for existing pipes between water main and HH
#    pipeDia=15 #assumed diameter of individual HH connectison 15mm
#    lossCoef=8 #assumed minor loss coefficient between main and the HH booster pump (or valve)
#    print('verified2.0')
#    #HH Water Tanks
#    pipeTankLength=1 #m a pipe is used to connect the household to the tank, useful in pump simulation. length 1m
#    pipeTankDia=200 #mm this placeholder pipe is 200mm
#    dayPercent=1 #fraction of the day in which the tank is assumed to fill 1=100%
#    tankHeight=1 #m of tank height
#
#    #Visual offest
#    xoff=5  #these values give the tanks their offest on the map
#    yoff=5
#
#    extraTankElev=0 #m 0 for sump or valve, -4 for booster pump
#
#    #Find nodes with demand and flag them for fixing
#    fixlist=[]
#    i=0
#    while i < len(junctions):
#        if junctions[i].Demand != 0: #then there is a demand at this node!
#            fixlist.append(i)
#        i+=1
#
#    #FIX (ie modify the junction, add new junctions, pipes and tanks)
#
#    k=0   #counter to track what number to number new tanks, junctions, and pipes
#    newJunctions=[]
#    for i in fixlist:   #i is now the indext of things to fix. call the right function!
#        
#        demand=junctions[i].Demand
#
#        #calculate equivalent HH connection characteristics based on node size
#        newSizes=SizeConversion(demand, householdDemand,dayPercent,pipeDia,lossCoef,tankHeight)
#
#        #remove demand
#        junctions[i].Demand=0
#
#        #add new node (to a list of things to tack on)
#        newJunctions.append(Junction("JB"+str(k),junctions[i].Elev,0," ",jcolon))
#
#        #add TANK
#        tanks.append(Tank("TB"+str(k),junctions[i].Elev+extraTankElev,0,0,tankHeight,newSizes['newTankDia'],0,tcolon))
#
#        #join with adequate pipes
#        pipes.append(Pipe("Ba"+str(k),junctions[i].ID,newJunctions[-1].ID,pipeLengthHH,newSizes['newPipeDia'],pipeRoughHH,newSizes['newLossCoeff'],"Open",pcolon))
#        pipes.append(Pipe("Bb"+str(k),newJunctions[-1].ID,tanks[-1].ID,pipeTankLength,pipeTankDia,pipeRoughHH,0,"Open",pcolon))
#
#        #find coordinates of current junction
#        xcurr=0
#        ycurr=0
#        j=0
#        while j<len(coordinates):
#            if coordinates[j].Node == junctions[i].ID:
#                xcurr=coordinates[j].Xcord
#                ycurr=coordinates[j].Ycord
#                j=len(coordinates)+1 #exit
#            else:
#                j+=1
#        if j==len(coordinates):
#            print("error, location of current junction ", junctions[i].ID, "not found")
#            
#        #site new junction and tank
#        coordinates.append(Coordinate(newJunctions[-1].ID,xcurr+xoff, ycurr+yoff,ccolon))
#        coordinates.append(Coordinate(tanks[-1].ID,xcurr+2*xoff,ycurr,ccolon))
#
#        k+=1 #additions counter
#
#    #tack on new junction nodes
#    junctions+=newJunctions
#    return (junctions,tanks,pipes,coordinates)

def MakeSpecifiedSumps( junctions,tanks,pipes,coordinates, HHDaily, sDepth, bpDepth,sList,bpList):
    
    #########################################
    #                                       #
    #                                       #
    #some SUMP MAKING CONSTANTS ARE HERE!!! #
    #                                       #
    #########################################

    #account for semicolon usage; if one of the categories doesn't have any entries, use the colon value from others
    jcolon=junctions[0].Colon

    if len(tanks):
        tcolon=tanks[0].Colon
    else:
        tcolon=jcolon

    pcolon=pipes[0].Colon
    ccolon=coordinates[0].Colon
    
    householdDemand=float(HHDaily) #was using 600 now use 175*5= #LPD; used to determine how many HH's are clumped at a junction

    #pipe between the water main and the HH
    pipeLengthHH=10 #m avg length between water main and HH's sump, meter or equivalent
    pipeRoughHH=110 #avg roughness factor for existing pipes between water main and HH
    pipeDia=15 #assumed diameter of individual HH connectison 15mm
    lossCoef=8 #assumed minor loss coefficient between main and the HH booster pump (or valve)
    print('verified2.0')
    #HH Water Tanks
    #pipeTankLength=1 #m a pipe is used to connect the household to the tank, useful in pump simulation. length 1m
    #pipeTankDia=200 #mm this placeholder pipe is 200mm
    dayPercent=1 #fraction of the day in which the tank is assumed to fill 1=100%
    tankHeight=1 #m of tank height

    #Visual offest
    xoff=5  #these values give the tanks their offest on the map
    yoff=5

    #extraTankElev=Depth #m 0 for sump or valve, -4 for booster pump

    #Find nodes with demand and flag them for fixing
    fixlist=[]
    i=0
    while i < len(junctions):
        if junctions[i].Demand != 0: #then there is a demand at this node!
            if junctions[i].ID in (sList+bpList):
                fixlist.append(i)
        i+=1
    #fix list is now a list of 4, 8,14, etc. of ascendking #s to fix.
        
    #FIX (ie modify the junction, add new junctions, pipes and tanks)

    k=0   #counter to track what number to number new tanks, junctions, and pipes
    #newJunctions=[]
    for i in fixlist:   #i is now the indext of things to fix. call the right function!
        
        demand=junctions[i].Demand

        #calculate equivalent HH connection characteristics based on node size
        newSizes=SizeConversion(demand, householdDemand,dayPercent,pipeDia,lossCoef,tankHeight)

        #remove demand
        junctions[i].Demand=0

        #add new node (to a list of things to tack on)
        #newJunctions.append(Junction("JB"+str(k),junctions[i].Elev,0," ",jcolon))

        #add TANK
        if junctions[i].ID in bpList:
            extraTankElev=bpDepth
        else:
            extraTankElev=sDepth
            
        tanks.append(Tank("TB"+str(k),junctions[i].Elev+extraTankElev,0,0,tankHeight,newSizes['newTankDia'],0,tcolon))

        #join with adequate pipes
        pipes.append(Pipe("B"+str(k),junctions[i].ID,tanks[-1].ID,pipeLengthHH,newSizes['newPipeDia'],pipeRoughHH,newSizes['newLossCoeff'],"Open",pcolon))

        #pipes.append(Pipe("B"+str(k),junctions[i].ID,newJunctions[-1].ID,pipeLengthHH,newSizes['newPipeDia'],pipeRoughHH,newSizes['newLossCoeff'],"Open",pcolon))
        #pipes.append(Pipe("Bb"+str(k),newJunctions[-1].ID,tanks[-1].ID,pipeTankLength,pipeTankDia,pipeRoughHH,0,"Open",pcolon))

        #find coordinates of current junction
        xcurr=0
        ycurr=0
        j=0
        while j<len(coordinates):
            if coordinates[j].Node == junctions[i].ID:
                xcurr=coordinates[j].Xcord
                ycurr=coordinates[j].Ycord
                j=len(coordinates)+1 #exit
            else:
                j+=1
        if j==len(coordinates):
            print("error, location of current junction ", junctions[i].ID, "not found")
            
        #site new junction and tank
        #coordinates.append(Coordinate(newJunctions[-1].ID,xcurr+xoff, ycurr+yoff,ccolon))
        coordinates.append(Coordinate(tanks[-1].ID,xcurr+xoff,ycurr+yoff,ccolon))

        k+=1 #additions counter

    #tack on new junction nodes
    #junctions+=newJunctions
    return (junctions,tanks,pipes,coordinates)


def MakeSomeSumps(junctionsFIX,tanksFIX,pipesFIX,coordinatesFIX,percentBPFIX,BPsuctionFIX):
    #1/15/15
    #use to make sure a variable amount of pumps and sumps can be created
    #Most of this function runs on order in which things are done. BPs are created first and are therefore [-2] and sumps last and therefore [-1]
    #########################################
    #                                       #
    #                                       #
    #   SUMP MAKING CONSTANTS ARE HERE!!!   #
    #                                       #
    #########################################
    #protect input variables:
    junctions=junctionsFIX
    tanks=tanksFIX
    pipes=pipesFIX
    coordinates=coordinatesFIX
    percentBP=percentBPFIX
    BPsuction=BPsuctionFIX
    
    if percentBP==1:
        print("wrong function use normal method for BPs")
    elif percentBP==0:
        print("wrong function use normal method for sumps")
    
    householdDemand=600 #LPD; used to determine how many HH's are clumped at a junction

    #pipe between the water main and the HH
    pipeLengthHH=10 #m avg length between water main and HH's sump, meter or equivalent
    pipeRoughHH=110 #avg roughness factor for existing pipes between water main and HH
    pipeDia=15 #assumed diameter of individual HH connectison 15mm
    lossCoef=8 #assumed minor loss coefficient between main and the HH booster pump (or valve)
    print('MakeSomeSumpsRunning with ration', percentBP)
    #HH Water Tanks
    pipeTankLength=1 #m a pipe is used to connect the household to the tank, useful in pump simulation. length 1m
    pipeTankDia=200 #mm this placeholder pipe is 200mm
    dayPercent=1 #fraction of the day in which the tank is assumed to fill 1=100%
    tankHeight=1 #m of tank height

    #Visual offest
    xoff=5  #these values give the tanks their offest on the map
    yoff=5

    #extraTankElev=0 #m 0 for sump or valve, -4 for booster pump

    #Find nodes with demand and flag them for fixing
    fixlist=[]
    i=0
    while i < len(junctions):
        if junctions[i].Demand != 0: #then there is a demand at this node!
            fixlist.append(i)
            print('demand found')
        i+=1

    #FIX (ie modify the junction, add new junctions, pipes and tanks)

    k=0   #counter to track what number to number new tanks, junctions, and pipes
    newJunctions=[]
    for i in fixlist:   #i is now the indext of things to fix. call the right function!
        
        demand=junctions[i].Demand

        #calculate equivalent HH connection characteristics based on node size
        #BPside
        newSizesBP=SizeConversion(demand*percentBP, householdDemand,dayPercent,pipeDia,lossCoef,tankHeight)
        #SumpSide
        newSizesS=SizeConversion(demand*(1-percentBP), householdDemand,dayPercent,pipeDia,lossCoef,tankHeight)

        print("new sizes BP and S",newSizesBP['newTankDia'],newSizesS['newTankDia'])
        
        #remove demand
        junctions[i].Demand=0

        #Do BP Side
        #add new node (to a list of things to tack on)
        #BP junction
        newJunctions.append(Junction("JB"+str(k),junctions[i].Elev,0," "))
        
        
        #add TANK
        #BP
        tanks.append(Tank("TB"+str(k),junctions[i].Elev+BPsuction,0,0,tankHeight,newSizesBP['newTankDia'],0))
        

        #join with adequate pipes
        #BP side
        pipes.append(Pipe("BaB"+str(k),junctions[i].ID,newJunctions[-1].ID,pipeLengthHH,newSizesBP['newPipeDia'],pipeRoughHH,newSizesBP['newLossCoeff'],"Open"))
        pipes.append(Pipe("BbB"+str(k),newJunctions[-1].ID,tanks[-1].ID,pipeTankLength,pipeTankDia,pipeRoughHH,0,"Open"))



        #find coordinates of current junction
        xcurr=0
        ycurr=0
        j=0
        while j<len(coordinates):
            if coordinates[j].Node == junctions[i].ID:
                xcurr=coordinates[j].Xcord
                ycurr=coordinates[j].Ycord
                j=len(coordinates)+1 #exit
            else:
                j+=1
        if j==len(coordinates):
            print("error, location of current junction ", junctions[i].ID, "not found")
            
        #site new junction and tank
        #BP
        coordinates.append(Coordinate(newJunctions[-1].ID,xcurr+xoff, ycurr+yoff))
        coordinates.append(Coordinate(tanks[-1].ID,xcurr+2*xoff,ycurr))


        

        

        #Now Do Sumps:
        #sump junction
        newJunctions.append(Junction("JS"+str(k),junctions[i].Elev,0," "))
        #sump
        tanks.append(Tank("TS"+str(k),junctions[i].Elev,0,0,tankHeight,newSizesS['newTankDia'],0))

        #add pipes
        pipes.append(Pipe("BaS"+str(k),junctions[i].ID,newJunctions[-1].ID,pipeLengthHH,newSizesS['newPipeDia'],pipeRoughHH,newSizesS['newLossCoeff'],"Open"))
        pipes.append(Pipe("BbS"+str(k),newJunctions[-1].ID,tanks[-1].ID,pipeTankLength,pipeTankDia,pipeRoughHH,0,"Open"))

        #add coordinates
        #SUMP
        coordinates.append(Coordinate(newJunctions[-1].ID,xcurr-xoff, ycurr+yoff))
        coordinates.append(Coordinate(tanks[-1].ID,xcurr-2*xoff,ycurr))

        
        k+=1 #additions counter
    #tack on new junction nodes
    junctions+=newJunctions
    
    return (junctions,tanks,pipes,coordinates)

#RPT FUNCTIONS
def FractionOfPipe(P1,P2,B1,B2):
    if P1>P2:
        t=P1
        P1=P2
        P2=t
    if B1>B2:
        t=B1
        B1=B2
        B2=t
    if P1==P2:
        if B1<P1 and P1<B2:
            frac=1
        else:
            frac=0
    else:
        frac=(min(P2,B2)-max(P1,B1))/(P2-P1)
    if frac<0:
        frac=0
    return frac

def TotalDuration(top,bot,timestep,linkData):
    score=0
    for pipe in linkData:
        i=0
        #print(pipe.Length)
        while i<len(pipe.P1):
            score+=pipe.Length*timestep*FractionOfPipe(pipe.P1[i],pipe.P2[i],top,bot)
            i+=1
    return score

#print(FractionOfPipe(1.1,0.9,1.0,1.05))

def TotalNetworkLength(linkData):
    #for each link add up its length
    total=0
    for p in linkData:
        total+=p.Length
    return total

def ReadTankPressures(filename):
    f=open(filename,"r")
    fullcontentList=f.readlines()
    f.close()
    i=0
    nodeData=[]
    while i < len(fullcontentList):
        row=fullcontentList[i].split() #whitespace is now gone from this row
        if len(row)<1:
            i+=1
        elif row[0]=="Node":
            #sub loop to grab Node data
            cat=row[0] #record the category of the data
            time=row[3] #time is now in format "6:45"
            
            #Sanity Check
            if row[1]=="Results":
                results=True
            else:
                results=False
                print("not Results found...")

            i+=5 #skip header
            row=fullcontentList[i].split()
            data=[]
            #print(row)
            while len(row) >0 and i<len(fullcontentList)-1: #breaks at white space or at end of file
                if row[0][:2]=="TB": #record only tank pressures
                    #to record all pressures remove the if statement and de-indent data.append(...
                    data.append([row[0],row[3]])#grad ID and Pressure
                    
                i+=1
                row=fullcontentList[i].split()
                #print("got here with i = ",str(i))
            if results==True:
                nodeData.append([cat,time,data]) #this will add ['Node','0:15',[[J121,0];[J122,0];......]]
            else:
                print("not Results found...")
        else:
            i+=1

    #now combine similar results
    nodeCombo=[]
    nodeCombo.append(nodeData[0])
    #print(nodeData[0][1])
    #print(nodeCombo[-1][1])

    j=1
    while j<len(nodeData):
        #print(nodeData[j][1])
        #print(nodeCombo[-1][1])
        if nodeData[j][1]==nodeCombo[-1][1] and nodeData[j][0]==nodeCombo[-1][0]: #if category and time match combine these entries
            nodeCombo[-1][2]+=nodeData[j][2]
        else:
            nodeCombo.append(nodeData[j])
        j+=1
    
    return nodeCombo

def FindTimeStep(nodeCombo):
    #calculate time step
    time2=nodeCombo[1][1]
    time1=nodeCombo[0][1]
    #print("time 2,1",time2,time1)
    timestep=float(60*(int(time2[0])-int(time1[0]))+int(time2[-2:])-int(time1[-2:]))        
    timestep=timestep/60 #in hours
    #print(timestep)

    return timestep

def ReadLinkPressures(filename):
    f=open(filename,"r")
    fullcontentList=f.readlines()
    f.close()
    i=0
    nodeData=[]
    while i < len(fullcontentList):
        row=fullcontentList[i].split() #whitespace is now gone from this row
        if len(row)<1:
            i+=1
        elif row[0]=="Node":
            #sub loop to grab Node data
            cat=row[0] #record the category of the data
            time=row[3] #time is now in format "6:45"
            
            #Sanity Check
            if row[1]=="Results":
                results=True
            else:
                results=False
                print("not Results found...")

            i+=5 #skip header
            row=fullcontentList[i].split()
            data=[]
            #print(row)
            while len(row) >0 and i<len(fullcontentList)-1: #breaks at white space or at end of file
                data.append([row[0],row[3]])#grad ID and Pressure                    
                i+=1
                row=fullcontentList[i].split()
                #print("got here with i = ",str(i))
            if results==True:
                nodeData.append([cat,time,data]) #this will add ['Node','0:15',[[J121,0];[J122,0];......]]
            else:
                print("not Results found...")
        else:
            i+=1

    #now combine similar results
    nodeCombo=[]
    nodeCombo.append(nodeData[0])
    #print(nodeData[0][1])
    #print(nodeCombo[-1][1])

    j=1
    while j<len(nodeData):
        #print(nodeData[j][1])
        #print(nodeCombo[-1][1])
        if nodeData[j][1]==nodeCombo[-1][1] and nodeData[j][0]==nodeCombo[-1][0]: #if category and time match combine these entries
            nodeCombo[-1][2]+=nodeData[j][2]
        else:
            nodeCombo.append(nodeData[j])
        j+=1


    #print(nodeCombo[0])
    #for row in nodeCombo[0][2]:
     #  print(row,"\n")

    #nodeCombo now has 1 entry per timestep in the simulation!
    nodeList=[]
    for row in nodeCombo[0][2]:
        nodeList.append(row[0])
    #print("nodelist",nodeList)

    #get LINK INFO
    #grab link info until keyword "node is hit"
    k=0
    linkData=[]
    setup=True
    while k < len(fullcontentList) and setup:
        row=fullcontentList[k].split() #whitespace is now gone in row 1!
        if len(row)<1:
            k+=1
        elif row[0]=="Link":
            #print(row)
            if row[3]!="Table:":
                print("uhoh something went wrong")
            k+=5 #skip header
            row=fullcontentList[k].split()
            #print(row)
            while len(row) >0 and k<len(fullcontentList)-1:
                Name=row[0]
                ID1=row[1]
                ID2=row[2]
                i1=nodeList.index(ID1)
                i2=nodeList.index(ID2)
                Length=row[3]
                Dia=row[4]
                newLink=Link(Name, ID1, ID2,i1,i2,Length,Dia)
                linkData.append(newLink)
                k+=1
                row=fullcontentList[k].split()
                #print("got here with i = ",str(i))
        elif row[0]=="Node":
            setup=False #break as teh list is done!
        else:
            k+=1
    #print("linkdata length",len(linkData))
    #for row in linkData:
     #   print(row.Name,row.ID1,row.ID2,row.i1)

    #calculate time step
    time2=nodeCombo[1][1]
    time1=nodeCombo[0][1]
    timestep=60*(int(time2[0])-int(time1[0]))+int(time2[-2:])-int(time1[-2:])
    timestep=timestep/60 #in hours
    #print(timestep)

    #Now aggregate pressure date onto links list
    #print(nodeCombo[-1])
    for pipe in linkData:
        #for each pipe, compile the time data
        i=0
        #print(nodeCombo[0])
        while i<len(nodeCombo):
            #print(nodeCombo[0][2][pipe.i1])
            #print(nodeCombo[i][2][pipe.i1][1],nodeCombo[i][2][pipe.i2][1])
            pipe.addPressure(nodeCombo[i][2][pipe.i1][1],nodeCombo[i][2][pipe.i2][1])
            i+=1

    return (timestep,linkData)

def PrintTankFillRates(filename):
    tankData=ReadTankPressures(filename) #list where each entry is like ['Node','0:15',[[TB121,0],[TB122,0],......]]
    timeStep=FindTimeStep(tankData)
    #print(timeStep)
    
    
    #now bin the data
    hist=[]
    for row in tankData: #for each timestep
        #print(row[1]) #print the timestamp
        low=float(0)
        med=float(0)
        high=float(0)
        full=float(0)
        for t in row[2]:
            lvl=float(t[1])
            #print(t)
            #print(t[1])
            if lvl<0.1:
                low+=1
            elif lvl<0.5:
                med+=1
            elif lvl<1:
                high+=1
            elif lvl==1:
                full+=1
            else:
                print('ERROR! tank heigh >1')
        #normalize
        numTanks=low+med+high+full
        result=[low,med,high,full]
        #print(result)
        result=[float(x/numTanks) for x in result]
        #print(result)    
        hist.append(result)
    
    times=[]
    lows=[]
    time=0
    for r in tankData: #generate x-axis values in hours
        times.append(time)
        time+=timeStep
    
    lows=[]
    meds=[]
    highs=[]
    full=[]
    
    #print(hist[:10])
    
    for k in hist:            #create stacked results
        curr=k[0]    
        lows.append(curr)
        curr+=k[1]
        meds.append(curr)
        curr+=k[2]
        highs.append(curr)
        curr+=k[3]
        full.append(curr)
        
    #find our current pressure tag
    pStr=filename[-7:-5]
    #plot it in the function and save the file
    plt.plot([], [], color='green', linewidth=10)    
    plt.plot([], [], color='blue', linewidth=10)
    plt.plot([], [], color='yellow', linewidth=10)
    plt.plot([], [], color='red', linewidth=10)

    
    plt.fill_between(times, lows, y2=0, where=None,facecolor='red',  interpolate=False,hold=True)
    plt.fill_between(times, lows,meds,where=None,facecolor='yellow', interpolate=False,hold=True,label='This is a test label')
    plt.fill_between(times, meds,highs, where=None,facecolor='blue',  interpolate=False,hold=True)
    plt.fill_between(times, highs, y2=1,where=None,facecolor="green",interpolate=False,hold=True,label='<10%')
    
    plt.xlim([1,24])
    plt.xlabel('Hours of Supply per Day')
    plt.ylabel('Fraction of Houses Supplied')
    plt.title('Percent of Daily Demand that Households Actually Get\n'+pStr+'m of Supply Pressure')
    #plt.legend(['P=10m 10-100%','P=20m 10-100%','P=40m 10-100%','P=60m 10-100%'],loc=0)
    plt.legend(['100%','50-100%','10-50%','<10%'])
    plt.savefig('Customer Satisfaction at '+pStr+'m.pdf')
    #plt.savefig('ComboFillRates2.pdf')
    plt.show()


def GetTankFillRates(filename):
    tankData=ReadTankPressures(filename) #list where each entry is like ['Node','0:15',[[TB121,0],[TB122,0],......]]
    timeStep=FindTimeStep(tankData)
    #print(timeStep)
    
    
    #now bin the data
    hist=[]
    for row in tankData: #for each timestep
        #print(row[1]) #print the timestamp
        low=float(0)
        med=float(0)
        high=float(0)
        full=float(0)
        for t in row[2]:
            lvl=float(t[1])
            #print(t)
            #print(t[1])
            if lvl<0.1:
                low+=1
            elif lvl<0.5:
                med+=1
            elif lvl<1:
                high+=1
            elif lvl==1:
                full+=1
            else:
                print('ERROR! tank heigh >1')
        #normalize
        numTanks=low+med+high+full
        result=[low,med,high,full]
        #print(result)
        result=[float(x/numTanks) for x in result]
        #print(result)    
        hist.append(result)
    
    times=[]
    lows=[]
    time=0
    for r in tankData: #generate x-axis values in hours
        times.append(time)
        time+=timeStep
    
    lows=[]
    meds=[]
    highs=[]
    full=[]
    
    #print(hist[:10])
    
    for k in hist:            #create stacked results
        curr=k[0]    
        lows.append(curr)
        curr+=k[1]
        meds.append(curr)
        curr+=k[2]
        highs.append(curr)
        curr+=k[3]
        full.append(curr)
        
        
    #plt.title('Percent of Daily Demand that Households Actually Get\n'+pStr+'m of Supply Pressure')
    #plt.legend(['100%','50-100%','10-50%','<10%'])
        
    return([times, lows, meds, highs])
   
def SeparateTankPressures(filename):
    tankData=ReadTankPressures(filename) #list where each entry is like ['Node','0:15',[[TB121,0],[TB122,0],......]]
    timeStep=FindTimeStep(tankData)
    
    f=open(filename,"r")
    fullcontentList=f.readlines()
    f.close()
    
    k=0
    linkData=[]
    setup=True
    i1='0'
    i2='0'
    Length='0'
    Dia='0'
    while k < len(fullcontentList) and setup:
        row=fullcontentList[k].split() #whitespace is now gone in row 1!
        if len(row)<1:
            k+=1
        elif row[0]=="Link":
            #print(row)
            if row[3]!="Table:":
                print("uhoh something went wrong")
            k+=5 #skip header
            row=fullcontentList[k].split()
            #print(row)
            while len(row) >0 and k<len(fullcontentList)-1:
                Name=row[0]
                ID1=row[1]
                ID2=row[2]
                #i1=nodeList.index(ID1)
                #i2=nodeList.index(ID2)
                #Length=row[3]
                #Dia=row[4]
                newLink=Link(Name, ID1, ID2,i1,i2,Length,Dia)
                linkData.append(newLink)
                k+=1
                row=fullcontentList[k].split()
                #print("got here with i = ",str(i))
        elif row[0]=="Node":
            setup=False #break as teh list is done!
        else:
            k+=1
    
    Ktanks=[]
    Ltanks=[]        
    for l in linkData:
        if l.ID1[:2]=="JP":
            Ktanks.append(l.ID2)
        else:
            Ltanks.append(l.ID2)
    
    return([Ktanks,Ltanks,timeStep,tankData])
    
        
    
