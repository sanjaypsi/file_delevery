import gym
from gym import spaces
import numpy as np
import maya.cmds as cmds

class MayaAnimationEnv(gym.Env):
    def __init__(self, start_frame, end_frame):
        super(MayaAnimationEnv, self).__init__()
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.current_frame = start_frame

        self.action_space = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-10, high=10, shape=(3,), dtype=np.float32)

        self.object_name = 'pCube1'
        self.initial_position = cmds.getAttr(f'{self.object_name}.translate')[0]

    def reset(self):
        self.current_frame = self.start_frame
        cmds.currentTime(self.current_frame)
        cmds.setAttr(f'{self.object_name}.translate', *self.initial_position)
        return np.array(self.initial_position, dtype=np.float32)

    def step(self, action):
        self.current_frame += 1
        cmds.currentTime(self.current_frame)

        new_position = np.array(cmds.getAttr(f'{self.object_name}.translate')[0]) + action
        cmds.setAttr(f'{self.object_name}.translate', *new_position)
        cmds.setKeyframe(self.object_name, attribute='translate', t=self.current_frame)

        target_position = np.array([5.0, 5.0, 5.0])
        reward = -np.linalg.norm(new_position - target_position)

        done = self.current_frame >= self.end_frame

        return np.array(new_position, dtype=np.float32), reward, done, {}

    def render(self, mode='human'):
        pass

    def close(self):
        pass
