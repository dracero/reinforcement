import pygame
import sys
import time
import random
import numpy as np
import gymnasium as gym
from gymnasium.spaces import Discrete, Box #Esto lo cambié, porque gymnasium usa otra sinstaxis


class SnakeEnv(gym.Env):
    def __init__(self):
        super(SnakeEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
    
        self.action_space = Discrete(4)
        self.observation_space = Box(low=0, high=255, shape=(1,), dtype=np.int32)#Voy a controlar el largo de la serpiente
         # Pygame Init
        pygame.init()

        # Play Surface
        self.size = self.width, self.height = 640, 320
        self.playSurface = pygame.display.set_mode(self.size)
        # Render the environment to the screen
        # Play Surface
        self.size = self.width, self.height = 640, 320
        self.playSurface = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Snake Game")

        # Colors
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)

        # Game settings
        self.delta = 10
        self.snakePos = [100, 50]
        self.snakeBody = [[100, 50], [90, 50], [80, 50]]
        self.foodPos = [400, 50]
        self.foodSpawn = True
        self.direction = 'RIGHT'
        self.score = 0
        self.reward = 0
        self.terminated = False
        self.truncated = False
        self.render()  # Llamada al método render para inicializar pygame
       
    
    # Game Over
    def gameOver(self):
        self.myFont = pygame.font.SysFont('monaco', 72)
        self.GOsurf = self.myFont.render("Game Over", True, self.red)
        self.GOrect = self.GOsurf.get_rect()
        self.GOrect.midtop = (320, 25)
        self.playSurface.blit(self.GOsurf, self.GOrect)
        self.blackshowScore(0)
        pygame.display.flip()
        time.sleep(4)
        pygame.quit()
        sys.exit()


    # Show Score
    def showScore(self, choice=1):
        self.SFont = pygame.font.SysFont('monaco', 32)
        self.Ssurf = self.SFont.render("Score  :  {0}".format(self.score), True, self.black)
        self.Srect = self.Ssurf.get_rect()
        if choice == 1:
            self.Srect.midtop = (80, 10)
        else:
            self.Srect.midtop = (320, 100)
        self.playSurface.blit(self.Ssurf,self.Srect)

    def step(self, action):
            # Map the action to direction
            action_map = {0: 'RIGHT', 1: 'LEFT', 2: 'UP', 3: 'DOWN'}
            changeto = action_map[action]

            # Validate direction
            if changeto == 'RIGHT' and self.direction != 'LEFT':
                self.direction = changeto
            if changeto == 'LEFT' and self.direction != 'RIGHT':
                self.direction = changeto
            if changeto == 'UP' and self.direction != 'DOWN':
                self.direction = changeto
            if changeto == 'DOWN' and self.direction != 'UP':
                self.direction = changeto

            # Update snake position
            if self.direction == 'RIGHT':
                self.snakePos[0] += self.delta
            if self.direction == 'LEFT':
                self.snakePos[0] -= self.delta
            if self.direction == 'DOWN':
                self.snakePos[1] += self.delta
            if self.direction == 'UP':
                self.snakePos[1] -= self.delta

            # Snake body mechanism
            self.snakeBody.insert(0, list(self.snakePos))
            if self.snakePos == self.foodPos:
                self.foodSpawn = False
                self.score += 1
                self.reward = 1  # Recompensa positiva por comer la comida
            else:
                self.snakeBody.pop()
            if self.foodSpawn == False:
                self.foodPos = [random.randrange(1, self.width // 10) * self.delta, random.randrange(1, self.height // 10) * self.delta]
                self.foodSpawn = True
               

            # Check for game over conditions
            if self.snakePos[0] >= self.width or self.snakePos[0] < 0 or self.snakePos[1] >= self.height or self.snakePos[1] < 0:
                self.terminated = True
                self.truncated = True
                self.reward = -10  # Recompensa negativa por chocar con la pared
                observation = np.array([len(self.snakeBody)], dtype=np.int32)
                return observation, self.reward, self.terminated,self.truncated, {}  # Game over
            for block in self.snakeBody[1:]:
                if self.snakePos == block:
                    self.terminated = True
                    self.truncated = True
                    self.reward = -10   # Recompensa negativa por chocar con el cuerpo
                    observation = np.array([len(self.snakeBody)], dtype=np.int32)
                    return observation, self.reward, self.terminated,self.truncated, {}  # Game over

            # If not game over return the current state, reward and done = False
            observation = np.array([len(self.snakeBody)], dtype=np.int32)
            return observation, self.reward, self.terminated,self.truncated, {}  # Game not over done = False

    def reset(self, seed = None):
            # Reset the state of the environment to an initial state
            self.delta = 10
            self.snakePos = [100, 50]
            self.snakeBody = [[100, 50], [90, 50], [80, 50]]
            self.foodPos = [400, 50]
            self.foodSpawn = True
            self.direction = 'RIGHT'
            self.score = 0
            self.reward = 0
            self.terminated = False
            self.truncated = False
            observation = np.array([len(self.snakeBody)], dtype=np.int32)
            return observation, {}

    def render(self, mode='human'):
        # FPS controller
        self.fpsController = pygame.time.Clock()
        self.playSurface.fill( self.white)
        for pos in  self.snakeBody:
            pygame.draw.rect( self.playSurface,  self.green, pygame.Rect(pos[0], pos[1],  self.delta,  self.delta))
        pygame.draw.rect( self.playSurface,  self.brown, pygame.Rect( self.foodPos[0],  self.foodPos[1],  self.delta,  self.delta))
        self.showScore()
        pygame.display.flip()
        self.fpsController.tick(20)