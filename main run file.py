from tkinter import *
import random
class Rectangle(object):
    def __init__(self, x1, y1, x2, y2, color="blue"): # initialize the attributes
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cx = (x1 + x2) / 2
        self.cy = (y1 + y2) / 2
        self.cy2 = 0
        self.cy3 = 0
        self.cy4 = 0
        self.width = x2 - x1
        self.height = y2 - y1
        self.color = color
        self.vFall = self.vJump = self.vSecondJump = 30
        self.g = 4
    
    def setcx(self, data):
        self.cx += data.scrollX

    def draw(self, canvas, image): # draw the rectangle
         canvas.create_image(self.cx, self.cy, image=image)
    
    def fall(self, data): # if player rectangle falls
        self.cy += self.vFall
        self.vFall += self.g
        self.cy2 = self.vFall + self.cy
        
    def setFallVelocity(self):
        self.vFall = 30
    
    def setJumpVelocity(self):
        self.vJump = 30
    
    def setSecondJumpVelocity(self):
        self.vSecondJump = 30

    def jump(self, data): # if player rectangle jumps
        self.cy -= self.vJump
        self.vJump -= self.g
        self.cy3 = self.cy - self.vJump
        
    
    def secondJump(self, data): # if player rectangle second jump
        self.cy -= self.vSecondJump
        self.vSecondJump -= self.g
        self.cy4 = self.cy - self.vSecondJump
    
    def move(self, dx, dy): # if player rectangle moves
        self.cx += dx
        self.cy += dy
    
    def shooting(self, dx):
        self.cx += dx
    
    def recoil(self, dx, dy=0):
        self.cx += dx
        self.cy += dy
        
def init(data):
    # There is only one init, not one-per-mode
    # buttonFrame = Frame(data.root)
    # b1 = Button(buttonFrame, text="button1", command=lambda:onButton(data,1))
    # b1.grid(row=0,column=0)
    # b2 = Button(buttonFrame, text="button2", command=lambda:onButton(data,2))
    # b2.grid(row=1,column=0)
    # b3 = Button(buttonFrame, text="button3", command=lambda:onButton(data,3))
    # b3.grid(row=2,column=0)
    # buttonFrame.pack(side=BOTTOM)
    # 
    data.mode = "splashScreen"
    imageData(data)
    mapData(data)
    playerData(data)
    bulletData(data)
    explosiveData(data)
    # scrollerData(data)
    data.pressedStatus = {"w": False, "s": False, "a": False, "d": False, "z": False, "Up": False, "Down": False, "Left": False, "Right": False, "m": False,
"r":False, "x":False, "n": False, "space":False}

def mapData(data):
    data.rows = 5
    data.cols = []
    for row in range(data.rows):
        col = random.randint(1, 3)
        data.cols.append(col)
    data.threeColMargin = 50
    data.twoColMargin = data.road.width() - 20
    data.oneColMargin = data.road.width() * 2 - 100
    data.threeColGap = (data.width - 2 * data.threeColMargin - 3 * data.road.width()) / 2
    data.twoColGap = data.width - 2 * data.twoColMargin - 2 * data.road.width()
    data.rowGap = (data.height - 5 * data.road.height()) / 6
    initMap(data)

def playerData(data):
    data.playerL = []
    data.num = 2
    data.playerWidth = data.playerHeight = 50
    initPlayer(data)
    data.count1 = 0
    data.count2 = 0
    data.player1IsJump = False
    data.player1IsFall = False
    data.player1IsSecondJump = False
    data.player2IsJump = False
    data.player2IsFall = False
    data.player2IsSecondJump = False
    data.isRecoilForPlayer1 = True
    data.isRecoilForPlayer2 = True
    data.player1Lives = 5
    data.player2Lives = 5
    data.isPaused = False
    data.isGameOver = False

def bulletData(data):
    data.bulletL = []
    data.num = 2
    initBullet(data)
    data.bulletWidth = 80
    data.bulletHeight = 5
    data.isRightShootingForPlayer1 = False
    data.isLeftShootingForPlayer1 = False
    data.isLeftShootingForPlayer2 = False
    data.isRightShootingForPlayer2 = False
    data.directionForPlayer1 = "right"
    data.directionForPlayer2 = "right"

