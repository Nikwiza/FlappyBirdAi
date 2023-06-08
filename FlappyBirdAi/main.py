# Imports for Env settup
from FlappyBirdEnv import *
from settings import *

# Imports for NN

from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

def build_model(states, actions):
    model = Sequential()
    model.add(Flatten(input_shape = states))
    model.add(Dense(40, activation = 'relu', input_shape = states))
    model.add(Dense(40, activation = 'relu'))
    model.add(Dense(40, activation = 'relu'))
    model.add(Dense(actions, activation = 'linear'))
    return model

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit = 50000, window_length = 1)
    dqn = DQNAgent(model = model, memory = memory, policy=policy, nb_actions = actions, nb_steps_warmup = 10, target_model_update = 1e-2)
    return dqn

if __name__ == "__main__":
    env = Game()

    # Actions and states
    states = env.observation_space.shape
    actions = env.action_space.n

    model = build_model(states, actions)
    model.summary()
    print(actions, states)

    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr = 1e-2), metrics = ['mae'])
    dqn.fit(env, nb_steps = 30000, visualize = False, verbose = 1)

    scores = dqn.test(env, nb_episodes = 100, visualize = False)
    print(np.mean(scores.history['episode_rewards']))

    dqn.save_weights('agent_weights.h5')


    # for episode in range (1):
    #     state = env.reset()
    #     done = False
    #     score = 0


    #     print('-----Start of episode----')

    #     while not done:
    #         # env.render()
    #         action = random.choice([0,1])
    #         n_state, reward, done, info = env.step(action)
    #         score += reward
    #         print('Values: {}  Score:{}'.format(env.observation, score))

    #     print('-----End of episode----')
