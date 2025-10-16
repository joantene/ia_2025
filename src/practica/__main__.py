from practica import  joc, agent, agent_amplada


def main():
    mida = (10, 10)

    agents = [
        agent_amplada.AgentAmplada(),
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)
    lab.comencar()


if __name__ == "__main__":
    main()