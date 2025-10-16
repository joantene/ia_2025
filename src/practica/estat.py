import copy

class Estat:

    #Declaracio de map amb el moviment
    moviment = {"N": (0,-1),
                "S": (0,1),
                "E": (1,0),
                "O": (-1,0)}
    
    #Metode constructor
    def __init__(self, pos_agent, pos_parets, desti, cami = None):
        if cami is None:
            cami = []
            
        self.pos_agent = pos_agent
        self.pos_parets = pos_parets
        self.desti = desti
        self.cost = 0
        self.accio = None

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
    def transicio(self, acc):
        nou_estat = copy.deepcopy(self)
        mov, acc = acc
        pes = 0
        esLegal = True
        self.posAntiga = self.pos_agent
        posObjectiu = self.pos_agent
        dir = Estat.moviment[mov]
        if acc == "BOTAR":
            posObjectiu = (self.pos_agent[0] + 2*dir[0], self.pos_agent[1] + 2*dir[1])
        if acc == "MOURE" or acc == "POSAR_PARET":
            posObjectiu = (self.pos_agent[0] + dir[0], self.pos_agent[1] + dir[1])

        if self.posLegal(posObjectiu) == False:
            esLegal = False
        else:
            if acc == "MOURE" or acc == "BOTAR":

                nou_estat.pos_agent = posObjectiu
                nou_estat.accio = acc
                pes = nou_estat.CalculaCost()
                nou_estat.pos_parets.add(self.posAntiga)
            elif acc == "POSAR_PARET":
                nou_estat.pos_parets.add(posObjectiu)
                nou_estat.accio = acc
                pes = nou_estat.CalculaCost()

        return nou_estat,esLegal, pes

    #Metode per comprovar si la posicio on ens volem moure es legal FALTA REVISAR MARGES 0 I 9
    def posLegal(self, posObjectiu):
        valid = True
        for p in self.pos_parets:
            if p == posObjectiu:
                valid = False
        return valid

    
    #Metode per comprovar si la posicio on ens volem moure es legal FALTA REVISAR MARGES 0 I 9
    def posLegal(self, posObjectiu):
        valid = True
        if posObjectiu[0] < 0 or posObjectiu[0] > 9 or posObjectiu[1] < 0 or posObjectiu[1] > 9:
            valid = False
        else:
            for p in self.pos_parets:
                if p == posObjectiu:
                    valid = False
        return valid

    #Metode genera fill
    def genera_fill(self):

        estats_generats= []
        accions_possibles = self.accions_possibles()
        for accions in accions_possibles:
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
        elif self.accio == "POSAR_PARET":
            self.cost = self.cost + 3

