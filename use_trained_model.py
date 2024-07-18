from stable_baselines3 import PPO
from maya_env import MayaAnimationEnv

# Load the trained model
model = PPO.load('ppo_maya_animation')

# Create the environment
env = MayaAnimationEnv(start_frame=101, end_frame=200)

# Reset the environment
obs = env.reset()

for _ in range(env.end_frame - env.start_frame):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    if done:
        break
