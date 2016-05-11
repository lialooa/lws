



def landGen(squareLimit,squareSize):    #generate the land pivot points

    if squareLimit<1: squareLimit=1     #square limit is a min square size when generator stop generate squares

    pivots=[[0,0,squareSize]]             #first pivot has null values
    os=squareSize//4                    #max value of oscillation. value taken by experimental way

    a=-1
    while squareSize>=squareLimit:          #min size of square side
        if a<0:                             #module that make matrix of apex for futher processing
            apexMatrix=pivots[:]
        elif a==0:
            apexMatrix=pivots[(4**a):]
        else:
            apexMatrix=pivots[(4**a)+1:]

        squareSideHL=squareSize//2

        for i in apexMatrix:                    # Main module of calculating pivot matrix

            osci=random.randrange(-os,os)       # every apex has his own oscillation
            osci1=random.randrange(-os,os)      #
            osci2=random.randrange(-os,os)      #
            osci3=random.randrange(-os,os)      #

            pivots.append([i[0]-squareSideHL+osci, i[1]-squareSideHL+osci, squareSideHL*2+osci])
            pivots.append([i[0]+squareSideHL+osci1, i[1]-squareSideHL+osci1, squareSideHL*2+osci1])
            pivots.append([i[0]+squareSideHL+osci2, i[1]+squareSideHL+osci2, squareSideHL*2+osci2])
            pivots.append([i[0]-squareSideHL+osci3, i[1]+squareSideHL+osci3, squareSideHL*2+osci3])

        squareSize=squareSideHL
        a+=1

    return pivots

