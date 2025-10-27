import unittest
import copy
from Constructor import Decoder

ORGAN_START = b'11111'
O_PARAM_ONE = b'00001'
O_PARAM_TWO = b'00101'
GENE_START = b'11010'
GENE_TYPE = b'1'          # Emitter
GENE_RATE = b''
GENE_FUNC = b'0110010'    # Exponential -> pow of 2
GENE_PARAMS = b'00010101' #Link to health and chem 5
GENE_TWO = b'0'
GENE_TWO_FUNC = b'11110101101000001' # Reverse sigmoid with coef = 86, mean= 65/128
GENE_TWO_PARAMS = b'00100011' # Link to reaction rate and chem 3
TEST_GENOME = ORGAN_START + O_PARAM_ONE + O_PARAM_TWO + GENE_START + GENE_TYPE + GENE_FUNC +GENE_PARAMS + GENE_TWO + GENE_TWO_FUNC + GENE_TWO_PARAMS + ORGAN_START



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
        receptor.release_chemical()
        self.assertAlmostEqual(read_val, 1/32, .001)
        
        self.assertTrue(organism_b.get_concentration(3) > .5)

class SecondTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
