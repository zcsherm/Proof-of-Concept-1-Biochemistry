import unittest
from Constructor import Decoder

ORGAN_START = b'11111'
O_PARAM_1 = b'00001'
O_PARAM_2 = b'00101'
GENE_START = b'11010'
GENE_TYPE = b'1'          # Emitter
GENE_FUNC = b'0110010'    # Exponential -> pow of 2
GENE_PARAMS = b'00010101' #Link to health and chem 5
GENE_TWO = b'0'
GENE_TWO_FUNC = b'11110101100001010' # Reverse sigmoid with coef = 1/86, mean= 10/128
GENE_TWO_PARAMS = b'00100011' # Link to reaction rate and chem 3
TEST_GENOME = ORGAN_START + O_PARAM_1 + O


class FirstTest(unittest.TestCase):

    def test1(self):
        pass
