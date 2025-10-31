"""
Handles possible methods for organism reproduction
"""
from Body import *
from Decoder import *
from utilities import *
import random

MUTATION_RATE = .01
START_FLIP_DIVISOR = 20
PARAM_FLIP_DIVISOR = 4
NON_CODING_DIVISOR = 1

# Genome parsing - possible combine this with decoder, that would mean genome is read once. Maybe having the Genome parsed into a directed graph would be easier?

# PARTHENOGENIC METHODS
def flip_at(pos, strand):
    val = int(strand[pos])-48
    chg = val^1
    strand = strand[:pos]+chr(chg+48).encode('utf-8')+strand[pos+1:]
    return strand

def flip_segment(segment, mutation_rate=MUTATION_RATE, divisor=1):
    count = 0
    for i in range(len(segment)):
        odds = (1 -(mutation_rate/divisor)) ** len(segment)
        roll = random.random()
        while roll > odds:
            count += 1
            roll = random.random()
        count = max(count, len(segment))
        for _ in range(len(count)):
            index = random.choice(range(len(segment)))
            segment = flip_at(index, segment)
    return segment

def increment_frame(frame, val):
    original length = length(frame)
    new_val = int(frame, 2) + val
    new_length = val.bit_length()
    
def random_bit_flip(organism, mutation_rate = MUTATION_RATE):
    """
    performs random bit flipping across the genome with equal weighting (highly chaotic, probably). Assumes it is getting an int back.
    """
    genome = bin(organism.get_genome())
    for i in range(1, genome.bit_length()):
        if random.random() < mutation_rate:
            genome = bit_flip(genome, i)
    return genome

def random_bit_flip_string(organism, mutation_rate = MUTATION_RATE):
    """
    Performs random bit flipping across genome, but treats genome as string instead. More promising I think. Assumes byt string returned
    """
    genome = organism.get_genome()
    for i in range(len(genome)):
        if random.random() < mutation_rate:
            genome = flip_at(i, genome)
    return genome
    
def bit_flip_in_params(organism, mutation_rate = MUTATION_RATE):
    """
    performs random bit flipping only on structures (does not flip OpCodes
    Add testing to ensure that structure is preserved.
    """
    organ_string = b''
    for organ in organism.get_organs():
        node= organ.get_dna_head()
        params = node.get_params()
        for i in range(len(params)):
            if random.random() < mutation_rate:
                params = flip_at(i, params)
        organ_string += params
        organ_string = organ_string + node.get_start() + params + node.get_noncoding()
        for gene in organ.get_genes():
            node = gene.get_dna_head()
            params = node.get_params()
            for i in range(len(params)):
                if random.random() < mutation_rate:
                    params = flip_at(i, params)
            organ_string += node.get_start() + params + node.get_noncoding()
    genome = organism.get_dna_head().get_noncoding()+organ_string
    return genome
    
def bit_flip_weighted(organism, mutation_rate = MUTATION_RATE):
    """
    Performs bit flipped on genome, but more strongly weighted for non coding sections
    Instead of checking every bit, lets just roll against the whole string? If it has length of 20, then its 1- odds ^ 20
    """
    genome = b''
    node = organism.get_dna_head()
    while node.next:
        start = node.get_start()
        if start is None:
            start = b''
        params = node.get_params()
        if params is None:
            params = b''
        noncoding = node.get_noncoding()
        if noncoding is None:
            noncoding = b''
        start = flip_segment(start, mutation_rate, START_FLIP_DIVISOR)
        params = flip_segment(params, mutation_rate, PARAM_FLIP_DIVISOR)
        noncoding = flip_segment(noncoding, mutation_rate, PARAM_NON_CODING
        
        genome += start+params+noncoding
        node = node.next
    return genome


def insert_to_preserve_order(organism, mutation_rate = MUTATION_RATE):
    """
    When a flip is performed that adds a structure that needs parameter values, random bits are inserted to preserve future reading frames
    # This might need to be handled by the decoder, perhaps by parsing the parents structure?
    """
    pass

def increment_decrement_frame(organism, mutation_rate = MUTATION_RATE):
    """
    Whenever a frame is read, that frame may be decremented or incremented.
    """
    genome = b''
    node = organism.get_dna_head()
    while node.next:
        
        if start is None:
            start = b''
        params = node.get_params()
        if params is None:
            params = b''
        noncoding = node.get_noncoding()
        if noncoding is None:
            noncoding = b''
    pass

# ANALOGOUS TO REALITY

def retrotransposition(organism, mutation_rate=MUTATION_RATE):
    """
    Copys a structure and pastes it elsewhere in the genome.
    """
    pass

def deletion(organism, mutation_rate=MUTATION_RATE):
    """
    Deletes a structure from the genome, preserve reading frame
    """
    pass

def duplication(organism, mutation_rate=MUTATION_RATE):
    """
    Duplicates a gene or structure and places it adjacent to this structure
    """
    pass
    
def point_deletion(organism, mutation_rate= MUTATION_RATE):
    """
    deletes a number of bits, preserve reading frame
    """
    pass
