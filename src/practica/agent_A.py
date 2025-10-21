from practica.agent import Viatger
from practica.estat import Estat

#Metode constructor| frontera: Estats pendents a explorar, tancat: ja explorats, cami_exit: 
class Agent_A(Viatger):
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
        p=10000000
        

        self.__frontera.append(Estat_Inicial)
        #Mentres quedin estats a frontera
        while self.__frontera:
            #Agafa l'estat actual del proxim element de frontera
            estat_actual = self.__frontera.pop(0)

            #Si ja hem explorat l'estat o hi ha una paret passa a una altre iteracio
            if estat_actual in self.__tancat or estat_actual.HiHaParet():
                continue


            p2 = estat_actual.cost
            if p2 < p:
                p = p2
                print(p)
            else:
                continue
          
               

            #Si hem arribat al desti final surt del bucle
            if estat_actual.DestiFinal():
                break

            #Te comprova tots els estats disponibles en aquell moment y actualitza frontera (estats a explorar)
            for f in estat_actual.genera_fill(percepcio["MIDA"]):
                self.__frontera.append(f)
                

            #Afegeix al tancat(ja explorats l'estat actual)
            self.__tancat.add(estat_actual)

        #Si l'estat actual es igual al desti que volem arribat guarda el cami y actualitza a true la variable true
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