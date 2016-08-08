// EPANETClasses2.py
//9/1/15
//sets up junction, tank, pipe, and coordinates classes

/* var AddWhiteSpaceColon = function (parsedRow, colonYN) {

    //this adds back in enough white space to satisfy EPANET
    // handles any mix of ints or strs in the row
    "use strict";
    try {
        spacedRow=parsedRow[0];
    }
    except{                     //empty row, a new line will be added at the end
        spacedRow=parsedRow;
    }
        
    spacedRow=String(spacedRow);    //incase first addition is a number
    var i=1;
    while (i< parsedRow.length()){

        white="        \t"
        try:
            spacedRow+=white+parsedRow[i]; // I tested the readability of this file without the spaces and it worked
        except:
            spacedRow+=white+str(parsedRow[i]);

        i+=1
    }
    if (colonYN){
        spacedRow+=white+";\n";
    }
    else:
        spacedRow+="\n";
        
    return spacedRow;
}; */

function AddWhiteSpaceColon(parsedRow, colonYN) {
    // this adds back in enough white space to satisfy EPANET
    // handles an mix of ints or strs in the row
    "use strict";
    this.parsedRow = parsedRow;
    this.colonYN = colonYN;
    this.spacedRow = "start";
    
    this.setSpace = function () {
        var spacedRow, i, white;
    
        spacedRow = "";
        
        if (this.colonYN) {
            spacedRow += parsedRow[0];
        }
        i = 1;
        white = "        \t";
        while (i < parsedRow.length - 1) {
            spacedRow += white + String(this.parsedRow[i]);
            i += 1;
        }
        if (this.colonYN) {
            spacedRow += white + String(this.parsedRow[i]);
        } else {
            spacedRow += "\n";
        }
    
        this.spacedRow = spacedRow;
    };
    this.toString = function () {
        return String(this.spacedRow);
    };
}
function Junction(ID, Elev, Demand, Pattern, Colon) {
    "use strict";
    var k = 0;
    this.isolated = " ";
    this.ID = String(ID);
    this.Elev = parseFloat(Elev);
    this.Demand = parseFloat(Demand);
    this.Pattern = String(Pattern);
    this.Colon = Colon;
    
    
    this.toString = function () {
        var white = "        \t";
        //this.ID = this.ID.substring(2, this.ID.length -10);
        if (Colon) {
            return this.ID + white + String(this.Elev) + white + String(this.Demand) + white + String(this.Pattern) + white + ";" + "\n";
        }
        else{
            return this.ID + white + String(this.Elev) + white + String(this.Demand) + white + String(this.Pattern) + white + " " + "\n";
            }
    };
    this.flatten = function () {
        return new AddWhiteSpaceColon([this.ID, this.Elev, this.Demand, this.Pattern], this.Colon);
    };

}
function Tank(ID, Elev, InitLvl, MinLvl, MaxLvl, Dia, MinVol, Colon) {
    "use strict";
    this.ID = String(ID);
    this.Elev = parseFloat(Elev);
    this.InitLvl = parseFloat(InitLvl);
    this.MinLvl = parseFloat(MinLvl);
    this.MaxLvl = parseFloat(MaxLvl);
    this.Dia = parseFloat(Dia);
    this.MinVol = parseFloat(MinVol);
    this.Colon = Colon;
    
    this.toString = function () {
        var white = "        \t";
        if (Colon) {
            return white + this.ID + white + String(this.Elev) + white + String(this.InitLvl) + white + String(this.MinLvl) + white + String(this.MaxLvl) + white + String(this.Dia) + white + String(this.MinVol) + white + ";" + "\n";
        }
        else{
            return white + this.ID + white + String(this.Elev) + white + String(this.InitLvl) + white + String(this.MinLvl) + white + String(this.MaxLvl) + white + String(this.Dia) + white + String(this.MinVol) + white + " " + "\n";
        }
    };
    /* Tank.flatten = function () {
        return new AddWhiteSpaceColon([this.ID,this.Elev, self.InitLvl, self.MinLvl, self.MaxLvl,self.Dia,self.MinVol],this.Colon);
    }; */

}

    
function Pipe(ID, Node1, Node2, Length, Dia, Rough, Loss, Status, Colon) {
    "use strict";
    this.isolated = " ";
    this.ID = String(ID);
    this.Node1 = String(Node1);
    this.Node2 = String(Node2);
    this.Length = parseFloat(Length);
    this.Dia = parseFloat(Dia);
    this.Rough = parseInt(Rough, 10);
    this.Loss = parseFloat(Loss);
    this.Status = String(Status);
    this.Colon = Colon;
    
    /*for (var k= 0; k < this.ID.length-1; k++){
            // ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz
        if ("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz".indexOf(this.ID.substring(k,k+1)) < 0){
            this.isolated += this.ID.substring(k,k+1);
        }
            
    }
    this.ID = this.isolated; */


    this.toString = function () {
        var white = "        \t";
        if(Colon){
        this.ID = this.ID.substring(this.ID.indexOf("\t") + "\t".length, this.ID.length);
        return this.ID + white + this.Node1 + white + this.Node2 + white + String(this.Length) + white + String(this.Dia) + white + String(this.Rough) + white + String(this.Loss) + white + this.Status + "  ;";
        }
        else {
        this.ID = this.ID.substring(this.ID.indexOf("\t") + "\t".length, this.ID.length);
        return this.ID + white + this.Node1 + white + this.Node2 + white + String(this.Length) + white + String(this.Dia) + white + String(this.Rough) + white + String(this.Loss) + white + this.Status + "   ";
        }
    };
    this.flatten = function () {
        return 5; // AddWhiteSpaceColon([this.ID,this.Node1,this.Node2, this.Length, this.Dia, this.Rough, this.Loss, this.Status],this.Colon)    
    };
    
}

