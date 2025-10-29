# handles reading a genome
from Body import *
from Organ import *
from BioChemGene import *
from Chemicals import *
from utilities import *

GENE_READ_LENGTH = 4
GENE_TYPES = 2
GENE_OPCODES = [0b11010]
ORGAN_OPCODES = [0b11111]

class Decoder:

    def __init__(self):
        """
        Initialize to begin reading a dna strand
        """
        self._genome = None
        self._current_pos = 1
        self._current_organism = Body()
        self._current_organ = None
        self._current_gene = None
        # Create a map for how many bits to read to assemble a function
        self._bits_for_funcs = dict(zip(func_names, bits_needed))

    def set_genome(self, genome):
        """
        Sets the active genome
        """

        self._genome = b'1' + genome # prepend a 1 to prevent leading zero discrepensies
        self._bin_genome = int(genome.decode(),2)
        self._leading_zeroes = len(self._genome)-self._bin_genome.bit_length()

        
    def finish_organism(self):
        """
        On reading the whole strand, the organism will be finished, and the decoder will be reset
        """
        if self._current_organ is not None:
            self._current_organism.add_organ(self._current_organ)
        creature = self._current_organism
        self._current_organism = Body()
        self._genome = None
        self._current_pos = 1
        self._current_organ = None
        self._current_gene = None
        return creature
    
    def read_at_pos(self, pos=None, length = 5):
        """
        Reads a section of Binary DNA, at a starting position and with a length
        """
        if pos == None:
            pos = self._current_pos
        if length == 0:
            return
        if pos >= len(self._genome):
            self._current_pos = len(self._genome)
            return 0
        if pos + length >= len(self._genome):
            self._current_pos = len(self._genome)
            return 0
        mask = ((1 << length) -1) << len(self._genome)-(length + pos)
        val = (mask & self._bin_genome) >> len(self._genome)-(length+pos)
        if pos == self._current_pos:
            self._current_pos += length
        return val

    def read_genome(self):
        """
        Continually reads the genome, constructing an organism as it goes.
        """
        while self._current_pos < len(self._genome) - 5:
            read_val = self.read_at_pos()
            # If the gene start code was encountered begin constructing a gene
            if read_val in GENE_OPCODES and self._current_organ is not None:
                self.read_gene_data()

            # If the organ start code was encountered, begin constructing an organ
            if read_val in ORGAN_OPCODES:
                self.read_organ_data()

        # Finalize the organism and return it when complete.
        final = self.finish_organism()
        return final

    def read_organ_data(self):
        """
        Reads organ data (right now, only has 3 parameters: health, activation, and reaction), constructs the organ.
        """
        # Assign the current organism the previously active organ
        if self._current_organ is not None:
            self._current_organism.add_organ(self._current_organ)

        # Create a new organ and get the parameters.
        self._current_organ = InternalOrgan('internal', self._current_organism)
        self._current_organ.set_def_health()
        val = self.read_at_pos()
        self._current_organ.set_reaction_rate(int(val)/32)
        self._current_organ.set_act_rate(int(self.read_at_pos())/32)
        return

    def read_gene_data(self):
        """
        Constructs a gene (currently only 2 types (emitter, and receptor))) and gets parameters for it.
        """
        # Find out what type of gene it is
        type = self.read_at_pos(length = 1)
        if type == 1:
            self._current_gene = Emitter(self._current_organ, 'emitter')
            rate = self.read_at_pos()
            self._current_gene.set_output_rate(int(rate))
        elif type == 0:
            self._current_gene = Receptor(self._current_organ, 'receptor')
        
        # Now parse the function this gene uses. Each function needs different parameters
        func = int(self.read_at_pos(length = 3))
        func_name = func_names[func]
        func_read_lengths = bits_needed[func]
        params = []
        # If the function needs parameters, then read each one as needed
        for param in func_read_lengths:
            params.append(self.read_at_pos(length = param))
        if params:
            function = functions[func](*params)
        else:
            function = functions[func]()
        self._current_gene.set_activation(func_name, function)

        # Now handle the other parameters of the gene
        val = int(self.read_at_pos(length = 4) % self._current_organ.get_param_numbers())
        p=  self._current_organ._parameters[val]
        self._current_gene.set_parameter(p[0], p[1])
        val = int(self.read_at_pos(length = 4))
        self._current_gene.set_chemical(val)
        self._current_organ.add_gene(self._current_gene)
        

