# -*- coding: utf-8 -*-
"""DQN-ModelFit-maxQ.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CWV8Jh7xN6d6YkXBVdf92Uy5n2ZyJrgi
"""


import gym
import numpy as np
import tensorflow as tf
from tqdm.notebook import tqdm
from collections import deque
import random

class DQN:
  def __init__(self):
    # Define hyperparameters
    self.env = gym.make("LunarLander-v2")

    self.n_action = self.env.action_space.n
    self.n_state_attribute = self.env.observation_space.shape[0]

    self.gamma = 0.99

    # Use epsilon-greedy algorithm
    self.epsilon = 1
    self.epsilon_decay = 0.996
    self.epsilon_min = 0.01

    self.lr = 0.001

    self.batch_size = 64
    self.model = self.model_init()

    # params for training
    self.n_episode = 500
    self.max_step = 3000
    self.replay_pool = deque(maxlen=1000000)

    self.average_100 = 0
    self.r_list = []
  
  def model_init(self):
    # Build network for DQN
    model = tf.keras.models.Sequential([
                                        tf.keras.layers.InputLayer(input_shape=(self.n_state_attribute, )),
                                        tf.keras.layers.Dense(128, activation='relu'),
                                        tf.keras.layers.Dense(128, activation='relu'),
                                        tf.keras.layers.Dense(self.n_action, activation='linear')
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=self.lr)
    model.compile(optimizer=optimizer, loss='mse')

    return model

  def run(self):
    prg_bar = tqdm(range(self.n_episode))
    for i in prg_bar:
      curr_state = self.env.reset()
      curr_state = np.reshape(curr_state, (1, self.n_state_attribute))
      total_reward = 0

      for j in range(self.max_step):
        # choose an action with epsilon-greedy
        curr_output = self.model.predict(curr_state)
        action = np.argmax(curr_output[0, :])
        self.env.render()
        if np.random.random() <= np.amax((self.epsilon, self.epsilon_min)):
          action = np.random.randint(self.n_action)

        new_state, reward, done, info = self.env.step(action)
        new_state = np.reshape(new_state, (1, self.n_state_attribute))
        total_reward += reward

        # Store info to the pool
        self.replay_pool.append([curr_state, action, reward, new_state, done])

        # if len(self.replay_pool) > self.max_replay_size:
        #   self.replay_pool = self.replay_pool[1:]

        self.train()

        curr_state = new_state
        if done:
          break
        
      self.r_list.append(total_reward)

      # Check whether the 200 points have been reached
      if len(self.r_list) < 100:
        average_100 = np.average(self.r_list)
      else:
        average_100 = np.average(self.r_list[-100:])

      print('Current total episodes:' + str(i) + '   Past episode score:' + str(total_reward) + '    Past average 100 score:' + str(average_100))

      if average_100 > 200:
        print('Finished! The average score for the past 100 episodes are ' + str(
                  average_100) + ', current episode = ' + str(len(self.r_list)))
        self.model.save('model_128_node')
        np.savetxt('r_list_128.txt', self.r_list)
        break

  def train(self):
      
      # Train the model
      if len(self.replay_pool) >= self.batch_size:
        sample = np.array(random.sample(self.replay_pool, self.batch_size))

        curr_s = np.concatenate(np.array([i[0] for i in sample]))
        a = np.array([i[1] for i in sample])
        r = np.array([i[2] for i in sample])
        next_s = np.concatenate(np.array([i[3] for i in sample]))
        d = np.array([i[4] for i in sample])

        targets = self.model.predict(curr_s).copy()
        td = r + self.gamma*(np.amax(self.model.predict(next_s), axis=1))*(1-d)

        for k in range(self.batch_size):
          targets[k, a[k]] = td[k]
        
        self.model.train_on_batch(x=curr_s, y=targets)
        
        self.epsilon *= self.epsilon_decay

dqn = DQN()
dqn.run()

