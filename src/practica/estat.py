import copy
"""CHAT
-Init
-Genera Fills
-Transicio
    """
class Estat:

    #Declaracio de map amb el moviment
    MOVIMENT = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "O": (-1, 0)}
    COSTS = {"MOURE": 1, "BOTAR": 2, "POSAR_PARET": 3, "ESPERAR": 0}
    
    #Metode constructor
    def __init__(self, pos_agent, pos_parets, desti, cami=None, cost=0):
        self.pos_agent = tuple(pos_agent)
        # fem frozenset per fer hashable; si ja és frozenset no passa res
        self.pos_parets = frozenset(pos_parets)
        self.desti = tuple(desti)
        self.cami = [] if cami is None else list(cami)
        self.cost = cost
        
    @property
    def accions_possibles(self):

        accions_possibles = []
        accions_possibles.append((0, "ESPERAR"))
        #MOURE
        for direccio in Estat.moviment:
            accions_possibles.append((direccio, "MOURE"))
        #BOTAR
        for direccio in Estat.moviment:
            accions_possibles.append((direccio, "BOTAR"))
        #POSAR PARET
        for direccio in Estat.moviment:
            accions_possibles.append((direccio, "POSAR_PARET"))

        return accions_possibles

    #Metode hash
    def __hash__(self):
        return hash((self.pos_agent, self.pos_parets))
    
    #Metode eq
    def __eq__(self, other):
        return self.pos_agent == other.pos_agent and self.pos_parets == other.pos_parets
        
    
#Metode transicio 
    import copy

    def transicio(self, accio):
        """
        Mètode corregit per utilitzar reassignació de frozenset (no té .add()).
        Acció: tuple (tipus, direccio)
        Retorna (nou_estat, es_legal_bool)
        """
        tipus, direccio = accio 
        x, y = self.pos_agent
        
        # 1. CAS ESPECIAL: ESPERAR
        if tipus == "ESPERAR":
            nou_estat = copy.deepcopy(self)
            nou_estat.cami.append(("ESPERAR", None)) 
            nou_estat.cost += self.COSTS.get("ESPERAR", 0)
            return nou_estat, True

        # Comprovació de direcció i càlcul del vector de moviment
        if direccio not in self.MOVIMENT:
            return self, False
            
        dx, dy = self.MOVIMENT[direccio] 

        # 2. Càlcul de posObjectiu i Preparació
        nou_estat = copy.deepcopy(self)
        esLegal = True
        posParet = None # Posició de la paret a afegir
        
        if tipus == "BOTAR":
            # Posició d'aterratge
            posObjectiu = (x + 2 * dx, y + 2 * dy)
            posParet = (x, y) # Paret es deixa a la posició actual
            
            if posObjectiu in self.pos_parets:
                esLegal = False

        elif tipus == "MOURE":
            # Posició final
            posObjectiu = (x + dx, y + dy)
            posParet = (x, y) # Paret es deixa a la posició actual
            
            if posObjectiu in self.pos_parets:
                esLegal = False

        elif tipus == "POSAR_PARET":
            # Posició on es col·loca la paret
            posParet = (x + dx, y + dy)
            
            if posParet in self.pos_parets or posParet == self.desti:
                esLegal = False
                
            posObjectiu = self.pos_agent # L'agent no es mou

        else:
            # Tipus d'acció desconeguda
            return self, False

        # 3. APLICACIÓ DELS CANVIS (Si és legal)
        if esLegal:
            if tipus in {"MOURE", "BOTAR"}:
                nou_estat.pos_agent = posObjectiu
                
                # 🔴 CORRECCIÓ FROZENSET (Unió i reassignació)
                nou_estat.pos_parets = nou_estat.pos_parets | {posParet}
                
            elif tipus == "POSAR_PARET":
                # 🔴 CORRECCIÓ FROZENSET (Unió i reassignació)
                nou_estat.pos_parets = nou_estat.pos_parets | {posParet}
                
            # Actualització final (cost i camí)
            nou_estat.cost += self.COSTS[tipus] 
            nou_estat.cami.append((tipus, direccio)) 
            
            return nou_estat, True
        
        # 4. Retorn en cas d'il·legalitat
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
    def genera_fill(self, mida):
        fills = []

        # Acció ESPERAR
        nou, ok = self.transicio(("ESPERAR", None))
        if ok:
            fills.append(nou)

        for direccio in self.MOVIMENT:
            dx, dy = self.MOVIMENT[direccio]
            
            
            # MOURE
            nx, ny = self.pos_agent[0] + dx, self.pos_agent[1] + dy
            if 0 <= nx < mida[0] and 0 <= ny < mida[1]:
                nou, ok = self.transicio(("MOURE", direccio))
                if ok:
                    fills.append(nou)

            # BOTAR
            nx, ny = self.pos_agent[0] + 2*dx, self.pos_agent[1] + 2*dy
            if 0 <= nx < mida[0] and 0 <= ny < mida[1]:
                nou, ok = self.transicio(("BOTAR", direccio))
                if ok:
                    fills.append(nou)

            # POSAR_PARET
            px, py = self.pos_agent[0] + dx, self.pos_agent[1] + dy
            if 0 <= px < mida[0] and 0 <= py < mida[1]:
                nou, ok = self.transicio(("POSAR_PARET", direccio))
                if ok:
                    
                    fills.append(nou)

        return fills

    #Metode per comprovar si som al desti
    def DestiFinal(self):
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
        if self.accio == "MOURE":
            self.cost = self.cost + 1
        elif self.accio == "BOTAR":
            self.cost = self.cost + 2
        else:
            self.cost = self.cost +3
            
    