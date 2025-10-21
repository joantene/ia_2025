from practica.agent import Viatger
from practica.estat import Estat


class AgentMinimax(Viatger):
    def __init__(self, poda=False):
        super().__init__()
        self.__cami_exit = None
        self.__poda = poda

    def cerca(self, estat: Estat, percepcio, alpha, beta, torn_max=True, profunditat=0, max_profunditat=10):
        # Condició de parada: estat meta o profunditat màxima
        if estat.DestiFinal() or profunditat >= max_profunditat:
            # Heurística: distància Manhattan negativa (millor si està més a prop)
            distancia = abs(estat.pos_agent[0] - estat.desti[0]) + abs(estat.pos_agent[1] - estat.desti[1])
            puntuacio = -distancia - estat.cost  # penalitzar cost i distància
            return estat, puntuacio

        puntuacio_fills = []

        for fill in estat.genera_fill(percepcio["MIDA"]):
            punt_fill = self.cerca(fill, percepcio, alpha, beta, not torn_max, profunditat + 1, max_profunditat)

            if torn_max:
                alpha = max(alpha, punt_fill[1])
            else:
                beta = min(beta, punt_fill[1])

            puntuacio_fills.append(punt_fill)

            if self.__poda and alpha >= beta:
                break

        if not puntuacio_fills:
            # No hi ha fills vàlids
            distancia = abs(estat.pos_agent[0] - estat.desti[0]) + abs(estat.pos_agent[1] - estat.desti[1])
            return estat, -distancia - estat.cost

        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1])
        if torn_max:
            return puntuacio_fills[-1]
        else:
            return puntuacio_fills[0]

    def pinta(self, display):
        pass

    def actua(self, percepcio):
        estat_inicial = Estat(
            pos_agent=percepcio["AGENTS"][self.nom],
            pos_parets=percepcio["PARETS"],
            desti=percepcio["DESTI"]
        )
        
        res = self.cerca(estat_inicial, percepcio, alpha=-float('inf'), beta=float('inf'))

        if isinstance(res, tuple) and res[0].cami is not None and len(res[0].cami) > 0:
            solucio, _ = res
            # Retornar la primera acció del camí
            accio = solucio.cami[0]
            tipus, direccio = accio
            
            if tipus == "ESPERAR":
                return "ESPERAR"
            elif tipus == "MOURE":
                return direccio
            elif tipus == "BOTAR":
                return direccio  # o retornar un format específic per BOTAR si cal
            elif tipus == "POSAR_PARET":
                return f"PARET_{direccio}"  # adapta segons el format que espera el joc
        
        return "ESPERAR"
