import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt


# -------------------------------
# Paràmetres de l'algoritme genètic
# -------------------------------
POPULATION_SIZE = 200       # nombre d'individus
CHROMOSOME_LENGTH = 50      # longitud de la seqüència d'accions
N_GENERATIONS = 300         # generacions màximes

TOURNAMENT_SIZE = 3         # selecció per torneig
CROSSOVER_RATE = 0.8        # probabilitat de creuament
MUTATION_RATE = 0.05        # probabilitat de mutació per gen

DISCOUNT_FACTOR = 0.99      # gamma per descomptar recompenses (coherent amb els apunts)


def create_env(render = False):
    """
    Crea l'entorn FrozenLake amb el paràmetre is_slippery activat,
    tal com indica l'enunciat de la pràctica.
    """
    env = gym.make(
        "FrozenLake-v1",
        is_slippery=True,
        render_mode="human" if render else None
    )
    return env


# ---------------------------------------------------
# Representació i inicialització
# ---------------------------------------------------

def init_population(pop_size: int, chromosome_length: int, n_actions: int) -> np.ndarray:
    """
    Inicialitza una població de cromosomes (seqüències d'accions).
    Cada gen és una acció ∈ {0, ..., n_actions-1}.
    """
    return np.random.randint(
        low=0,
        high=n_actions,
        size=(pop_size, chromosome_length),
        dtype=np.int32
    )


# ---------------------------------------------------
# Avaluació (fitness)
# ---------------------------------------------------

def run_episode_with_chromosome(env, chromosome: np.ndarray) -> float:
    """
    Executa un episodi de FrozenLake seguint la seqüència d'accions
    codificada al cromosoma.

    Retorna un "retorn descomptat" aproximat:

        G ≈ sum_t gamma^t * reward_t

    on reward_t és la recompensa de l'entorn (0 o 1 normalment).
    A més, afegim shaping amb la distància a la casella objectiu per
    discriminar millor entre camins dolents i camins "gairebé bons".
    """
    state, _ = env.reset()
    done = False
    total_return = 0.0
    discount = 1.0

    # Dimensions del mapa (FrozenLake-v1 per defecte és 4x4, però pot variar)
    n_states = env.observation_space.n
    side = int(np.sqrt(n_states))  # assumim tauler quadrat

    # Coordenada de l'objectiu (per defecte FrozenLake té el goal a l'última casella)
    goal_state = n_states - 1
    goal_row, goal_col = divmod(goal_state, side)

    for action in chromosome:
        if done:
            break

        next_state, reward, terminated, truncated, _ = env.step(int(action))
        done = terminated or truncated

        # Retorn descomptat (coherent amb la definició de Gt als apunts)
        total_return += discount * reward
        discount *= DISCOUNT_FACTOR

        state = next_state

        # Si s'ha arribat al goal, aturam l'episodi
        if done:
            break

    # Shaping addicional: penalitzar la distància a l'objectiu.
    # Això és útil perquè el problema té recompensa esparsa.
    row, col = divmod(state, side)
    manhattan_dist = abs(goal_row - row) + abs(goal_col - col)

    # Fitness base: retorn descomptat
    fitness = total_return * 100.0  # escalar perquè tingui més pes

    # Penalització per haver caigut en un forat (reward=0 i estat terminal abans d'arribar)
    # No podem distingir 100% segur entre forat i res més, però en general,
    # si done i reward=0 → molt probablement forat.
    if done and total_return == 0.0:
        fitness -= 100.0

    # Shaping per distància: com més a prop del goal, millor (valor més gran)
    fitness += -manhattan_dist

    return fitness


def evaluate_population(env, population: np.ndarray) -> np.ndarray:
    """
    Calcula el fitness de tots els individus de la població.
    """
    fitnesses = np.zeros(population.shape[0], dtype=np.float32)
    for i, chromosome in enumerate(population):
        fitnesses[i] = run_episode_with_chromosome(env, chromosome)
    return fitnesses


# ---------------------------------------------------
# Selecció, creuament i mutació
# ---------------------------------------------------

def tournament_selection(population: np.ndarray,
                         fitnesses: np.ndarray,
                         tournament_size: int) -> np.ndarray:
    """
    Selecció per torneig:
      - Es trien `tournament_size` individus a l'atzar
      - Es retorna el millor d'ells
    """
    indices = np.random.choice(len(population), size=tournament_size, replace=False)
    best_idx = indices[np.argmax(fitnesses[indices])]
    return population[best_idx].copy()


