import pygame, sys, pickle
from pygame import *

from worldGens import *
#from diamondSquareGenerator import *

class InGameCamera():
    def __init__(self,startX,startY, winWidth, winHeight, worldWidth, worldHeight, graficPath, graficPack):
        self.worldWidth=worldWidth
        self.worldHeight=worldHeight

        self.tileSize=32
        self.winWidth=winWidth
        self.winHeight=winHeight

        self.graficPath=graficPath
        self.graficPack=graficPack

        #how much tiles we can take from w_vizualType table
        self.cameraWidth=winWidth/self.tileSize
        self.cameraHeight=winHeight/self.tileSize
        if self.cameraHeight%self.tileSize!=0: self.cameraHeight+=1  #no black line at bottom

        #calculating position depend on camera center
        self.cameraTopX=startX-(self.cameraWidth/2)
        self.cameraTopY=startY-(self.cameraHeight/2)
        self.cameraBottomX=self.cameraTopX+self.cameraWidth
        self.cameraBottomY=self.cameraTopY+self.cameraHeight

        self.actualPointX=self.cameraTopX
        self.actualPointY=self.cameraTopY

        self.limitsCheck()
        self.loadTileImages(graficPack,graficPath)

    def limitsCheck(self):
        w='WORLD IS OVER'
        #out of window checking
        if self.cameraTopX<0:
            self.cameraTopX=0
            self.actualPointX=0
            print w+' in left!'
        if self.cameraTopY<0:
            self.cameraTopY=0
            self.actualPointY=0
            print w+' in top!'
        if self.cameraBottomX>=self.winWidth:
            self.cameraBottomX=self.winWidth
            self.cameraTopX-=1
            self.actualPointX-=1
            print w+' in right! cameraBottomX=',cameraBottomX
        if self.cameraBottomY>=self.winHeight:
            self.cameraBottomY=self.winHeight
            self.cameraTopY-=1
            self.actualPointY-=1
            print w+' in bottom! cameraBottomY', cameraBottomX

    def loadTileImages(self,tilePack,directoryPath):
        self.tileImages={}
        for cell in tilePack:
            self.tileImages[str(cell)]=image.load(directoryPath+str(cell)+'.bmp')

    def draw(self,direction,worldMapLandscape,worldMapForest):
        if direction==1:    #move top
            self.cameraTopY-=1
            self.actualPointY-=1
        elif direction==2:  #move right
            self.cameraTopX+=1
            self.actualPointX+=1
        elif direction==3:  #move bottom
            self.cameraTopY+=1
            self.actualPointY+=1
        elif direction==4:   #move left
            self.cameraTopX-=1
            self.actualPointX-=1

        elif direction==5:   #move top+right
            self.cameraTopY-=1
            self.actualPointY-=1
            self.cameraTopX+=1
            self.actualPointX+=1
        elif direction==6:   #bottom+right
            self.cameraTopY+=1
            self.actualPointY+=1
            self.cameraTopX+=1
            self.actualPointX+=1
        elif direction==7:  #bottom+left
            self.cameraTopY+=1
            self.actualPointY+=1
            self.cameraTopX-=1
            self.actualPointX-=1
        elif direction==8:  #top+left
            self.cameraTopY-=1
            self.actualPointY-=1
            self.cameraTopX-=1
            self.actualPointX-=1
        else: pass

        self.limitsCheck()

        self.cameraBottomX=self.cameraTopX+self.cameraWidth
        self.cameraBottomY=self.cameraTopY+self.cameraHeight

        #draw tile images into surfaces
        drawX=drawY=0
        i1=j1=0
        for i in range(self.cameraTopX,self.cameraBottomX):
            for j in range(self.cameraTopY, self.cameraBottomY):
                #calculating start drawing position
                drawX=i1*self.tileSize
                drawY=j1*self.tileSize

                #draw the land
                tile=self.tileImages[str(worldMapLandscape[j][i])]
                worldMapLandscapeSurface.blit(tile,(drawX,drawY))

                #draw the forests

                tile=self.tileImages[str(worldMapForest[j][i])]
                worldMapForestsSurface.blit(tile,(drawX,drawY))

                j1+=1
            i1+=1
            j1=0

