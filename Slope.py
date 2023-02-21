import pygame
import random
import sys
import os
import time
import pygame.font
from easygui import *
os.environ['SDL_VIDEO_CENTERED'] = '1'
#initiallizes pygame library
from pygame.locals import *
import easygui
from os import path
#import easygui

pygame.init()
#sound for obstacles and power ups
PU_sound = pygame.mixer.Sound('PU_sound.wav')
hit_sound = pygame.mixer.Sound('fireHitSound.wav')
#music
pygame.mixer.music.load("game_music.wav")

global screen
global w,h
global W, H
W,H=640,480

w,h=933,600
FPS=30
#the variable storing the screen is a global variable 

screen=pygame.display.set_mode((w,h))
#screen displayed at the given width and height as parameter
backgroundGame=pygame.image.load("BackgroundGame.png").convert()
background_rect = backgroundGame.get_rect()


background = pygame.image.load("BackgroundSlope.png").convert()
instructionsScreen = pygame.image.load("instructionsScreen.png").convert()

gameOverBg=pygame.image.load("gameOver.png").convert()

#gamebackground = pygame.image.load(
#background image is loaded onto the screen


pygame.display.set_caption('slope game')
#caption on top of the window will be the above statement
exitWindow=False
#boolean value to represent that the user has not exited the program yet

radius=20
global score_file

score_file = "scoreFile.txt"


GRAY    = (100,100,100)
NAVYBLUE= (60 , 60,100)
WHITE   = (255,255,255)
RED     = (255,  0,  0)
GREEN   = (0  ,255,  0)
BLUE    = (0  ,  0,255)
YELLOW  = (255,255,  0)
ORANGE  = (255,128,  0)
PURPLE  = (255,0  ,255)
CYAN    = (0  ,255,255)
BLACK   = (0  ,  0,  0)
bright_red = (255,0,0)
bright_green = (0,255,0)


clock=pygame.time.Clock()
#The clock can be used to limit the framerate of a game, as well as track the time used per frame
background=pygame.image.load("BackgroundSlope.png").convert()


x_move_vel=6.0
lives=3
win = pygame.display.set_mode((w, h)) #This was changed

class spikes(pygame.sprite.Sprite):
    #class for one of the obstacles
    def __init__(self,obsX,obsY):
        pygame.sprite.Sprite.__init__(self)
        #loading the spikes image
        self.image = pygame.image.load('spikes.png').convert()
        # get the rectangular area of the Surface
        self.rect= self.image.get_rect()
        #x and y coordinates of the rectangular area given
        self.rect.x=obsX
        self.rect.y=obsY
        self.lives=lives
        #boolean to check if game has finished
        self.finished=False
        #boolean to check if shooting bullets
        self.shooting=False

    def draw(self):
        #drawing the image onto the screen
        screen.blit(self.image,self.rect.x,self.rect.y)

    def update(self):
        #if game has finished, remove sprite
        if self.finished:
            self.kill()
        #if given right to shoot bullets
        '''if self.shooting:
            #calls instance of enemy bullet function
            if random.random() > 0.99:
                eBullet=EnemyBullet(self.rect.centerx,self.rect.top,-5,-1)
                all_sprites.add(eBullet)
                spikeBullets.add(eBullet)'''
            
            
#Object which activates the shooting of the bullets
        
class bullet(pygame.sprite.Sprite):
    def __init__(self,bulletX,bulletY):
        pygame.sprite.Sprite.__init__(self)
        #IMAGE USED AS THE POWER UP OBJECT
        #rectangle
        #self.image = pygame.image.load("bulletPlayer.png").convert()
        #colour will be yellow
        self.image = pygame.Surface((10,20))
        self.image.fill(YELLOW)
        #get rectangular suruface of the image
        self.rect = self.image.get_rect()
        #X AND Y COORDINATES OF POWER UP OBJECT
        self.rect.x = bulletX
        self.rect.y = bulletY
        #speed at which the bullet will go
        self.speedx=20
        self.speedy=7
        
    def update(self):
        #function to make missile move diagonally on slope
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #if the bullet passes the width
        if self.rect.right > w:
            self.kill()

#object for the bullet of the enemy bullet
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self,bulletX,bulletY,speedX,speedY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("fireblast1.png").convert()
        #colour will be yellow
        #self.image = pygame.Surface((10,20))
        #self.image.fill(RED)
        #get rectangular suruface of the image
        self.rect = self.image.get_rect()
        #X AND Y COORDINATES OF POWER UP OBJECT
        self.rect.x = bulletX
        self.rect.y = bulletY
        #speed at which the bullet will go
        self.speedx=speedX
        self.speedy=speedY
        self.counter=0
        
    def update(self):
        #function to make missile move diagonally on slope
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #if the bullet passes the width
        if self.rect.right > w:
            self.kill()


'''if self.rect.top > h + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)'''