def imageData(data):
    data.player1 = PhotoImage(file="player1.gif")
    data.player2 = PhotoImage(file="player2.gif")
    data.road = PhotoImage(file="road.gif")
    data.road = data.road.subsample(4, 4)
    data.bullet = PhotoImage(file="bullet.gif")
    data.explosive = PhotoImage(file="explosive.gif")
    data.background = PhotoImage(file="background.gif")
    data.background2 = PhotoImage(file="background2.gif")
    data.background2 = data.background2.zoom(4, 4)
    data.campaign = PhotoImage(file="campaign.gif")
    data.campaign = data.campaign.subsample(2, 2)
    data.credit = PhotoImage(file="credit.gif")
    data.credit = data.credit.subsample(2, 2)
    data.help = PhotoImage(file="help.gif")
    data.help = data.help.subsample(16, 16)
    data.menu = PhotoImage(file="menu.gif")
    data.restart = PhotoImage(file="restart.gif")
    data.restart = data.restart.subsample(2, 2)

def explosiveData(data):
    data.explosiveL = []
    data.num = 2
    initExplosive(data)
    data.explosiveW = 50
    data.explosiveH = 20
    data.isPlayer1 = False
    data.isPlayer2 = False
# def scrollerData(data):
#     data.scrollX = 0  # amount view is scrolled to the right
#     data.scrollY = 0  # amount view is scrolled to the up
#     data.centerX = (data.playerL[0].cx + data.playerL[1].cx) / 2
#     data.centerY = (data.playerL[0].cy + data.playerL[1].cy) / 2
#     data.isPlayer1Move = False
#     data.isPlayer2Move = False
    
def initMap(data): # initialize the map
    data.mapL = [[0] * data.cols[row] for row in range(data.rows)]
    for row in range(data.rows):
        if (data.cols[row] == 1):
            oneColMap(data, row)
        elif (data.cols[row] == 2):
            twoColMap(data, row)
        elif (data.cols[row] == 3):
            threeColMap(data, row)
    
def oneColMap(data, row):
    x1 = data.oneColMargin
    x2 = x1 + data.road.width()
    y1 = data.rowGap + row * data.road.height() + row * data.rowGap
    y2 = y1 + data.road.height()
    r = Rectangle(x1, y1, x2, y2)
    data.mapL[row][data.cols[row] - 1] = r
    
def twoColMap(data, row):
    for elem in range(data.cols[row]):
        x1 = data.twoColMargin + elem * data.road.width() + elem * data.twoColGap
        x2 = x1 + data.road.width()
        y1 = data.rowGap + row * data.road.height() + row * data.rowGap
        y2 = y1 + data.road.height()
        r = Rectangle(x1, y1, x2, y2)
        data.mapL[row][elem] = r

def threeColMap(data, row):
    for elem in range(data.cols[row]):
        x1 = data.threeColMargin + elem * data.road.width() + elem * data.threeColGap
        y1 = data.rowGap + row * data.road.height() + row * data.rowGap
        x2 = x1 + data.road.width()
        y2 = y1 + data.road.height()
        r = Rectangle(x1, y1, x2, y2)
        data.mapL[row][elem] = r

def initPlayer(data): # initialize the player
    for player in range(data.num):
        x1 = data.mapL[0][0].cx - data.playerWidth / 2
        y1 = data.mapL[1][0].cy - data.playerHeight
        x2 = x1 + data.playerWidth
        y2 = y1 + data.playerHeight
        r = Rectangle(x1, y1, x2, y2)
        data.playerL.append(r)

def initBullet(data):
    for bullet in range(data.num):
        bullet = Rectangle(data.playerL[bullet].x1, data.playerL[bullet].y1, 
        data.playerL[bullet].x2, data.playerL[bullet].y2, "red")
        data.bulletL.append(bullet)

def initExplosive(data):
    for explosive in range(data.num):
        explosive = Rectangle(data.playerL[explosive].x1, data.playerL[explosive].y1, 
        data.playerL[explosive].x2, data.playerL[explosive].y2, "red")
        data.explosiveL.append(explosive)
####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
    elif (data.mode == "campaign"): campaignMousePressed(event, data)
    elif (data.mode == "customGame"): customGameMousePressed(event, data)
    elif (data.mode == "credit"): creditMousePressed(event, data)
    elif (data.mode == "help"): helpMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
    elif (data.mode == "campaign"):   campaignKeyPressed(event, data)
    elif (data.mode == "customGame"): customGameKeyPressed(event, data)
    elif (data.mode == "credit"): creditKeyPressed(event, data)
    elif (data.mode == "help"):       helpKeyPressed(event, data)

def keyReleased(event, data):
    if (data.mode == "campaign"): campaignKeyReleased(event, data)

