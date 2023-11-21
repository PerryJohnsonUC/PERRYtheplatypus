import enum
import pygame
from HonorsRules import EventTypes, GameEvents, GameMode, GeneratePlayfieldIndicators, Inserts
#from GameListGeneration import GenerateModeList
from HonorsRules import GenerateModeList
from HonorsIndicator import SetIndicators


#Define settings for machine
class Machine_Settings:
	balls_per_game = 3
	ball_save_time = 20 #In seconds
	n_max_players = 4
	def __init_(self):
		pass



#Define class for player
class Player:
	mode_list = [] #List containing active modes
	indicator_dict = {} #Dictionary of playfield indicators (inserts)
	ball_count = 1 #Current ball number
	extra_ball_count = 0 #Any extra balls available
	total_score = 0 #Player score


	def __init__(self):
		self.mode_list = GenerateModeList()



	#Update method used to update game state for specific event
	def update(self,event,machine):
		#Loop through each active mode in mode list
		for mode in self.mode_list:
			#Update mode and store score from that mode and any screen splash (graphics, text, etc.)
			(score, display_splash, led_animations,background) = mode.UpdateState(event,None)
			#If there is any kind of splash effect add it to the animation list
			if(display_splash):
				machine.animation_list.extend(display_splash)
			#If there is any kind of led effect add it to the led animation list
			if(led_animations):
				machine.led_animation_list.extend(led_animations)
			machine.background = background

			#Add score from mode to the total score
			self.total_score = self.total_score+score
			#Print any debug output from mode
			mode.PrintMode()
		#If it isn't just a time tick event, output total score to debug screen
		if(event != GameEvents.TIME_TICK):
			print(f'Total Score: {self.total_score}')
	
	#End ball
	def end_ball(self):
		for mode in self.mode_list:
			#Update mode and store score from that mode and any screen splash (graphics, text, etc.)
			(score, display_splash, led_animations,background) = mode.UpdateState(GameEvents.BALL_END,None)
		#Check for extra ball
		if self.extra_ball_count>0:
			self.extra_ball_count -= 1
		else:
			self.ball_count += 1

	#Start ball
	def start_ball(self):
		pass

class MachineStates(enum.Enum):
	ATTRACT_MODE = enum.auto()
	START_MODE = enum.auto()
	PLAY_MODE = enum.auto()


