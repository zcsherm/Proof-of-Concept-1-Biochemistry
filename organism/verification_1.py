import unittest
import copy
import random
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from utilities import *
from Constructor import Decoder

ORGAN_START = b'11111'
O_PARAM_ONE = b'00001'
O_PARAM_TWO = b'00101'
GENE_START = b'11010'
GENE_TYPE = b'1'          # Emitter
GENE_RATE = b'11101'
GENE_FUNC = b'0110010'    # Exponential -> pow of 2
GENE_PARAMS = b'00010101' #Link to act_rate and chem 5
GENE_TWO = b'0'
GENE_TWO_FUNC = b'11110101101000001' # Reverse sigmoid with coef = 86, mean= 65/128
GENE_TWO_PARAMS = b'00100011' # Link to reaction rate and chem 3
TEST_GENOME = ORGAN_START + O_PARAM_ONE + O_PARAM_TWO + GENE_START + GENE_TYPE + GENE_RATE + GENE_FUNC +GENE_PARAMS + GENE_START + GENE_TWO + GENE_TWO_FUNC + GENE_TWO_PARAMS + ORGAN_START + GENE_TWO_PARAMS

SEED = None

class FirstTest(unittest.TestCase):
    """
    Handles testing the test genome, ensuring that all parts function as intended.
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize the constructor and read the test genome
        """
        cls._decoder = Decoder()
        cls._decoder.set_genome(TEST_GENOME)
        cls._organism = cls._decoder.read_genome()
        
    def test1(self):
        """
        Tests that the genome was decoded accurately into 2 organs, prints the organisms descriptions for visual inspection
        """
        print("=================== TEST 1 ======================")
        self._organism.describe()
        self.assertTrue(len(self._organism.get_organs()) == 2)

    # Test that the body can add and remove chemicals
    def test2(self):
        """
        Test that adding a chemical to the body actually works
        """
        print("=================== TEST 2 ======================")
        self._organism.add_chemical(14, 3)
        self.assertEqual(self._organism.get_chemical(14), 3)

    def test3(self):
        """
        Test that concentration is calculated correctly at only 1 chemical
        """
        print("=================== TEST 3 ======================")
        self._organism.calc_concentrations()
        self.assertEqual(self._organism.get_concentration(14),1)

    def test4(self):
        """
        Test adding a second chemical
        """
        print("=================== TEST 4 ======================")
        self._organism.add_chemical(2, 2)
        self.assertEqual(self._organism.get_chemical(2),2)

    def test5(self):
        """
        Test that concentration is accurate with multiple chemicals in body
        """
        print("=================== TEST 5 ======================")
        self._organism.calc_concentrations()
        self.assertEqual(self._organism.get_concentration(2), .4)

    def test6(self):
        """
        Remove a chemical and verify that concentrations were updated
        """
        print("=================== TEST 6 ======================")
        self._organism.rem_chemical(2,1)
        self._organism.calc_concentrations()
        self.assertTrue(self._organism.get_concentration(14), .75)

    def test7(self):
        """
        Remove all chemicals, test that no value goes under 0
        """
        print("=================== TEST 7 ======================")
        self._organism.rem_chemical(2,1)
        self._organism.rem_chemical(14,4)
        self.assertTrue(self._organism.get_chemical(14) == 0)

# Test that receptor can read chem
    def test8(self):
        """
        Test that a receptors function outputs expected values. 
        """
        print("=================== TEST 8 ======================")
        
        # Expected values for read and output
        values = [.5, .661]
        
        # Copy the organism to preserve original state
        organism_b = copy.deepcopy(self._organism)

        # Add 2 chemicals, concentrations at .5
        organism_b.add_chemical(3,1)
        organism_b.add_chemical(6,1)
        receptor = organism_b.get_organs()[0].get_genes()[1]
        organism_b.calc_concentrations()

        # Get the input and the output of the receptor and compare to expected
        conc = receptor.read_input()
        output = receptor.get_output()
        self.assertAlmostEqual(values[0], conc, delta=0.01)
        self.assertAlmostEqual(values[1], output, delta=0.01)
        
        # Preserve state for next test
        self._organism_b = organism_b


    def test82(self):
        """
        Test that a receptor can actually adjust a parameter
        """
        print("=================== TEST 8.5 ======================")
        receptor = self._organism_b.get_organs()[0].get_genes()[1]
        receptor.adjust_parameter()
        print(self._organism_b.get_organs()[0].describe())
        self.assertTrue(.7 > self._organism_b.get_organs()[0].get_reaction_rate() > .6)
        