def timerFired(data):
    if (data.mode == "splashScreen"): splashScreenTimerFired(data)
    elif (data.mode == "campaign"):   campaignTimerFired(data)
    elif (data.mode == "customGame"): customGameTimerFired(data)
    elif (data.mode == "credit"): creditTimerFired(data)
    elif (data.mode == "help"):       helpTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
    elif (data.mode == "campaign"):   campaignRedrawAll(canvas, data)
    elif (data.mode == "customGame"): customGameRedrawAll(canvas, data)
    elif (data.mode == "credit"): creditRedrawAll(canvas, data)
    elif (data.mode == "help"):       helpRedrawAll(canvas, data)

####################################
# splashScreen mode
####################################

def splashScreenMousePressed(event, data):
    if (data.width - 100 - data.campaign.width() / 2 <= event.x <= data.width - 100 + data.campaign.width() and 100 - data.campaign.height() / 2 <= event.y <=
100 + data.campaign.height()/2):
        data.mode = "campaign"
    elif (data.width - 100 - data.campaign.width() / 2 <= event.x <= data.width - 100 + data.campaign.width() and 300 - data.campaign.height() / 2 <= event.y <=
300 + data.campaign.height()/2):
        data.mode = "credit"
    elif (data.width - 100 - data.campaign.width() / 2 <= event.x <= data.width - 100 + data.campaign.width() and 500 - data.campaign.height() / 2 <= event.y <=
500 + data.campaign.height()/2):
        data.mode = "help"

def splashScreenKeyPressed(event, data):
    pass

def splashScreenTimerFired(data):
    pass

def splashScreenRedrawAll(canvas, data):
    canvas.create_image(data.width / 2, data.height / 2, image=data.background2)
    canvas.create_image(data.width - 100, 100, image = data.campaign)
    canvas.create_image(data.width - 100, 300, image = data.credit)
    canvas.create_image(data.width - 100, 500, image = data.help)
    canvas.create_text(320, data.height - 40, text="CRAZY SHOOTING", fill="red", 
    font="helvetica 70 bold")

# def onButton(data, buttonId):
#     if (buttonId == 1): button1Pressed(data)
#     elif (buttonId == 2): button2Pressed(data)
####################################
# help mode
####################################

def helpMousePressed(event, data):
    if (data.width / 2 - data.menu.width()/2 <= event.x <= data.width /2 + data.menu.width()/2 and 500 - data.menu.width()/2 <= event.y <= 500 + data.menu.width()/2):
        data.mode = "splashScreen"

def helpKeyPressed(event, data):
    pass
    
def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="green")
    canvas.create_image(data.width / 2, 500, image = data.menu)
    canvas.create_text(data.width/2, data.height / 2 - 50, text="""
Controls

Player 1 controls:
WASD - movement
Z - shoot
X - throw bomb

Player 2 controls:
Arrow keys - movement
M - shoot
N - throw bomb

Press space to pause the game
""", font="verdana 24 bold")

####################################
# campaign mode
####################################

def campaignMousePressed(event, data): # mouse operation
    if (data.isPaused):
        if (data.width / 2 - data.restart.width()/2 <= event.x <= data.width/2 + data.restart.width() / 2 and data.height / 2 + 125 - data.restart.height() / 2 <= event.y <= data.height / 2 + 125 + data.restart.height() / 2):
            init(data)
            data.mode = "campaign"
        elif (data.width / 2 - data.menu.width()/2 <= event.x <= data.width/2 + data.menu.width() / 2 and data.height / 2 + 250 - data.menu.height() / 2 <= event.y <= data.height / 2 + 250 + data.menu.height() / 2):
            init(data)

def campaignKeyPressed(event, data): # key operation
    data.pressedStatus[event.keysym] = True
    if (data.pressedStatus["space"]):
        data.isPaused = not data.isPaused
        return
    if (data.isGameOver or data.isPaused):
        return 
    player1Operation(data)
    player2Operation(data)

def campaignKeyReleased(event, data):
    data.pressedStatus[event.keysym] = False