class InGameInterface():
    def __init__(self, winWidth, winHeight,interfaceWidth):
        self.winWidth=winWidth
        self.winHeight=winHeight

        self.rightPanelWidth=interfaceWidth

        self.fontColor=(255,255,255)
        self.fontSize=12
        self.textLineSpacing=15

        self.textPositionStartX=10   #relatively right panel start X/Y
        self.textPositionStartY=10

        self.fontObject=pygame.font.Font('freesansbold.ttf', self.fontSize)

    def showInterface(self):
        #interface panel

        self.rightPanelStartX=self.winWidth-self.rightPanelWidth
        self.rightPanelStartY=0

        pygame.draw.rect(basicSurface, (170,170,170), (self.rightPanelStartX, self.rightPanelStartY, self.rightPanelWidth, self.winHeight))

    def showText(self,sendedText):
        #show text

        sendedTextKeys=sendedText.keys()
        i=0
        for key in sendedTextKeys:
            i+=1
            self.finalText=key+' = '+str(sendedText[key])
            self.textSurfaceObject = self.fontObject.render(self.finalText, True, self.fontColor)
            self.textRectObject = self.textSurfaceObject.get_rect()
            self.textPositionStartY=i*self.textLineSpacing
            self.textRectObject.topleft = (self.rightPanelStartX+self.textPositionStartX*2, self.rightPanelStartY+self.textPositionStartY)

            basicSurface.blit(self.textSurfaceObject, self.textRectObject)

class LoadedGame():
    def __init__(self,fileName):

        try:
            self.loadGameFile=open(fileName,'r')
        except:
            print 'file ',fileName,' not found!'

        self.loadGame=pickle.load(self.loadGameFile)

        self.theLand=self.loadGame['theLand']
        self.thePeaks=self.loadGame['thePeaks']
        self.theMountain=self.loadGame['theMountain']
        self.theHills=self.loadGame['theHills']
        self.theSea=self.loadGame['theSea']
        self.heightMap=self.loadGame['heightMap']
        self.resourcesMap=self.loadGame['resourcesMap']
        self.worldHeight=len(self.heightMap)
        self.worldWidth=len(self.heightMap[0])

def saveGame(fileName,theLand,thePeaks,theMountain,theHills,theSea,heightMap,resourcesMap):
    path='g:\\gd\\mom_na\\dev\\'
    fileNamePath=path+str(fileName)+'.sav'
    # matrixes for save: theLand, thePeaks, theMountain, theHills, heightMap, resourcesMap
    savedGame={'theLand':theLand,'thePeaks':thePeaks,'theMountain':theMountain,'theHills':theHills,'theSea':theSea,'heightMap':heightMap,'resourcesMap':resourcesMap}
    savedGameFile=open(fileNamePath,'w')
    pickle.dump(savedGame,savedGameFile)
    savedGameFile.close()
    print 'Game saved in '+fileName

def newGame():          #<<<<<----- generators list HERE
    actualGenerator=1                               #set the number of one that you are currently using
    generatorsList=[PivotsMethodGen,DiamondSquareGen]                #yes, you can add new gererator here.

    generator=generatorsList[actualGenerator](100)  #<<<<---- get the world

    return generator

def loadGame():

    path='g:\\gd\\mom_na\\dev\\'            # user must input file name of saved game here!!
    fileName=path+'testSaveFile.sav'        # see above ^^^

    generator=LoadedGame(fileName)                  #<<<<---- get the saved world
    print 'Game loaded!'

    return generator

def cameraPreparation():
    #Make ingame camera which show the world map
    vizualRepresent=1                               #0 - simple, >=1 - another types
    theWorldVizualization=WorldVizualizator(theWorld,vizualRepresent)  #<<<<---- make vizual represent of the world

    cameraStartX=theWorld.worldWidth/2
    cameraStartY=theWorld.worldHeight/2

    worldWidth=theWorldVizualization.theWorld.worldWidth
    worldHeight=theWorldVizualization.theWorld.worldHeight
    graficPath=theWorldVizualization.graficPath
    graficPack=theWorldVizualization.graficPack

    camera=InGameCamera(cameraStartX,cameraStartY,mainWindowsMapAreaWidth,mainWindowsMapAreaHeight,worldWidth,worldHeight,graficPath,graficPack)

    return camera,theWorldVizualization

