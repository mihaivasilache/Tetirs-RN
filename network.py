from collections import deque

from keras import *
import os
import random
from keras.models import load_model
from keras.layers import *
from keras.optimizers import *


class Network:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.8
        self.epsilon = 1.0
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.9995
        self.learning_rate = 0.01
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(self.state_size, input_dim=self.state_size, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        # print(act_values[0], np.argmax(act_values[0]))
        if act_values[0][0] == act_values[0][1] == act_values[0][2] == act_values[0][3]:
            return random.randrange(self.action_size)
        # print(act_values[0], np.argmax(act_values[0]))
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        mini_batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in mini_batch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            # print(self.model.predict(state))
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        # if self.epsilon < self.epsilon_min:
        #     self.learning_rate = 0.00001

    def save_model(self, filename):
        self.model.save(filename)

    def load_model(self, filename):
        if os.path.exists(filename):
            self.model = load_model(filename)
            print('Loading network: '+os.path.split(filename)[1])
            return True

        return False