def player1Operation(data):
    if (data.pressedStatus["a"]):
        movePlayer1(data)
        checkForPlayer1IsFall(data)
    elif (data.pressedStatus["d"]):
        movePlayer1(data)
        checkForPlayer1IsFall(data)
    elif (data.pressedStatus["w"]):
        data.count1 += 1
        chooseJumpForPlayer1(data)
    elif (data.pressedStatus["s"]):
        data.player1IsFall = True
    elif (data.pressedStatus["z"]):
        createBulletForPlayerOne(data)
    elif(data.pressedStatus["x"]):
        createExplosivesForPlayerOne(data)
    if (data.pressedStatus["w"] and data.pressedStatus["a"]):
        data.count1 += 1
        data.playerL[0].move(-30, 0)
        chooseJumpForPlayer1(data)
    if (data.pressedStatus["w"] and data.pressedStatus["d"]):
        data.count1 += 1
        data.playerL[0].move(+30, 0)
        chooseJumpForPlayer1(data)
    if (data.pressedStatus["s"] and data.pressedStatus["a"]):
        data.playerL[0].move(-30, 0)
        data.player1IsFall = True
    if (data.pressedStatus["s"] and data.pressedStatus["a"]):
        data.playerL[0].move(+30, 0)
        data.player1IsFall = True
        
def player2Operation(data):
    if (data.pressedStatus["Left"]):
        movePlayer2(data)
        checkForPlayer2IsFall(data)
    elif (data.pressedStatus["Right"]):
        movePlayer2(data)
        checkForPlayer2IsFall(data)
    elif (data.pressedStatus["Up"]):
        data.count2 += 1
        chooseJumpForPlayer2(data)
    elif (data.pressedStatus["Down"]):
        data.player2IsFall = True
    elif (data.pressedStatus["n"]):
        createBulletForPlayerTwo(data)
    elif (data.pressedStatus["m"]):
        createExplosivesForPlayerTwo(data)
    if (data.pressedStatus["Up"] and data.pressedStatus["Left"]):
        data.count2 += 1
        data.playerL[1].move(-30, 0)
        chooseJumpForPlayer2(data)
    if (data.pressedStatus["Up"] and data.pressedStatus["Right"]):
        data.count2 += 1
        data.playerL[1].move(+30, 0)
        chooseJumpForPlayer2(data)
    if (data.pressedStatus["Down"] and data.pressedStatus["Left"]):
        data.playerL[1].move(-30, 0)
        data.player2IsFall = True
    if (data.pressedStatus["Down"] and data.pressedStatus["Right"]):
        data.playerL[1].move(+30, 0)
        data.player2IsFall = True

def movePlayer1(data):
    if (data.pressedStatus["a"]):
        data.playerL[0].move(-20, 0)
        data.directionForPlayer1 = "left"
        # data.scrollX = (data.playerL[0].cx + data.playerL[1].cx) / 2 - data.centerX
    elif (data.pressedStatus["d"]):
        data.playerL[0].move(+20, 0)
        data.directionForPlayer1 = "right"
        # data.scrollX = (data.playerL[0].cx + data.playerL[1].cx) / 2 - data.centerX
    data.isPlayer1Move = True

def movePlayer2(data):
    if (data.pressedStatus["Left"]):
        data.playerL[1].move(-20, 0)
        data.directionForPlayer2 = "left"
        # data.scrollX = (data.playerL[0].cx + data.playerL[1].cx) / 2 -data.centerX
    elif (data.pressedStatus["Right"]):
        data.playerL[1].move(+20, 0)
        data.directionForPlayer2 = "right"
        # data.scrollX = (data.playerL[0].cx + data.playerL[1].cx) / 2 - data.centerX
    data.isPlayer2Move = True
    
def createBulletForPlayerOne(data):
    if (data.directionForPlayer1 == "right"):
        x1 = data.playerL[0].cx
        y1 = data.playerL[0].cy - data.bulletHeight / 2
        data.bulletL[0] = Rectangle(x1, y1, x1 + data.bulletWidth, y1 + 
        data.bulletHeight, color = "red")
        data.isRightShootingForPlayer1 = True
        data.isLeftShootingForPlayer1 = False
    elif (data.directionForPlayer1 == "left"):
        x1 = data.playerL[0].cx - data.bulletWidth
        y1 = data.playerL[0].cy - data.bulletHeight / 2
        data.bulletL[0] = Rectangle(x1, y1, x1 + data.bulletWidth, y1 + 
        data.bulletHeight, color = "red")
        data.isLeftShootingForPlayer1 = True
        data.isRightShootingForPlayer1 = False
    data.isRecoilForPlayer2 = True