class skyBullets(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
       
        #rectangular surface for bullet
        self.image = pygame.image.load("skysky.png").convert()
        '''self.image = pygame.Surface((20,30))
        self.image.fill(WHITE)'''
        #rectangular surface around image
        self.rect = self.image.get_rect()
        #X AND Y COORDINATES OF POWER UP OBJECT
        self.rect.x = random.randrange(w - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.rect.centerx = w / 2
        #y coordinate speed
        self.speedy = 3
        self.finished=False
        
        
    def update(self):
        #increase y spped so it falls down continously
        self.rect.y += self.speedy
        #If goes below height, assign new coordinates
        if self.rect.top > h:
            self.rect.x=random.randrange(w - self.rect.width)
            self.rect.y=-25
        if self.finished==True:
            #sprite removed
            self.kill()

skyBullet_group=pygame.sprite.Group()
    

#class for enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #check if on the slope(boolean)
        #at the start, the ball is not on slope as its falling
        #self.image = pygame.image.load("1.png").convert()
        
        self.image = pygame.Surface((50,50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        #X AND Y COORDINATES OF POWER UP OBJECT
        self.rect.x = x
        self.rect.y = y
        self.rect.centerx = w / 2
        self.finished=False
        
        
    def shoot(self):
        #call an instance of the class
        eBullet=EnemyBullet(self.rect.centerx,self.rect.top,-5,-1)
        #add to all sprites and bullet group
        all_sprites.add(eBullet)
        bullet_Enemygroup.add(eBullet)
        #if the game has finished
        if self.finished==True:
            #sprite removed
            self.kill()

spikeBullets=pygame.sprite.Group()
bullet_Enemygroup=pygame.sprite.Group()

#function for text    
def bText(text,font):
    textsurface = font.render(text,1,RED)
    #creates the text including color etc
    return textsurface, textsurface.get_rect()
    #creates a rectangle to act as a border for the text

def button(message,x,y,w,h,color,buttonFunction=None):
    mouse = pygame.mouse.get_pos()
    #gets coordinates of mouse movement
    click = pygame.mouse.get_pressed()
    #checks if any part of mouse is clicked
    pygame.draw.rect(screen,color,(x,y,w,h))
    if x+w > mouse[0] >x and y+h > mouse[1] >y:
        #checks if mouse is hovering over the buttons
        pygame.draw.rect(screen,GREEN,(x,y,w,h))
        #the border of the button is drawn if the mouse hovers over it
        if click[0] == 1 and buttonFunction != None:
            buttonFunction()
    smalltext=pygame.font.SysFont("comicsansms",20)
    #creates a Font object from system fonts
    textSurf, textRect = bText(message,smalltext)
    #calls function to create text and border
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    #allows text to be in the center of the button
    screen.blit(textSurf, textRect)
    #draws text as well as the button to the display

def pyQuit():
    pygame.quit()
    quit()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #lives
        self.lives=3.0
        self.score=5
        #x/y coordinates and y velocity
        self.player_x = 10.0
        self.player_y = 10.0
        self.player_yvel = 0.0
        #radius and y acceleration/
        self.radius=37
        self.yaccel = 1.0
        #max y coordinate
        self.max_yvel = 10.0
        #check if on the slope(boolean)
        #at the start, the ball is not on slope as its falling
        self.on_slope = False
        #x velocity
        self.x_move_vel = 6.0
        #slope coordinates
        self.slope_x1 = 10.0             #x and y coordinates of the slope
        self.slope_y1 = 200.0

        self.slope_x2 = 640.0
        self.slope_y2 = 400.0
        #radius of the missile(circular)
        self.missile_radius=5
        #image of the ball
        self.image_orig=pygame.image.load('moncler.png')
        #copy of the original image is made
        self.image=self.image_orig.copy()
        #gets rectangle of the image for collisions
        self.rect=self.image.get_rect()

        
        #x/y coordinates and y velocity
        self.rect.x = 10.0
        self.rect.y = 10.0
        '''#centre of image
        self.rect.centerx = w / 2
        #bottom of screen/image
        self.rect.bottom = h - 10'''
        
        #dimensions
        self.player_w = self.radius
        self.player_h = self.radius
        self.moving_x= self.x_move_vel
        #slope
        #set boolean value
        #check if player is invincible
        self.invincible=False
        self.bulletsAllowed=False
        #counter for time of invincibility
        self.countInvincible=0
        self.rot=0#how far in degrees it roates
        self.rot_speed = 1 #how many degees it should rotate at each update
        self.last_update = pygame.time.get_ticks() #How many ticks it has been since the game has started
        

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50: #how many milisconds
            self.last_update = now #ie reset
            #(Find the remainder only i.e. loop back to the 0)
            self.rot = self.rot + self.rot_speed % 360
            #rotate the clean original image
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            #Draw a rect around the new rotated image
            self.rect = self.image.get_rect()
            #keep the image centred on its axis
            self.rect.center = old_center
            
        

        
    def update(self):
        self.rotate()
        #collects all user eventsz
        for event in pygame.event.get():
            #if user presses quit button
            if event.type == pygame.QUIT:
                    running=False
            #if user presses down on left/right/up        
            elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        left_key_down = True
                    elif event.key == K_RIGHT:
                        right_key_down = True
                    elif event.key == K_UP:
                            # jumping -- give a velocity pulse
                            # only allowed if on the slope
                        #only jump if on the slope
                        if self.on_slope:
                            self.player_yvel=-10
            #once the key is released(left/right)
            elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        left_key_down = False
                    elif event.key == K_RIGHT:
                        right_key_down = False
                
        self.moving_x = +self.x_move_vel
        
        # adjust the Y-coordinates of the player if he walks
        # along the slope
        if self.on_slope and self.moving_x != 0:
            #self.player_y += self.moving_x * ((self.slope_y2 - self.slope_y1) / (self.slope_x2 - self.slope_x1))
            self.rect.y += self.moving_x * ((self.slope_y2 - self.slope_y1) / (self.slope_x2 - self.slope_x1))
            
        # player Y acceleration
        if self.player_yvel < self.max_yvel:
            self.player_yvel += self.yaccel
        #self.player_y += self.player_yvel
        self.rect.y += self.player_yvel
        
        

        # player X movement
        #self.player_x += self.moving_x
        self.rect.x += self.moving_x

        # player slope hit check
        self.on_slope = False
        # within the horizontal confines of slope ?
        if self.slope_x1 <= self.rect.x + self.player_w <= self.slope_x2 - self.player_w:
            # find out the Y-coordinate of the slope's intersection
            # to the player's current X-coordinate, and check
            # if the player's bottom Y position trespasses that.
            # if so, set the `on_slope' flag and zero the player's
            # Y velocity
            #proj_y = self.slope_y1 + (self.player_x - self.slope_x1) * ((self.slope_y2 - self.slope_y1) / (self.slope_x2 - self.slope_x1))
            proj_y = self.slope_y1 + (self.rect.x - self.slope_x1) * ((self.slope_y2 - self.slope_y1) / (self.slope_x2 - self.slope_x1))
            if self.rect.y + self.player_h >= proj_y:
                    self.player_y = proj_y - self.player_h
                    self.rect.y = proj_y - self.player_h
                    self.player_yvel = 0
                    self.on_slope = True

        counter=0
        
        if self.rect.x > W:
            self.rect.x = 10.0
            
            counter=counter+1
        
        #if invincibility aquired
        if self.invincible==True:
            #decrease the speed of the x coordinate
            if self.countInvincible<110:
                self.x_move_vel = 3.0

            if self.countInvincible>=110: #have 60 frames passed
                #after certain time, player no longer invincible
                self.invincible=False
                #back to normal x coordinate velocity
                self.x_move_vel = 6.0
                
                countInvincible=0 #reset our counter
            self.countInvincible+=1
            
        if self.lives<0:
            self.kill()
            
            
    def shoot(self):
    
        if self.bulletsAllowed==True:
            #call an instance of the class
            Bullet=bullet(self.rect.centerx,self.rect.top)
            #add to all sprites and bullet group
            all_sprites.add(Bullet)
            bullet_group.add(Bullet)
            

        
bullet_group=pygame.sprite.Group()

class PU_object(pygame.sprite.Sprite):
    def __init__(self,puX,puY):
        #ALL THE ATTRIBUTES THAT THE OBJECT HAS 
        pygame.sprite.Sprite.__init__(self)
        #IMAGE USED AS THE POWER UP OBJECT
        self.image = pygame.image.load("powerUp.png")
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        #X AND Y COORDINATES OF POWER UP OBJECT
        self.rect.x = puX
        self.rect.y = puY
        self.obtained=False
        self.finished=False
        

    def draw(self):
        #FUNCTION TO DRAW POWER UP OBJECT TO THE SCREEN
        screen.blit(self.image,self.rect.x,self.rect.y)
        #pygame.display.update()
    def update(self):
        #if the game has finished
        if self.finished==True:
            #sprite removed
            self.kill()

    
    
all_sprites=pygame.sprite.Group()
        
#function that displays the  results
def see_Leaderboard():
    #width and height of leaderboard display
    w,h=933,600
    leaderboard=pygame.image.load("leaderboard.png").convert()
    leaderboard_display=pygame.display.set_mode((w,h))
    #read content of file
    scores_file=open(score_file, 'r')
    users2DArray=eval(scores_file.read())
    #create font to output text from file
    #myFont = pygame.font.Font('freesansbold.ttf', 15)
    #myText = myFont.render(High_scores, True, WHITE)
    #closing file
    scores_file.close()
    L_screen=True
    #while loop for event handling
    while L_screen:
        for event in pygame.event.get():
            #collects events within the program
            if event.type == pygame.QUIT:
                #if user presses top right quit button on screen
                ExitWindow=True
                pygame.quit()
                quit()
        leaderboard_display.blit(leaderboard, [0,0])
        #y coordinate of scores
        y=250
        #loops through 2D array of names and scores
        
        for i in range(len(users2DArray)):
            #x coordinates
            x=400
            #padding to allow aligning of scores and names
            padding=8-len(users2DArray[i][0])
            #concatenate scores and names with padding
            linetoPrint=(str(users2DArray[i][0]) + (padding* "  ") + str(users2DArray[i][1]))
            #creates font for leaderboard items
            myFont = pygame.font.Font('freesansbold.ttf', 25)
            #renders font made and drawn onto the screen
            myText = myFont.render(linetoPrint, True, WHITE)
            leaderboard_display.blit(myText, [x,y+35 *i])
            
        #TEXT TO OUTPUT COLUMNS NAME AND SCORE   
        column1 = myFont.render("NAME", True, RED)
        leaderboard_display.blit(column1, [x,200])
        column2 = myFont.render("SCORE", True, RED)
        leaderboard_display.blit(column2, [x+100,200])
        
        #draw background and text on screen        
        #leaderboard_display.blit(leaderboard, [0,0])
        #leaderboard_display.blit(myText, [5,300])
        #button to point back to main menu
        
        button("main menu",366,100,200,50,WHITE,mainMenu)
        #updating display
        pygame.display.update()        
        

def Leaderboard():
    #the window by which the gui comes up will be called 'leaderboard'
    button=""
    version = "leaderboard"
    #options to press for the buttons
    options = ["choice 1: yes","choice 2: no way"]
    #creates the GUI box with the the message, the title of the window, and options ot press
    button=buttonbox("Would you like to go on the leaderboard", title=version, choices = options)
    #if 1st button pressed, it will output this
    #boolean to test if user input is valid
    valid=False
    if button == options[1]:
        msgbox("you will be taken to the main menu" ,"No leaderBoard")
        mainMenu()
    if button == options[0]:
        #msgbox("You shall be taken to the leaderboard" ,"No leaderBoard")
        #fields to enter username
        msg = "Enter your username. No more than 8 characters"
        title="username"
        fieldNames=["username"]
        fieldValues = multenterbox(msg,title, fieldNames)
        #prevents input from being blanck
        while 1:
            if fieldValues == None:
                break
                mainMenu()
            errmsg = ""
            #loops through field names and outputs mesage
            for i in range(len(fieldNames)):
              if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
            #user input correct
            if errmsg == "":
                #input from user is valid
                valid=True
                break# no problems found
            #output box again for user to input value with error message
                
                
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
            
    #if input is valid
    if valid:
        #prevents input from being blanck
        while 1:
            #input is not valid
            if fieldValues == None:
                valid=False
                mainMenu()
                break
            errmsg=""
            #checks if the name is in the file
            if fieldValues[0] in open(score_file).read():
                errmsg = errmsg + ('"%s" is already taken' % fieldValues[0])
                #username reset
                fieldValues[0]=""
            if errmsg == "":
                #input from user is valid
                valid=True
                break# no problems found
            
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
            
            
        #opens the file in read format
        score_Wfile = open(score_file, "r")
        #function to read contents of the file

        #creates an array to store the score and the user
        LeaderboardList=[]
        #create another array within the leaderboard array so it becomes 2d array
        username=fieldValues[0]
                    
            
        #cuts the username into the first 8 characters thus creating a limit
        username=username[0:8]
        LeaderboardList.append(username)
        LeaderboardList.append(scorePlayer)
        #for loop to split file to list through split function
        
        #evaluates file
        with open(score_file) as file:
            tempArray=eval(score_Wfile.read())
            
        #sorts file    
        tempSort=sorted(tempArray,key=lambda x: x[1], reverse=True)

        #if leaderboards not full. append and sort.
        if len(tempArray)< 10:
            #append input to array
            tempArray.append(LeaderboardList)
            tempSort.append(LeaderboardList)
            #sort the array once it has been appended to 
            tempSort=sorted(tempSort,key=lambda x: x[1], reverse=True)
            #then overwrite into the file
            score_Wfile = open(score_file, "w")
            score_Wfile.write(str(tempSort))
            score_Wfile.close()

        #if leaderboard is full    
        if len(tempArray) >= 10:
            #new empty array
            tempList=[]
            #append and sort
            tempArray.append(LeaderboardList)
            tempSort=sorted(tempArray,key=lambda x: x[1], reverse=True)
            #only include first 10 of the new sorted values
            for i in range(10):
                tempList.append(tempSort[i])

            
            #overwrite changes to the file
            score_Wfile = open(score_file, "w")
            score_Wfile.write(str(tempList))
            score_Wfile.close()
            #tell user that didn't make it that their score was too low
            msgbox("If you do not see your name and your score, your score may be too low" ,"No leaderBoard")
            
            
        #sort the list which has included the new value inserted
        tempSort=sorted(tempSort,key=lambda x:x[1], reverse=True)
        tempSort=sorted(tempSort,key=lambda x:x[1], reverse=True)

       
            
        
        #Overwrites file using the sorted array
        
        mainMenu()
        
   
        
        
    #if 2nd button pressed it will output this
    
    '''
    #allows user to confirm their adding to the leaderboard
    yes="do you want to continue"
    no="confirm this"
    #if they choose to continue
    if ccbox(yes,no):
        pass
    #if they press cancel
    else:
        mainMenu()'''
        
        
    
    '''
    msg = "Enter your username"
    title = "Leaderboard submission"
    fieldNames = ["UserName"]
    fieldValues = multenterbox(msg, title, fieldNames)
    if fieldValues is None:
        sys.exit(0)
    # make sure that none of the fields were left blank
    while 1:
        errmsg = ""
        for i, name in enumerate(fieldNames):
            if fieldValues[i].strip() == "":
              errmsg += "{} is a required field.\n\n".format(name)
        if errmsg == "":
            break # no problems found
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
        if fieldValues is None:
            break'''
    
def game():

    
    #creates a window for the game
   

    #W=933
    #H=600
    
    global win
    win = pygame.display.set_mode((W, H))
    pygame.display.set_caption('Slope game')
    #fpsClock = pygame.time.Clock()
    # Variables: are the movement keys down ?
    left_key_down = False
    right_key_down = False

    # Variables: player in-game coordinates
    global player_x
    player_x = 10.0
    player_y = 10.0

    # Variable: player Y velocity
    player_yvel = 0.0
    slope_x1 = 10.0             #x and y coordinates of the slope
    slope_y1 = 200.0

    slope_x2 = 640.0
    slope_y2 = 400.0
    on_slope = False
             
    coordinates = [[(10,200)],
                   [(640,400)],
                   [(121, 236)],
                   [(68, 221)],
                   [(32, 206)],
                   [(54, 215)],
                   [(79, 224)],
                   [(122, 234)],[(150, 247)],
                   [(177, 252)],[(199, 259)],
                   [(218, 269)],[(250, 279)],
                   [(284, 291)],[(310, 296)],
                   [(343, 308)],[(368, 311)],
                   [(397, 320)],[(419, 329)],
                   [(478, 348)],[(510, 360)],
                   [(540, 371)],[(564, 376)],
                   [(595, 385)],[(614, 390)],
                   [(634, 396)],[(635, 396)]]  
    
    
    
    #
    #	CONSTANTS
    #
    player_yvel = 0.0
    '''radius=20                   #size of the ball
    missile_radius=5

    player_w = radius		# player width
    player_h = radius		# player height

    yaccel = 1.0		# player Y accelearation
    max_yvel = 20.0		# player max Y velcoity

    slope_x1 = 10.0             #x and y coordinates of the slope
    slope_y1 = 200.0

    slope_x2 = 640.0
    slope_y2 = 400.0

    #at the start, the ball is not on slope as its falling
    on_slope = False
    
    #velocity of x coordinate of player
    global x_move_vel
    x_move_vel = 6.0'''
    
    
    #array of power up images
    power_up_array=[1,2,3,4,5,6]
    
    #sprite group for player (ball)
    player_spritesGroup=pygame.sprite.Group()

    #calling instance of ball class and adding to player sprite group
    ballPlayer=Player()
    player_spritesGroup.add(ballPlayer)
    #adding ball class instance to all_sprites group
    all_sprites.add(ballPlayer)

    
    
    POWER_UP_GROUP=pygame.sprite.Group()
    

    #background screen
    pygame.draw.rect(win,WHITE, (0,0, 640, 480))
    
   

    
    #player sprite group
    player_spritesGroup.draw(win)
    
    
    x=random.randint(1,3)
    #from random integers, if the number is 2
    
    #add to obstacle and all sprite group      
    running=True

    x=0.99 

    #creating enemy sprite group
    enemies=pygame.sprite.Group()
    
    
    #call instance of the power up object
    
    
    obstacle_group=pygame.sprite.Group()
    ShootCounter=0

    #play music constantly
    pygame.mixer.music.play(-1)

    #SET OF COORDINATES
    realX=[75,144,204,251,288,333,382,433,476,506,553,591,621]
    realY=[227,220,242,245,240,250,268,285,305,306,314,315,300]


    
    
    slope=False
    EnemySlope=False
    #set of x and y coordinates seperately 
    realX2 = [75,144,204,251,288,333,382,433,476,506,553,591,621]
    #yCoordinates = [200,640,236,221,206,215,234,247,252,259,269,279,291,296,308,311,329,329,348,360,371,376,385,390,396,396]
    realY2 = [210,225,230,255,245,255,284,315,315,316,324,335,320]
    #chooses random coordinates
    yCoordinatesEnemy = [165, 705, 180, 266, 281, 293, 272, 294, 305, 348, 320, 334, 331,361]
    #keep choosing coordinates until it is coordinates of the slope
    while not EnemySlope:
        Yenemy=random.choice(realY)#Enemy)
        X=random.choice(realX)
        #when indexes equal, it means that the coordinates are on the slope
        if realX.index(X) == realY.index(Yenemy):
            #stop choosing coordinates
            EnemySlope=True
            break
    #once coordinates are correct, call instance of enemy class
    if EnemySlope==True:
        enemy=Enemy(X,Yenemy)
        
        


    enemies=pygame.sprite.Group()

    skyBullet_group=pygame.sprite.Group()

   

    
        
    while running:
        
        #implementing the bullets coming from the sky
        if random.random() > 0.99 and ballPlayer.score>10:
            skyShoot=skyBullets()
            all_sprites.add(skyShoot)
            skyBullet_group.add(skyShoot)
            
        #testing for collisions between the sky bullets and player
        skyShot= pygame.sprite.groupcollide(player_spritesGroup,skyBullet_group,False,True)
        if skyShot:
            ballPlayer.lives=ballPlayer.lives-1
            pygame.mixer.Sound.play(hit_sound)
            
                
        #testing for collisions between the sky bullets and player's bullets   
        skyShotBullet= pygame.sprite.groupcollide(bullet_group,skyBullet_group,False,True)
        if skyShotBullet:
            ballPlayer.score=ballPlayer.score+1
            pygame.mixer.Sound.play(PU_sound)
    
                    
                
        
        '''#overlapping
        self.all_sprites=pygame.sprite.Group() #create group of sprites
        self.mobs = pygame.sprite.Group() #new group for the spikes
        self.bird = Bird() #create a new player object
        self.all_sprites.add(self.bird) #add birds to the group
        self.m = Mob() #create an instance of the Mob object
        self.all_sprites.add(self.m)
        self.mobs.add(self.m)     
        #print(Num)
        for i in range(Num):#repeats for the random number that was stored earlier
            self.m = Mob() 
            overlap = pygame.sprite.spritecollide(self.m, self.mobs, True)
            self.mobs.add(self.m)
            self.all_sprites.add(self.m)
        self.run()'''
    
        ballPlayer.rect.y += ballPlayer.player_yvel
        
        #if it hits the obstacle, increase score by 1                           
        Obshits = pygame.sprite.groupcollide(obstacle_group, bullet_group,True,False)
        if Obshits:
            ballPlayer.score+=1
        power_up=pygame.sprite.Group()


        X=random.choice(realX2)
        Y=random.choice(realY2)
        #when coordinates equal, it means they are on the slope
        if realX2.index(X) == realY2.index(Y):
            slope=True
            
        
        
        #creates instance for power up object class
        

        for event in pygame.event.get():
            #if user presses quit button
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            #if user presses down on left/right/up        
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    #decrease y coordinate for jumping
                    ballPlayer.player_yvel-=10
                    ballPlayer.player_yvel+=1
                if event.key == K_SPACE:
                    ballPlayer.shoot()
                        
                if event.key == K_p:
                    global pause
                    pause=True
                    pauseMenu()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                #print(pos)

        if random.random() > 0.90:
            spikesPU=True
            if spikesPU and slope==True:
                #call an instance of the spikes class
                spike=spikes(X,Y)
                '''overlap=pygame.sprite.spritecollide(spike,obstacle_group,True)
                if overlap:
                    spikesPU=False'''
                #sprite group for obstacles
                obstacle_group.add(spike)
                all_sprites.add(spike)

                #testing for overlap between obstacle and power up
                '''spike_overlap= pygame.sprite.spritecollide(spike,obstacle_group,False)
                if spike_overlap:
                    slope=False
                    print('Spikes overlap')'''

                #if overlap between spikes dont output it    
        
                    
                        
        #making the power up come at random times
        if random.random() > 0.90 and slope==True:
            pu=PU_object(X,Y)
            pu.obtained=False
            #overlap between power up objects 
            overlapEnemy= pygame.sprite.groupcollide(POWER_UP_GROUP,enemies,True,False)
            if overlapEnemy:
                slope=False
            #overlap of the power up objects
            overlapPUobject= pygame.sprite.spritecollide(pu,POWER_UP_GROUP,True)
            if overlapEnemy:
                slope=False
                
            '''if slope==True:
                all_sprites.add(pu)
                POWER_UP_GROUP.add(pu)'''
            all_sprites.add(pu)
            POWER_UP_GROUP.add(pu)
                
            
            
        #print(lives)
    #built in function to check if two sprites collided
        obtain_PU= pygame.sprite.groupcollide(POWER_UP_GROUP,player_spritesGroup,True,False)
        image=random.choice(power_up_array)
    #if power up has been obtained
        if obtain_PU:
            
            pu.obtained=True
            pygame.mixer.Sound.play(PU_sound)
            
           
            #if invincible power up chosen
            if image==power_up_array[0]:
                ballPlayer.score+=10
                ballPlayer.lives+=2
                ballPlayer.invincible=True
                
            #if the extra life power up is chosen
            if image==power_up_array[1]:
                ballPlayer.lives+=1
            #if the score booster power up is chosen    
            if image==power_up_array[2]:
                ballPlayer.score+=10
                
            #if bullet object is chosen
            if image==power_up_array[3]:
                ballPlayer.bulletsAllowed=True
                #display text telling user it has gained bullets
                while ballPlayer.bulletsAllowed:
                    button("bullets",275,10,10,0,WHITE,None)
                    if ballPlayer.bulletsAllowed==False:
                        break
                    #allowes player to move
                    if random.random()>0.95:
                        break
                    pygame.display.update()
                    
                    
                
                
            if image==power_up_array[4]:
                ballPlayer.bulletsAllowed=True
                #display text telling user it has gained bullets
                while ballPlayer.bulletsAllowed:
                    button("bullets",275,10,10,0,WHITE,None)
                    if ballPlayer.bulletsAllowed==False:
                        break
                    #allowes player to move
                    if random.random()>0.95:
                        break
                    pygame.display.update()
                    
                
                
            if image==power_up_array[5]:
                ballPlayer.bulletsAllowed=True
                #display text telling user it has gained bullets
                while ballPlayer.bulletsAllowed:
                    button("bullets",275,10,10,0,WHITE,None)
                    if ballPlayer.bulletsAllowed==False:
                        break
                    #allowes player to move
                    if random.random()>0.95:
                        break
                    pygame.display.update()
                    
                
            
        pygame.display.update()            
            
    
            
            #choose power up at random intervals
            
            #if it is the invincible power up
        
        
        #testing for overlap between enemy and power up
        '''overlapPU=pygame.sprite.groupcollide(enemies,POWER_UP_GROUP,True,False)
        if overlapPU:
            slope=False
            print('overlap')'''
        
        #testing for overlap between obstacle and power up
        overlapPUenemy=pygame.sprite.groupcollide(POWER_UP_GROUP,enemies,True,False)
        if overlapPUenemy:
            slope=False
            

        #testing for overlap between obstacle and power up
        overlapPU=pygame.sprite.groupcollide(obstacle_group,POWER_UP_GROUP,True,False)
        if overlapPU:
            slope=False
            

        #testing for overlap between enemy and obstacle
        overlap=pygame.sprite.groupcollide(enemies,obstacle_group,False,True)
        if overlap:
            slope=False
             
        
       #collision between spikes bullets and the player. resulting in lives decreasing 
        spike_hit= pygame.sprite.groupcollide(spikeBullets,player_spritesGroup,True,False)
        if spike_hit:
            ballPlayer.lives-=1
            
        enemyShot=pygame.sprite.groupcollide(bullet_Enemygroup,bullet_group,True,False)
        #decreases the score by 3
        if enemyShot:
            ballPlayer.score+=1
            pygame.mixer.Sound.play(PU_sound)


        #checking if enemy shoots at player
        enemyShoot=pygame.sprite.groupcollide(bullet_Enemygroup,player_spritesGroup,True,False)
        #decreases the score by 3
        if enemyShoot:
            ballPlayer.score-=3
            ballPlayer.lives-=1
            pygame.mixer.Sound.play(hit_sound)
                
        obstacle_hit= pygame.sprite.groupcollide(obstacle_group,player_spritesGroup,True,False)
        #if a collision between an obstacle and the player has occured
        if obstacle_hit:
            #update once
            ballPlayer.lives=ballPlayer.lives-1
            #player no longer allowed bullets
            ballPlayer.bulletsAllowed=False
            #play crash shound
            pygame.mixer.Sound.play(hit_sound)
            
            
        
        all_sprites.update()
        #player_spritesGroup.update()
        
        
        #choose number from 0 to 1
        if random.random() > 0.9:
            #builds enemy sprite group
            enemies=pygame.sprite.Group()
            #adds enemy to groups
            all_sprites.add(enemy)
            enemies.add(enemy)
            #chooses number between 0 to 1 again
            if random.random() > 0.9:
                #enemy shoots
                enemy.shoot()
                
            '''#moving enemy bullets    
            if ballPlayer.rect.x > enemy.rect.x:
                enemy.rect.centerx=enemy.rect.centerx*-1
                enemy.rect.top=enemy.rect.top*-1'''

        #checks if enemies are hit, if hit, score increases by 3        
        enemyHits=pygame.sprite.groupcollide(enemies, bullet_group,True,True)
        if enemyHits:
            ballPlayer.score+=3
            
        #collision with the actual enemy 
        enemyCollide=pygame.sprite.groupcollide(enemies, player_spritesGroup,True,False)
        if enemyCollide:
            #causes lives reduction by one
            ballPlayer.lives-=1
            #player no longer allowed bullets
            ballPlayer.bulletsAllowed=False
            #play crash sound
            pygame.mixer.Sound.play(hit_sound)
            
            

        bullets=3
        presses=0
            
        #pygame.display.update()
        
        win.blit(backgroundGame,background_rect)
        
        #POWER_UP_GROUP.draw(win)
        slope=pygame.draw.line(win, WHITE, (slope_x1, slope_y1), (slope_x2, slope_y2), 2)

        all_sprites.draw(win)
        clock.tick(FPS)
        ##text to show the lives and the score
        button("lives: " + (str(ballPlayer.lives)),120,10,10,0,WHITE,None)
        button("score: " + (str(ballPlayer.score)),450,10,0,0,WHITE,None)
        
        #if player loses all its lives
        if ballPlayer.lives < 0:
            gameOver(gameOverBg)
            enemy.finished=True
            pu.finished=True
            spike.finished=True
            pygame.mixer.music.stop()
            

        #allows no negative scoreZz    
        if ballPlayer.score < 0:
            ballPlayer.score=0

        #increases chance of enemies and obstacles coming
        #based on how well user is progressing in terms of scores and lives

            

        #will create a global variable for the score
        global scorePlayer        
        scorePlayer=ballPlayer.score  
        

        pygame.display.update()
   

def unpause():
    #game no longer paused
    global pause
    pause=False
    gameScreen=pygame.display.set_mode((W,H))
    #music carries on playing
    pygame.mixer.music.unpause()
    
    
def instructionsPage():
    #displaying the instructions page
    w,h=933,600
    instructions=pygame.display.set_mode((w,h))
    while pause:
        for event in pygame.event.get():
            #collects events within the program
            if event.type == pygame.QUIT:
                #if user presses top right quit button on screen
                ExitWindow=True
                pygame.quit()
                quit()
        #draws background
        instructions.blit(instructionsScreen, [0,0])
        #button to return to game
        button("continue",350,550,200,50,WHITE,unpause)
        #update display
        pygame.display.update()
        
def instructionsPageMain():
    #displaying the instructions page
    w,h=933,600
    instructions=pygame.display.set_mode((w,h))
    main=True
    while main:
        for event in pygame.event.get():
            #collects events within the program
            if event.type == pygame.QUIT:
                #if user presses top right quit button on screen
                ExitWindow=True
                pygame.quit()
                quit()
        #draws background
        instructions.blit(instructionsScreen, [0,0])
        #button to return to game
        button("main menu",350,550,200,50,WHITE,mainMenu)
        #update display
        pygame.display.update()

#function to play the music
def OnSound():
    pygame.mixer.music.play(-1)

#function to stop playing the music
def OffSound():
    pygame.mixer.music.stop()
    


    
def pauseMenu():
    #displaying the pause screen
    w,h=933,600
    pauseScreen=pygame.display.set_mode((w,h))
    menu=pygame.image.load("pauseMenu.png")
    OffSound=pygame.image.load("mute.png")
    #OnSound=pygame.image.load("TurnOn.png")
    
    #iniially has not left the window, boolean value is false
    pygame.mixer.music.pause()
    
    musicStopped=False
    
    while pause:
        for event in pygame.event.get():
            #collects events within the program
            if event.type == pygame.QUIT:
                #if user presses top right quit button on screen
                ExitWindow=True
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click
                x, y = event.pos
                a, b = event.pos
                #if the rectangular area of the image collides with mouse click
                if OffSound.get_rect().collidepoint(x,y):
                    pygame.mixer.music.stop()
                    musicStopped=True
                    
                #if the rectangular area of the image collides with mouse click

            #if user presses the s key, the music will be played again
            elif event.type == KEYDOWN:
                if event.key == K_s:
                    pygame.mixer.music.play(-1)
                    
                    
                
                
                
        pauseScreen.blit(menu, [0,0])
        pauseScreen.blit(OffSound, (23,10))
        #pauseScreen.blit(OnSound, (889,10))
        #draws background onto the game display
        #button("turn off sound",23,10,200,50,WHITE,OffSound)
        #button("turn on sound",893,10,200,50,WHITE,OnSound)'''
        button("continue",350,150,200,50,WHITE,unpause)
        #button to start game
        button("see instructions",350,250,200,50,WHITE,instructionsPage)
        #button to see instructions
        #button("see leaderboard",350,350,200,50,WHITE,see_LeaderboardPause)
        #button to see leaderboard
        button("quit",350,350,200,50,WHITE,pyQuit)

        pygame.display.update()



def gameOver(gameOverBg):
    paused=False
    w,h=933,600#width height of game over screen
    #displaying screen
    GOscreen=pygame.display.set_mode((w,h))
    #boolean value showing game has finished
    gameOver=True
    while gameOver:
        pygame.mixer.music.stop()
        for sprite in all_sprites:
            sprite.kill()
        for event in pygame.event.get():
            #collects events within the program
            if event.type == pygame.QUIT:
                #if user presses top right quit button on screen
                ExitWindow=True
                pygame.quit()
                quit()
        #draws background
        GOscreen.blit(gameOverBg, [0,0])
        #buttons of game
        button("back to main menu",150,150,200,50,WHITE,mainMenu)
        button("click to go on leaderboad",370,150,250,50,WHITE,Leaderboard)
        #button to see leaderboard
        button("quit",650,150,200,50,WHITE,pyQuit)
        #updates the display
        pygame.display.update()

def mainMenu():
    exitWindow=False
    #iniially has not left the window, boolean value is false

    while not exitWindow:
        for event in pygame.event.get():
            #collects events within the program
            if event.type == pygame.QUIT:
                #if user presses top right quit button on screen
                ExitWindow=True
                pygame.quit()
                quit()
            
        screen.blit(background, [0,0])
        #draws background onto the game display
        button("play game",350,150,200,50,WHITE,game)
        #button to start game
        button("see instructions",350,250,200,50,WHITE,instructionsPageMain)
        #button to see instructions
        button("see leaderboard",350,350,200,50,WHITE,see_Leaderboard)
        #button to see leaderboard
        button("quit",350,450,200,50,WHITE,pyQuit)

    
        pygame.display.update()


mainMenu()



'''pygame.quit()
quit()'''

