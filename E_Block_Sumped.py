

#Imports
    
 from EPANETClasses4 import * #get all classes 5from EPANETClasses file
 from EPANETFunctions5 import * #get all functions from EPANETFunctions file (technically classes are already imported via functions file... oh well!
        
#READ

filename="E_Block_Paterned.inp"

data=ReadEPANET(filename)

#divide up data (of type dictionary) into its components
fullcontentList=data['FullContent']
junctions=data['Junctions']
tanks=data['Tanks']
pipes=data['Pipes']
coordinates=data['Coordinates']
demands=data['Demands']

#print('last junction',junctions[-1])

#WRITE Parsed Original (for debugging)
#WriteEPANET(filename[:-4]+"_parsed.inp", junctions, tanks, pipes, coordinates, demands, fullcontentList)

#COMBINE Demands into Junctions

jIndex=[]
for j in junctions:
    jIndex.append(j.ID)

#for every entry in the demands list, pop it, and =+ the demand of that junction

for d in demands:
    ji=jIndex.index(d.ID)
    junctions[ji].Demand+=d.Demand

demands=[] #now erase this section

#WRITE simple demand version
#WriteEPANET(filename[:-4]+"_demand.inp", junctions, tanks, pipes, coordinates, demands, fullcontentList)

#ROUND KEY VALUES
[junctions,tanks,pipes]=RoundKeyValues(junctions,tanks,pipes)

#ID zones to give BPs
KList=[]
LList=[]

for j in junctions:
    if j.ID[:2]!="JP":
        LList.append(j.ID) #if not JP -> L-block -> valve
    else:
        KList.append(j.ID) #else K-block -> no pumps but OHT
            


#INSERT SUMPS
    #for constants see MakeSumps Function
[junctionsR,tanksR,pipesR,coordinatesR]=MakeSpecifiedSumps(junctions,tanks,pipes,coordinates,1100,0,0,KList,LList)

# junctions,tanks,pipes,coordinates, HHDaily, sDepth, bpDepth,sList,bpList):
#[junctionsR2,tanksR2,pipesR2,coordinatesR2]=MakeSpecifiedSumps(800,-4,junctionsR,tanksR,pipesR,coordinatesR,bpList)

#WRITE sumped version demand version
WriteEPANET(filename[:-4]+"NBP.inp", junctionsR, tanksR, pipesR, coordinatesR, demands, fullcontentList)

#WriteEPANET(filename[:-4]+"_SomeBPs.inp", junctionsR2, tanksR2, pipesR2, coordinatesR2, demands, fullcontentList)
print('DONE EXECUTION')
