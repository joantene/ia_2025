import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle

def run(episodes, is_training=True, render=False):

    env = gym.make('FrozenLake-v1', is_slippery=True,
                   render_mode='human' if render else None)

    if is_training:
        q = np.zeros((env.observation_space.n, env.action_space.n))
    else:
        f = open("frozen_lake4x4.pk1", "rb")
        q = pickle.load(f)
        f.close()

    learning_rate = 0.9  # alpha
    discount_factor = 0.9  # gamma

    epsilon = 1.0
    decay_rate = 0.0001
    rng = np.random.default_rng()

    rewards_per_episode = np.zeros(episodes)

    for episode in range(episodes):
        state = env.reset()[0]
        terminated = False
        truncated = False


        if is_training:
            # ---- SARSA: triem l'acció inicial amb política epsilon-greedy ----
            if rng.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q[state, :])

            while not terminated and not truncated:
                # Executem l'acció actual
                new_state, reward, terminated, truncated, info = env.step(action)

                # Triem la següent acció A' amb la mateixa política (on-policy)
                if not terminated and not truncated:
                    if rng.random() < epsilon:
                        next_action = env.action_space.sample()
                    else:
                        next_action = np.argmax(q[new_state, :])
                    td_target = reward + discount_factor * q[new_state, next_action]
                else:
                    # Estat terminal → Q(S', A') = 0
                    next_action = None
                    td_target = reward

                # Actualització SARSA:
                # Q(S,A) ← Q(S,A) + α [R + γ Q(S',A') − Q(S,A)]
                q[state, action] = q[state, action] + learning_rate * (
                    td_target - q[state, action]
                )

                # Passem a (S', A')
                state = new_state
                if next_action is not None:
                    action = next_action

        else:
            # Mode avaluació: fem servir política purament cobdiciosa (greedy)
            while not terminated and not truncated:
                action = np.argmax(q[state, :])
                new_state, reward, terminated, truncated, info = env.step(action)
                state = new_state

        # Decaïment d'epsilon només durant entrenament
        if is_training:
            epsilon = max(epsilon - decay_rate, 0)
            if epsilon == 0:
                learning_rate = 0.0001

        # Comptam episodis d'èxit (arribar a la meta)
        if reward == 1:
            rewards_per_episode[episode] = 1

    env.close()

    # Suma de recompenses dels darrers 100 episodis
    sum_rewards = np.zeros(episodes)
    for t in range(episodes):
        sum_rewards[t] = np.sum(rewards_per_episode[max(0, t-100):(t+1)])
    plt.plot(sum_rewards)
    plt.savefig("frozen_lake4x4_rewards.png")

    # Guardar Q només si entrenam
    if is_training:
        f = open("frozen_lake4x4.pk1", "wb")
        pickle.dump(q, f)
        f.close()


if __name__ == "__main__":
    run(15000, is_training=True, render=False)
