from practica.agent import Viatger
from practica.estat import Estat
from queue import PriorityQueue


#Metode constructor| frontera: Estats pendents a explorar, tancat: ja explorats, cami_exit: 
class Agent_A(Viatger):
    def __init__(self):
        super().__init__()
        self.__frontera = None
        self.__tancat = None
        self.__cami_exit = None

    
    def cerca(self, estat_inicial: Estat, percepcio):
        #Inicialitzacio de variables a 0
        self.__frontera = PriorityQueue()
        self.__tancat = set()
                

        self.__frontera.put((estat_inicial.CalculaCost(), estat_inicial))
        actual = None
        #Mentres quedin estats a frontera
        while not self.__frontera.empty():
            #Agafa l'estat actual del proxim element de frontera
            _, actual = self.__frontera.get()

            #Si ja hem explorat l'estat o hi ha una paret passa a una altre iteracio
            if actual in self.__tancat :
                continue
          
            #Si hem arribat al desti final surt del bucle
            if actual.DestiFinal():
                break
            
            estat_fills = actual.genera_fill(percepcio["MIDA"])
            #Te comprova tots els estats disponibles en aquell moment y actualitza frontera (estats a explorar)
            for f in estat_fills:
                self.__frontera.put((f.CalculaCost(), f))
                

            #Afegeix al tancat(ja explorats l'estat actual)
            self.__tancat.add(actual)

        #Si l'estat actual es igual al desti que volem arribat guarda el cami y actualitza a true la variable exit
        if actual.DestiFinal():
            self.__cami_exit = actual.cami
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