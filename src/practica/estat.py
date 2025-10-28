import copy

class Estat:

    #Declaracio de map amb el moviment
    DIRECCIO = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "O": (-1, 0)}
    MOVIMENT = {"MOURE": 1, "BOTAR": 2, "POSAR_PARET": 3, "ESPERAR": 0}
    
    #Metode constructor
    def __init__(self, pos_agent, pos_parets, mida_taulell, desti, cami=None, cost=0):
        #Asignacio de variables
        self.pos_agent = tuple(pos_agent) 
        self.pos_parets = frozenset(pos_parets) 
        self.desti = tuple(desti) 
        self.cami = [] if cami is None else list(cami) 
        self.cost = cost 
        self.mida_taulell = mida_taulell 
        

    #Metode hash
    def __hash__(self):
        return hash((self.pos_agent, self.pos_parets))
    
    #Metode eq
    def __eq__(self, other):
        return self.pos_agent == other.pos_agent and self.pos_parets == other.pos_parets
  
    
    #Metode transicio 
    def transicio(self, accio):
        #Inicialitzacio i assignacio de variables
        nou_estat = copy.deepcopy(self)
        mov, dir = accio
        esLegal = True
        posObjectiu = nou_estat.pos_agent
        cost = 0

        #Comprova que la direccio passada estigui dins les possibilitats
        if dir not in self.DIRECCIO:
            return self, False
        
        #Obte les cordenades mitjançant del map DIRECCIO
        cord = Estat.DIRECCIO[dir]

        #Cas "ESPERAR"
        if mov == "ESPERAR":
             nou_estat = copy.deepcopy(self)
             #Afegeix l'accio al cami
             nou_estat.cami.append(("ESPERAR", None)) 
             #Actualitza el cost
             cost += self.MOVIMENT.get("ESPERAR", 0)
             return nou_estat, esLegal
        
        #Cas "BOTAR"
        if mov == "BOTAR":
            #Actualitza les coordenades
            posObjectiu = (self.pos_agent[0] + 2*cord[0], self.pos_agent[1] + 2*cord[1])
            #Comprova si el moviment es legal
            if self.posLegal(posObjectiu) == False:
                esLegal = False

        #Cas "MOURE"
        elif mov == "MOURE":
            #Actualitza les coordenades
            posObjectiu = (self.pos_agent[0] + cord[0], self.pos_agent[1] + cord[1])
            #Comprova si el moviment es legal
            if self.posLegal(posObjectiu) == False:
                esLegal = False

        #Cas "POSAR_PARET"
        elif mov == "POSAR_PARET":
             #Actualitza les coordenades
             posObjectiu = (self.pos_agent[0] + cord[0], self.pos_agent[1] + cord[1])
             #Comprova si el moviment es legal
             if self.posLegal(posObjectiu) == False or posObjectiu == self.desti:
                esLegal = False
        else:
            #Accio fora de les opcions
            return self, False

        #Si es legal
        if esLegal:
            #Cas "MOURE" i "BOTAR"
            if mov == "MOURE" or mov == "BOTAR":
                #Actualitza els atributs de la classe estat
                nou_estat.pos_agent = posObjectiu
                nou_estat.pos_parets = nou_estat.pos_parets | {self.pos_agent}
                nou_estat.cost += self.MOVIMENT[mov] 
                nou_estat.cami.append((mov, dir)) 
            #Cas "POSAR_PARET"
            elif mov == "POSAR_PARET":
                #Actualitza els atributs de la classe estat
                nou_estat.pos_parets = nou_estat.pos_parets | {self.pos_agent}
                nou_estat.cost += self.MOVIMENT[mov] 
                nou_estat.cami.append((mov, dir)) 
            return nou_estat, esLegal
        else:
            #En cas d'ilegalitat
            return self, False
            
                    
    #Metode per comprovar si la posicio on ens volem moure es legal
    def posLegal(self, posObjectiu):
        valid = True
        #Comprova que no hagi una paret
        for p in self.pos_parets:
            if p == posObjectiu:
                valid = False
        
        #Comprovar que no seguem defora del taulell
        #(negatiu)
        if posObjectiu[0] < 0 or posObjectiu[1] < 0:
            valid=False
        
        # mes gran que "mida_taulell"
        limits = self.mida_taulell[1]
        if posObjectiu[0] >= limits or posObjectiu[1] >= limits:
            valid=False

        #Retorna si es valid
        return valid
    
        

    #Metode genera fill
    def genera_fill(self):
        fills = []
        NouEstat, Legal = self.transicio(("ESPERAR", None))
        #Comprova si es legal 
        #Afegeix a fills
        if Legal:
            fills.append(NouEstat)

        #Per a cada cas restant comprova si es legal 
        #Afegeix a fills
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
    
