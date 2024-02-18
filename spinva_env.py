import pygame
import time
import numpy as np
import gymnasium as gym
from gymnasium.spaces import Discrete, Box #Esto lo cambié, porque gymnasium usa otra sinstaxis
from collections import deque
import random
import math
from pygame import mixer


# game loop
class SpinvaEnv(gym.Env):

    def __init__(self):
        super(SpinvaEnv, self).__init__()
        # Define action and observation space
		# They must be gym.spaces objects
		# Example when using discrete actions:
        self.action_space = Discrete(3) 
		# I'm going to control the points of the game
        self.observation_space = Box(low=0, high=540, shape=(1,), dtype=np.int32)
        self.reward = 0
        self.terminated = False
        self.truncated = False
        self.prev_actions = []
        # initializing pygame
        pygame.init()
        # creating screen
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # caption and icon
        pygame.display.set_caption("Welcome to Space Invaders Game by:- styles")
        # Score
        self.score_val = 0
        self.scoreX = 5
        self.scoreY = 5
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        # player
        self.playerImage = pygame.image.load('data/spaceship.png')
        self.player_X = 370
        self.player_Y = 523
        self.player_Xchange = 0
        # Invader
        self.invaderImage = []
        self.invader_X = []
        self.invader_Y = []
        self.invader_Xchange = []
        self.invader_Ychange = []
        self.no_of_invaders = 1
        # bullet
        self.bulletImage = pygame.image.load('data/bullet.png')
        self.bullet_X = 0
        self.bullet_Y = 500
        self.bullet_Xchange = 0
        self.bullet_Ychange = 3
        self.bullet_state = "rest"
        # Game Over
        self.game_over_font = pygame.font.Font('freesansbold.ttf', 64)
    
    def show_score(self,x, y):
        self.score = self.font.render("Points: " + str(self.score_val), True, (255,255,255))
        self.screen.blit(self.score, (x , y ))
    def game_over(self):
        self.game_over_text = self.game_over_font.render("GAME OVER", True, (255,255,255))
        self.screen.blit(self.game_over_text, (190, 250))
        # Background Sound
        # Collision Concept
    def isCollision(self,x1, x2, y1, y2):
        self.distance = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2)))
        if self.distance <= 50:
            return True
        else:
            return False
   
    
    def step(self, action):
        
        running = True
        while running:
            # RGB
            self.screen.fill((0, 0, 0))
            # action is an integer: 0 (LEFT), 1 (RIGHT), or 2 (SPACE)
            if action == 0:  # LEFT
                self.player_Xchange = -1.7
            elif action == 1:  # RIGHT
                self.player_Xchange = 1.7
            elif action == 2:  # SPACE
                if self.bullet_state == "rest":
                    self.bullet_X = self.player_X
                    self.bullet(self.bullet_X, self.bullet_Y)
                    #self.bullet_sound = mixer.Sound('data/bullet.wav')
                    #self.bullet_sound.play()
            #drawing the invaders
            for _ in range(self.no_of_invaders):
                self.invaderImage.append(pygame.image.load('data/alien.png'))
                self.invader_X.append(random.randint(64, 737))
                self.invader_Y.append(random.randint(30, 180))
                self.invader_Xchange.append(1.2)
                self.invader_Ychange.append(50)
            # Bullet
            # rest - bullet is not moving
            # fire - bullet is moving
            # adding the change in the player position
            self.player_X += self.player_Xchange
            for i in range(self.no_of_invaders):
                self.invader_X[i] += self.invader_Xchange[i]

            # bullet movement
            if self.bullet_Y <= 0:
                self.bullet_Y = 600
                self.bullet_state = "rest"
            if self.bullet_state == "fire":
                self.bullet(self.bullet_X, self.bullet_Y)
                self.bullet_Y -= self.bullet_Ychange

            # movement of the invader
            for i in range(self.no_of_invaders): 
                if self.invader_Y[i] >= 450:
                    if abs(self.player_X-self.invader_X[i]) < 80:
                        for j in range(self.no_of_invaders):
                            self.invader_Y[j] = 2000
                            #self.explosion_sound = mixer.Sound('data/explosion.wav')
                            #self.explosion_sound.play()
                        #self.game_over()
                        self.terminated = True
                        self.truncated = True
                        self.reward = -10   # Recompensa negativa por chocar con el cuerpo
                        observation = np.array([self.score_val], dtype=np.int32)
                        return observation, self.reward, self.terminated,self.truncated, {}  # Game over
                        #break

                if self.invader_X[i] >= 735 or self.invader_X[i] <= 0:
                    self.invader_Xchange[i] *= -1
                    self.invader_Y[i] += self.invader_Ychange[i]
                # Collision
                collision = self.isCollision(self.bullet_X, self.invader_X[i], self.bullet_Y, self.invader_Y[i])
                if collision:
                    self.score_val += 1
                    self.bullet_Y = 600
                    self.bullet_state = "rest"
                    self.invader_X[i] = random.randint(64, 736)
                    self.invader_Y[i] = random.randint(30, 200)
                    self.invader_Xchange[i] *= -1
                    self.reward = 1  

                self.invader(self.invader_X[i], self.invader_Y[i], i)
            
            # If not game over return the current state, reward and done = False
            observation = np.array([self.score_val], dtype=np.int32)
            return observation, self.reward, self.terminated,self.truncated, {}  # Game not over done = False
            
                
   
    def reset(self, seed=None):#Its a function that reset the game

        # player
        self.playerImage = pygame.image.load('data/spaceship.png')
        self.player_X = 370
        self.player_Y = 523
        self.player_Xchange = 0
        # Invader
        self.invaderImage = []
        self.invader_X = []
        self.invader_Y = []
        self.invader_Xchange = []
        self.invader_Ychange = []
        self.no_of_invaders = 2
        # Bullet
        # rest - bullet is not moving
        # fire - bullet is moving
        self.bulletImage = pygame.image.load('data/bullet.png')
        self.bullet_X = 0
        self.bullet_Y = 500
        self.bullet_Xchange = 0
        self.bullet_Ychange = 3
        self.bullet_state = "rest"
        self.score_val = 0
        self.reward = 0
        self.terminated = False
        self.truncated = False
        observation = np.array([self.score_val], dtype=np.int32)
        return observation, {}

    def render(self, mode='human'):
        #mixer.init()
        # Background Sound
        #mixer.music.load('data/background.wav')
        #mixer.music.play(-1)
        # restricting the spaceship so that it doesn't go out of screen
        if self.player_X <= 16:
            self.player_X = 16
        elif self.player_X >= 750:
            self.player_X = 750
        self.player(self.player_X, self.player_Y)
        self.show_score(self.scoreX, self.scoreY)
        pygame.display.update()


    def player(self,x, y):
        self.screen.blit(self.playerImage, (x - 16, y + 10))


    def invader(self,x, y, i):
        self.screen.blit(self.invaderImage[i], (x, y))


    def bullet(self,x, y):
        #global bullet_state
        self.screen.blit(self.bulletImage, (x, y))
        self.bullet_state = "fire"
        
        