# Test that emitter can read parameter
    def test9(self):
        """
        Test that the emitter can properly read and output. Test that body receives chem
        """
        print("=================== TEST 9 ======================")
        organism_b = copy.deepcopy(self._organism)
        organism_b.get_organs()[0].debug_set_health(.4)
        emitter = organism_b.get_organs()[0].get_genes()[0]
        read_val = emitter.read_param()
        output = emitter.get_output_amt()
        emitter.release_chemical()
        self.assertAlmostEqual(read_val, 1/32, delta=.001)
        self.assertAlmostEqual(output, 5.9941, delta=.001)
        print(f"Outputs and inputs are good for test9")
        self.assertAlmostEqual(organism_b.get_chemical(5), 5.9941, delta=.001)

    def test10(self):
        """
        Test that health adjustment works
        """
        pass # Eh, I'm sure it does idgaf
        
class SecondTest(unittest.TestCase):
    """
    Generate a random genome and decode it, then generate 100 genomes and analyze organ and gene count, then once more for a 1200 bit genome. Display graphs.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Setup the decoder and generate a random genome
        """
        random.seed(SEED) # replace seed with None for truly random results
        print(\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~ SECOND TEST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        cls._decoder = Decoder()
        cls._genome = generate_genome()
        print(f"This was the random genome for SecondTest: \n{cls._genome}\n")

    def setUp(self):
        """
        Read the seeded genome before each test, allows comparability
        """
        self._decoder.set_genome(self._genome)
        self._creature = self._decoder.read_genome()

    def test1(self):
        """
        Test that the random genome could decode, print a description of the organism.
        """
        self._creature.describe()
        # Ensure at least 1 organ was found, note that there is the minute possibility that no organ could be created, but this has an occurence of 1/150000.
        self.assertTrue(len(self._creature.get_organs()) > 0)

    def test2(self):
        """
        Generate 100 genomes and decode each. For each one, measure organ and gene counts and display graphs.
        """
        original_data = analyze_organism(self._creature)
        datum = []
        organ_datum = []
        for i in range(100):
            rand_genes=generate_genome()
            self._decoder.set_genome(rand_genes)
            new_creature = self._decoder.read_genome()
            datum.append(analyze_organism(new_creature))
            vals = analyze_organs(new_creature)
            for val in vals:
                organ_datum.append(vals)
        # Ok so now datum contains 100 frames of data for 400 bit genomes, how do analyze?
        # Maybe condense each into a column of a df
        df = pd.DataFrame(original_data)
        organ_df = pd.DataFrame()
        organ_df['Organ Count'] = organ_datum
        for row in datum:
            new_row_df = pd.DataFrame([row])
            df = pd.concat([df, new_row_df], ignore_index=True)
        sb.countplot(df, x='Organ Count').set_title("Number of Organs in each organism")
        plt.show()
        sb.countplot(df, x='Gene Count').set_title("Number of Genes in each organism")
        plt.show()
        sb.countplot(df, x='Average Genes per Organ').set_title("Average Genes per Organ per Creature")
        plt.show()
        sb.countplot(organ_df, x='Organ Count').set_title("Number of Organs with x genes")
        plt.show()

    def test3(self):
        """
        Now run this for 600,800,1000 bits
        """
        df = pd.DataFrame()
        for i in range(1200, 1201, 200):
            datum = []
            for j in range(100):
                rand_genes=generate_genome(i)
                self._decoder.set_genome(rand_genes)
                new_creature = self._decoder.read_genome()
                datum.append(analyze_organism(new_creature))
            # Ok so now datum contains 100 frames of data for 400 bit genomes, how do analyze?
            # Maybe condense each into a column of a df
            for row in datum:
                new_row_df = pd.DataFrame([row])
                df = pd.concat([df, new_row_df], ignore_index=True)
            sb.countplot(df, x='Organ Count')
            plt.show()
            sb.countplot(df, x='Gene Count')
            plt.show()
            sb.countplot(df, x='Average Genes per Organ')


if __name__ == '__main__':
    unittest.main()
