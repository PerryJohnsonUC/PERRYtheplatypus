import enum
import pygame
import EventAnimations
from GameParameters import EventTypes, GameEvents, GameMode


#Define main mode states
class GeneralModeStates(enum.Enum):
    INITIAL = enum.auto()


#Define main mode internal variables
class general_mode_vars:
    ramp_count = 0
    orbit_count = 0
    spin_count = 0
    pop_count = 0
    loop_count = 0

    ramp_skill = 0
    orbit_skill = 0
    spin_skill = 0
    pop_skill = 0
    loop_skill = 0

    ramp_score = 10
    orbit_score = 10
    spin_score = 10
    pop_score = 10
    loop_score = 10

    text = "You got skills"

def general_mode_st(self,event: GameEvents,screen):
    score =0
    light_show = []
    self.alerts = []
    #mode_font = pygame.font.Font('Guardians.ttf', 17)
	#mode_text = mode_font.render(f'{self.mode_vars.}',True, (255,255,255))
    skill_font = pygame.font.Font('Guardians.ttf', 12)

    match self.current_state:
        case GeneralModeStates.INITIAL:
            #Draw shot counts
            ramp_text = skill_font.render(f'{self.mode_vars.ramp_count}',True,(255,255,255))
            light_show.append(EventAnimations.image_splash_hold(1,ramp_text,ramp_text.get_rect(center=(1224,75))))
            
            skill_text = skill_font.render(f'{self.mode_vars.orbit_count}',True,(255,255,255))
            light_show.append(EventAnimations.image_splash_hold(1,skill_text,skill_text.get_rect(center=(1224,75+40))))           
            
            skill_text = skill_font.render(f'{self.mode_vars.spin_count}',True,(255,255,255))
            light_show.append(EventAnimations.image_splash_hold(1,skill_text,skill_text.get_rect(center=(1224,75+80))))               
            
            skill_text = skill_font.render(f'{self.mode_vars.pop_count}',True,(255,255,255))
            light_show.append(EventAnimations.image_splash_hold(1,skill_text,skill_text.get_rect(center=(1224,75+120))))           
            
            skill_text = skill_font.render(f'{self.mode_vars.loop_count}',True,(255,255,255))
            light_show.append(EventAnimations.image_splash_hold(1,skill_text,skill_text.get_rect(center=(1224,75+160))))             

    if EventTypes.RAMP_SHOT in event.types:
        self.mode_vars.ramp_count += 1
        if(self.mode_vars.ramp_count>10):
            self.mode_vars.ramp_count=0
            if(self.mode_vars.ramp_skill<10):
                self.mode_vars.ramp_skill += 1
        score += int(self.mode_vars.ramp_score*(1+self.mode_vars.ramp_skill/10))

    if EventTypes.ORBIT_SHOT in event.types:
        self.mode_vars.orbit_count += 1
        if(self.mode_vars.orbit_count>10):
            self.mode_vars.orbit_count=0
            if(self.mode_vars.orbit_skill<10):
                self.mode_vars.orbit_skill += 1

    if EventTypes.SPINNER in event.types:
        self.mode_vars.spin_count += 1
        if(self.mode_vars.spin_count>10):
            self.mode_vars.spin_count=0
            if(self.mode_vars.spin_skill<10):
                self.mode_vars.spin_skill += 1

    if EventTypes.POP_BUMPER in event.types:
        self.mode_vars.pop_count += 1
        if(self.mode_vars.pop_count>10):
            self.mode_vars.pop_count=0
            if(self.mode_vars.pop_skill<10):
                self.mode_vars.pop_skill += 1

    if EventTypes.LOOP_SHOT in event.types:
        self.mode_vars.loop_count += 1
        if(self.mode_vars.loop_count>10):
            self.mode_vars.loop_count=0
            if(self.mode_vars.loop_skill<10):
                self.mode_vars.loop_skill += 1
        
    if event == GameEvents.TIME_TICK:
        skillbar_image = pygame.image.load("SkillBar.png")
        for i in range(1,self.mode_vars.ramp_skill+1):
            light_show.append(EventAnimations.image_splash_hold(1,skillbar_image,skillbar_image.get_rect(center=(1132+6*(i-1),75))))

        for i in range(1,self.mode_vars.orbit_skill+1):
            light_show.append(EventAnimations.image_splash_hold(1,skillbar_image,skillbar_image.get_rect(center=(1132+6*(i-1),75+40))))

        for i in range(1,self.mode_vars.spin_skill+1):
            light_show.append(EventAnimations.image_splash_hold(1,skillbar_image,skillbar_image.get_rect(center=(1132+6*(i-1),75+80))))

        for i in range(1,self.mode_vars.pop_skill+1):
            light_show.append(EventAnimations.image_splash_hold(1,skillbar_image,skillbar_image.get_rect(center=(1132+6*(i-1),75+120))))

        for i in range(1,self.mode_vars.loop_skill+1):
            light_show.append(EventAnimations.image_splash_hold(1,skillbar_image,skillbar_image.get_rect(center=(1132+6*(i-1),75+160))))
    
    return (score,light_show)