def createBulletForPlayerTwo(data):
    if (data.directionForPlayer2 == "right"):
        x1 = data.playerL[1].cx
        y1 = data.playerL[1].cy - data.bulletHeight / 2
        data.bulletL[1] = Rectangle(x1, y1, x1 + data.bulletWidth, y1 + 
        data.bulletHeight, color = "red")
        data.isRightShootingForPlayer2 = True
        data.isLeftShootingForPlayer2 = False
    elif (data.directionForPlayer2 == "left"):
        x1 = data.playerL[1].cx - data.bulletWidth
        y1 = data.playerL[1].cy - data.bulletHeight / 2
        data.bulletL[1] = Rectangle(x1, y1, x1 + data.bulletWidth, y1 + 
        data.bulletHeight, color = "red")
        data.isLeftShootingForPlayer2 = True
        data.isRightShootingForPlayer2 = False
    data.isRecoilForPlayer1 = True

def createExplosivesForPlayerOne(data):
    x1 = data.playerL[0].cx
    y1 = data.playerL[0].cy - data.explosiveH / 2
    data.explosiveL[0] = Rectangle(x1, y1, x1 + data.explosiveW, y1 + 
    data.explosiveH)
    data.isRecoilForPlayer2 = True
    data.isPlayer1 = True

def createExplosivesForPlayerTwo(data):
    x1 = data.playerL[1].cx
    y1 = data.playerL[1].cy - data.explosiveH / 2
    data.explosiveL[1] = Rectangle(x1, y1, x1 + data.explosiveW, y1 + 
    data.explosiveH)
    data.isRecoilForPlayer1 = True
    data.isPlayer2 = True

def checkForPlayer1IsFall(data):
    playerCenterX = data.playerL[0].cx
    playerCenterY = data.playerL[0].cy
    distanceX = data.playerL[0].width / 2
    distanceY = data.playerL[0].height / 2
    flag = True
    for row in range(data.rows):
        for col in range(data.cols[row]):
            if (playerCenterY + distanceY <= data.mapL[row][col].cy):
                if (playerCenterX + distanceX >= data.mapL[row][col].x1 and playerCenterX - distanceX <= data.mapL[row][col].x2):
                    flag = False
    if (flag):
        data.player1IsFall = True

def checkForPlayer2IsFall(data):
    playerCenterX = data.playerL[1].cx
    playerCenterY = data.playerL[1].cy
    distanceX = data.playerL[1].width / 2
    distanceY = data.playerL[1].height / 2
    flag = True
    for row in range(data.rows):
        for col in range(data.cols[row]):
            if (playerCenterY + distanceY <= data.mapL[row][col].cy):
                if (playerCenterX + distanceX >= data.mapL[row][col].x1 and playerCenterX - distanceX <= data.mapL[row][col].x2):
                    flag = False
    if (flag):
        data.player2IsFall = True

def chooseJumpForPlayer1(data):
    if (data.count1 == 1):
        data.player1IsJump = True
    elif (data.count1 == 2):
        data.player1IsJump = False
        data.player1IsSecondJump = True
        data.count1 = 0

def chooseJumpForPlayer2(data):
    if (data.count2 == 1):
        data.player2IsJump = True
    elif (data.count2 == 2):
        data.player2IsJump = False
        data.player2IsSecondJump = True
        data.count2 = 0

def campaignTimerFired(data): # time function
    if (not data.isGameOver and not data.isPaused):
        timerFiredForPlayer1(data)
        timerFiredForPlayer2(data)

def timerFiredForPlayer1(data):
    jumpMotionForPlayer1(data)
    fallMotionForPlayer1(data)
    shootMotionForPlayer1(data)
    explosionForPlayer1(data)

def jumpMotionForPlayer1(data):
    if (data.player1IsJump):
        data.playerL[0].jump(data)
        # data.scrollY = (data.playerL[0].cy + data.playerL[1].cy) / 2 - data.centerY
        if (edgeDetectForPlayer1(data)):
            data.player1IsJump = False
            data.playerL[0].setJumpVelocity()
            data.count1 = 0
    elif (data.player1IsSecondJump):
        data.playerL[0].secondJump(data)
        # data.scrollY = (data.playerL[0].cy + data.playerL[1].cy) / 2 - data.centerY
        if (edgeDetectForPlayer1(data)):
            data.player1IsSecondJump = False
            data.playerL[0].setSecondJumpVelocity()
            data.count1 = 0
    data.isPlayer1Move = True

def fallMotionForPlayer1(data):
    if (data.player1IsFall):
        data.playerL[0].fall(data)
        # data.scrollY = (data.playerL[0].cy + data.playerL[1].cy) / 2 - data.centerY
        if (edgeDetectForPlayer1(data)):
            data.player1IsFall = False
            data.playerL[0].setFallVelocity()
        elif (data.playerL[0].cy >= data.height):
            data.player1Lives -= 1
            data.playerL[0].cy = 0 + data.playerHeight / 2
            data.playerL[0].cx = random.uniform(data.threeColMargin, data.width - data.threeColMargin)
            data.playerL[0].vFall = 30
        if (data.player1Lives == 0):
            data.isGameOver = True
    data.isPlayer1Move = True
    
