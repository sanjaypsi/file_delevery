import gym
from gym import spaces
import numpy as np

class MockMayaAnimationEnv(gym.Env):
    def __init__(self, start_frame, end_frame, initial_position):
        super(MockMayaAnimationEnv, self).__init__()
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.current_frame = start_frame
        self.position = np.array(initial_position)

        self.action_space = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-10, high=10, shape=(3,), dtype=np.float32)

    def reset(self):
        self.current_frame = self.start_frame
        self.position = np.array(initial_position)
        return self.position

    def step(self, action):
        self.current_frame += 1
        self.position += action

        target_position = np.array([5.0, 5.0, 5.0])
        reward = -np.linalg.norm(self.position - target_position)

        done = self.current_frame >= self.end_frame

        return self.position, reward, done, {}

    def render(self, mode='human'):
        pass

    def close(self):
        pass