#Machine class
class Machine:
	player_count = 0 #How many players
	active_player = None #Which player is active
	active_player_index = 0
	player_list = [] #List containing all active players (of player type)
	machine_state = MachineStates.ATTRACT_MODE #Start in attract_mode
	machine_settings = Machine_Settings() #Class containing machine settings
	animation_list = [] #List containing all animations/sprites
	led_animation_list = [] #List of LEDs to activate
	ball_count =0
	max_animations = 0
	led_states = [0,0,0]
	blink_count = 0
	playfield_inserts = {} #Dictionary containing all playfield inserts
	background = []
	attract_background = pygame.transform.scale(pygame.image.load("Background_Images/P&F.jpg"),(1280,720))

	def __init__(self) -> None:
		self.playfield_inserts = GeneratePlayfieldIndicators()

	def update(self,event_list,screen):
		self.blink_count += 1
		font = pygame.font.Font(None, 20)
		
		#Display info frame

		#frame_image = pygame.image.load("Frame.png")
		#screen.blit(frame_image,(0,0))



		match self.machine_state:
			case MachineStates.ATTRACT_MODE:
				screen.blit(self.attract_background, (0,0))
				if GameEvents.START_PUSH in event_list:
					if self.player_count < self.machine_settings.n_max_players:
						self.ball_count =1
						self.player_list = []
						temp_player = Player()
						self.player_list.append(temp_player)
						self.player_count = 1
						self.active_player_index = 0
						self.active_player = self.player_list[self.active_player_index]
						pygame.mixer.music.load('worky.mp3')
						pygame.mixer.music.play(-1)
						self.machine_state = MachineStates.PLAY_MODE
						
						
			case MachineStates.PLAY_MODE:

				#pygame.mixer.music.set_volume(.1)
				#Check for end of ball
				if GameEvents.BALL_END in event_list: #End of ball detected, end player
					self.animation_list = []
					if self.active_player.extra_ball_count > 0:
						#End player
						self.active_player.end_ball()
					else:
						#End player
						self.active_player.end_ball()
						#If it isn't the last player for this ball, move to next player
						self.active_player_index += 1 #Increment player

						if (self.active_player_index<self.player_count):			
							self.active_player = self.player_list[self.active_player_index]
						else: #Else, it is the last player
							#Reset to player 1
							self.active_player_index=0
							#If it isn't the last ball of the game
							if self.ball_count<self.machine_settings.balls_per_game:
								#Go back to player 1
								
								self.active_player = self.player_list[self.active_player_index]
								self.ball_count += 1
							else:
								self.machine_state = MachineStates.ATTRACT_MODE

				else:
					#Check for start button push
					if GameEvents.START_PUSH in event_list:
						if (self.player_count < self.machine_settings.n_max_players) and (self.active_player.ball_count==1):
							temp_player = Player()
							self.player_list.append(temp_player)
							self.player_count += 1
					#Loop through events and update modes for active player
					for event in event_list:
						#print event name (if not generic time tick)
						if((event != GameEvents.TIME_TICK) and (event is not None)):
							print(f'Event: {event.name}')
						self.active_player.update(event,self)
					#After all modes are updated, loop through list of animations
					
					screen.blit(self.background, (0,0))
					#Loop through animations and display on screen
					for animation in self.animation_list[:]:
						#print(str(animation))
						if animation.update(screen):
							self.animation_list.remove(animation)
					
					#Reset all indicators to off
					

					#Loop through LED animations and update LED states
					clear_animation = SetIndicators('Clear Inserts',1,None,False,None)
					clear_animation.update(self.playfield_inserts)
					for led_animation in self.led_animation_list[:]:
						#update led animation and remove if duration is zero or less
						if led_animation.update(self.playfield_inserts):
							self.led_animation_list.remove(led_animation)

					#Loop through playfield indicators and update led_buffer arrays
					self.led_states = [0,0,0]
					for led in self.playfield_inserts.values():
						led.set_buffer(self.led_states,self.blink_count)

					#bg = pygame.image.load(background_name)
					#scaled_bg = pygame.transform.scale(bg,(1280,720))


					screen_width,screen_height = screen.get_size()
					score_spacing = screen_width/4
					count =0
					score_font = pygame.font.Font('Guardians.ttf', 25)
					
					active_font = pygame.font.Font('Guardians.ttf', 40)
					active_text = active_font.render(f'{self.active_player.total_score}',True, (0,0,0))
					screen.blit(active_text, active_text.get_rect(center = tuple(map(sum,zip(screen.get_rect().center,(0,-270))))))
					
					player_font = pygame.font.Font('Guardians.ttf', 17)
					player_text = player_font.render(f'Player {self.active_player_index+1}',True, (0,0,0))
					screen.blit(player_text, player_text.get_rect(center = tuple(map(sum,zip(screen.get_rect().center,(0,-340))))))
					
					ball_font = pygame.font.Font('Guardians.ttf', 40)
					ball_text = ball_font.render(f'{self.ball_count}',True, (0,0,0))
					screen.blit(ball_text, ball_text.get_rect(center=(955,97)))



					#active_text = active_font.render(f'{self.active_player.total_score}',True, (202,68,167))
					for player in self.player_list:

						score_text = score_font.render(f'{player.total_score}',True, (0,0,0))
						
						x_offset = score_spacing/2 + count*score_spacing
						y_offset = screen_height-30
						offset = (x_offset,y_offset)
						count += 1
						screen.blit(score_text, score_text.get_rect(center = (offset)))



						




