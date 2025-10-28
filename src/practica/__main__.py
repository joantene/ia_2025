from practica import agent_minimax as agent
from practica import joc


def main():
    mida = (5,5)

    agents = [
        agent.AgentMinimax(), agent.AgentMinimax()
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)
    lab.comencar()


if __name__ == "__main__":
    main()