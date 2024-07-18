from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from maya_env import MayaAnimationEnv

# Instantiate the environment
env = MayaAnimationEnv(start_frame=1, end_frame=100)

# Check the environment
check_env(env)

# Instantiate the agent
model = PPO('MlpPolicy', env, verbose=1)

# Train the agent
model.learn(total_timesteps=10000)

# Save the model
model.save('ppo_maya_animation')
