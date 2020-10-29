import pygame
import resource_mgr as rmg
import sys
import random

SCREEN = None
FRAME_RATE = 30
CLOCK = None
RMG = None
WIDTH, HEIGHT = 576, 930


class GameMgr:
    def __init__(self):
        self.isInited = False

        self.game_active = False

        self.floor_x_pos = 0

        self.gravity = 0.20
        self.bird_movement = 0

        self.SPAWNPIPE_EVENT = pygame.USEREVENT
        self.FLYFLAP_EVENT = pygame.USEREVENT+1
        self.SCORE_SOUND_VAL = 100
        self.pipe_height = [500, 600, 700]

        self.pipe_list = []
        self.bird_rect = None

        self.score = 0
        self.hight_score = 0

        self.game_over_rect = None
        self.score_sound_countdown = self.SCORE_SOUND_VAL

    def initPyGame(self):
        if self.isInited:
            return
        pygame.mixer.pre_init(frequency=44100, size=32, channels=2, buffer=512)
        pygame.init()

        global SCREEN
        SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

        global CLOCK
        CLOCK = pygame.time.Clock()

        global RMG
        RMG = rmg.ResourceMgr.getInstance()
        self.isInited = True

    def CreateSpawnPipe(self):
        height = random.choice(self.pipe_height)
        pipe_obj = RMG.pipe.get_rect(midtop=(600, height))
        top_pipe = RMG.pipe.get_rect(midbottom=(600, height-500))
        self.pipe_list.append(pipe_obj)
        self.pipe_list.append(top_pipe)

    def MoveSpawnPipe(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 5

            if pipe.centerx<-100:
                self.pipe_list.remove(pipe)

        print(len(self.pipe_list))      
        return self.pipe_list

    def checkCollision(self):
        if self.bird_rect.top <= -100 or self.bird_rect.bottom >= HEIGHT+20:
            if self.game_active == True:
                RMG.PlayHitSound()
            return True

        for pipe in self.pipe_list:
            if self.bird_rect.colliderect(pipe):
                if self.game_active == True:
                    RMG.PlayHitSound()
                return True

        return False

    def startNewGame(self):
        self.pipe_list.clear()
        if self.bird_rect:
            self.bird_rect.center = (100, 512)
        else:
            self.bird_rect = RMG.bird.get_rect(center=(100, 512))

        self.bird_movement = 0
        # UI
        self.game_font = pygame.font.Font("04B_19.TTF", 40)
        self.score = 0
        self.game_over_rect = RMG.game_over.get_rect(center=(288, 512))
        self.score_sound_countdown = 100
        self.game_active = True

    def eventDistribute(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird_movement = 0  # stop move
                    self.bird_movement -= 10  # move up before stop move will feel better
                    RMG.PlayFlapSound()
                if event.key == pygame.K_SPACE and self.game_active == False:
                    self.startNewGame()
            if event.type == self.SPAWNPIPE_EVENT and self.game_active:
                self.CreateSpawnPipe()

            if event.type == self.FLYFLAP_EVENT:
                RMG.BirdAnimation()
                self.bird_rect = RMG.bird.get_rect(
                    center=(100, self.bird_rect.centery))

        return True

    def DrawPipe(self):
        # print(self.game_active)
        if self.game_active:
            self.MoveSpawnPipe()
        for pipe in self.pipe_list:
            if pipe.bottom >= HEIGHT:
                SCREEN.blit(RMG.pipe, pipe)
            else:
                flip_pipe = pygame.transform.flip(RMG.pipe, False, True)
                SCREEN.blit(flip_pipe, pipe)

    def DrawFloor(self):
        SCREEN.blit(RMG.floor_surface, (self.floor_x_pos, 830))
        SCREEN.blit(RMG.floor_surface, (self.floor_x_pos+WIDTH, 830))
        self.floor_x_pos -= 1 if self.game_active else 0
        if self.floor_x_pos <= -WIDTH:
            self.floor_x_pos = 0

    def RotateBird(self):
        # RMG.bird
        new_bird = pygame.transform.rotozoom(
            RMG.bird, -self.bird_movement*3, 1)
        return new_bird

    def DrawBird(self):
        self.bird_movement += self.gravity
        rotate_bird = self.RotateBird() if self.game_active else RMG.bird
        self.bird_rect.centery += self.bird_movement if self.game_active else 0
        SCREEN.blit(rotate_bird, self.bird_rect)
        self.game_active = not self.checkCollision()

    def DrawScore(self):
        self.score += 0.01 if self.game_active else 0
        self.hight_score = max(self.hight_score, self.score)
        score_surface = self.game_font.render(
            "Score: %d" % self.score, True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(450, 80))
        SCREEN.blit(score_surface, score_rect)

        high_score_surface = self.game_font.render(
            "High Score: %d" % self.hight_score, True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(200, 80))
        SCREEN.blit(high_score_surface, high_score_rect)
        if self.game_active and self.score_sound_countdown <= 0:
            RMG.PlayPointSound()
            self.score_sound_countdown = self.SCORE_SOUND_VAL
        else:
            self.score_sound_countdown -= 1

    def Update(self):
        SCREEN.blit(RMG.bg_surface, (0, 0))

        self.DrawBird()
        self.DrawPipe()
        self.DrawFloor()
        self.DrawScore()
        if self.game_active == False:
            SCREEN.blit(RMG.game_over, self.game_over_rect)

        pygame.display.update()
        if CLOCK:
            CLOCK.tick(120)

    def Start(self):
        self.initPyGame()

        pygame.time.set_timer(self.SPAWNPIPE_EVENT, 1500)
        pygame.time.set_timer(self.FLYFLAP_EVENT, 100)
        self.startNewGame()
        while True:
            # image of player 1
            # background image
            if not SCREEN:
                break
            if False == self.eventDistribute():
                break

            self.Update()

        print("Game END!!!")
        exit()


if __name__ == "__main__":
    GameMgr().Start()
