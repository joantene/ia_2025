import copy

class Estat:

    #Declaracio de map amb el moviment
    DIRECCIO = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "O": (-1, 0)}
    MOVIMENT = {"MOURE": 1, "BOTAR": 2, "POSAR_PARET": 3, "ESPERAR": 0}
    
    #Metode constructor
    def __init__(self, pos_agent, pos_parets, desti, cami=None, cost=0):
        self.pos_agent = tuple(pos_agent)
        # fem frozenset per fer hashable; si ja és frozenset no passa res
        self.pos_parets = frozenset(pos_parets)
        self.desti = tuple(desti)
        self.cami = [] if cami is None else list(cami)
        self.cost = cost
        

    #Metode hash
    def __hash__(self):
        return hash((self.pos_agent, self.pos_parets))
    
    #Metode eq
    def __eq__(self, other):
        return self.pos_agent == other.pos_agent and self.pos_parets == other.pos_parets
  
    
    #Metode transicio 
    def transicio(self, accio):
        nou_estat = copy.deepcopy(self)
        mov, dir = accio
        esLegal = True
        posObjectiu = nou_estat.pos_agent
        cost = 0
        if dir not in self.DIRECCIO:
            return self, False
        cord = Estat.DIRECCIO[dir]
        if mov == "ESPERAR":
             nou_estat = copy.deepcopy(self)
             nou_estat.cami.append(("ESPERAR", None)) 
             cost += self.MOVIMENT.get("ESPERAR", 0)
             return nou_estat, esLegal
        if mov == "BOTAR":
            posObjectiu = (self.pos_agent[0] + 2*cord[0], self.pos_agent[1] + 2*cord[1])
            if self.posLegal(posObjectiu) == False:
                esLegal = False

        elif mov == "MOURE":
            posObjectiu = (self.pos_agent[0] + cord[0], self.pos_agent[1] + cord[1])
            if self.posLegal(posObjectiu) == False:
                esLegal = False

        elif mov == "POSAR_PARET":
             posObjectiu = (self.pos_agent[0] + cord[0], self.pos_agent[1] + cord[1])
             if self.posLegal(posObjectiu) == False or posObjectiu == self.desti:
                esLegal = False
        else:
            #Accio fora de les opcions
            return self, False

        if esLegal:
            if mov == "MOURE" or mov == "BOTAR":

                nou_estat.pos_agent = posObjectiu
                nou_estat.pos_parets = nou_estat.pos_parets | {self.pos_agent}
                nou_estat.cost += self.MOVIMENT[mov] 
                nou_estat.cami.append((mov, dir)) 
            elif mov == "POSAR_PARET":
                nou_estat.pos_parets = nou_estat.pos_parets | {self.pos_agent}
                nou_estat.cost += self.MOVIMENT[mov] 
                nou_estat.cami.append((mov, dir)) 
            return nou_estat, esLegal
        else:
            return self, False
            
                    

    #Metode per comprovar si la posicio on ens volem moure es legal FALTA REVISAR MARGES 0 I 9
    def posLegal(self, posObjectiu):
        valid = True
        for p in self.pos_parets:
            if p == posObjectiu:
                valid = False
        return valid
        
    
    #Metode genera fill
    def genera_fill(self):
        fills = []
        NouEstat, Legal = self.transicio(("ESPERAR", None))
        if Legal:
            fills.append(NouEstat)

        for direccio in self.DIRECCIO:
            for moviment in self.MOVIMENT:
                if moviment == "ESPERAR":
                    break
                NouEstat, Legal = self.transicio((moviment, direccio))
                if Legal:
                    fills.append(NouEstat)

        return fills

    #Metode per comprovar si som al desti
    def es_meta(self):
        if self.desti == self.pos_agent:
            return True 
        return False
    
    #Metode per comprovat si la posicio on ens volem moure hi ha una paret
    def HiHaParet(self):
        for p in self.pos_parets:
            if p == self.pos_agent:
                return True
        return False

    #funcio per calcular el cost de l'euristica
    def CalculaCost(self):
        heuristica = abs(self.pos_agent[0] - self.desti[0]) + abs(self.pos_agent[1] - self.desti[1])
        return self.cost + heuristica
    
