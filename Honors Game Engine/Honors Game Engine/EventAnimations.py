import pygame

class text_splash_hold:
    def __init__(self,hold_time,text,font_size,offset):
        self.hold_time = hold_time
        self.text = text
        self.font_size = font_size
        font = pygame.font.Font('marspolice_i.ttf', self.font_size)
        self.splash_text = font.render(self.text, True, (255, 255, 255))
        self.width = self.splash_text.get_width()
        self.height = self.splash_text.get_height()
        self.offset = offset

    def update(self,screen):
        # Set up the font object
        #screen_size = screen.get_size()
        screen.blit(self.splash_text, self.splash_text.get_rect(center = tuple(map(sum,zip(screen.get_rect().center,self.offset)))))
        
        self.hold_time -= 1
        return (self.hold_time == 0) #Remove if time is up

class sprite_splash_hold:
    def __init__(self,hold_time,text,font_size,offset):
        self.hold_time = hold_time
        self.text = text
        #self.font_size = font_size
        #font = pygame.font.Font(None, self.font_size)
        #self.splash_text = font.render(self.text, True, (255, 255, 255))
        temp = pygame.image.load("Jackpot_alpha.png").convert_alpha()
        self.sprite_surf = pygame.transform.scale_by(temp,(2,2))
        self.width = self.sprite_surf.get_width()
        self.height = self.sprite_surf.get_height()
        self.offset = offset

    def update(self,screen):
        # Set up the font object
        #screen_size = screen.get_size()
        screen.blit(self.sprite_surf , self.sprite_surf.get_rect(center = tuple(map(sum,zip(screen.get_rect().center,self.offset)))))
        self.hold_time -= 1
        return (self.hold_time == 0) #Remove if time is up

class sprite_splash_permenant:
    def __init__(self,offset):
        temp = pygame.image.load("test_alpha.png").convert_alpha()
        self.sprite_surf = pygame.transform.scale_by(temp,(2,2))
        self.width = self.sprite_surf.get_width()
        self.height = self.sprite_surf.get_height()
        self.offset = offset
        self.active = True

    def update(self,screen):
        screen.blit(self.sprite_surf , self.sprite_surf.get_rect(center = tuple(map(sum,zip(screen.get_rect().center,self.offset)))))
        return (not self.active) #Remove if time is up

class image_splash_hold:
    def __init__(self,hold_time,surf,offset):
        self.hold_time = hold_time
        self.sprite_surf = surf
        self.width = self.sprite_surf.get_width()
        self.height = self.sprite_surf.get_height()
        self.offset = offset

    def update(self,screen):
        # Set up the font object
        #screen_size = screen.get_size()
        screen.blit(self.sprite_surf , self.offset)
        self.hold_time -= 1
        return (self.hold_time == 0) #Remove if time is up

