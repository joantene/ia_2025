import copy

class Estat:

    #Declaracio de map amb el moviment
    moviment = {"N": (0,-1),
                "S": (0,1),
                "E": (1,0),
                "O": (-1,0)}
    
    #Metode constructor
    def __init__(self, pos_agent, pos_parets, desti, accio, cost):
        if cami is None:
            cami = []
            
        self.pos_agent = pos_agent
        self.pos_parets = pos_parets
        self.desti = desti
        self.accio = accio
        self.cost = cost

        self.cami = cami
        
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
        return hash(self.pos_agent, self.pos_parets)
    
    #Metode eq
    def __eq__(self, other):
        return self.pos_agent == other.pos_agent and self.pos_parets == other.pos_parets
        
    #Metode transicio 
    """IMPLEMENTAR"""
    def transicio(self, acc, dir):
        nou_estat = copy.deepcopy(self)
        acc, pos = acc
        pes = 0

        if acc == "G":
            nou_estat.info[pos] = Estat.gira(nou_estat.info[pos])
            pes = 1
        elif acc == "D" or acc == "B":
            moneda = nou_estat.info[pos]
            if acc == "B":
                moneda = Estat.gira(moneda)

            nou_estat.info[self.__pos_lliure()] = moneda
            nou_estat.info[pos] = " "
            pes = 2

        return nou_estat, pes
    
    #Metode genera fill
    def genera_fill(self):

        estats_generats= []

        for accions in self.moviment:
            fill, es_legal = self.transicio(accions)
            if es_legal:
                fill.cami.append(accions)
                estats_generats.append(fill)

        return estats_generats

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

