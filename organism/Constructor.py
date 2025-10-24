# handles reading a genome
from Body import *
from Organ import *
from BioChemGene import *
from Chems import *
from utilities import *

GENE_READ_LENGTH = 4
GENE_TYPES = 2
GENE_START = b'11010'
ORGAN_START = b'11111'

class Decoder:

    def __init__(self):
        self._genome = None
        self._current_pos = 0
        self._current_organism = Body.Body()
        self._current_organ = None
        self._current_gene = None
        self._bits_for_funcs = dict(zip(func_names, bits_needed))

    def set_genome(self, genome):
        self._genome = genome
        
    def finish_organism(self):
        creature = self._current_organism
        self._current_organism = Body.Body()
        self._genome = None
        self._current_pos = 0
        self._current_organ = None
        self._current_gene = None
        return creature
    
    def read_at_pos(self, pos= self._current_pos, length = 5):
        if length = 0:
            return
        mask = ((1 << length) -1) << self._genome.bit_length()-(length + pos)
        val = bin((mask & self._genome) >> self._genome.bit_length()-(length+start_pos))
        if pos == self._current_pos:
            self._current_pos += length
        return val

    def read_genome(self):
        while self._current_pos < self._genome.bit_length() - 5:
            read_val = self._read_at_pos()
            if read_val == b'11010' and self._current_organ is not None:
                self.read_gene_data()
            if read_val == b'11111':
                self.read_organ_data()
        final = self.finish_organism()
        return final

    def read_organ_data():
        if self._current_organ != None:
            self._current_organism.add_organ(self._current_organ)
        self._current_organ = Organ(self)
        return

    def read_gene_data():
        type = self.read_at_pos(length = 1)
        if type == 1:
            self._current_gene = Emitter(self, 'emitter')
            rate = self.read_at_pos()
            self._current_gene.set_rate(int(rate))
        elif type == 0:
            self._current_gene = Receptor(self, 'receptor')
        
        # Now parse the function this gene uses.
        func = int(self.read_at_pos(length = 3))
        func_name = function_names[func]
        func_read_lengths = self._bits_for_funcs[func_name]
        params = []
        for param in func_read_lengths:
            params.append(self.read_at_pos(length = param))
        if params:
            function = functions[func](*params)
        else:
            function = function[func]()
        self._current_gene.set_function(func_name, function)
        
        