def ridgeGen(basicRidgePivotsMatrix):   #ridge generator

    def osci(x,l):
        a=random.randrange(1,x//l)*random.choice([-1,1])
        return a

    #at first step we get start points from actual pivots matrix and decide whether to be ridge here

    ridgeStep=5             # step of ridge peaks. there is will be the next peak.
    minMassifNumber=3       # minimum number of massif in the ridge.
    oscilationLimit=4       # if oscilation Limit=4 then limit is 1/4 of square lenght

    if ridgeStep>9: ridgeStep=9 #it can't be more then max massif size!

    minRidgeLenght=ridgeStep*minMassifNumber
    landTooSmall=0
    while 1 or landTooSmall<10:
        while 1:    #take start and finish pivots
            preStartPivot=random.choice(basicRidgePivotsMatrix)
            preFinishPivot=random.choice(basicRidgePivotsMatrix)
            if preStartPivot!=preFinishPivot:
                startFinishPivots=[preStartPivot,preFinishPivot]
                break
        startFinishPivots=[[a+osci(pivot[2],oscilationLimit) for a in pivot] for pivot in startFinishPivots]

        ridgeLenghtByX=abs(startFinishPivots[0][0]-startFinishPivots[1][0])
        ridgeLenghtByY=abs(startFinishPivots[0][1]-startFinishPivots[1][1])

        if ridgeLenghtByX>=minRidgeLenght or ridgeLenghtByY>=minRidgeLenght:
            break
        else:
            landTooSmall+=1

    if landTooSmall==10:     #if can't create ridge start and finish point 10 times then land too small for ridge
        print "land too small", ridgeLenghtByX, ridgeLenghtByY, minRidgeLenght

    #distance between start and finish point must be aliquot to ridge step
    #we need to move these point to achive aliquoting
    coin=random.choice([0,1]) #compress or move apart these points

    points=[[startFinishPivots[0][0],startFinishPivots[1][0]],[startFinishPivots[0][1],startFinishPivots[1][1]]]

    side=0 #0 - move left point, 1 - move right point
    for cell in points:
        while (cell[0]-cell[1])%ridgeStep!=0:
            if coin==1:  #move apart by one point
                if side==0:
                    cell[0]-=1
                    side=1
                else:
                    cell[1]+=1
                    side=0
            else:       #compress by one point
                if side==0:
                    cell[0]+=1
                    side=1
                else:
                    cell[1]-=1
                    side=0

    startFinishPivots=[[points[0][0],points[1][0]],[points[0][1],points[1][1]]]

    #at second step we resolve dijkstra algorithm

    infinityNumber=10000

    dijNodeMatrixLenght=abs(startFinishPivots[0][0]-startFinishPivots[1][0])/ridgeStep  #make matrix shorter
    dijNodeMatrixHeight=abs(startFinishPivots[0][1]-startFinishPivots[1][1])/ridgeStep  #

    dijNodeMatrix=[]                                            #node matrix module
    prePre=[infinityNumber,"a","b"]                             #
    preDijNodeMatrix=[0]*(dijNodeMatrixLenght+1)                    #
    for i in range((dijNodeMatrixHeight+1)):                        #
        dijNodeMatrix.append(preDijNodeMatrix[:])                   #
    dijNodeMatrix=[[prePre[:] for x in row] for row in dijNodeMatrix]   #


    dijNodeMatrix[0][0][0]=0                                    #first point cost is null

    i=0
    j=0
    lastRow=0
    startCost=1     #basic min cost
    finishCost=9    #basic max cost

    for row in dijNodeMatrix:   #start calculate costs
        for cell in row:
            if i==0 and j==0: pass  #pass basic cell
            else:
                if i!=0:
                    newValue=lastCell[0]+random.randrange(startCost,finishCost) #arc cost is randomize!
                    if newValue<cell[0]:    #horizontal arcs part
                        cell[0]=newValue
                        cell[1]=i-1
                        cell[2]=j

                if lastRow==0: pass #calculating of vertical arc start from second step
                else:
                    newValue=lastRow[i][0]+random.randrange(startCost,finishCost)
                    if newValue<cell[0]:    #vertical arcs part
                        cell[0]=newValue
                        cell[1]=i
                        cell[2]=j-1

            lastCell=cell
            i=i+1

        lastRow=row
        i=0
        j=j+1
    #print dijNodeMatrixLenght,dijNodeMatrixLenght
    #print dijNodeMatrix

    #at third step we make route matrix
    routeMatrix=[[dijNodeMatrixLenght,dijNodeMatrixHeight]]             #final route point
    lastRoutePoint=[dijNodeMatrix[-1][-1][1],dijNodeMatrix[-1][-1][2]]  #first calculated route point
    routeMatrix.append(lastRoutePoint)

    while lastRoutePoint!=[0,0]:
        x=dijNodeMatrix[lastRoutePoint[1]][lastRoutePoint[0]][1]
        y=dijNodeMatrix[lastRoutePoint[1]][lastRoutePoint[0]][2]
        routePoint=[x,y]
        routeMatrix.append(routePoint)
        lastRoutePoint=routePoint

    routeMatrix.reverse()
    #print routeMatrix

    #at forth step we make ridgePivotMatrix

    ridgePivotsMatrix=[]

    dirCorrX=1
    dirCorrY=1
    if startFinishPivots[1][0]-startFinishPivots[0][0]<0: dirCorrX=-1
    if startFinishPivots[1][1]-startFinishPivots[0][1]<0: dirCorrY=-1

    i=0
    for point in routeMatrix:
        x=startFinishPivots[0][0]+(point[0])*dirCorrX*ridgeStep     #calculate and restore value of coord
        y=startFinishPivots[0][1]+(point[1])*dirCorrY*ridgeStep     #

        ridgePivotsMatrix.append([x,y])
        i+=1

    #now we have a ridge route and we can make a ridge itself

    #on every ridge route point (aka peak) we place the massif. ridge is a block of massif moving on route
    #we need three matrix: snow peak coord, mountain coord and hills coord

    hillsMatrix=[]
    mountainMatrix=[]
    snowPeakMatrix=[]

    for pivot in ridgePivotsMatrix:
        massif=massifMaker(pivot)
        hillsMatrix+=massif[0]
        mountainMatrix+=massif[1]
        snowPeakMatrix+=massif[2]


    landscapeMaker(worldLandscape,ridgePivotsMatrix,worldSize)
    #print worldHeight
    #print hillsMatrix
    return [hillsMatrix,mountainMatrix,snowPeakMatrix]

def massifGen(landPivotsMatrix): #create some massifs on the land using massif maker

    coord=[]
    hillsMatrix=[]
    mountainMatrix=[]
    snowPeakMatrix=[]
    massifPivotsMatrix=[]
    osci=[0,0]

    massifMass=10    #number of massif on a map. 1 - massif in every possible tile, 100 - very rarely massif

    for pivot in landPivotsMatrix:

        if pivot[2]<9:  #can't build massif in square less then massif size
            pass
        else:           #else we need decide can we build massif in these square or not
            decision=random.randrange(massifMass)
            if decision==1:      #yes we can build massif

                possibleOsci=pivot[2]-9                                             #oscilator
                if possibleOsci>0:                                                  #
                    for i in osci:
                        i=(random.randrange(0,possibleOsci))*random.choice([-1,1])   #

                x=pivot[0]+osci[0]      #coord of massif center
                y=pivot[1]+osci[1]      #
                osci=[0,0]

                massifPivotsMatrix.append([x,y])

                massif=massifMaker([x,y])
                hillsMatrix+=massif[0]
                mountainMatrix+=massif[1]
                snowPeakMatrix+=massif[2]


    landscapeMaker(worldLandscape,massifPivotsMatrix,worldSize)

    return [hillsMatrix,mountainMatrix,snowPeakMatrix]

def massifMaker(pivotMatrix):       #create massif matrix

    def mountainType(elementCase):  #function of mountain type choosing
        coin=random.randrange(100)
        if coin<=70: a=elementCase[0]
        else: a=elementCase[1]
        return a

    #massif.
    #massif consisf four elements: snow peak, mountain, hill, plain
    # in center of massif placed highest elements. on an edge lowest
    # we will get a highest massif element and make it basic for other massif elements


    massifMatrixSize=9
    massifMatrix=[]
    preMassifMatrix=[0]*massifMatrixSize
    for i in range(9):
        massifMatrix.append(preMassifMatrix[:])

    elementsCaseMatrix=[[[1,0],[1,0],[0,1],[0,0]],
                        [[2,1],[1,0],[0,1],[0,0]],
                        [[3,2],[2,1],[1,0],[0,1]]]
    maxElement=random.randrange(3)

    startX=massifMatrixSize//2
    startY=startX

    massifMatrix[startY][startX]=maxElement   #center of massif is always max element

    i=3                 #actual matrix size
    step=0

    while i<=massifMatrixSize:

        elementCase=elementsCaseMatrix[maxElement][step]     #make case of elements variations

        x=startX-i//2    #actual x
        y=startY-i//2    #actual y

        for j in range(i):
            massifMatrix[y][x+j]=mountainType(elementCase)          #top
            massifMatrix[y+i-1][x+j]=mountainType(elementCase)      #bottom

        for j in range(1,i-1):
            massifMatrix[y+j][x]=mountainType(elementCase)          #left
            massifMatrix[y+j][x+i-1]=mountainType(elementCase)      #right

        i=i+2
        step=step+1

    hillsMatrix=[]
    mountainMatrix=[]
    snowPeakMatrix=[]

    i=j=0
    for row in massifMatrix:
        for mountainType in row:
            if mountainType!=0:
                coord1=pivotMatrix[0]-4+i
                coord2=pivotMatrix[1]-4+j
                coord=[coord1,coord2]

                if mountainType==1:
                    hillsMatrix.append(coord)
                elif mountainType==2:
                    mountainMatrix.append(coord)
                elif mountainType==3:
                    snowPeakMatrix.append(coord)
            i+=1
        j+=1
        i=0

    return [hillsMatrix,mountainMatrix,snowPeakMatrix]

def landscapeMaker(HeightMatrix, PeakMatrix, worldSize):    #create landscape based on Peaks and accessory height pyramid

    #def whiteNoize(amplitude,rawMatrix):
     #   newMatrix=[[cell+random.randint(0,amplitude) for cell in row] for row in rawMatrix]
      #  return newMatrix

    #at first we need make an accessory height matrix
    accMatrix=[]
    accMatrixLenMin=3

    accMatrixLenMax=worldSize[1]-1

    preAccMatrix=[0]*accMatrixLenMax
    for i in range(accMatrixLenMax):
        accMatrix.append(preAccMatrix[:])

    #the we need calculate cell value of accessory matrix. we use it in calculating landscape
    height=100
    startX=accMatrixLenMax//2
    startY=startX

    i=accMatrixLenMin-1
    accMatrix[startY][startX]=height
    #print accMatrixLenMax, startX, startY
    while i<=accMatrixLenMax:
        height=int(height/1.1)
        #if height<1: height=1
        #print height
        #height-=3
        x=startX-i//2
        y=startY-i//2
        #print i, x,y

        for j in range(i+1):                  #this block fill square by heights. in next step this square arise in lenght
            accMatrix[y][x+j]=height        # top row
            accMatrix[y+i][x+j]=height      # bottom row
        for j in range(i-1):                            # intermediate part
            accMatrix[y+j+1][x]=height      # left side
            accMatrix[y+j+1][x+i]=height    # right

        i=i+2


    #print accMatrix[4]
    #in next step we need calculate height map using accMatrix as a template and mountain peaks matrix as a start point

    #osci can help us make peaks different in height
    osciMax=2  #percentage of height

    if osciMax<2: osci=2 #it can't be less then 2 because min osci is 1.

    amplitude=1

    for Peak in PeakMatrix:

        featuredAccMatrix=[[cell+random.randint(0,amplitude) for cell in row] for row in accMatrix]

        startX=Peak[0]
        startY=Peak[1]

        osci=random.randrange(1,osciMax)    #peak height oscilation. every peak has own height bonus

        for i in range(accMatrixLenMax):
            x=startX-accMatrixLenMax//2+i
            for j in range(accMatrixLenMax):
                y=startY-accMatrixLenMax//2+j
                try:
                    HeightMatrix[y][x]=max([HeightMatrix[y][x],featuredAccMatrix[j][i]])#+osci    #final height!
                    #print worldHeightMatrix[x][y]
                except:
                    #print x,y, i, j
                    pass

def lakeEraser(theLandPivotsMatrix, worldSize):     #erase any lake

    def floodFill(x, y, oldColor, newColor, lakeMatrix):
        lookAround=[[-1,0],[0,-1],[1,0],[0,1]]
        theStack = [ (x, y) ]
        maxX=len(lakeMatrix[0])-1
        maxY=len(lakeMatrix)-1
        while len(theStack) > 0:
            x, y = theStack.pop()

            if lakeMatrix[y][x] != oldColor:
                continue
            lakeMatrix[y][x] = newColor

            for cell in lookAround:
                pX=x+cell[0]
                pY=y+cell[1]
                if pX<0 or pY<0 or pX>maxX or pY>maxY: pass
                else:
                    #print pX,pY
                    theStack.append( (pX , pY) )

        return lakeMatrix

    #  1) we need create the lake matrix bidder then mainland matrix in 2 points
    lakeMatrixSizeX=worldSize[0]
    lakeMatrixSizeY=worldSize[1]
    makeItBigger=2

    lakeMatrix=[]
    preLakeMatrix=[0]*(lakeMatrixSizeX+makeItBigger)
    for i in range((lakeMatrixSizeY+makeItBigger)):
        lakeMatrix.append(preLakeMatrix[:])    #lake matrix created

    # 2) we need paint lands matrix in lake matrix so that the borders of lake must be free

    startX=lakeMatrixSizeX/2
    startY=lakeMatrixSizeY/2

    for pivot in theLandPivotsMatrix:
        x=pivot[0]-pivot[2]//2+1
        y=pivot[1]-pivot[2]//2+1
        r=pivot[2]

        for l in range(y,y+r):
            for k in range(x,x+r):
                try:
                    lakeMatrix[l][k]=2
                except:
                    print k,l
                    pass


    # 3)  we need fill lake with water. we start with 0,0 coord which is not the land in any way

    if lakeMatrix[0][0]!=0: print "can't floodfill lakematrix!", lakeMatrix[0][0]
    lakeMatrix=floodFill(0, 0, 0, 1, lakeMatrix)

    #we have lake matrix with three type of number: 1 is a water, 2 is a land and 0 is a lake!
    #to destroy these lake tiles we need add them to any land matrix of actual mainland matrix. It make them land too.
    # we create new matrix that land body matrix

    theLandMatrix=[]
    y=0
    for row in lakeMatrix:
        x=0
        for cell in row:
            if cell!=1:
                theLandMatrix.append([x,y])
            x+=1
        y+=1

    return theLandMatrix

def riverGen(worldLandscapeMatrix,springPivot,worldSize):
    def worldSides(dir):
        if dir==[0,-1]: a='S'
        elif dir==[1,0]: a='E'
        elif dir==[0,1]: a='N'
        elif dir==[-1,0]: a='W'
        return a

    # river generator based on some ideas.
    # a) river can not flow up. we need world landscape matrix for this.
    # b) river generator use some rules for make a river. we need it for more naturally looking river
    # c) river looking for a shore and if it found then river flow to the shore and finished his way. we need it for more naturally looking river

    theRiver=[springPivot]    #first river tile is a spring tile

    directions=[[0,-1],[1,0],[0,1],[-1,0]]
    directionsDict={'N':0,'E':0,'S':0,'W':0}    #first rule set. North=0, East=0 and so far.
    forbidDirectionDict={'N':'S','E':'W','S':'N','W':'E'}

    oldWorldSide='A'                            #first rule set.
    forbidDirections=['A','A']

    actualDirectionsDict=directionsDict.copy()         #first rule set.

    maxSteps=3
    minSteps=1
    riverStep=1
    if minSteps>maxSteps: minSteps=maxSteps

    iii=0
    riverFlowStop=0
    while riverFlowStop==0:

        #the rules: 1) river cant'f flow in the same direction more then maxSteps times.
        #the rules: 2) river can't flow in forbid directions (there are the same directions when it flow last time)

        actualRiverTile=theRiver[-1]
        actualHeight=worldLandscape[actualRiverTile[1]][actualRiverTile[0]]

        directionsPool=directions[:]
        step=4

        while directionsPool:   #try pick up directions and check if it not higher then last point
            #print "step", step
            direction=random.choice(range(step))        #!!!take new direction!!!
            newDirection=directionsPool[direction]      #

            #print "direction",direction, "directionsPool",directionsPool

            worldSide=worldSides(newDirection)      # first rule set

            if actualDirectionsDict[worldSide]>=maxSteps: #we reach maxSteps limit in actual direction (1-th rule set)
                directionsPool.remove(newDirection)
                step-=1
            else:
                if worldSide in forbidDirections:   #2-th rule set

                    directionsPool.remove(newDirection)
                    step-=1

                else:

                    nextRiverTile=[actualRiverTile[0]+newDirection[0],actualRiverTile[1]+newDirection[1]]
                    nextHeight=worldLandscape[nextRiverTile[1]][nextRiverTile[0]]

                    if nextRiverTile not in theLand:       #first river end - river reach sea
                        riverFlowStop=1
                        break

                    for river in theRivers:             #second river end - river reach another river
                        if nextRiverTile in river:
                            riverFlowStop=1
                            break

                    if nextHeight>actualHeight:         #new height higher than actual height (0-th rule set)
                        directionsPool.remove(newDirection)
                        #print directionsPool
                        step-=1
                    else:
                        theRiver.append(nextRiverTile)
                        if worldSide==oldWorldSide:         #1-th rule set
                            actualDirectionsDict[worldSide]+=1
                        else:
                            actualDirectionsDict=directionsDict.copy()
                            oldWorldSide=worldSide
                            #print "actualDirectionsDict droped", actualDirectionsDict, '/', directionsDict
                        forbidDirections=forbidDirections[1:]   # 2-th rule set
                        forbidDirections.append(forbidDirectionDict[worldSide])
                        #print forbidDirections

                        break

        else:
            print "river can't flow futher! Direction pool is over."
            riverFlowStop=1

        if riverFlowStop==1: break
        iii+=1
    #print "river done in", iii, 'steps'

        #there are can be some river ends.
        #first is a (sea) shore. when the river come to shore it an end.
        #second is an another river. in this case actual river became inflow. (we need shuffle river pivots for this reason!)
        #third case is a river can't flow in any directions. that mean we need make a lake.

        # first river end


    return theRiver

def tilePainter(objectType,objectMatrix,worldMapMatrix):
    pass
    object={'land':200,
            'mountain':300,
            'hill':330,
            'snowPeak':390,
            'forest':400,
            'river':150}

    tileType=object[objectType]

    for cell in objectMatrix:
        try:
            worldMap[cell[1]][cell[0]]=tileType
        except:
            #print "x,y",cell[0], cell[1]
            pass

def forestGen(theLandMatrix,theRivers,theRidge,theMassives):

    # At first we create matrix content all busy tiles by another landscape elements, Forest can't be placed there
    busyTilesMatrix=[]
    for cell in theRidge:       #we can't place forest in mountain (ridge)
        for point in cell:
            busyTilesMatrix.append(point)
    for cell in theMassives:    #we can't place forest in mountain (massives)
        for point in cell:
            busyTilesMatrix.append(point)
    for cell in theRivers:      #we can't place forest in river
        for point in cell:
            busyTilesMatrix.append(point)

    #Then we create a forests. Forest is a simple square placed on a land. It is not placed at cell with river or any rock.

    theForests=[]
    howMuchOfForests=20     #this is var is a percent of whole land! 20 is the forest cover ~20% of the land!
    forestBlockSizeMax=4
    numberOfForestsBlocks=(len(theLandMatrix)/100*howMuchOfForests)/(forestBlockSizeMax)

    usedForestBlockCenters=[]
    forestBlockNumber=0
    while forestBlockNumber<=numberOfForestsBlocks:

        forestBlockCenter=random.choice(theLandMatrix)      #get posible forest point

        if forestBlockCenter not in usedForestBlockCenters: #did we use this point yet?

            forestBlockSize=random.randint(1,forestBlockSizeMax)
            forestBlockStartX=forestBlockCenter[0]-forestBlockSize/2
            forestBlockStarty=forestBlockCenter[1]+forestBlockSize/2

            for i in range(forestBlockSize):
                for j in range(forestBlockSize):
                    x=forestBlockStartX+i
                    y=forestBlockStarty+j
                    forestTile=[x,y]

                    if forestTile in theLandMatrix:     #forest tile IS in the land, not the sea
                        #for busyTiles in busyTilesMatrix:
                        if forestTile not in busyTilesMatrix: #tile is free from other landscape elements
                            theForests.append(forestTile)

            usedForestBlockCenters.append(forestBlockCenter)
            forestBlockNumber+=1

    return theForests





#------------------------------- MAIN ---------------------------------------------




# 1) we create world map matrix

#world size
worldHeight=100
worldWidth=worldHeight*2
worldSize=[worldWidth,worldHeight]

worldMap=[]
worldLandscape=[]

preWorldMap=[100]*worldWidth
preWorldLandscape=[0]*worldWidth

for i in range(worldHeight):
    worldMap.append(preWorldMap[:])
    worldLandscape.append(preWorldLandscape[:])

# 2) next we fill the world with a land.

#the Land consist from two main variable: the start pivot point and the land body

#squareSize=20               #variable which define size of the Land
squareSize=worldHeight/4               #variable which define size of the Land


nakedLandPivots=landGen(0,squareSize)     #basic land pivot points is not related to the world coordinates.

#correction of basic land pivots point for relate them to the world coord.
startX=worldWidth/2
startY=worldHeight/2
theLandPivots=[]
for i in range(len(nakedLandPivots)):
    x=nakedLandPivots[i][0]+startX
    y=nakedLandPivots[i][1]+startY
    r=nakedLandPivots[i][2]
    theLandPivots.append([x,y,r])


theLand=lakeEraser(theLandPivots,worldSize)     #this function erase a lakes and make the land body from basic land pivots

# 3) at next step we need create a mountain. it consist of two steps: creating of the ridge and creating of the massives
#at same time we need create landscape matrix

# 3.1) creating of the ridge. the land can consist only one ridge at time!

basicRidgePivots=theLandPivots[1:5]

theRidge=ridgeGen(basicRidgePivots)

# 3.2) creating the massives. the land can consist of some massif.

theMassives=massifGen(theLandPivots)

# 4) Rivers.

# 4.1 Rivers start points generation (aka Springs). Springs can be in a hills only.
# we need make one hills list and grab some point from it.

possibleSpringsPivots=theRidge[0]+theMassives[0]

springsNumber=5
springPivots=[]

for i in range(springsNumber):
    a=random.choice(possibleSpringsPivots)
    if a not in springPivots:
        springPivots.append(a)

theRivers=[]
for springPivot in springPivots:
    river=riverGen(worldLandscape,springPivot,worldSize)
    theRivers.append(river)

theForests=forestGen(theLand,theRivers,theRidge,theMassives)

worldResources=resourcesGen(worldLandscape)

forestsMap=[]

# LAST STEP we need "paint" all this matrix in the world map

tilesVariant=1

if tilesVariant==0:

    tilePainter('land',theLand,worldMap)        # paint the land

    i=0
    while i<3:
        #hill/mountain/snowpeak
        matrix=theRidge[i]                      #paint the ridge
        if i==0:
            tilePainter('hill',matrix,worldMap)
        elif i==1:
            tilePainter('mountain',matrix,worldMap)
        elif i==2:
            tilePainter('snowPeak',matrix,worldMap)
        i+=1

    i=0
    while i<3:
        #hill/mountain/snowpeak
        massif=theMassives[i]                   #paint the massives
        if i==0:
            tilePainter('hill',massif,worldMap)
        elif i==1:
            tilePainter('mountain',massif,worldMap)
        elif i==2:
            tilePainter('snowPeak',massif,worldMap)
        i+=1

    for river in theRivers:                     #paint the rivers
        tilePainter('river',river,worldMap)

    tilePainter('forest',theForests,worldMap)   #paint the forests

elif tilesVariant==1:
    for land in theLand:
        worldMap[land[1]][land[0]]=worldResources[land[1]][land[0]]['landscape vizual type']

        if worldResources[land[1]][land[0]].get('forest vizual type')!=None:
            forestsMap.append([land[0],land[1],worldResources[land[1]][land[0]]['forest vizual type']])
