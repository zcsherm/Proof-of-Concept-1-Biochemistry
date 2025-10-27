"""
A simple structure for prototyping
"""
from utilities import *

class Organ:
    def __init__(self, type, owner):
        # Should probably have the owner referenced by ID to save space, then have a get_owner_by_id() to get the actual organism
        self._genes = []
        self._id = generate_id()
        self._owner = owner
        self._health = 1
        self._parameters = []

class InternalOrgan(Organ):
    """
    Internal organs focus on managing bloodstream and chemicals
    """
    def add_gene(self, gene):
        self._genes.append(gene)

    def set_def_health(self, val=1):
        """
        Sets the default health
        """
        self._health = val
        self._health_receptors = []
        self._parameters.append(('health', self._health))

    def set_act_rate(self, act_rate):
        """
        Determines how often this organ is activated
        """
        self._act_rate = act_rate
        self._act_rate_receptors = []
        self._parameters.append(('activation rate', self._act_rate))

    def set_reaction_rate(self, rate):
        self._reaction_rate = rate
        self._reaction_rate_receptors = []
        self._parameters.append(('reaction rate', self._reaction_rate))

    def get_param_numbers(self):
        return len(self._parameters)

    def get_param_at_index(self, index):
        return self._parameters[index]

    def read_health_from_gene(self, output):
        """
        This is passed to the gene(hopefully space efficient) and it should add the output to a queue, which is then averaged
        """
        self._health_receptors.append(output)

    def read_act_rate_from_gene(self, output):
        self._act_rate_receptors.append(output)

    def read_reaction_rate_from_gene(self, output):
        self._reaction_rate_receptors.append(output)

    def clear_receptors(self):
        self._health_receptors = []
        self._act_rate_receptors = []
        self._reaction_rate_receptors = []
    
    def get_parameter(self, param):
        if param == 'health':
            return self._health
        if param == 'activation rate':
            return self._act_rate
        if param == 'reaction rate':
            return self._reaction_rate
            
    def release_chemical(self, chemical, amount):
        amount *= self._health
        self._owner.add_chemical(chemical, amount)
        
    def get_health(self):
        return self._health

    def get_act_rate(self):
        return self._act_rate

    def get_reaction_rate(self):
        return self._reaction_rate

    def get_concentration(self, chemical):
        return self._owner.get_concentration(chemical)
        
    def get_param_adjust(self, gene=>Receptor):
        return gene.adjust_parameter()
        
    def activate_organ(self):
        for gene in self._genes:
            type = gene.get_type()
            if type == 'receptor':
                gene.adjust_parameter()
            elif type == 'emitter':
                gene.release_chemical()
        self._reaction_rate = sum(self._reaction_rate_receptors) / max(len(self._reaction_rate_receptors),1)
        self._act_rate = sum(self._act_rate_receptors) / max(len(self._act_rate_receptors), 1)
        average_health_change = sum(self._health_receptors) / max(len(self._health_receptors), 1)
        self._health = health_decay(self._health, average_health_change)
