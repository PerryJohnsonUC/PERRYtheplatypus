



# import package pygame
from cgi import test
from functools import total_ordering
from platform import node
from tkinter.messagebox import NO
import pygame
import os
import enum
import types
from GameParameters import EventTypes, GameEvents, GameMode
from GameListGeneration import GenerateModeList
from MachineClasses import Machine
from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController
#import spidev

# We only have SPI bus 0 available to us on the Pi
bus = 0

#Device is the chip select pin. Set to 0 or 1, depending on the connections
device = 1

# Enable SPI
Ftdi.show_devices()
spi = SpiController()
spi.configure('ftdi://ftdi:232h:/1')
spi_port = spi.get_port(cs=0, freq=250E3, mode=0)# Assuming D3 is used for chip select.

msg = [0x76]

pygame.init()

pygame.font.init()
pygame.mixer.pre_init(44100,-16,1,1024)
pygame.mixer.init();
#amixer set PCM -- 1000
  
score = 0;  
 
clock = pygame.time.Clock()
  
# Form screen with 400x400 size
# and with resizable
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
  
# set title
pygame.display.set_caption('Resizable')

# Set up the font object
font = pygame.font.Font(None, 36)  

background_name = "Background_Images/frame_00_delay-0.1s.jpg"


blaster_sound = pygame.mixer.Sound('blaster.wav')
blaster_sound.set_volume(1)

pygame.mixer.music.load('Background.mp3')

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.1)

old_data = 0;
# run window
running = True
cool_down = 0;
bg_frame_index =0

mode_list = GenerateModeList()

count = 0
total_score = 0

mecha_font = pygame.font.Font('marspolice_i.ttf', 24)

test_machine = Machine()

class test_sprite(pygame.sprite.Sprite):
	def __init__(self) -> None:
		
		temp = pygame.image.load("Jackpot_alpha.png").convert_alpha()
		self.surf = pygame.transform.scale_by(temp,(2,2))
		self.surf.set_colorkey((255,255,255),pygame.RLEACCEL)
		self.rect = self.surf.get_rect()

amazing_sprite = test_sprite()


test_animation_list = []

bg_delay = 2
bg_update_count = bg_delay


while running:

	#Draw blank screen
	screen.fill((0, 0, 0))
	
	#Draw background animation
	# (to improve performance, it would better to preload all of these frames in a list at
	# startup and then index here)
	bg_update_count += 1
	if bg_update_count >= bg_delay:
		background_name = "Background_Images/frame_"+ str(bg_frame_index).zfill(2) + "_delay-0.1s.jpg"
		if bg_frame_index < 71:
			bg_frame_index += 1
		else:
			bg_frame_index = 0
		bg = pygame.image.load(background_name)
		large_bg = pygame.transform.scale(bg,(1280,568))
		bg_update_count = 0

	screen.blit(large_bg, (0,75))

	#Create event list and preload with time tick event
	test_event_list = [GameEvents.TIME_TICK]
	

	#This is were we would get node board info via spi and check for machine events
	write_buf = bytearray([0x11,0x22,0x33,0x44,4,5,6])
	node_board_events = spi_port.exchange(out=write_buf,readlen=0,start=True,stop=True,duplex=True)
	#print(node_board_events.hex())
	####################################################
	#Parse node board data
	####################################################
	switch_states_0 = node_board_events[1]
	switch_states_1 = node_board_events[2]
	falling_edges_0 = node_board_events[3]
	falling_edges_1 = node_board_events[4]
	#print('Switch States 0:'+ switch_states_0.to_bytes().hex())

	#####################################################
	#Check for events (mostly falling edges)
	#####################################################
	if falling_edges_0 & 0b00000001:
		print('Falling Edge')
		test_event_list.append(GameEvents.LEFT_RAMP_EXIT)
	if falling_edges_0 & 0b00000010:
		test_event_list.append(GameEvents.CENTER_SPINNER)
	if falling_edges_0 & 0x04:
		test_event_list.append(GameEvents.RIGHT_RAMP_EXIT)
	if falling_edges_0 & 0x08:
		test_event_list.append(GameEvents.LEFT_ORBIT)
	if falling_edges_0 & 0x10:
		test_event_list.append(GameEvents.RIGHT_ORBIT)	
	if falling_edges_0 & 0x20:
		test_event_list.append(GameEvents.BALL_END)
	if falling_edges_0 & 0x40:
		test_event_list.append(GameEvents.START_PUSH)		

	#Loop through pygames events and check for key presses
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				test_event_list.append(GameEvents.LEFT_RAMP_EXIT)
			if event.key == pygame.K_s:
				test_event_list.append(GameEvents.CENTER_SPINNER)
			if event.key == pygame.K_d:
				test_event_list.append(GameEvents.RIGHT_RAMP_EXIT)
			if event.key == pygame.K_p:
				test_event_list.append(GameEvents.START_PUSH)
			if event.key == pygame.K_BACKSPACE:
				test_event_list.append(GameEvents.BALL_END)
			if event.key == pygame.K_e:
				test_event_list.append(GameEvents.RIGHT_ORBIT)
			if event.key == pygame.K_q:
				test_event_list.append(GameEvents.LEFT_ORBIT)
			if event.key == pygame.K_w:
				test_event_list.append(GameEvents.POP_0)

	#Update high level game states	
	test_machine.update(test_event_list,screen)


	
	

	
	#screen.blit(amazing_sprite.surf ,(500,300))
	
	#list_data = spi.xfer2(msg)
	list_data = (0,1)
	data = list_data[0]
	



	# Update the display
	pygame.display.flip()
	
	# Limit the frame rate
	clock.tick(30)
	
  
# quit pygame after closing window
pygame.quit()