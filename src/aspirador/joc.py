from iaLib import agent, joc

class Aspirador(joc.JocNoGrafic):

    def __init__(self, agents: list[agent.Agent] | None = None):
        if agents is None:
            agents = []
        super(Aspirador, self).__init__(agents=agents)
        # Definimos las dos habitaciones
        self.habitaciones = {"E": False, "D" : False}
        # Declaram l'aspirador
        self.Aspirador = "E"


    def _draw(self): 
        # Mostram on es troba l'aspirador
        print("L'Aspirador es troba a l'habitacio ",self.Aspirador)

        #Mostram l'estat de les dues habitacions
        print("L'habitacio de l'esquerra es troba neta? ",self.habitaciones["E"])
        print("L'habitacio de la dreta es troba neta? ",self.habitaciones["D"])
        pass


    def percepcio(self):
        # Mostram la posicio actual de l'aspirador
        print("L'Aspirador es troba a l'habitacio ",self.Aspirador)

        # Mostram si l'habitacio es neta o bruta
        if self.Aspirador == "E":
            print("L'habitacio es troba neta? ",self.habitaciones["E"])
        else:
            print ("L'habitacio es troba neta ",self.habitaciones["D"])
        pass


    def _aplica(self, accio, params=None, agent_actual=None):
        # accio de netejar
        if accio == "Netejar":
            if self.Aspirador == "E":
                if not self.habitaciones["E"]:
                    self.habitaciones["E"] = True
            else:
                if not self.habitaciones["D"] :
                    self.habitaciones["D"] = True
            
        # accio de moure
        elif accio == "Moure":
            if self.Aspirador == "E":
                self.Aspirador = "D"
            else:
                self.Aspirador = "E"

        # accio de comprovar
        elif accio == "comprovar":
            if self.habitaciones["E"] and self.habitaciones["D"]:
                print("Les dues estan netes")
            else:
                print ("Les dues NO estan netes")
        pass

