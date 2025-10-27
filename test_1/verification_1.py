import unittest
import copy
import random
import numpy as np
import seaborn as sb
import matplotlib as plt
from utilities import generate_genome, analyze_organism
from Constructor import Decoder

ORGAN_START = b'11111'
O_PARAM_ONE = b'00001'
O_PARAM_TWO = b'00101'
GENE_START = b'11010'
GENE_TYPE = b'1'          # Emitter
GENE_RATE = b'11101'
GENE_FUNC = b'0110010'    # Exponential -> pow of 2
GENE_PARAMS = b'00010101' #Link to health and chem 5
GENE_TWO = b'0'
GENE_TWO_FUNC = b'11110101101000001' # Reverse sigmoid with coef = 86, mean= 65/128
GENE_TWO_PARAMS = b'00100011' # Link to reaction rate and chem 3
TEST_GENOME = ORGAN_START + O_PARAM_ONE + O_PARAM_TWO + GENE_START + GENE_TYPE + GENE_RATE + GENE_FUNC +GENE_PARAMS + GENE_TWO + GENE_TWO_FUNC + GENE_TWO_PARAMS + ORGAN_START

SEED = 69420

class FirstTest(unittest.TestCase):
    """
    Still to test:
    Read random genome
    Do all parts work?
    Add/Rem chemicals
    Change of parameters?
    Change of parameters from genes?
    Genes reading chems?
    Genes output chems
    """
    @classmethod
    def setUpClass(cls):
        cls._decoder = Decode()
        cls._decoder.set_genome(TEST_GENOME)
        cls._organism = cls._decoder.read_genome()
        
    def test1(self):
        # test that the decoder actually parses the sample Genome, visually inspect output
        self._organism.status()
        self.assertTrue(len(self._organism.get_organs()) == 1)

# Test that the body can add and remove chemicals
    def test2(self):
        # Test add chemical
        self._organism.add_chem(14, 3)
        self.assertEqual(self._organism.get_chemical(14), 3)

    def test3(self):
        self.assertEqual(self._organism.get_concentration(14),1)

    def test4(self):
        self._organism.add_chem(2, 2)
        self._organism.assertEqual(self._organism.get_chemical(2),2)

    def test5(self):
        self._organism.assertEqual(self._organism.get_concentration(2), .2)

    def test6(self):
        self._organism.rem_chemical(2,1)
        self._organism.assertTrue(self._organism.get_concentration(14), .75)

    def test7(self):
        self._organism.rem_chemical(2,1)
        self._organism.rem_chemical(14,4)
        self.assertTrue(self._organism.get_chemical(14) == 0)

# Test that receptor can read chem
    def test8(self):
        values = [.5, .661]
        organism_b = copy.deepcopy(self._organism)
        organism_b.add_chemical(3,1)
        organism_b.add_chemical(6,1)
        receptor = organism_.get_organs()[0].get_genes()[1]
        conc = receptor.read_input()
        output = receptor.get_output()
        self.assertAlmostEqual(values, values, delta=0.01)
        print("Outputs are good for Test8")
        receptor.adjust_parameter()
        self.assertTrue(.7 > organism_b.get_organs()[0].get_reaction_rate() > .6)

# Test that emitter can read parameter
    def test9(self):
        organism_b = copy.deepcopy(self._organism)
        organism_b.debug_set_health(.4)
        emitter = organism_b.get_organs[0].get_genes[0]
        read_val = emitter.read_param()
        output = emitter.get_output_amt()
        emitter.release_chemical()
        self.assertAlmostEqual(read_val, 1/32, delta=.001)
        self.assertAlmostEqual(output, .0048, delta=.001)
        print(f"Outputs and inputs are good for test9")
        self.assertAlmostEqual(organism_b.get_chemical(3), .0048, delta=.001)

class SecondTest(unittest.TestCase):

    def setUpClass(cls):
        random.seed(SEED) # Comment out for truly random testing.
        cls._decoder = Decode()
        cls._genome = generate_genome()

    def setUp(self):
        this._decoder.set_genome(this._genome)
        self._creature = this._decoder.read_genome()

    def test1(self):
        self._creature.describe()
        # Ensure at least 1 organ was found.
        self.assertTrue(len(self._creature.get_organs()) > 0)

    def test2(self):
        # Generate 100 genomes and construct a creature for each, then find out how many organs/genes there were and plot these
        original_data = analyze_organism(self._creature)
        datum = []
        for i in range(100):
            rand_genes=generate_genome()
            self._decoder.set_genome(rand_genes)
            new_creature = self._decoder.read_genome()
            datum.append(analyze_organism(new_creature))
        # Ok so now datum contains 100 frames of data for 400 bit genomes, how do analyze?
        # Maybe condense each into a column of a df
        df = pd.DataFrame(original_data)
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