def shootMotionForPlayer1(data):
    player1cx = data.playerL[0].cx
    player2cx = data.playerL[1].cx
    player1cy = data.playerL[0].cy
    player2y1 = data.playerL[1].cy - data.playerWidth / 2
    player2y2 = data.playerL[1].cy + data.playerWidth / 2
    player1Bulletx1 = data.bulletL[0].cx - data.bulletWidth / 2
    player1Bulletx2 = data.bulletL[0].cx + data.bulletWidth / 2
    player2x1 = data.playerL[1].cx - data.playerWidth / 2
    player2x2 = data.playerL[1].cx + data.playerWidth / 2
    if (data.isLeftShootingForPlayer1):
        data.bulletL[0].shooting(-50)
        if (player2cx < player1cx and player2y2 > player1cy > player2y1
        and player1Bulletx1 <= player2x2):
            data.playerL[1].recoil(-50)
            checkForPlayer1IsFall(data)
            data.isLeftShootingForPlayer1 = False
    elif (data.isRightShootingForPlayer1):
        data.bulletL[0].shooting(+50)
        if (player2cx > player1cx and player2y2 > player1cy > player2y1 and 
        player1Bulletx2 >= player2x1):
            data.playerL[1].recoil(+50)
            checkForPlayer1IsFall(data)
            data.isRightShootingForPlayer1 = False

def explosionForPlayer1(data):
    r = 100
    player2cx = data.playerL[1].cx
    player2cy = data.playerL[1].cy
    player1Explosivecx = data.explosiveL[0].cx
    player1Explosivecy = data.explosiveL[0].cy
    distanceX = player1Explosivecx - player2cx
    distanceY = player1Explosivecy - player2cy
    if ((distanceX**2 + distanceY**2) <= r**2):
        data.playerL[1].recoil(100, -100)

def timerFiredForPlayer2(data):
    jumpMotionForPlayer2(data)
    fallMotionForPlayer2(data)
    shootMotionForPlayer2(data)

def jumpMotionForPlayer2(data):
    if (data.player2IsJump):
        data.playerL[1].jump(data)
        # data.scrollY = (data.playerL[0].cy + data.playerL[1].cy) / 2 - data.centerY
        if (edgeDetectForPlayer2(data)):
            data.player2IsJump = False
            data.playerL[1].setJumpVelocity()
            data.count2 = 0
    elif (data.player2IsSecondJump):
        data.playerL[1].secondJump(data)
        # data.scrollY = (data.playerL[0].cy + data.playerL[1].cy) / 2 - data.centerY
        if (edgeDetectForPlayer2(data)):
            data.player2IsSecondJump = False
            data.playerL[1].setSecondJumpVelocity()
            data.count2 = 0
    data.isPlayer2Move = True

def fallMotionForPlayer2(data):
    if (data.player2IsFall):
        data.playerL[1].fall(data)
        # data.scrollY = (data.playerL[0].cy + data.playerL[1].cy) / 2 - data.centerY
        if (data.playerL[1].cy >= data.height):
            data.player2Lives -= 1
            data.playerL[1].cy = 0 + data.playerHeight / 2
            data.playerL[1].cx = random.uniform(data.threeColMargin, data.width - data.threeColMargin)
            data.playerL[1].vFall = 30
        if (data.player2Lives == 0):
            data.isGameOver = True
        if (edgeDetectForPlayer2(data)):
            data.player2IsFall = False
            data.playerL[1].setFallVelocity()
    data.isPlayer2Move = True

def shootMotionForPlayer2(data):
    player1cx = data.playerL[0].cx
    player2cx = data.playerL[1].cx
    player2cy = data.playerL[1].cy
    player1y1 = data.playerL[0].cy - data.playerWidth / 2
    player1y2 = data.playerL[0].cy + data.playerWidth / 2
    player2Bulletx1 = data.bulletL[1].cx - data.bulletWidth / 2
    player2Bulletx2 = data.bulletL[1].cx + data.bulletWidth / 2
    player1x1 = data.playerL[0].cx - data.playerWidth / 2
    player1x2 = data.playerL[0].cx + data.playerWidth / 2
    if (data.isLeftShootingForPlayer2):
        data.bulletL[1].shooting(-50)
        if (player1cx < player2cx and player1y2 > player2cy > player1y1
        and player2Bulletx1 <= player1x2):
            data.playerL[0].recoil(-50)
            checkForPlayer1IsFall(data)
            data.isLeftShootingForPlayer2 = False
    elif (data.isRightShootingForPlayer2):
        data.bulletL[1].shooting(+50)
        if (player1cx > player2cx and player1y2 > player2cy > player1y1 and 
        player2Bulletx2 >= player1x1):
            data.playerL[0].recoil(+50)
            checkForPlayer1IsFall(data)
            data.isRightShootingForPlayer2 = False

