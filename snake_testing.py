from snake_env import SnakeEnv

env = SnakeEnv()
# Reset the environment     
env.reset()

# Box(4,) means that it is a Vector with 4 components
print("Observation space:", env.observation_space)
print("Shape:", env.observation_space.shape)
# Discrete(2) means that there is two discrete actions
print("Action space:", env.action_space)

# Sample a random action
action = env.action_space.sample()
print("Sampled action:", action)

obs, reward, done, info, info = env.step(action)
# Note the obs is a numpy array
# info is an empty dict for now but can contain any debugging info
# reward is a scalar
print(obs.shape, reward, done, info, info)