'''from snake_env import SnakeEnv


env = SnakeEnv()
episodes = 10

for episode in range(episodes):
	done = False
	obs = env.reset()
	while True:#not done:
		random_action = env.action_space.sample()
		print("action",random_action)
		obs, reward, terminated, truncated, info = env.step(random_action)
		print('reward',reward)
		'''
from stable_baselines3.common.env_checker import check_env
from snake_env import SnakeEnv

env = SnakeEnv()
# If the environment don't follow the interface, an error will be thrown
check_env(env, warn=True)