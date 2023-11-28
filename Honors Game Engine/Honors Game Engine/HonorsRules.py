import enum
from telnetlib import GA
import pygame
from multiprocessing import Event
import types
import EventAnimations
from HonorsIndicator import Indicator,HorizontalSweep,SetIndicators,VerticalSweep





#Define event types within the game
#These are used within the rules to check if an event matched a broad class of events.
#This way, you don't have to list every possible shot/event of that type within the if statement.
#For example, you may have a mode which looks for ramp shots, and you have three ramps in your game.
#Instead of listing every possible ramp shot in the if statements, you can just check if the event of a ramp type.
#Events can have more than one type.
class EventTypes(enum.Enum):

    #Game Specific Events
    MAIN_SHOT = enum.auto() #I use these to qualify modes
    SPINNER = enum.auto()
    POP_BUMPER = enum.auto()
    SLINGSHOT = enum.auto()
    RAMP_SHOT = enum.auto()
    TIME_TICK = enum.auto()
    ORBIT_SHOT = enum.auto()
    LOOP_SHOT = enum.auto()
    SWITCH_HIT = enum.auto()
    MODE_QUALIFIER = enum.auto()

#Define Game Event enumerations
class GameEvents(enum.Enum):

    #Don't change this
    def __new__(cls,*args, **kwds):
        #value = len(cls.__members__)+1
        value = args[0]
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    #Don't change this
    def __init__(self,init_event_mask,init_event_list):
        self.event_mask = init_event_mask
        self.types = init_event_list

    #This is where we define all the possible events within our game
    #Each event has an ID, switch mask, and list of event types

    #Don't change this group, these are the same accross all machines
    #Game Event         #Switch Mask    #Event type
    TIME_TICK =         None,           [EventTypes.TIME_TICK]
    START_PUSH =        [3,0x01],       []
    LAUNCH_PUSH =       [3,0x02],       []
    BALL_LAUNCH =       [3,0x04],       []
    BALL_DRAIN =        [3,0x08],       []
    TILT =              [3,0x01],       []
    BALL_END  =         [3,0x08],       []
    LEFT_FLIPPER =      [3,0x10],       []
    RIGHT_FLIPPER =     [3,0x20],       []
    LEFT_STROKE =       [3,0x40],       []
    RIGHT_STROKE =      [3,0x80],       []
    LAUNCH_SWITCH =     [1,0x02],       []

    #These events are specific to your particular machine and you can change these
    LEFT_ORBIT =        [4,0x01],     [EventTypes.MAIN_SHOT,EventTypes.ORBIT_SHOT,EventTypes.MODE_QUALIFIER]    
    LEFT_RAMP_EXIT =    [4,0x02],     [EventTypes.MAIN_SHOT,EventTypes.RAMP_SHOT,EventTypes.MODE_QUALIFIER]
    CENTER_SPINNER =    [4,0x04],     [EventTypes.MAIN_SHOT,EventTypes.SPINNER,EventTypes.MODE_QUALIFIER]
    RIGHT_RAMP_EXIT =   [4,0x08],     [EventTypes.MAIN_SHOT,EventTypes.RAMP_SHOT,EventTypes.MODE_QUALIFIER]
    RIGHT_ORBIT =       [4,0x10],     [EventTypes.MAIN_SHOT,EventTypes.ORBIT_SHOT,EventTypes.MODE_QUALIFIER]

    POP_0 =             [1,0x10],     [EventTypes.POP_BUMPER]
    POP_1 =             [1,0x20],     [EventTypes.POP_BUMPER]
    POP_2 =             [1,0x40],     [EventTypes.POP_BUMPER]
    SCOOP_0 =           [4,0x20],     [EventTypes.MAIN_SHOT]