#TODO
def GenerateModeList():

    #Define Ball Lock internal states
    class BallLockModeStates(enum.Enum):
        INITIAL = enum.auto()
        LOCKED_1 = enum.auto()
        LOCKED_2 = enum.auto()
        MULTI_ACTIVATED = enum.auto()

    #Define ball lock internal variables
    class ball_lock_vars:
        def __init__(self):
            self.count = 0

    #Define Ball Lock state transitions
    def ball_lock_st(self, event: GameEvents, screen):
        score = 0
        light_show = []
        self.alerts = []

        match self.current_state:

            case BallLockModeStates.INITIAL:
                if event == GameEvents.LEFT_RAMP_EXIT:
                    score = 100
                    self.current_state = BallLockModeStates.LOCKED_1
            case BallLockModeStates.LOCKED_1:
                if event == GameEvents.CENTER_SPINNER:
                    score = 200
                    self.current_state = BallLockModeStates.LOCKED_2
            case BallLockModeStates.LOCKED_2:
                if event == GameEvents.RIGHT_RAMP_EXIT:
                    score = 500
                    self.current_state = BallLockModeStates.MULTI_ACTIVATED
                    self.mode_vars.count = 0
                    self.alerts.append('Multiball Activated')
                    light_show.append(EventAnimations.text_splash_hold(130,'Eli & Emmy',100,(0,-140)))
                    light_show.append(EventAnimations.text_splash_hold(130,'Multiball Activated',100, (0,0)))
                    blaster_sound = pygame.mixer.Sound('EEMultiball_Robot.wav')
                    #blaster_sound.set_volume(1)
                    pygame.mixer.Sound.play(blaster_sound)
                    #light_show =  DisplayText('Multiball Activated',40,screen)
                    #print('Multiball Activated')
            case BallLockModeStates.MULTI_ACTIVATED:
                if event == GameEvents.TIME_TICK:
                    self.mode_vars.count = self.mode_vars.count+1
                if (self.mode_vars.count>300):
                    self.current_state = BallLockModeStates.INITIAL
                    self.mode_vars.count =0
                    self.alerts.append('Multiball Timed Out')
                    light_show.append(EventAnimations.text_splash_hold(120,'Multiball Timed Out',100, (0,0)))
                    #print('Multiball Timed Out')
        return (score,light_show)

    def ball_lock_mode_display(self, detail: int):
        match detail:
            case 0:
                return
            case 1:
                print(f"\tMode: {self.name}")
                return
            case 2:
                print(f"\tMode: {self.name}")
                temp_state = self.GetState()
                print(f"\t\t State: {temp_state.name}")
                print(f"\t\t Count: {self.mode_vars.count}")
                if len(self.alerts)>0:
                    print(f"\t\t Alerts:")
                    for alerts in self.alerts:
                        print(f"\t\t  {alerts}")
                return
            case _:
                return

    test_mode = GameMode('Test Mode',BallLockModeStates.INITIAL,ball_lock_st,ball_lock_vars())

    #Define main mode states
    class MainModeStates(enum.Enum):
        INITIAL = enum.auto()
        QUALIFIED = enum.auto()
        ACTIVATED = enum.auto()

    #Define main mode internal variables
    class main_mode_vars:
        qualified_shots = 0
        sprite_hold = []
        text = "Hit Main Shots"

    #init_main_mode_vars = main_mode_vars()

    def main_mode_st(self,event: GameEvents,screen):
        score =0
        light_show = []
        self.alerts = []
        #mode_font = pygame.font.Font('Guardians.ttf', 17)
		#mode_text = mode_font.render(f'{self.mode_vars.}',True, (255,255,255))
        match self.current_state:
            case MainModeStates.INITIAL:
                mode_font = pygame.font.Font('Guardians.ttf', 17)
                mode_text = mode_font.render("Shoot Main Shots",True, (255,255,255))
                light_show.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(207,80))))
                if EventTypes.MAIN_SHOT in event.types:
                    self.mode_vars.qualified_shots += 1
                    shot_sound = pygame.mixer.Sound('blaster.wav')
                    shot_sound.set_volume(.3)
                    pygame.mixer.Sound.play(shot_sound)
                    if self.mode_vars.qualified_shots > 9:
                        self.current_state = MainModeStates.QUALIFIED
                        self.mode_vars.qualified_shots = 0
                        self.alerts.append('Main mode qualified')
                        temp_sprite = EventAnimations.text_splash_hold(120,'Activated',100, (0,100))
                        self.mode_vars.sprite_hold = temp_sprite
                        light_show.append(temp_sprite)
                    #print('Main mode qualified')
                progress_image = pygame.image.load("Mode_Level.png")
                if event == GameEvents.TIME_TICK:
                    for count in range(0,self.mode_vars.qualified_shots+1):
                        if count>0:
                            #progress_image = pygame.image.load("Mode_Level.png")
                            temp_sprite1 = EventAnimations.image_splash_hold(1,progress_image,(32+(32*(count-1)),95))
                            light_show.append(temp_sprite1)
                            temp_sprite2 = EventAnimations.image_splash_hold(1,progress_image,(32+(32*(count-1))+16,95))
                            light_show.append(temp_sprite2)
                        #screen.blit(progress_image,(879+(32*(count-1)),95))
                        #screen.blit(progress_image,(879+(32*(count-1))+16,95))
            case MainModeStates.QUALIFIED:
                if EventTypes.SPINNER in event.types:
                    self.current_state = MainModeStates.INITIAL
                    self.alerts.append('Main Jackpot')
                    light_show.append(EventAnimations.sprite_splash_hold(120,'Main Jackpot',100, (0,100)))
                    jackpot_sound = pygame.mixer.Sound('EliJackpot.wav')
                    jackpot_sound.set_volume(1)
                    pygame.mixer.Sound.play(jackpot_sound)
                    #print('Main Jackpot')
                    score = 1000
                elif event == GameEvents.LEFT_RAMP_EXIT:
                    self.current_state = MainModeStates.INITIAL
                    light_show.append(EventAnimations.text_splash_hold(120,'Deactivated',100, (0,100)))
                    #self.mode_vars.sprite_hold.active = FALSE                
                
                if(event == GameEvents.TIME_TICK):
                    mode_font = pygame.font.Font('Guardians.ttf', 17)
                    mode_text = mode_font.render("Center Jackpot",True, (255,255,255))
                    light_show.append(EventAnimations.image_splash_hold(1,mode_text,mode_text.get_rect(center=(207,80))))
                    progress_image = pygame.image.load("Mode_Level.png")
                    for count in range(1,11):
                        #progress_image = pygame.image.load("Mode_Level.png")
                        temp_sprite1 = EventAnimations.image_splash_hold(1,progress_image,(32+(32*(count-1)),95))
                        light_show.append(temp_sprite1)
                        temp_sprite2 = EventAnimations.image_splash_hold(1,progress_image,(32+(32*(count-1))+16,95))
                        light_show.append(temp_sprite2)

        
        return (score,light_show)

    #Create main mode
    main_mode = GameMode('Main Mode',MainModeStates.INITIAL,main_mode_st,main_mode_vars())

    #Create general mode
    general_mode = GameMode('General Mode',GeneralModeStates.INITIAL,general_mode_st,general_mode_vars())

    #Create list of modes
    mode_list = [test_mode,main_mode,general_mode]
    #mode_list = [test_mode,main_mode]
    return mode_list