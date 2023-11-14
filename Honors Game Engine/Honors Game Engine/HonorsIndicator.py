from typing import List
import numpy as np
import math
import enum

class Indicator():
    status = False
    blinking = False
    blink_rate = None
    output_mask = [0,0]
    name  = None

    def __init__(self,name: str,position: List[int],mask: List[int]):
        #Define name
        self.name = name
        #Set position
        self.position = position
        self.x = self.position[0]
        self.y = self.position[1]
        #Define driver mask
        self.output_mask = mask
        

    def set_position(self,position):
        playfield_offset = self.adjusted_position-self.position
        self.position = position
        self.adjusted_position = np.add(position,playfield_offset)
        self.x = self.position[0]
        self.y = self.position[1]

    def set_x(self,x):
        playfield_offset = self.adjusted_position-self.position
        self.position = [x,self.position[1]]
        self.adjusted_position = np.add(self.position,playfield_offset)
        self.x = self.position[0]
        self.y = self.position[1]

    def set_y(self,y):
        playfield_offset = self.adjusted_position-self.position
        self.position = [self.position[0],y]
        self.adjusted_position = np.add(self.position,playfield_offset)
        self.x = self.position[0]
        self.y = self.position[1]

    def set_blinkrate(self,blink_rate):
        self.blink_rate = blink_rate


    def set_buffer(self,buffer: List[int],blink_count: int):
        #If indicator is on
        if self.status:
            buffer[self.output_mask[0]] = buffer[self.output_mask[0]] | self.output_mask[1]
        #If indicator status is false, but blink rate is set
        elif self.blink_rate is not None:
            if int(blink_count / self.blink_rate)%2 == 0:
                buffer[self.output_mask[0]] = buffer[self.output_mask[0]] | self.output_mask[1]
        








class PlayfieldAnimation:
    def __init__(self,name: str, duration: int,indicator_list: List[Indicator]):
        self.name = name #Name of animation
        self.duration = duration #How many frames does the animation last
        self.indicator_list = indicator_list #Which indicators does it affect



class SetIndicators(PlayfieldAnimation):  
    def __init__(self, name: str, duration: int, indicator_list: List[Indicator], status: bool, blink_rate: int):
        super().__init__(name,duration,indicator_list) #Initialize generic animation
        #Define whether we are turning indicators on or off
        #status == True: Turn on insert
        #status == Fales: Turn off insert
        self.status = status
        self.blink_rate = blink_rate

    #Update function that sets relevant indicators on or off
    def update(self,playfield_indicators: dict) -> bool:
        #If a list of indicators is not provided apply to all indicators
        if(self.indicator_list is None):
            update_list = list(playfield_indicators.keys())
        else:
            update_list = self.indicator_list       
        
        #Loop through the update list
        for i in update_list:
            playfield_indicators[i].status = self.status
            playfield_indicators[i].blink_rate = self.blink_rate
        #Decrement duration
        self.duration -= 1
        #If duration is zero or less return true which indicates removal
        return (self.duration <= 0)

class VerticalSweep(PlayfieldAnimation):
    def __init__(self, name: str, speed: float, indicator_list: List[Indicator], beam_width: float, initial_y: float):

        super().__init__(name,speed,indicator_list)
        self.speed = speed
        self.beam_width = beam_width
        self.y_position = initial_y

    def update(self,playfield_indicators) -> bool:
        if(self.indicator_list is None):
            update_list = list(playfield_indicators.keys())
        else:
            update_list = self.indicator_list

        self.y_position += self.speed
        #Loop through each indicator to see if it is within the beam width
        for i in update_list:
            if abs(playfield_indicators[i].y-self.y_position) <= self.beam_width:
                playfield_indicators[i].status = True
            #else:
            #    playfield_indicators[i].status = False
        return( (self.y_position < (-1*self.beam_width-5)) or (self.y_position> (48+self.beam_width)))

class HorizontalSweep(PlayfieldAnimation):
    def __init__(self, name: str, speed: float, indicator_list: List[Indicator], beam_width: float, initial_x: float):

        super().__init__(name,speed,indicator_list)
        self.speed = speed
        self.beam_width = beam_width
        self.x_position = initial_x

    def update(self,playfield_indicators) -> bool:
        if(self.indicator_list is None):
            update_list = list(playfield_indicators.keys())
        else:
            update_list = self.indicator_list

        self.x_position += self.speed
        #Loop through each indicator to see if it is within the beam width
        for i in update_list:
            if abs(playfield_indicators[i].x-self.x_position) <= self.beam_width:
                playfield_indicators[i].status = True
            #else:
            #    playfield_indicators[i].status = False
        return( ((self.x_position) < (-1*self.beam_width-5)) or (self.x_position> (24+self.beam_width)))