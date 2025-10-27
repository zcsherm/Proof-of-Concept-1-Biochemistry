import unittest
from Constructor import Decoder

ORGAN_START = b'11111'
O_PARAM_ONE = b'00001'
O_PARAM_TWO = b'00101'
GENE_START = b'11010'
GENE_TYPE = b'1'          # Emitter
GENE_FUNC = b'0110010'    # Exponential -> pow of 2
GENE_PARAMS = b'00010101' #Link to health and chem 5
GENE_TWO = b'0'
GENE_TWO_FUNC = b'11110101100001010' # Reverse sigmoid with coef = 1/86, mean= 10/128
GENE_TWO_PARAMS = b'00100011' # Link to reaction rate and chem 3
TEST_GENOME = ORGAN_START + O_PARAM_ONE + O_PARAM_TWO + GENE_START + GENE_TYPE + GENE_FUNC +GENE_PARAMS + GENE_TWO + GENE_TWO_FUNC + GENE_TWO_PARAMS



class FirstTest(unittest.TestCase):

    def test1(self):
        pass