class WorldVizualizator():
    def __init__(self, theWorld, vizualRepresent):
        self.theWorld=theWorld
        self.worldMap=[]
        self.worldForestMap=[]

        for i in range(self.theWorld.worldHeight):
            self.worldMap.append([100]*self.theWorld.worldWidth)         #fill the world with water and make worldMap matrix itself.
            self.worldForestMap.append(['000']*self.theWorld.worldWidth)   #make the forests maxrix and fill it with no forest var

        #now we can make world layers matrixs which will be used for surface making later.

        #there are two type of vizual represent of the world. the first is simple, which don't use vizual types, it use matrix of generator itself (theLand, theMountain, etc) and standart tiles icons.
        #another types based on vizual elements calculated by ResourcesGen function.

        if vizualRepresent==0:

            # Simple vizual represent.

            #we need function which would paint landscape in the world map
            def painter(landscapeElement,landscapeType):    #landscapeType is a 'land' or 'hills' or etc
                if landscapeType=='land': brush=200
                elif landscapeType=='peaks': brush=300
                elif landscapeType=='mountain': brush=310
                elif landscapeType=='hills': brush=320
                else:
                    print 'no landscape type choosed or wrong landscape type!'

                for element in landscapeElement:
                    worldMap[element[1]][element[0]]=brush

            #then we paint lanscape elements
            painter(self.theWorld.theLand,'land')               #theLand
            painter(self.theWorld.thePeaks,'peaks')             #thePeaks
            painter(self.theWorld.theMountain,'mountain')       #theMountain
            painter(self.theWorld.theHills,'hills')             #theHills

            self.graficPath='g:/gd/mom_na/dev/grafics/tiles/Standart/'
            self.graficPack=['000',100,150,200,300,310,320,400]

            self.worldForestMap=[['000']*theWorld.worldWidth]*theWorld.worldHeight
            self.tileResources={}
            self.showResources=0


        elif vizualRepresent==1:

            #calculate resources of the world
            self.resourcesMap=ResourcesGen(self.theWorld.theLand,self.theWorld.theSea, self.theWorld.heightMap)

            #then create worldMap and worldForestMap
            for j in range(self.theWorld.worldHeight):
                for i in range(self.theWorld.worldWidth):
                    self.worldMap[j][i]=self.resourcesMap.worldResources[j][i]['landscape vizual type']
                    if self.resourcesMap.worldResources[j][i].get('forest vizual type')!=None:
                        self.worldForestMap[j][i]=self.resourcesMap.worldResources[j][i]['forest vizual type']

            self.graficPath='g:/gd/mom_na/dev/grafics/tiles/Alt/'
            self.graficPack=['000',100,150,200,201,202,203,210,211,212,213,220,221,230,231,232,233,240,241,250,251,260,270,290,291,292,293,294,295,296,297,298,299,300,330,390,400]

            self.tileResources={}
            self.showResources=1

        else:
            print "No vizual represent choosed or wrong vizual represent number."


#------------------------------- MAIN ---------------------------------------------

#pygame start
pygame.init()

FPS=60 # frames per second setting
fpsClock=pygame.time.Clock()

tileSize=32
mainWindowWidth=1000     #WINDOWS SIZE (width)
mainWindowHeight=600    #WINDOWS SIZE (height)

basicSurface=pygame.display.set_mode((mainWindowWidth, mainWindowHeight))

pygame.display.set_caption('Last Wizard Stand')

mainInterface=200
mainWindowsMapAreaWidth=mainWindowWidth-mainInterface
mainWindowsMapAreaHeight=mainWindowHeight

worldMapLandscapeSurface=Surface((mainWindowsMapAreaWidth,mainWindowsMapAreaHeight))

worldMapForestsSurface=Surface((mainWindowsMapAreaWidth,mainWindowsMapAreaHeight))
worldMapForestsSurface.set_colorkey((255,0,255))

titleSurface=Surface((mainWindowWidth,mainWindowHeight))

directoryPath='g:\\gd\\mom_na\\dev\\grafics\\'
titleImage=image.load(directoryPath+'Title.png')
titleSurface.blit(titleImage,(0,0))

titleButtonSurface=Surface((225,55))
titleButtonSurface.set_colorkey((255,0,255))

titleButton=image.load(directoryPath+'titleButton.bmp')

titleButtonSurface.blit(titleButton,(0,0))
titleSurface.blit(titleButtonSurface,(750,460))
titleSurface.blit(titleButtonSurface,(750,525))


# ------------------------------- pre MAIN LOOP -----------------------------
gameState=0     #title screen show

interface=InGameInterface(mainWindowWidth,mainWindowHeight,mainInterface)
tileResources=None  #mouse button isn't pressed on start