#These are the mappings between key presses on your keyboard and events.
#This allows you to simulate events on the keyboard without the physical pinball hardware.
#You can reassign this if you want to your particular events
Keyboard_Mapping_Dict = {
    pygame.K_q:     GameEvents.BALL_DRAIN,
    pygame.K_w:     GameEvents.BALL_LAUNCH,
    pygame.K_e:     GameEvents.LEFT_FLIPPER,
    pygame.K_r:     GameEvents.RIGHT_FLIPPER,
    pygame.K_t:     GameEvents.LEFT_STROKE,
    pygame.K_y:     GameEvents.RIGHT_STROKE,
    pygame.K_u:     GameEvents.START_PUSH,
    
    pygame.K_i:     GameEvents.LAUNCH_SWITCH,
    pygame.K_a:     GameEvents.SCOOP_0,
    pygame.K_s:     GameEvents.LEFT_ORBIT,
    pygame.K_d:     GameEvents.LEFT_RAMP_EXIT,
    pygame.K_f:     GameEvents.CENTER_SPINNER,
    pygame.K_g:     GameEvents.RIGHT_RAMP_EXIT,
    pygame.K_h:     GameEvents.RIGHT_ORBIT,
    pygame.K_j:     None,

    pygame.K_k:     None,
    pygame.K_z:     GameEvents.POP_0,
    pygame.K_x:     GameEvents.POP_1,
    pygame.K_c:     GameEvents.POP_2,
    pygame.K_v:     None,
    pygame.K_b:     None,
    pygame.K_n:     None,
    pygame.K_m:     None,
    pygame.K_COMMA: None,

    pygame.K_LEFT:  GameEvents.LEFT_FLIPPER,
    pygame.K_RIGHT: GameEvents.RIGHT_FLIPPER,
    pygame.K_UP:    GameEvents.LAUNCH_PUSH,
    pygame.K_DOWN:  GameEvents.BALL_DRAIN,

    pygame.K_RETURN:  GameEvents.START_PUSH,
    pygame.K_BACKSPACE: GameEvents.BALL_DRAIN,
    pygame.K_SPACE: GameEvents.BALL_LAUNCH
}   


#This is the default scoring for particular shots when there isn't a special score implemented within your rules
Default_Scoring_Dict = {
    GameEvents.TIME_TICK: 0,
    GameEvents.SCOOP_0: 100,
    GameEvents.LEFT_ORBIT: 100,
    GameEvents.LEFT_RAMP_EXIT: 100,
    GameEvents.CENTER_SPINNER: 100,
    GameEvents.RIGHT_RAMP_EXIT: 100,
    GameEvents.RIGHT_ORBIT: 100,
    GameEvents.LEFT_FLIPPER: 0,
    GameEvents.LEFT_STROKE: 0,
    GameEvents.RIGHT_FLIPPER: 0,
    GameEvents.RIGHT_STROKE: 0
    }
   
#Default Scoring for when an event/shot isn't part of the active mode
#This is basically just a class wrapper for the dictionary above
#DON'T CHANGE THIS
def basic_scoring(event: GameEvents, m_vars):
    return Default_Scoring_Dict.get(event,100)

#This is a class containing the different background images you plan to use in your rules
class BackgroundImages():
    BEARCAT = pygame.transform.scale(pygame.image.load("Background_Images/Bearcat.png"),(1280,720))
    MONOGRAM = pygame.transform.scale(pygame.image.load("Background_Images/Monogram.png"),(1280,720))
    #Don't change this part
    def __init__(self) -> None:
        pass

#These are all of the different inserts you have on your playfield.
#You can change these and name them whatever you want
class Inserts(enum.Enum):
    POPBUMPER_A = enum.auto()
    POPBUMPER_B = enum.auto()

    IR_TOWER = enum.auto()
    IR_ROLLERCOASTER = enum.auto()
    IR_RAMP = enum.auto()

    ITALIAN_BOTTOM_RIGHT = enum.auto()
    ITALIAN_BOTTOM_LEFT = enum.auto()

    TRIPLE_DROP_TARGET = enum.auto()
    ROLLERCOASTER_TARGET_A = enum.auto()
    ROLLERCOASTER_TARGET_B = enum.auto()
    FRIEND_TARGET_A = enum.auto()
    FRIEND_TARGET_B = enum.auto()



    
