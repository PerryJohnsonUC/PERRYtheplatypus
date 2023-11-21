# import package pygame
from cgi import test
from functools import total_ordering
from platform import node
from tkinter.messagebox import NO
import pygame
import os
import enum
import types
from HonorsRules import EventTypes, GameEvents, GameMode
from HonorsRules import GenerateModeList
from MachineClasses import Machine
from HonorsRules import Keyboard_Mapping_Dict
from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController
from HonorsIndicator import Indicator
#import spidev





# Enable SPI using ftdi chip
#Ftdi.show_devices()
#devices = Ftdi.list_devices()
devices = []
if len(devices)>0:
	print('FTDI Detected')
	spi_present = True
	spi = SpiController()
	spi.configure('ftdi://ftdi:232h:/1')
	spi_port = spi.get_port(cs=0, freq=250E3, mode=0)# Assuming D3 is used for chip select.
else:
	spi_present = False
	print('FTDI Not Detected. Running in Debug Mode')

msg = [0x76]

#Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100,-16,1,1024)
pygame.mixer.init()
#Create game clock
clock = pygame.time.Clock()

# Form screen with 1280x720 size
# and with resizable
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))  

# set title
pygame.display.set_caption('Honors Pinball Engine P&F')

#Define starting background image
background_name = "Background_Images/Monogram.png" 

test_machine = Machine()




# run window
running = True

pygame.mixer.music.load('P&FTheme.mp3')
pygame.mixer.music.play(-1)

while running:

	#Draw blank screen
	screen.fill((0, 0, 0))
	
	#Create event list and preload with time tick event
	test_event_list = [GameEvents.TIME_TICK]
	

	#This is were we would get node board info via spi and check for machine events
	write_buf = bytearray([
		test_machine.led_states[0],
		test_machine.led_states[1],
		test_machine.led_states[2],
		0x44,4,5,6])

	####################################################
	#Parse node board data
	####################################################
	if spi_present:
		node_board_events = spi_port.exchange(out=write_buf,readlen=0,start=True,stop=True,duplex=True)
		#print(node_board_events.hex())

		#Loop through each possible event
		for event in GameEvents:
			if event.event_mask is not None:
				if event.event_mask[0]>1:
					if node_board_events[event.event_mask[0]] & event.event_mask[1]:
						print(event)
						test_event_list.append(event)
						pass

	
	#Loop through pygames events and check for key presses
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			#Detect keyboard emulated events
			if event.key in Keyboard_Mapping_Dict:
				#print(event.unicode)
				print(Keyboard_Mapping_Dict[event.key])
				test_event_list.append(Keyboard_Mapping_Dict[event.key])


	#Update high level game states	
	test_machine.update(test_event_list,screen)

	# Update the display
	pygame.display.flip()
	#print(clock.get_fps())

	# Limit the frame rate
	clock.tick(30)
	
  
# quit pygame after closing window
pygame.quit()
