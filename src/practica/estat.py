import copy

class Estat:

    #Declaracio de map amb el moviment
    MOVIMENT = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "O": (-1, 0)}
    COSTS = {"MOURE": 1, "BOTAR": 2, "POSAR_PARET": 3}
    
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
    """IMPLEMENTAR"""
    def transicio(self, accio):

        """
        Acció: tuple (tipus, direccio)
        tipus ∈ {"MOURE","BOTAR","POSAR_PARET","ESPERAR"}
        direccio ∈ {"N","S","E","O"} o None

        Retorna (nou_estat, es_legal_bool)
        """
        tipus, direccio = accio
        x, y = self.pos_agent

        # Cas especial: esperar
        if tipus == "ESPERAR":
            nou = copy.deepcopy(self)
            nou.cami.append(("ESPERAR", None))
            # Pots deixar cost 0 si esperar no ha de costar res
            nou.cost += 0
            return nou, True

        # Si no hi ha direcció vàlida
        if direccio not in self.MOVIMENT:
            return self, False

        dx, dy = self.MOVIMENT[direccio]

        # 🔹 1. MOURE
        if tipus == "MOURE":
            nx, ny = x + dx, y + dy
            if (nx, ny) in self.pos_parets:
                return self, False  # No pots moure't dins una paret

            noves_parets = set(self.pos_parets)
            noves_parets.add((x, y))  # Deixa paret darrere
            nou = Estat(
                pos_agent=(nx, ny),
                pos_parets=noves_parets,
                desti=self.desti,
                cami=self.cami + [(tipus, direccio)],
                cost=self.cost + self.COSTS["MOURE"]
            )
            return nou, True

        # 🔹 2. BOTAR
        if tipus == "BOTAR":
            nx, ny = x + 2 * dx, y + 2 * dy
            if (nx, ny) in self.pos_parets:
                return self, False  # No pots caure dins una paret

            noves_parets = set(self.pos_parets)
            noves_parets.add((x, y))
            nou = Estat(
                pos_agent=(nx, ny),
                pos_parets=noves_parets,
                desti=self.desti,
                cami=self.cami + [(tipus, direccio)],
                cost=self.cost + self.COSTS["BOTAR"]
            )
            return nou, True

        # 🔹 3. POSAR_PARET
        if tipus == "POSAR_PARET":
            px, py = x + dx, y + dy
            if (px, py) in self.pos_parets or (px, py) == self.desti:
                return self, False  # No pots posar paret al destí o damunt d'una paret

            noves_parets = set(self.pos_parets)
            noves_parets.add((px, py))
            nou = Estat(
                pos_agent=(x, y),
                pos_parets=noves_parets,
                desti=self.desti,
                cami=self.cami + [(tipus, direccio)],
                cost=self.cost + self.COSTS["POSAR_PARET"]
            )

            return nou, True

        # 🔹 Si no entra en cap cas
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