function Coordinate(Node, Xcord, Ycord, Colon) {
    "use strict";
    this.Node = String(Node);
    this.Xcord = parseFloat(Xcord);
    this.Ycord = parseFloat(Ycord);
    this.Colon = Colon;
    
    this.toString = function () {
        var white = "        \t";
        return this.Node + white + String(this.Xcord) + white + String(this.Ycord) + "\n";
    };
    this.flatten = function () {
        return 5; // AddWhiteSpaceColon([this.Node,this.Xcord,this.Ycord],this.Colon);
    };
    
    
}


function DemandSpec(ID, Demand, Pattern, Colon) {
    "use strict";
    this.ID = String(ID);
    this.Demand = parseFloat(Demand);
    this.Pattern = String(Pattern);
    this.Colon = Colon;
        
    this.toString = function () {
        var white = "        \t";
        if (Colon){
        return String(this.ID) + white + String(this.Demand) + white + this.Pattern +  ";" + "\n";
        }
        else{
        return String(this.ID) + white + String(this.Demand) + white + this.Pattern +  " " + "\n";
        }
    };
    this.flatten = function () {

        return 5; // AddWhiteSpaceColon([this.ID,this.Demand,this.Pattern],this.Colon);
    };

}

/* def MakeSpecifiedSumps( junctions,tanks,pipes,coordinates, HHDaily, sDepth, bpDepth,sList,bpList){
    
    #########################################
    #                                       #
    #                                       #
    #some SUMP MAKING CONSTANTS ARE HERE!!! #
    #                                       #
    #########################################

    #account for semicolon usage; if one of the categories doesn't have any entries, use the colon value from others
    jcolon=junctions[0].Colon
    */
    /* if (tanks):
        tcolon=tanks[0].Colon
    else:
        tcolon=jcolon

    pcolon=pipes[0].Colon
    ccolon=coordinates[0].Colon
    
    householdDemand=float(HHDaily)  //was using 600 now use 175*5= #LPD; used to determine how many HH's are clumped at a junction

    // pipe between the water main and the HH
    pipeLengthHH=10 //m avg length between water main and HH's sump, meter or equivalent
    pipeRoughHH=110 //avg roughness factor for existing pipes between water main and HH
    pipeDia=15 //assumed diameter of individual HH connectison 15mm
    lossCoef=8 //assumed minor loss coefficient between main and the HH booster pump (or valve)
    // HH Water Tanks
    //pipeTankLength=1 #m a pipe is used to connect the household to the tank, useful in pump simulation. length 1m
    //pipeTankDia=200 #mm this placeholder pipe is 200mm
    dayPercent=1 //fraction of the day in which the tank is assumed to fill 1=100%
    tankHeight=1 //m of tank height

    //Visual offest
    xoff=5  //these values give the tanks their offest on the map
    yoff=5

    extraTankElev=Depth //m 0 for sump or valve, -4 for booster pump

    //Find nodes with demand and flag them for fixing
    fixlist=[]
    i=0
    while i < len(junctions):
        if junctions[i].Demand != 0: //then there is a demand at this node!
            if junctions[i].ID in (sList+bpList):
                fixlist.append(i)
        i+=1
    //fix list is now a list of 4, 8,14, etc. of ascendking #s to fix.
        
    //FIX (ie modify the junction, add new junctions, pipes and tanks)

    k=0   //counter to track what number to number new tanks, junctions, and pipes
    // newJunctions=[]
    for i in fixlist:   //i is now the indext of things to fix. call the right function!
        
        demand=junctions[i].Demand

        //calculate equivalent HH connection characteristics based on node size
        newSizes=SizeConversion(demand, householdDemand,dayPercent,pipeDia,lossCoef,tankHeight)

        //remove demand
        junctions[i].Demand=0

        //add new node (to a list of things to tack on)
        //newJunctions.append(Junction("JB"+str(k),junctions[i].Elev,0," ",jcolon))

        //add TANK
        if junctions[i].ID in bpList:
            extraTankElev=bpDepth
        else:
            extraTankElev=sDepth
            
        tanks.append(Tank("TB"+str(k),junctions[i].Elev+extraTankElev,0,0,tankHeight,newSizes['newTankDia'],0,tcolon))

        //join with adequate pipes
        pipes.append(Pipe("B"+str(k),junctions[i].ID,tanks[-1].ID,pipeLengthHH,newSizes['newPipeDia'],pipeRoughHH,newSizes['newLossCoeff'],"Open",pcolon))

        //pipes.append(Pipe("B"+str(k),junctions[i].ID,newJunctions[-1].ID,pipeLengthHH,newSizes['newPipeDia'],pipeRoughHH,newSizes['newLossCoeff'],"Open",pcolon))
        //pipes.append(Pipe("Bb"+str(k),newJunctions[-1].ID,tanks[-1].ID,pipeTankLength,pipeTankDia,pipeRoughHH,0,"Open",pcolon))

        //find coordinates of current junction
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
            
        //site new junction and tank
        //coordinates.append(Coordinate(newJunctions[-1].ID,xcurr+xoff, ycurr+yoff,ccolon))
        coordinates.append(Coordinate(tanks[-1].ID,xcurr+xoff,ycurr+yoff,ccolon))

        k+=1 //additions counter

    //tack on new junction nodes
    //junctions+=newJunctions
    return (junctions,tanks,pipes,coordinates)
} */

