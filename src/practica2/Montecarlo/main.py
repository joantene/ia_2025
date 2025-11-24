import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle

def run(episodes, is_training=True, render=False):

    env = gym.make('FrozenLake-v1', is_slippery=True,
                   render_mode='human' if render else None)

    if is_training:
        # Q(s, a) ∈ R (arbitrarily), for all s ∈ S, a ∈ A(s)
        q = np.zeros((env.observation_space.n, env.action_space.n))

        # Returns(s, a) <- empty list, for all s ∈ S, a ∈ A(s)
        returns = {}
        
    else:
        f = open("frozen_lake4x4.pk1", "rb")
        q = pickle.load(f)
        f.close()

    discount_factor = 0.9  # gamma

    epsilon = 1.0
    decay_rate = 0.0001
    rng = np.random.default_rng()

    rewards_per_episode = np.zeros(episodes)

    # Loop forever (for each episode):
    for episode in range(episodes):
        # Choose S_0 ∈ S, A_0 ∈ A(S_0) randomly... (Initialization)
        state = env.reset()[0]
        terminated = False
        truncated = False
        
        # Llista per guardar (state, action, reward) per a l'episodi
        history = []
        
        # Generate an episode from S_0, A_0, following π: S_0, A_0, R_1, ..., S_T-1, A_T-1, R_T
        while(not terminated and not truncated):
            # Choose A_t using policy derived from Q (ε-greedy)
            if is_training and rng.random() < epsilon:
                action = env.action_space.sample()  
            else:
                action = np.argmax(q[state, :])

            new_state, reward, terminated, truncated, info = env.step(action)
            
            history.append((state, action, reward))
            
            state = new_state
            

        if is_training:
            # G <- 0
            G = 0.0
            visited_sa = set() # Per implementar First-Visit MC
            
            # Loop for each step of episode, t = T-1, T-2, ..., 0:
            for i in range(len(history) - 1, -1, -1):
                s, a, r = history[i]
                
                # G ← gamma * G + R_t+1 
                G = discount_factor * G + r
                
               # Unless the pair S_t, A_t appears in S_0, A_0, ..., S_t-1, A_t-1:
                if (s, a) not in visited_sa:
                    visited_sa.add((s, a)) 

                    if (s, a) not in returns:
                        returns[(s, a)] = []
                    
                    # Append G to Returns(S_t, A_t)
                    returns[(s, a)].append(G)
                    
                    # Q(S_t, a) <- average(Returns(S_t, a))
                    q[s, a] = np.mean(returns[(s, a)])

            # π(S_t) <- argmax_a Q(S_t, a) 
            epsilon = max(epsilon - decay_rate, 0)
            

        # Registre de recompenses (si la recompensa final és 1)
        # La recompensa final és la darrera 'r' observada a 'history', que és la R_T
        final_reward = history[-1][2] if history else 0
        if final_reward == 1:
            rewards_per_episode[episode] = 1

    env.close()


    sum_rewards = np.zeros(episodes)
    for t in range(episodes):
        sum_rewards[t] = np.sum(rewards_per_episode[max(0, t-100):(t+1)])
    plt.plot(sum_rewards)
    plt.savefig("frozen_lake4x4_rewards_mc.png")

    if is_training:
        f = open("frozen_lake4x4.pk1", "wb")
        pickle.dump(q, f)
        f.close()    
        
if __name__ == "__main__":
    run(15000, is_training=True, render=False)