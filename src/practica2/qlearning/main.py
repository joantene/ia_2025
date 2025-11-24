import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle

def run(episodes,is_training=True, render=False):

    env = gym.make('FrozenLake-v1', is_slippery=True, render_mode='human' if render else None)

    if is_training:
        # Initialize Q(s, a), for all s ∈ S+, a ∈ A(s), arbitrarily except that Q(terminal, ·) = 0
        q = np.zeros((env.observation_space.n, env.action_space.n))
    else:
        f = open("frozen_lake4x4.pk1", "rb")
        q = pickle.load(f)
        f.close()

    # Algorithm parameters: step size α ∈ (0, 1]
    learning_rate = 0.9 # alpha
    # (Discount factor γ is implicitly used in the update rule)
    discount_factor = 0.9 # gamma

    # Algorithm parameters: small ε > 0
    epsilon = 1
    decay_rate = 0.0001
    rng = np.random.default_rng()

    rewards_per_episode = np.zeros(episodes)

    # Loop for each episode:
    for episode in range(episodes):
        # Initialize S
        state = env.reset()[0]
        terminated = False
        truncated = False

        # Loop for each step of episode:
        while(not terminated and not truncated):
            # Choose A from S using policy derived from Q (e.g., ε-greedy)
            if is_training and rng.random() < epsilon:
                action = env.action_space.sample()  
            else:
                action = np.argmax(q[state, :])

            # Take action A, observe R, S'
            new_state, reward, terminated, truncated, info = env.step(action)
            if is_training:
                # Q(S, A) <- Q(S, A) + α [R + γ max_a Q(S', a) - Q(S, A)]
                q[state, action] = q[state, action] + learning_rate * (reward + discount_factor * np.max(q[new_state, :]) - q[state, action])

            # S <- S'
            state = new_state

        # until S is terminal (Handled by the `while(not terminated and not truncated)` condition)
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