function RoundBetter(num, number_of_places) {
    "use strict";
    var tenToWhat = Math.pow(10, number_of_places);
    this.awesome = Math.round(num * tenToWhat) / tenToWhat;
}

/*function makeSpecifiedSumps(junctionsIN, tanksIN, pipesIN, coordinatesIN, HHDaily, sDepth, bpDepth, sList, bpList) {
    
    this.junctionsOut = junctionsIN;
    this.tanksOut = tanksIN;
    this.pipesOut = pipesIN;
    this.coordinatesOut = coordinatesIN;
    
    
    var householdDemand = parseFloat(HHDaily);
    var pipeLengthHH=10; //m avg length between water main and HH's sump, meter or equivalent
    var pipeRoughHH=110; //avg roughness factor for existing pipes between water main and HH
    var pipeDia=15; //assumed diameter of individual HH connectison 15mm
    var lossCoef=8; //assumed minor loss coefficient between main and the HH booster pump (or valve)
    var dayPercent=1; //fraction of the day in which the tank is assumed to fill 1=100%
    var tankHeight=1; //m of tank height

    var xoff=5;  //these values give the tanks their offest on the map
    var yoff=5;
    //Find nodes with demand and flag them for fixing
    var fixlist = [];
    var yy = 0;
    while (yy < junctionsIN.length) {
        if (junctionsIN[yy].Demand !== 0) { //then there is a demand at this node!
            if (sList.indexOf(junctionsIN[yy].ID) >= 0 || bpList.indexOf(junctionsIN[yy].ID) >= 0) {
                fixlist.push(yy);
            }
        }
        yy += 1;
    //fix list is now a list of 4, 8,14, etc. of ascendking #s to fix.
    }
    // this.test = fixList;
    // document.getElementById("JUNCTIONS").innerHTML = fixList;
    //FIX (ie modify the junction, add new junctions, pipes and tanks)
    
    var k = 0;   //counter to track what number to number new tanks, junctions, and pipes
    //newJunctions=[]
    var demandForFixing, newSizes, extraTankElev, addedTank, addedPipe, addedCoordinate, xcurr, ycurr, j, lastElementOfTanks;
    
    for (fix in fixlist) {
        
        demandForFixing = junctionsIN[fixlist[fix]].Demand;
        
        newSizes = new SizeConversion(demandForFixing, householdDemand, dayPercent, pipeDia, lossCoef, tankHeight);
        
        junctionsIN[fixlist[fix]].Demand = 0;
        
        
        if (bpList.indexOf(junctionsIN[fixlist[fix]].ID) >= 0){
            extraTankElev = bpDepth;
        }
        
        else{
            extraTankElev = sDepth;
        }
        
        //addedTank = new Tank("TB"+String(k),extraTankElev, 0, 0, tankHeight, newSizes.newTankDia, 0, true);
        addedTank = new Tank("cheese", 5, 0,0,1,10,0,true);
        //tanksIn.push(addedTank);
        // i subtracted parseFloat(junctionsIN[fixlist[fix]].ID)
        // join with adequate pipes 
       //addedPipe = new Pipe("B", 5.9, "life", 10, 10, 10, 10, "Open", true);
       addedPipe = new Pipe ("B"+String(k), junctionsIN[fixlist[fix]].ID, "string", pipeLengthHH, newSizes.newPipeDia, pipeRoughHH, newSizes.newLossCoeff, "Open", true);
       
        pipesIN.push(addedPipe);
        
        //pipes.append(Pipe("B"+str(k),junctions[i].ID,newJunctions[-1].ID,pipeLengthHH,newSizes['newPipeDia'],pipeRoughHH,newSizes['newLossCoeff'],"Open",pcolon))
        //pipes.append(Pipe("Bb"+str(k),newJunctions[-1].ID,tanks[-1].ID,pipeTankLength,pipeTankDia,pipeRoughHH,0,"Open",pcolon))

        //find coordinates of current junctions
        xcurr=0;
        ycurr=0;
        j=0;
        
        while (j< coordinatesIN.length){
            if (coordinatesIN[j].Node == junctionsIN[fixlist[fix]].ID){
                xcurr=coordinatesIN[j].Xcord;
                ycurr=coordinatesIN[j].Ycord;
                j=coordinatesIN.length + 1; //exit
            }
            else{
                j+=1;
            }
        }
        
        //if j==len(coordinates):
        //    print("error, location of current junction ", junctions[i].ID, "not found")
            
        //site new junction and tank
        //coordinates.append(Coordinate(newJunctions[-1].ID,xcurr+xoff, ycurr+yoff,ccolon))
        
        var addedCoordinate = new Coordinate("string",xcurr+xoff,ycurr+yoff,false);
        coordinatesIN.push(addedCoordinate);
        k += 1;
        
    
    }
    
    this.junctionsOut = junctionsIN;
    this.tanksOut = tanksIN;
    this.pipesOut = pipesIN;
    this.coordinatesOut = coordinatesIN;

    
    
} */
function SizeConversion(demand, householdDemand, dayPercent, pipeDia, lossCoef, tankHeight) {

    "use strict";
    this.newPipeDia = 0;
    this.newTankDia = 0;
    this.newLossCoef = 0;
    //Demand in LPS
    //steps for fixing a junction:
        //1 convert demand to an equivalent number or people
        //2 convert people into an equivalent size of pipe and tank and loss coefficient
        //3 round floats
    var ppl, newPipeDia, oldTankDia, newTankDia, newLossCoef, PipeRound, TankRound, LossRound;
    ppl = demand / (householdDemand / 24 / 3600);
    //print("SizeConversion ppl count is ", ppl)
    //step2
    newPipeDia = pipeDia * Math.pow(ppl, 0.3799);
    oldTankDia = Math.pow((dayPercent * householdDemand / 1000 * 4 / 3.1415 / tankHeight), 0.5);
    newTankDia = oldTankDia * Math.pow(ppl, 0.5);
    newLossCoef = lossCoef / Math.pow(ppl, 0.4804);

    //round values to 2 decimal places
    PipeRound = new RoundBetter(newPipeDia, 2);
    newPipeDia = PipeRound.awesome;
    
    TankRound = new RoundBetter(newTankDia, 3);
    newTankDia = TankRound.awesome;

    LossRound = new RoundBetter(newLossCoef, 2);
    newLossCoef = LossRound.awesome;
    
    this.newPipeDia = newPipeDia;
    this.newTankDia = newTankDia;
    this.newLossCoef = newLossCoef;
}