def explosionForPlayer2(data):
    r = 100
    player1cx = data.playerL[0].cx
    player1cy = data.playerL[0].cy
    player2Explosivecx = data.explosiveL[0].cx
    player2Explosivecy = data.explosiveL[0].cy
    distanceX = player2Explosivecx - player1cx
    distanceY = player2Explosivecy - player1cy
    if ((distanceX**2 + distanceY**2) <= r**2):
        data.playerL[1].recoil(100, -100)
        
def edgeDetectForPlayer1(data): # detect the edges of the rectangle
    playerLeft = data.playerL[0].cx - data.playerL[0].width / 2
    playerRight = data.playerL[0].cx + data.playerL[0].width / 2 
    playerDown = data.playerL[0].cy + data.playerL[0].height / 2 
    playerDown2 = data.playerL[0].cy2 + data.playerL[0].height / 2
    playerDown3 = data.playerL[0].cy3 + data.playerL[0].height / 2
    playerDown4 = data.playerL[0].cy4 + data.playerL[0].height / 2
    if (data.player1IsJump):
        playerDownAfter = playerDown3
        print(playerDownAfter, playerDown)
        return edgeDetect(data, playerLeft, playerRight, playerDown, playerDownAfter)
    elif (data.player1IsFall):
        playerDownAfter = playerDown2
        return edgeDetect(data, playerLeft, playerRight, playerDown, playerDownAfter)
    elif (data.player1IsSecondJump):
        playerDownAfter = playerDown4
        return edgeDetect(data, playerLeft, playerRight, playerDown, playerDownAfter)

def edgeDetectForPlayer2(data):
    playerLeft = data.playerL[1].cx - data.playerL[1].width / 2
    playerRight = data.playerL[1].cx + data.playerL[1].width / 2 
    playerDown = data.playerL[1].cy + data.playerL[1].height / 2 
    playerDown2 = data.playerL[1].cy2 + data.playerL[1].height / 2
    playerDown3 = data.playerL[1].cy3 + data.playerL[1].height / 2
    playerDown4 = data.playerL[1].cy4 + data.playerL[1].height / 2
    if (data.player2IsJump):
        playerDownAfter = playerDown3
        return edgeDetect(data, playerLeft, playerRight, playerDown, playerDownAfter)
    elif (data.player2IsFall):
        playerDownAfter = playerDown2
        return edgeDetect(data, playerLeft, playerRight, playerDown, playerDownAfter)
    elif (data.player2IsSecondJump):
        playerDownAfter = playerDown4
        return edgeDetect(data, playerLeft, playerRight, playerDown, playerDownAfter)

def edgeDetect(data, playerLeft, playerRight, playerDown, playerDownAfter):
    for row in range(data.rows):
        for col in range(data.cols[row]):
            roadLeft = data.mapL[row][col].x1
            roadRight = data.mapL[row][col].x2
            roadCenterY = data.mapL[row][col].cy
            if (playerLeft <= roadRight and playerRight >= roadLeft and playerDown <= roadCenterY):
                if (playerDownAfter >= roadCenterY):
                    return True
    return False
    
def campaignRedrawAll(canvas, data): # redraw all the pieces
    # sx = data.scrollX
    # sy = data.scrollY
    canvas.create_image(data.width / 2, data.height / 2, image=data.background)
    for row in range(data.rows):
        for col in range(data.cols[row]):
            data.mapL[row][col].draw(canvas, data.road)
    data.playerL[0].draw(canvas, data.player1)
    data.playerL[1].draw(canvas, data.player2)
    # drawPlayer(canvas, data, sx, sy)
    drawBullet(canvas, data)
    drawExplosive(canvas, data)
    drawLives(canvas, data)
    if (data.isPaused):
        drawGamePaused(canvas, data)
    elif (data.isGameOver):
        drawGameEnd(canvas, data)
    
        
