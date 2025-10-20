from practica import agent_A as agent
from practica import joc


def main():
    mida = (10, 10)

    agents = [
        agent.agent_A(),
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)
    lab.comencar()


if __name__ == "__main__":
    main()