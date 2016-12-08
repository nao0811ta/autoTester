from singleton import Singleton

from cnn_dqn_agent import CnnDqnAgent

import io
import os
from PIL import Image
from PIL import ImageOps
import threading
import numpy as np

#@Singleton
class Agent:
    agent_initialized = False
    cycle_counter = 0
    thread_event = threading.Event()
    reward_sum = 0

    def __init__(self, args):
        print "start to load cnn model"
        self.args = args
        self.cnnDqnAgent = CnnDqnAgent(use_gpu=self.args.gpu)
        print 'finish loading cnn model'
        self.cnnDqnAgent.agent_init()
        print 'finish init cnn dqn agent'

    def received_message(self, agentServer, dat):
        image = []
        for i in xrange(self.depth_image_count):
            image.append(Image.open(io.BytesIO(bytearray(dat['image'][i]))))

        observation = {"image": image}

        # print 'scale'
        # print observation['scale']
        reward = dat['reward']
        end_episode = dat['endEpisode']

        if not self.agent_initialized:
            print 'connected and agent started..'
            self.agent_initialized = True
            action = self.cnnDqnAgent.agent_start(observation)
            agentServer.send_action(action)
            if not os.path.exists(self.args.log_file):
                with open(self.args.log_file, 'w') as the_file:
                    the_file.write('cycle, episode_reward_sum \n')
        else:
            self.thread_event.wait()
            self.cycle_counter += 1
            self.reward_sum += reward

            if end_episode:
                self.cnnDqnAgent.agent_end(reward)
                action = self.cnnDqnAgent.agent_start(observation)  # TODO
                agentServer.send_action(action)
                with open(self.args.log_file, 'a') as the_file:
                    the_file.write(str(self.cycle_counter) +
                                   ',' + str(self.reward_sum) +
                                   ',' + str(self.scale_x) +
                                   ',' + str(self.scale_y) +
                                   ',' + str(self.scale_z) + '\n')
                self.reward_sum = 0
            else:
                action, eps, obs_array = self.cnnDqnAgent.agent_step(reward, observation)
                agentServer.send_action(action)
                self.cnnDqnAgent.agent_step_update(reward, action, eps, obs_array)

        self.thread_event.set()
