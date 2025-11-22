import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle

def run(episodes,is_training=True, render=False):

    env = gym.make('FrozenLake-v1', is_slippery=True, render_mode='human' if render else None)

    if is_training:
        q = np.zeros((env.observation_space.n, env.action_space.n))
    else:
        f = open("frozen_lake4x4.pk1", "rb")
        q = pickle.load(f)
        f.close()

    learning_rate = 0.9 # alpha
    discount_factor = 0.9 # gamma

    epsilon = 1
    decay_rate = 0.0001
    rng = np.random.default_rng()

    rewards_per_episode = np.zeros(episodes)

    for episode in range(episodes):
        state = env.reset()[0]
        terminated = False
        truncated = False

        while(not terminated and not truncated):
            if is_training and rng.random() < epsilon:
                action = env.action_space.sample()  
            else:
                action = np.argmax(q[state, :])

            new_state, reward, terminated, truncated, info = env.step(action)
            if is_training:
                q[state, action] = q[state, action] + learning_rate * (reward + discount_factor * np.max(q[new_state, :]) - q[state, action])

            state = new_state


        epsilon = max(epsilon - decay_rate, 0)

        if(epsilon == 0):
            learning_rate = 0.0001

        if reward == 1:
            rewards_per_episode[episode] = 1

    env.close()

    sum_rewards = np.zeros(episodes)
    for t in range(episodes):
        sum_rewards[t] = np.sum(rewards_per_episode[max(0, t-100):(t+1)])
    plt.plot(sum_rewards)
    plt.savefig("frozen_lake4x4_rewards.png")

    if is_training:
        f = open("frozen_lake4x4.pk1", "wb")
        pickle.dump(q, f)
        f.close()    
        
if __name__ == "__main__":
    run(15000, is_training=True, render=False)