function isolate(non_iso){
    "use strict";
    this.isolated = "did not function";
    
    var toReturn = "";
    for (var q = 0; q < non_iso.length; q++){
        if (non_iso.substring(q,q+1) == "a" || non_iso.substring(q,q+1) == "b" || non_iso.substring(q,q+1) == "c" || non_iso.substring(q,q+1) == "d" || non_iso.substring(q,q+1) == "e" || non_iso.substring(q,q+1) == "f" || non_iso.substring(q,q+1) == "g" || non_iso.substring(q,q+1) == "h" || non_iso.substring(q,q+1) == "i" || non_iso.substring(q,q+1) == "j" || non_iso.substring(q,q+1) == "k" || non_iso.substring(q,q+1) == "l" || non_iso.substring(q,q+1) == "m" || non_iso.substring(q,q+1) == "n" || non_iso.substring(q,q+1) == "o" || non_iso.substring(q,q+1) == "p" || non_iso.substring(q,q+1) == "q" || non_iso.substring(q,q+1) == "r" || non_iso.substring(q,q+1) == "s" || non_iso.substring(q,q+1) == "t" || non_iso.substring(q,q+1) == "u" || non_iso.substring(q,q+1) == "v" || non_iso.substring(q,q+1) == "w" || non_iso.substring(q,q+1) == "x" || non_iso.substring(q,q+1) == "y" || non_iso.substring(q,q+1) == "z" || non_iso.substring(q,q+1) == "1" || non_iso.substring(q,q+1) == "2" || non_iso.substring(q,q+1) == "3" || non_iso.substring(q,q+1) == "4" || non_iso.substring(q,q+1) == "5" || non_iso.substring(q,q+1) == "6" || non_iso.substring(q,q+1) == "7" || non_iso.substring(q,q+1) == "8" || non_iso.substring(q,q+1) == "9" || non_iso.substring(q,q+1) == "0" || non_iso.substring(q,q+1) == "A" || non_iso.substring(q,q+1) == "B" || non_iso.substring(q,q+1) == "C" || non_iso.substring(q,q+1) == "D" || non_iso.substring(q,q+1) == "E" || non_iso.substring(q,q+1) == "F" || non_iso.substring(q,q+1) == "G" || non_iso.substring(q,q+1) == "H" || non_iso.substring(q,q+1) == "I" || non_iso.substring(q,q+1) == "J" || non_iso.substring(q,q+1) == "K" || non_iso.substring(q,q+1) == "L" || non_iso.substring(q,q+1) == "M" || non_iso.substring(q,q+1) == "N" || non_iso.substring(q,q+1) == "O" || non_iso.substring(q,q+1) == "P" || non_iso.substring(q,q+1) == "Q" || non_iso.substring(q,q+1) == "R" || non_iso.substring(q,q+1) == "S" || non_iso.substring(q,q+1) == "T" || non_iso.substring(q,q+1) == "U" || non_iso.substring(q,q+1) == "V" || non_iso.substring(q,q+1) == "W" || non_iso.substring(q,q+1) == "X" || non_iso.substring(q,q+1) == "Y" || non_iso.substring(q,q+1) == "Z" ){
            toReturn += non_iso.substring(q,q+1);
        }
    }
    
    this.isolated = toReturn;
}
