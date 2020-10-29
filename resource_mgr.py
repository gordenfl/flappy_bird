import pygame


class ResourceMgr:
    instance = None

    @staticmethod
    def getInstance():
        if ResourceMgr.instance:
            return ResourceMgr.instance
        ResourceMgr.instance = ResourceMgr()
        return ResourceMgr.instance

    def __init__(self):
        bg_surface = pygame.image.load(
            "assets/background-day.png").convert()
        self.bg_surface = pygame.transform.scale2x(bg_surface)

        floor_surface = pygame.image.load("assets/base.png").convert()
        self.floor_surface = pygame.transform.scale2x(floor_surface)

        bird_down = pygame.transform.scale2x(pygame.image.load(
            "assets/bluebird-downflap.png").convert_alpha())
        bird_mid = pygame.transform.scale2x(pygame.image.load(
            "assets/bluebird-midflap.png").convert_alpha())
        bird_up = pygame.transform.scale2x(pygame.image.load(
            "assets/bluebird-upflap.png").convert_alpha())
        self.bird_frame = [bird_down, bird_mid, bird_up]
        self.bird_index = 0
        self.bird = self.bird_frame[self.bird_index]

        pipe = pygame.image.load("assets/pipe-green.png").convert()
        self.pipe = pygame.transform.scale2x(pipe)

        self.game_over = pygame.transform.scale2x(pygame.image.load(
            "assets/message.png").convert_alpha())

        self.flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
        self.hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
        self.die_sound = pygame.mixer.Sound("sound/sfx_die.wav")
        self.point_sound = pygame.mixer.Sound("sound/sfx_point.wav")
        self.swooshing_sound = pygame.mixer.Sound("sound/sfx_swooshing.wav")

    def BirdAnimation(self):
        self.bird_index = (self.bird_index+1) % 3
        self.bird = self.bird_frame[self.bird_index]

    def PlayFlapSound(self):
        self.flap_sound.play()
    
    def PlayHitSound(self):
        self.hit_sound.play()

    def PlayDieSound(self):
        self.die_sound.play()
    
    def PlayPointSound(self):
        self.point_sound.play()

    def PlaySwooshingSound(self):
        self.swooshing_sound.play()