def one_point_crossover(parent1: np.ndarray,
                        parent2: np.ndarray,
                        crossover_rate: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Creuament d'un punt:
      - Amb probabilitat `crossover_rate`, es tria un punt de tall
        i es combinen els cromosomes.
      - En cas contrari, es copien els pares.
    """
    if np.random.rand() > crossover_rate:
        return parent1.copy(), parent2.copy()

    length = len(parent1)
    point = np.random.randint(1, length)  # punt de tall (no a l'inici ni al final)
    child1 = np.concatenate([parent1[:point], parent2[point:]])
    child2 = np.concatenate([parent2[:point], parent1[point:]])
    return child1, child2


def mutate(chromosome: np.ndarray,
           mutation_rate: float,
           n_actions: int) -> np.ndarray:
    """
    Mutació independent per gen amb probabilitat `mutation_rate`.
    Cada mutació substitueix l'acció per una d'aleatòria.
    """
    for i in range(len(chromosome)):
        if np.random.rand() < mutation_rate:
            chromosome[i] = np.random.randint(0, n_actions)
    return chromosome


# ---------------------------------------------------
# Algoritme genètic principal
# ---------------------------------------------------

def genetic_algorithm_frozenlake(render_best=False):
    env = create_env(render=False)
    n_actions = env.action_space.n

    # Inicialització de la població
    population = init_population(POPULATION_SIZE, CHROMOSOME_LENGTH, n_actions)

    best_fitness_history = []
    avg_fitness_history = []

    # Guardarem el millor individu trobat
    global_best_fitness = -np.inf
    global_best_individual = None

    for generation in range(N_GENERATIONS):
        # Avaluar població
        fitnesses = evaluate_population(env, population)

        best_idx = np.argmax(fitnesses)
        best_fitness = fitnesses[best_idx]
        avg_fitness = np.mean(fitnesses)

        # Actualitzar millor global
        if best_fitness > global_best_fitness:
            global_best_fitness = best_fitness
            global_best_individual = population[best_idx].copy()

        best_fitness_history.append(best_fitness)
        avg_fitness_history.append(avg_fitness)

        print(f"Gen {generation:03d} | Best fitness: {best_fitness:.2f} | "
              f"Avg fitness: {avg_fitness:.2f}")

        # Criteri d'aturada: si fitness molt alt (arribar al goal vàries vegades)
        if global_best_fitness >= 90.0:
            print("Sembla que hem trobat una bona solució, aturant abans de temps.")
            break

        # Nova població amb elitisme
        new_population = []

        # Elitisme: mantenim el millor individu de la generació actual
        new_population.append(population[best_idx].copy())

        # Omplim la resta de la població
        while len(new_population) < POPULATION_SIZE:
            # Selecció de pares
            parent1 = tournament_selection(population, fitnesses, TOURNAMENT_SIZE)
            parent2 = tournament_selection(population, fitnesses, TOURNAMENT_SIZE)

            # Creuament
            child1, child2 = one_point_crossover(parent1, parent2, CROSSOVER_RATE)

            # Mutació
            child1 = mutate(child1, MUTATION_RATE, n_actions)
            child2 = mutate(child2, MUTATION_RATE, n_actions)

            new_population.append(child1)
            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        population = np.array(new_population, dtype=np.int32)

    env.close()

    print("\n=== Resultat final GA ===")
    print(f"Millor fitness global: {global_best_fitness:.2f}")
    print("Millor cromosoma (accions):")
    print(global_best_individual)

    # Dibuixem la corba d'aprenentatge (millor i mitjana)
    plt.plot(best_fitness_history, label="Millor fitness")
    plt.plot(avg_fitness_history, label="Fitness mitjà")
    plt.xlabel("Generació")
    plt.ylabel("Fitness")
    plt.legend()
    plt.title("Algoritme genètic a FrozenLake")
    plt.tight_layout()
    plt.savefig("ga_frozenlake_fitness.png")
    plt.close()

    # Opcional: executar un episodi amb el millor cromosoma i renderitzar-lo
    if render_best:
        env = create_env(render=True)
        state, _ = env.reset()
        done = False
        total_reward = 0

        for action in global_best_individual:
            if done:
                break
            state, reward, terminated, truncated, _ = env.step(int(action))
            done = terminated or truncated
            total_reward += reward

        print(f"Recompensa total amb el millor individu: {total_reward}")
        env.close()


if __name__ == "__main__":
    # Pots canviar render_best=True per veure'l a la pantalla
    genetic_algorithm_frozenlake(render_best=False)
