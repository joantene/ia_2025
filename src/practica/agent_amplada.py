from practica.estat import Estat
from practica.agent import Viatger

#Cerca no informada, BFS

class agent_amplada(Viatger):
    def __init__(self):
        
            super().__init__()
            self.__frontera = None
            self.__tancat = None
            self.__cami_exit = None


    def cerca(self, Estat_Inicial: Estat, percepcio):
        #Inicialitzacio de variables a 0
        self.__frontera = []
        self.__tancat = set()
        exit = False

        self.__frontera.append(Estat_Inicial)
        while self.__frontera:
            estat_actual = self.__frontera.pop(0)

            if estat_actual in self.__tancat or estat_actual.HiHaParet():
                continue

            if estat_actual.DestiFinal():
                break

            for f in estat_actual.genera_fill(percepcio["MIDA"]):
                self.__frontera.append(f)

            self.__tancat.add(estat_actual)

        if estat_actual.DestiFinal():
            self.__cami_exit = estat_actual.cami
            exit = True


        return exit
    
    def actua(self, percepcio: dict):


        if self.__cami_exit is None:
            estat_inicial = Estat(
                pos_agent=percepcio["AGENTS"][self.nom],
                pos_parets=percepcio["PARETS"],
                desti=percepcio["DESTI"],
            )

            self.cerca(estat_inicial, percepcio)


        if self.__cami_exit:

            direccio = self.__cami_exit.pop(0)

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