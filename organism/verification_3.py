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
TEST_GENOME = ORGAN_START + O_PARAM_ONE + O_PARAM_TWO + GENE_START + GENE_TYPE + GENE_RATE + GENE_FUNC +GENE_PARAMS + GENE_START + GENE_TWO + GENE_TWO_FUNC + GENE_TWO_PARAMS + GENE_START + GENE_THREE + GENE_THREE_PARAMS + GENE_THREE_CHEMS + ORGAN_START + b'1010101010101010101010101010'

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
        for _ in range(1000):
            new = flip_segment(TEST_A, .5)
            if new == TEST_A:
                same += 1
            else:
                not_same += 1
        self.assertAlmostEqual(.5, same/not_same, delta=.05)

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
                         
    def test05(self):
        """
        Test that increment frame works in normal situations
        """
        self.assertEqual(TEST_G, increment_frame(TEST_H,-1)) # This should fail 
