import enum
from multiprocessing import Event
import types

#Define screen characteristics
#screen_width = 1480
#screen_height = 768

#Define General Game Events



#Define event types within the game
#These are used within the rules to check if an event matched a broad class of events.
#This way, you don't have to list every possible shot/event of that type within the if statement.
#For example, you may have a mode which looks for ramp shots, and you have three ramps in your game.
#Instead of listing every possible ramp shot in the if statements, you can just check if the event of a ramp type.
#Events can have more than one type.
class EventTypes(enum.Enum):

    #Game Specific Events
    MAIN_SHOT = enum.auto()
    SPINNER = enum.auto()
    POP_BUMPER = enum.auto()
    SLINGSHOT = enum.auto()
    RAMP_SHOT = enum.auto()
    TIME_TICK = enum.auto()
    ORBIT_SHOT = enum.auto()
    LOOP_SHOT = enum.auto()
    SWITCH_HIT = enum.auto()


#Define Game Event enumerations
class GameEvents(enum.Enum):

    def __new__(cls,*args, **kwds):
        #value = len(cls.__members__)+1
        value = args[0]
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self,init_event_mask,init_event_list):
        self.event_mask = init_event_mask
        self.types = init_event_list

    #This is where we define all the possible events within our game
    #Each event has an ID and list of event types
    LEFT_RAMP_EXIT =    0,      [EventTypes.MAIN_SHOT,EventTypes.RAMP_SHOT]
    CENTER_SPINNER =    1,      [EventTypes.MAIN_SHOT,EventTypes.SPINNER]
    RIGHT_RAMP_EXIT =   2,      [EventTypes.MAIN_SHOT,EventTypes.RAMP_SHOT]
    RIGHT_ORBIT =       9,      [EventTypes.MAIN_SHOT,EventTypes.ORBIT_SHOT]
    LEFT_ORBIT =        10,     [EventTypes.MAIN_SHOT,EventTypes.ORBIT_SHOT]
    POP_0 =             11,     [EventTypes.POP_BUMPER]

    TIME_TICK =         None,   [EventTypes.TIME_TICK]
    #General Game Event
    START_PUSH =        3,      []
    LAUNCH_PUSH =       4,      []
    BALL_LAUNCH =       5,      []
    BALL_DRAIN =        6,      []
    TILT =              7,      []
    BALL_END  =         8,      []

#Default Mode Display Function
#This function prints out mode state information to the output window
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
class GameMode:
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
        (score,lightshow) = self.h_update(self, event,screen)
        return (score, lightshow)
