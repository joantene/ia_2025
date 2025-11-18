from practica.agent import Viatger
from practica.estat import Estat


class AgentMinimax(Viatger):
    #Metode constructor
    def __init__(self, poda=False):
        super().__init__()
        self.__poda = poda

    #Metode Cerca
    def cerca(self, estat: Estat, percepcio, alpha, beta, torn_max=True, profunditat=0, max_profunditat=4):
        # Condició de parada: estat meta o profunditat màxima
        if estat.es_meta() or profunditat >= max_profunditat:
            # Heurística: distància Manhattan negativa (millor si està més a prop)
            distancia = abs(estat.pos_agent[0] - estat.desti[0]) + abs(estat.pos_agent[1] - estat.desti[1])
            puntuacio = -distancia - estat.cost  # penalitzar cost i distància
            return estat, puntuacio

        puntuacio_fills = []

        for fill in estat.genera_fill():
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

    #Metode pinta
    def pinta(self, display):
        pass

    #Metode actua
    def actua(self, percepcio):
        #Inicialitza estat inicial en el cas que aquest sigui null
        estat_inicial = Estat(
            pos_agent=percepcio["AGENTS"][self.nom],
            pos_parets=percepcio["PARETS"],
            desti=percepcio["DESTI"],
            mida_taulell=percepcio["MIDA"]
        )
        #Crida el metode cerca
        res = self.cerca(estat_inicial, percepcio, alpha=-float('inf'), beta=float('inf'))

        if isinstance(res, tuple) and res[0].cami is not None and len(res[0].cami) > 0:
            solucio, _ = res
            #Extreu les passes i actua
            direccio = solucio.cami[0]
            
            if direccio[0] == "ESPERAR":
                return "ESPERAR", None
            if direccio[0] == "MOURE":
                return "MOURE", direccio[1]  
            if direccio[0] == "BOTAR":
                return "BOTAR", direccio[1]    
            if direccio[0] == "POSAR_PARET":

                return "POSAR_PARET", direccio[1]
                
            else:
                return "ESPERAR", None
            
        else:
            return "ESPERAR", None