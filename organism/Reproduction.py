"""
Handles possible methods for organism reproduction
"""
from Body import *
from Decoder import *
from utilities import *
import random

MUTATION_RATE = .01

# Genome parsing - possible combine this with decoder, that would mean genome is read once. Maybe having the Genome parsed into a directed graph would be easier?

# PARTHENOGENIC METHODS
def random_bit_flip(organism, mutation_rate = MUTATION_RATE):
    """
    performs random bit flipping across the genome with equal weighting (highly chaotic, probably)
    """
    genome = organism.get_genome()
    for i in range(1, genome.bit_length()):
        if random.random() < mutation_rate:
            genome = bit_flip(genome, i)
    return genome

def bit_flip_in_params(organism, mutation_rate = MUTATION_RATE):
    """
    I need to make another decoder that tracks frame views, organ starts, and gene starts? 
    performs random bit flipping only on structures (does not flip OpCodes
    """
    pass

def bit_flip_weighted_to_params(organism, mutation_rate = MUTATION_RATE):
    """
    Performs bit flipped on genome, but more strongly weighted to parameters
    """
    pass

def insert_to_preserve_order(organism, mutation_rate = MUTATION_RATE):
    """
    When a flip is performed that adds a structure that needs parameter values, random bits are inserted to preserve future reading frames
    """
    pass

def increment_decrement_frame(organism, mutation_rate = MUTATION_RATE):
    """
    Whenever a frame is read, that frame may be decremented or incremented.
    """
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
