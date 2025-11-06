import unittest
import copy
import random
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from utilities import *
import Constructor
from Constructor import Decoder, DecoderLinkedList
from Reproduction import *


ORGAN_START = b'11001000'
O_PARAM_ONE = b'00001'
O_PARAM_TWO = b'00101'
GENE_START = b'01100100'
GENE_TYPE = b'0001'          # Emitter
GENE_RATE = b'11101'
GENE_FUNC = b'0110010'    # Exponential -> pow of 2
GENE_PARAMS = b'00010101' #Link to act_rate and chem 5
GENE_TWO = b'0000'
GENE_TWO_FUNC = b'11110101101000001' # Reverse sigmoid with coef = 86, mean= 65/128
GENE_TWO_PARAMS = b'00100011' # Link to reaction rate and chem 3
GENE_THREE = b'0010' # Reaction gene
GENE_THREE_PARAMS = b'00110001' # 2, 1
GENE_THREE_CHEMS =b'010000011000100001001000000010' # 16, 6, 8, 4, 32, 2
TEST_GENOME = ORGAN_START + O_PARAM_ONE + O_PARAM_TWO + GENE_START + GENE_TYPE + GENE_RATE + GENE_FUNC +GENE_PARAMS + GENE_START + GENE_TWO + GENE_TWO_FUNC + GENE_TWO_PARAMS + GENE_START + GENE_THREE + GENE_THREE_PARAMS + GENE_THREE_CHEMS + ORGAN_START + b'10101010101010101101010101010101001010101010'

TEST_A = b'110101'
TEST_B = b'111101'
TEST_C = b'010101'
TEST_D = b'110100'
TEST_E = b'110110'
TEST_F = b'110100'

TEST_G = b'11111'
TEST_H = b'00000'

SEED = None

class TestOne(unittest.TestCase):
    """
    Test that mutation related methods work as expected.
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize the constructor and read the test genome
        """
        cls._decoder = DecoderLinkedList()
        cls._decoder.set_genome(TEST_GENOME)
        cls._organism = cls._decoder.read_genome()
        cls._emitter_gene = cls._organism.get_organs()[0].get_genes()[0]
        cls._receptor_gene = cls._organism.get_organs()[0].get_genes()[1]
        cls._reaction_gene = cls._organism.get_organs()[0].get_genes()[2]
        
    def setUp(self):
        print(f"\n==================== {self._testMethodName} ====================\n")
        
    def test01(self):
        """
        Test that flip_at is valid in middle
        """
        self.assertEqual(flip_at(2, TEST_A), TEST_B)

    def test02(self):
        self.assertEqual(flip_at(0, TEST_A), TEST_C)

    def test03(self):
        self.assertEqual(flip_at(5, TEST_A), TEST_D)

    def test04(self):
        """
        Test that mutation occurs roughly half the time with flip segment and mutation of .5
        """
        same = 0
        not_same = 0
        for _ in range(10000):
            new = flip_segment(TEST_A, .5)
            if new == TEST_A:
                same += 1
            else:
                not_same += 1
        self.assertAlmostEqual(.5, same/not_same, delta=.1)

    def test05(self):
        """
        Test that increment frame works in normal situations
        """
        self.assertEqual(TEST_A, increment_frame(TEST_F)) 

    def test06(self):
        """
        Test that increment frame works in normal situations
        """
        self.assertEqual(TEST_A, increment_frame(TEST_E,-1))

    def test07(self):
        """
        Test that increment frame works in normal situations
        """
        self.assertEqual(TEST_H, increment_frame(TEST_G)) 
                         
    def test08(self):
        """
        Test that increment frame works in normal situations
        """
        self.assertEqual(TEST_G, increment_frame(TEST_H,-1))

    def test09(self):
        """
        Test difference between genomes with full random
        """
        scores = []
        for _ in range(100):
            count = 0
            new = random_bit_flip_string(self._organism, .01)
            for i in range(1,len(new)):
                if new[i] == self._organism.get_genome()[i]:
                    count += 1
            score = count/len(new)
            scores.append(score)
        sb.countplot(scores)
        plt.show()

    def test10(self):
        """
        Same as above, but now we test phenotype similarity
        Maybe add a print out for organsisms with differing quantities?
        How to test parameter similiarity? If a gene is added, how can you tell what the parent is supposed to be? Maybe the ID is inherited?
        """
        number_dif_organs = 0
        number_dif_genes = 0
        number_dif_params = 0
        num_organs = len(self._organism.get_organs())
        num_of_genes = sum([len(organ.get_genes() for organ in self._organism.get_organs()])
        for _ in range(100):
            new = random_bit_flip_string(self._organism, .01)
            self._decoder.set_genome(new)
            creature = self._decoder.read_genome()
            if creature.get_organs() != num_organs:
                number_dif_organs += 1
            if sum([len(organ.get_genes() for organ in self._organism.get_organs()] != num__of_genes:
                number_dif_genes += 1
        print(f"\nOut of 100 random bitflips, there were {number_dif_organs} creatures with a different amount of organs, and {number_dif_genes} creatures with a different number of genes.")
        
class TestTwo(unittest.TestCase):
    """
    Now we'll do some examinations on mutation over time, mainly parthenogenic
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize the constructor and read the test genome
        """
        cls._decoder = DecoderLinkedList()
        cls._decoder.set_genome(TEST_GENOME)
        cls._organism = cls._decoder.read_genome()
        cls._emitter_gene = cls._organism.get_organs()[0].get_genes()[0]
        cls._receptor_gene = cls._organism.get_organs()[0].get_genes()[1]
        cls._reaction_gene = cls._organism.get_organs()[0].get_genes()[2]
        
    def setUp(self):
        print(f"\n==================== {self._testMethodName} ====================\n")

    def test01(self):
        """
        Produce 100 generations descended from test genome, printing description every 10 gens
        """
        self._organism.describe()
        for i in range(1,101):
            self._decoder.set_genome(random_bit_flip_string(self._organism))
            org = self._decoder.read_genome()
            if i % 10 == 0:
                print(f"=========== Gen {i} ============")
                org.describe()
                print()
        