mouseOldPos=mouse.get_pos()

# ------------------------------- MAIN LOOP -----------------------------

while True:

    if gameState==0:
        #title screen
        basicSurface.blit(titleSurface,(0,0))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_x):
                pygame.quit()
                sys.exit()

            if event.type==MOUSEBUTTONDOWN:
                mouseClick=mouse.get_pressed()
                if mouseClick[0]:
                    x=event.pos[0]
                    y=event.pos[1]

                    if (x>=750 and x<=750+225) and (y>=460 and y<=460+55):
                        gameState=100
                        theWorld=newGame()
                        camera,theWorldVizualization=cameraPreparation()[0],cameraPreparation()[1]

                    if (x>=750 and x<=750+225) and (y>=525 and y<=525+55):
                        gameState=100
                        theWorld=loadGame()
                        camera,theWorldVizualization=cameraPreparation()[0],cameraPreparation()[1]

    if gameState==100:
        # normal game

        cameraDirection=0       #camera don't move when idle

        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_x):
                pygame.quit()
                sys.exit()

            #map moving by keyboard
            if event.type==KEYDOWN and event.key==K_UP:
                cameraDirection=1
            if event.type==KEYDOWN and event.key==K_RIGHT:
                cameraDirection=2
            if event.type==KEYDOWN and event.key==K_DOWN:
                cameraDirection=3
            if event.type==KEYDOWN and event.key==K_LEFT:
                cameraDirection=4
            if event.type==KEYUP:
                cameraDirection=0

            if event.type==KEYDOWN and event.key==K_s:
                saveGame('testSaveFile',theWorld.theLand,theWorld.thePeaks,theWorld.theMountain,theWorld.theHills,theWorld.theSea,theWorld.heightMap,theWorldVizualization.resourcesMap.worldResources)
            if event.type==KEYDOWN and event.key==K_l:
                theWorld=loadGame()
                camera,theWorldVizualization=cameraPreparation()[0],cameraPreparation()[1]
            if event.type==KEYDOWN and event.key==K_q:
                gameState=0

            #left mouse click will show list of tile resources
            if event.type==MOUSEBUTTONDOWN:
                mouseClick=mouse.get_pressed()
                if mouseClick[0]:
                    x=camera.actualPointX+event.pos[0]/32
                    y=camera.actualPointY+event.pos[1]/32

                    #if x<worldWidth and y<worldHeight and event.pos[0]<interfaceZone:   #we can't get tile info if mouse cursor in the interface area
                        #print 'x,y=',x,y
                    if theWorldVizualization.showResources!=0:
                        tileResources=theWorldVizualization.resourcesMap.worldResources[y][x]
                        #print 'actualPointX, actualPointY=',camera.actualPointX, camera.actualPointY

            #right mouse click and hold will move map
            if event.type==MOUSEMOTION:
                if mouse.get_pressed()[2]:
                        corrector=1
                        x,y=event.pos[0]/corrector,event.pos[1]/corrector
                        print x,y
                        if x==mouseOldPos[0] and y>mouseOldPos[1]:   #move top
                            cameraDirection=1
                        if x<mouseOldPos[0] and y==mouseOldPos[1]:   #move right
                            cameraDirection=2
                        if x==mouseOldPos[0] and y<mouseOldPos[1]:   #move bottom
                            cameraDirection=3
                        if x>mouseOldPos[0] and y==mouseOldPos[1]:   #move left
                            cameraDirection=4

                        if x<mouseOldPos[0] and y>mouseOldPos[1]:   #move top+right
                            cameraDirection=5
                        if x<mouseOldPos[0] and y<mouseOldPos[1]:   #move bottom+right
                            cameraDirection=6
                        if x>mouseOldPos[0] and y<mouseOldPos[1]:   #move bottom+left
                            cameraDirection=7
                        if x>mouseOldPos[0] and y>mouseOldPos[1]:   #move top+left
                            cameraDirection=8
                        else:
                            pass
                        mouseOldPos=(x,y)

        camera.draw(cameraDirection,theWorldVizualization.worldMap,theWorldVizualization.worldForestMap)
        interface.showInterface()
        if tileResources:
            interface.showText(tileResources)

        basicSurface.blit(worldMapLandscapeSurface,(0,0))
        basicSurface.blit(worldMapForestsSurface,(0,0))


    pygame.display.update()
    fpsClock.tick(FPS)