# def drawPlayer(canvas, data, sx, sy):
#     if (data.isPlayer1Move):
#         print("hello")
#         canvas.create_image(data.playerL[0].cx, data.playerL[0].cy, image = data.player1)
#         canvas.create_image(data.playerL[1].cx - sx, data.playerL[1].cy - sx, image = data.player2)
#         data.isPlayer1Move = False
#     elif (data.isPlayer2Move):
#         print("world")
#         canvas.create_image(data.playerL[0].cx - sx, data.playerL[0].cy - sx, image = data.player1)
#         canvas.create_image(data.playerL[1].cx, data.playerL[1].cy, image = data.player2)
#         data.isPlayer2Move = False
#     elif (data.isPlayer2Move and data.isPlayer1Move):
#         print("helloworld")
#         canvas.create_image(data.playerL[0].cx - sx, data.playerL[0].cy - sx, image = data.player1)
#         canvas.create_image(data.playerL[1].cx - sx, data.playerL[1].cy - sx, image = data.player2)
#         data.isPlayer1Move = False
#         data.isPlayer2Move = False
#     else:
#         print("hahaha")
#         canvas.create_image(data.playerL[0].cx, data.playerL[0].cy, image = data.player1)
#         canvas.create_image(data.playerL[1].cx, data.playerL[1].cy, image = data.player2)

def drawBullet(canvas, data):
    if (data.isLeftShootingForPlayer1 or data.isRightShootingForPlayer1):
        data.bulletL[0].draw(canvas, data.bullet)
    elif (data.isLeftShootingForPlayer2 or data.isRightShootingForPlayer2):
        data.bulletL[1].draw(canvas, data.bullet)

def drawExplosive(canvas, data):
    if (data.isPlayer1):
        data.explosiveL[0].draw(canvas, data.explosive)
        data.isPlayer1 = False
    elif (data.isPlayer2):
        data.explosiveL[1].draw(canvas, data.explosive)
        data.isPlayer2 = False

def drawLives(canvas, data):
    canvas.create_text(150, 550, text="Player 1 lives: " + str(data.player1Lives), font="verdana 24 bold")
    canvas.create_text(750, 550, text="Player 2 lives: " + 
str(data.player2Lives), font="verdana 24 bold")

def drawGamePaused(canvas, data):
    canvas.create_text(data.width / 2, data.height / 2, text="GAME PAUSED", font = "verdana 70 bold")
    canvas.create_image(data.width / 2, data.height / 2 + 125, image = data.restart)
    canvas.create_image(data.width / 2, data.height / 2 + 250, image = data.menu)

def drawGameEnd(canvas, data):
    if (data.player1Lives > data.player2Lives):
        canvas.create_text(data.width / 2, data.height / 2, text=
        "player 1 Wins", font="verdana 70 bold")
    elif (data.player2Lives > data.player1Lives):
        canvas.create_text(data.width / 2, data.height / 2, text=
        "player 2 wins", font="verdana 70 bold")
    else:
        canvas.create_text(data.width / 2, data.height / 2, text=
        "draw", font="verdana 70 bold")
####################################
# customized game mode
####################################

def CustomizedGameMousePressed(event, data):
    pass

def CustomizedGamePressed(event, data):
    pass

def CustomizedGameTimerFired(data):
    pass

def CustomizedGameRedrawAll(canvas, data):
    pass

####################################
# credit mode
####################################

def creditMousePressed(event, data):
    if (data.width / 2 - data.menu.width()/2 <= event.x <= data.width /2 + data.menu.width()/2 and 500 - data.menu.width()/2 <= event.y <= 500 + data.menu.width()/2):
        data.mode = "splashScreen"

def creditKeyPressed(event, data):
    if (event.keysym == "s"):
        data.mode = "splashScreen"
    elif (event.keysym == "g"):
        data.mode = "campaign"
    elif (event.keysym == "h"):
        data.mode = "help"

def creditTimerFired(data):
    pass

def creditRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    canvas.create_image(data.width / 2, 500, image = data.menu)
    canvas.create_text(data.width/2, data.height / 2, text="""
Wenkai Pan
    coding, design, music, master game tester
""", fill="white", font="verdana 24 bold")
####################################
# use the run function as-is(code from lecture 4.2)
####################################


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyWrapper(keyFn, event, canvas, data):
        keyFn(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    # create the root and the canvas
    root = Tk()
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<KeyPress>", lambda event:
                            keyWrapper(keyPressed, event, canvas, data))
    root.bind("<KeyRelease>", lambda event:
                            keyWrapper(keyReleased, event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 600)