#This function generates a dictionary of all the playfield inserts/indicators
#Each Insert/Indicator has four attributes that you will need to define
#Dictionary Key: This is the enumerator for the insert which you defined above in the Inserts class
#The other three attributes are passed to the Indicator initializer function
#Name: Name of the insert, this isn't really used within this version of the game engine, but you can still give it a name.
#Position: This a a list of x and y coordincates in inches: [x,y], which defines the location of the insert on the playfield.
#          These coordinates are used within some of LED animation functions. However, if you aren't using the premade animations,
#          you can just define the location as [0,0] or really any arbitrary position.
#Driver Mask: This defines which output of the I/O that insert is connected to. The first element of the list defines which bank,
#          and the second element defines which pin. The pin is defined as an 8-bit mask with a '1' in the postion corresponding
#          to desired output. For example, if you have an insert connected to the second pin of Bank 1, you would define the output 
#          mask as [1,0b00000010] if using binary representation or [1,0x02] if using hex representation. 
#TODO change the driver mask
def GeneratePlayfieldIndicators():
    temp_dict = {
        Inserts.FRIEND_TARGET_A: Indicator('',[0,0],[0,0x80]),
        Inserts.FRIEND_TARGET_B: Indicator('',[0,0],[0,0x40]),
        Inserts.ITALIAN_BOTTOM_LEFT: Indicator('',[0,0],[0,0x08]),
        Inserts.ITALIAN_BOTTOM_RIGHT: Indicator('',[0,0],[0,0x04]),
        Inserts.POPBUMPER_A: Indicator('',[0,0],[1,0x01]),
        Inserts.POPBUMPER_B: Indicator('',[0,0],[1,0x01]),
        Inserts.IR_TOWER: Indicator('',[0,0],[1,0x01]),
        Inserts.IR_RAMP: Indicator('',[0,0],[1,0x01]),
        Inserts.IR_ROLLERCOASTER: Indicator('',[8,0],[1,0x01]),
        Inserts.IR_ROLLERCOASTER: Indicator('',[8,0],[1,0x01]),
        Inserts.ROLLERCOASTER_TARGET_A: Indicator('',[8,0],[1,0x01]),
        Inserts.ROLLERCOASTER_TARGET_B: Indicator('',[8,0],[1,0x01]),
        Inserts.TRIPLE_DROP_TARGET: Indicator('',[8,0],[1,0x01])
        }
    return temp_dict



#Default Mode Display Function
#This function prints out mode state information to the output window
#DON'T CHANGE THIS
def default_mode_display(self):
    match self.display_detail:
        case 0:
            return 
        case 1:
            print(f"\tMode: {self.name}")
            return
        case 2:
            print(f"\tMode: {self.name}")
            temp_state = self.GetState()
            print(f"\t\t State: {temp_state.name}")
            vars_dict = vars(self.mode_vars)
            for var, value in vars_dict.items():
                print(f"\t\t", var, ": ", value)
            if len(self.alerts)>0:
                print(f"\t\t Alerts:")
                for alerts in self.alerts:
                    print(f"\t\t  {alerts}")
            return
        case 3:
            #print(f"\tMode: {self.name}")
            if len(self.alerts)>0:
                print(f"\tMode: {self.name}")
                print(f"\t\t Alerts:")
                for alerts in self.alerts:
                    print(f"\t\t  {alerts}")
            return

#Define Game Mode Class
#This defines the generic game mode class.
#DON'T CHANGE THIS
class GameMode:
    background_images = BackgroundImages()
    state_functions = {}
    display_handle = default_mode_display
    display_detail = 3
    alerts = []
    def __init__(self, init_name: str, init_state: str, func_handle: types.FunctionType, internal_variables):
        self.name = init_name
        self.current_state = init_state
        self.h_update = func_handle
        self.mode_vars = internal_variables

    def PrintMode(self):
        self.display_handle()
    
    def AddStateFunction(self, func_name: str, func_handle: types.FunctionType):
        temp_name = func_name.upper()
        self.state_functions[temp_name] = func_handle

    def GetState(self)-> str:
        return self.current_state

    def SetState(self, set_state: str):
        self.current_state = set_state.upper()

    def UpdateState(self, event: GameEvents,screen):
        (score,animation,led_animation,background) = self.h_update(self, event,screen)
        return (score, animation,led_animation,background)

#This is a wrapper function that creates a list of all your modes.
#Most of you will only need one mode (which may contain submodes), but hypothetically you
#can have multiple modes running in parallel.
#TODO
def GenerateModeList():
    #You must define three things for each mode
    #Mode States Enumerator: This is an enumerator class in which you define the states of the mode
    #Mode Variables Classes: This is a class containing any variables used within the mode
    #Mode State Transistion Function: This is a function that defines the state transistions between the states of the mode.
    #This is the heart of the rules and will include any scoring, graphics, sounds, and music calls as well.
    
    ##############################################################################################################
    #Mode States Enumerator
    ##############################################################################################################
    #Define States of Main Mode.
    #You can have submodes/substates that can be actived as well.
    class MainModeStates(enum.Enum):
        #This is the starting mode in which the player must with mode qualifier shots to qualify a mode
        QUALIFYING_MODES = enum.auto() 
        #Once enough qualifying shots are made, you move to the MODE_QUALIFIED state and awat for the player to hit the
        #Scoop shot
        MODE_QUALIFIED = enum.auto()
        #Once the scoop shot is made, the machine waits for you to select your mode
        MODE_SELECTION = enum.auto()
        #Mode A has three diferrent stages you progress through
        MODE_A_0 = enum.auto()
        MODE_A_1 = enum.auto()
        MODE_A_2 = enum.auto()
        #Mode B is time based and has just one state
        MODE_B = enum.auto()

    ##############################################################################################################
    #Mode Variable Class
    ##############################################################################################################
    #This class contains any internal variables for that particular mode
    class main_modes_var:
        def __init__(self):
            self.qualifying_shot_count = 0 #This keeps track of how many mode qualifying shots have been made
            self.mode_selection_index = 0 #This keeps track of which mode the user has selected
            self.time_count = 0 #This keeps track of the time remaining within Mode B

    ##############################################################################################################
    #Mode State Transition Function
    ##############################################################################################################
    #This contains the heart of the rules for your machine.
    #Essentially, we represent the rules as a gian state machine using the states defined above in the MainModeStates
    # enumerator and the events defined in the above GameEvents enumerator
    #This function will be called by the MachineClasses file (you don't need to worry about it), and will be passed an event.
    #You will then update your rules/state machine based on that event.
    #Within these rules, you will calculate/define four things
    #1) score: This variable stores the score recieved for event
    #2) animations: This is a list containing animation functions from the EventAnimations file. These functions draw graphics
    #               and text onto the display. You can append multiple animations/graphics to this list
    #3) led_animations: This is a list containing LED/insert animation function from teh HonorsIndicator file. This animations
    #               turn on or off the inserts on your playfield.
    def main_modes_st(self, event: GameEvents, screen):
        #initialize score variable to zero
        #this will get updated by the following code as needed
        score = 0 #Initialize score to zero, if your rules don't change it, it will return zero (which is okay)
        animations = [] #List of graphic animations
        led_animations = [] #List of LED/Insert Animations
        background = self.background_images.MONOGRAM #Background image, your rules can change this
        self.alerts = [] #This is used for game engine debugging purposes (Don't set or change)

        #update state machine and state transitions here
        #Case statement based on current mode state
        match self.current_state:
            #Currently qualifying a mode by making qualifying shots
            case MainModeStates.QUALIFYING_MODES:
                #These three line define a font, generate a text graphic using that font, then add the graphic animation to the list
                mode_font = pygame.font.Font('Guardians.ttf', 72)
                mode_text = mode_font.render("Shoot Main Shots",True, (0,0,0))
                #append image_splash_hold animaiton to animations list. 
                #Note that the duration is 1. This means it will only be shown for one frame, which is okay, because we redraw it every update 
                animations.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(640,300))))
                #Turn on main shot inserts. Note duration is 1.
                led_animations.append(SetIndicators('test',1,
                    [Inserts.LEFT_ORBIT,Inserts.LEFT_RAMP,Inserts.CENTER_SPINNER,Inserts.RIGHT_RAMP,Inserts.RIGHT_ORBIT],True,None))

                #Check if event is from a qualifying shot. Note we are checking the types list of the event.
                if EventTypes.MODE_QUALIFIER in event.types:
                    #Print debug output
                    print('Qualifying Shot')
                    #Create Shot Made text graphic and append to animation list
                    #Note this animation duration is 20 frames long.
                    mode_font = pygame.font.Font('Guardians.ttf', 72)
                    mode_text = mode_font.render("Shot Made",True, (0,0,0))
                    animations.append(EventAnimations.image_splash_hold(20,mode_text,mode_text.get_rect(center=(640,400))))
                    #Load and play sound effect for shot
                    shot_sound = pygame.mixer.Sound('blaster.wav')
                    shot_sound.set_volume(.3)
                    pygame.mixer.Sound.play(shot_sound)
                    #Increment qualifying shot count
                    self.mode_vars.qualifying_shot_count += 1
                    #Check if there is enough qualifying shots, then change state
                    if self.mode_vars.qualifying_shot_count >= 3:
                        self.current_state = MainModeStates.MODE_QUALIFIED
                        self.mode_vars.qualifying_shot_count = 0
                #This mode has no special scoring so just update score using the basic_scoring function
                score = basic_scoring(event,self.mode_vars)

            #Mode selection is qualified, waiting for scoop shot
            case MainModeStates.MODE_QUALIFIED:
                #Create text graphic
                mode_font = pygame.font.Font('Guardians.ttf', 72)
                mode_text = mode_font.render("Shoot The Scoop",True, (0,0,0))
                animations.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(640,300))))
                #Light up the Scoop insert and set to blinking
                led_animations.append(SetIndicators('test',1,[Inserts.SCOOP],False,30))
                #Check if scoop shot
                if event == GameEvents.SCOOP_0:
                    #Update state to mode selection menu
                    self.current_state = MainModeStates.MODE_SELECTION
                    self.mode_vars.mode_selection_index = 0
                #Update score using basic scoring rules
                score = basic_scoring(event,self.mode_vars)
            #Mode scoop shot and currently selecting mode
            case MainModeStates.MODE_SELECTION:
                #Create "select your mode" text graphic
                mode_font = pygame.font.Font('Guardians.ttf', 72)
                mode_text = mode_font.render("Select Your Mode",True, (0,0,0))
                animations.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(640,300))))

                #Check if right flipper button pressed
                if event == GameEvents.RIGHT_FLIPPER:
                    #Increment mode slection index
                    #Check for wrap around (this would be more interesting if we had more than two modes)
                    if self.mode_vars.mode_selection_index < 1:
                        self.mode_vars.mode_selection_index += 1
                    else:
                        self.mode_vars.mode_selection_index = 0
                if event == GameEvents.LEFT_FLIPPER:
                    #Decrement mode slection index
                    #Check for wrap around
                    if self.mode_vars.mode_selection_index > 0:
                        self.mode_vars.mode_selection_index -= 1
                    else:
                        self.mode_vars.mode_selection_index = 1
                
                #Update text indicating selected mode        
                if self.mode_vars.mode_selection_index == 0:
                    led_animations.append(SetIndicators('test',1,[Inserts.LEFT_RAMP],True,None))
                    mode_font = pygame.font.Font('Guardians.ttf', 72)
                    mode_text = mode_font.render("Mode A",True, (0,0,0))
                    animations.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(640,400))))
                else:
                    led_animations.append(SetIndicators('test',1,[Inserts.RIGHT_RAMP],True,None))
                    mode_font = pygame.font.Font('Guardians.ttf', 72)
                    mode_text = mode_font.render("Mode B",True, (0,0,0))
                    animations.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(640,400))))
                
                #If start button is hit, activate selected mode
                if event == GameEvents.BALL_LAUNCH:
                    #Add a sweeping animation for inserts
                    led_animations.append(HorizontalSweep('Test Sweep',.3,None,1,-1.1))
                    #Update state (for submodes) and change background music
                    if self.mode_vars.mode_selection_index == 0:
                        self.current_state = MainModeStates.MODE_A_0
                        pygame.mixer.music.load('Salvation Code.mp3')
                        pygame.mixer.music.play(-1)
                    else:
                        self.current_state = MainModeStates.MODE_B
                        self.mode_vars.time_count = 900
                        pygame.mixer.music.load('2517.mp3')
                        pygame.mixer.music.play(-1)

                #Calculate score using basic scoring
                score = basic_scoring(event,self.mode_vars)

            #The first step of the Mode A sequence of shots
            case MainModeStates.MODE_A_0:
                #Instruct which shot to make
                mode_font = pygame.font.Font('Guardians.ttf', 72)
                mode_text = mode_font.render("Shoot the Left Ramp",True, (0,0,0))
                animations.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(640,300))))
                #If that shot was made, award 1000 points and progress to next state
                if event == GameEvents.LEFT_RAMP_EXIT:
                    score = 1000
                    self.current_state = MainModeStates.MODE_A_1
                #If it was another shot, apply basic scoring
                else:
                    score = basic_scoring(event,self.mode_vars)
                #If the ball ends during this mode, end mode and go back to qualifying shots
                if event == GameEvents.BALL_END:
                    self.current_state = MainModeStates.QUALIFYING_MODES
            #The second shot of Mode A
            case MainModeStates.MODE_A_1:
                #Instruct player on which shot to make
                mode_font = pygame.font.Font('Guardians.ttf', 72)
                mode_text = mode_font.render("Shoot the Right Ramp",True, (0,0,0))
                animations.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(640,300))))
                #If correct shot was made, award 1000 points
                if event == GameEvents.RIGHT_RAMP_EXIT:
                    score = 1000
                    self.current_state = MainModeStates.MODE_A_2
                else:
                    score = basic_scoring(event,self.mode_vars)
                #If ball ends, go back to qualifying shots
                if event == GameEvents.BALL_END:
                    self.current_state = MainModeStates.QUALIFYING_MODES
            #The third and final shot of Mode A
            case MainModeStates.MODE_A_2:
                #Instruct which shot to make
                mode_font = pygame.font.Font('Guardians.ttf', 72)
                mode_text = mode_font.render("Shoot Center Spinner",True, (0,0,0))
                animations.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(640,300))))
                #If shot made award points
                if event == GameEvents.CENTER_SPINNER:
                    score = 5000
                    #End mode and go back to qualifying modes
                    self.current_state = MainModeStates.QUALIFYING_MODES
                #Otherwise award basic scoring
                else:
                    score = basic_scoring(event,self.mode_vars)
                #If ball ends, end mode and go back to qualifying modes
                if event == GameEvents.BALL_END:
                    self.current_state = MainModeStates.QUALIFYING_MODES
            case MainModeStates.MODE_B:
                #Change background for this mode
                background = self.background_images.BEARCAT
                #Instruct player which shot to make
                mode_font = pygame.font.Font('Guardians.ttf', 72)
                mode_text = mode_font.render("Shoot Center Spinner",True, (0,0,0))
                animations.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(640,300))))
                mode_font = pygame.font.Font('Guardians.ttf', 72)
                #Show time remaining in this mode
                mode_text = mode_font.render(f"Count Down {int(self.mode_vars.time_count/30)}",True, (0,0,0))
                animations.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(640,400))))                
                #If it is a timer tick event, update time remaining
                if event == GameEvents.TIME_TICK:
                    self.mode_vars.time_count -= 1
                    #If out of time, reset back to qualifying modes.
                    if self.mode_vars.time_count <= 0:
                        self.current_state = MainModeStates.QUALIFYING_MODES
                #If spinner shot made, award points
                if event == GameEvents.CENTER_SPINNER:
                    score = 500
                #Otherwise use basic scoring
                else:
                    score = basic_scoring(event,self.mode_vars)
                #If ball ends, reset to qualifying modes
                if event == GameEvents.BALL_END:
                    self.current_state = MainModeStates.QUALIFYING_MODES
        
        #Return results of event
        return (score,animations,led_animations,background)

    #Create Main Mode using states, state transitions, and variables
    main_mode = GameMode('Main Mode',MainModeStates.QUALIFYING_MODES,main_modes_st,main_modes_var())

    #Create list of all modes (you will probably only have one)
    mode_list = [main_mode]
    #Return list of modes
    return mode_list