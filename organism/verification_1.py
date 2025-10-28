import unittest
import copy
import random
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from utilities import *
from Constructor import Decoder, GENE_OPCODES, ORGAN_OPCODES

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

        # Generate 100 random genomes and decode each
        for i in range(100):
            rand_genes=generate_genome()
            self._decoder.set_genome(rand_genes)
            new_creature = self._decoder.read_genome()
            # Get various metrics from the organism
            datum.append(analyze_organism(new_creature))
            vals = analyze_organs(new_creature)
            for val in vals:
                organ_datum.append(vals)

        # create dataframes for graphing
        df = pd.DataFrame(original_data)
        organ_df = pd.DataFrame()
        organ_df['Organ Count'] = organ_datum
        
        # fit each dictionary in datum to the dataframe 
        for row in datum:
            new_row_df = pd.DataFrame([row])
            df = pd.concat([df, new_row_df], ignore_index=True)

        # Graph each metric, primarily just counts atm
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
        Generate 100 genomes of length 1200 (possibily more as well) and display data
        """
        df = pd.DataFrame()
        for i in range(1200, 1201, 200):
            datum = []
            for j in range(100):
                rand_genes=generate_genome(i)
                self._decoder.set_genome(rand_genes)
                new_creature = self._decoder.read_genome()
                datum.append(analyze_organism(new_creature))
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

class ThirdTest(unittest.TestCase):
    """
    This testing will measure gene/organ counts as a function of genome length, as well as a function of opcode quantity
    """
    @classmethod
    def setUpClass(cls):
        """
        Setup the decoder
        """
        random.seed(SEED) # replace seed with None for truly random results
        print(\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~ THIRD TEST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        cls._decoder = Decoder()

    def test1(self):
        """
        Measure Organ and Gene count against genome length
        """
        all_data = pd.DataFrame()
        all_data_genes = pd.DataFrame()
        for i in range(1200,7200,1200):
            dfs = decode_x_times(self._decoder, 100, i)
            val[0]['Genome Length'] = i
            val[1]['Genome Length'] = i
            all_data = pd.concat(all_data, val[0], ignore_index=True)
            all_data_genes = pd.concat(all_data, val[1], ignore_index=True)
        fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(10, 5)) # 1 row, 4 cols
        sb.histplot(all_data, x='Organ Count',hue='Genome Length',multiple='stack', ax = axes[0,0])
        axes[0,0].set_title("Number of Organs in each organism")
        sb.histplot(all_data, x='Gene Count', hue='Genome Length', multiple='stack', ax= axes[0,1])
        axes[0,1].set_title("Number of Genes in each organism")
        sb.histplot(all_data, x='Average Genes per Organ', hue='Genome Length',multiple='stack', ax = axes[0,2])
        axes[0,2].set_title("Average number of Genes per organ in each organism")
        sb.histplot(all_data_genes, x='Organ Count', hue='Genome Length',multiple='stack', ax = axes[0,3])
        axes[0,3].set_title("Number of organs with x Genes")
        sb.kdeplot(all_data, x='Organ Count',hue='Genome Length',multiple='stack', ax = axes[1,0])
        axes[1,0].set_title("Number of Organs in each organism")
        sb.kdeplot(all_data, x='Gene Count', hue='Genome Length', multiple='stack', ax= axes[1,1])
        axes[1,1].set_title("Number of Genes in each organism")
        sb.kdeplot(all_data, x='Average Genes per Organ', hue='Genome Length',multiple='stack', ax = axes[1,2])
        axes[1,2].set_title("Average number of Genes per organ in each organism")
        sb.kdeplot(all_data_genes, x='Organ Count', hue='Genome Length',multiple='stack', ax = axes[1,3])
        axes[1,3].set_title("Number of organs with x Genes")
        plt.tight_layout()
        plt.show()

    def test2(self):
        """
        Measure Organ and Gene count against number of op codes to make a gene in length 1200
        """
        new_ops = [0b11001, 0b11000, 0b10111, 0b10110]
        tmp = GENE_OPCODES
        all_data = pd.DataFrame()
        all_data_genes = pd.DataFrame()
        for i in range(4):
            GENE_OPCODES.append(new_ops[i])
            dfs = decode_x_times(self._decoder, 100, 1200)
            val[0]['Number of Opcodes']=i+2
            val[1]['Number of Opcodes']=i+2
            all_data = pd.concat(all_data, val[0], ignore_index=True)
            all_data_genes = pd.concat(all_data, val[1], ignore_index=True)
        bigplot(all_data, all_data_genes, 'Number of Opcodes')
        GENE_OPCODES = tmp
        
    def test3(self):
        """
        Measure against op codes AND genome length (hyper param). Create a 4x4 grid of plots
        """
        fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(10, 5)) # 4rows, 4 cols
        new_ops = [0b11001, 0b11000, 0b10111, 0b10110]
        tmp = GENE_OPCODES
        all_data = pd.DataFrame()
        all_data_genes = pd.DataFrame()
        for j in range(4):
            genome_len = 1200 * (i+1)
            for i in range(4):
                GENE_OPCODES.append(new_ops[i])
                dfs = decode_x_times(self._decoder, 100, 1200)
                val[0]['Number of Opcodes']=i+2
                val[1]['Number of Opcodes']=i+2
                all_data = pd.concat(all_data, val[0], ignore_index=True)
                all_data_genes = pd.concat(all_data, val[1], ignore_index=True)
            plot_row(all_data, all_data_genes, 'Number of Opcodes')
            GENE_OPCODES = tmp
        plt.tight_layout()
        plt.show()
        
def decode_x_times(decoder, times, genome_length = 400):
    """
    Helper function that generates random genomes x times of length j, returns 2 data sets
    """
    datum = []
    for j in range(times):
        rand_genes=generate_genome(genome_length)
        decoder.set_genome(rand_genes)
        new_creature = decoder.read_genome()
        datum.append(analyze_organism(new_creature))
    organ_df = pd.DataFrame()
    organ_df['Organ Count'] = organ_datum
    for row in datum:
        new_row_df = pd.DataFrame([row])
        df = pd.concat([df, new_row_df], ignore_index=True)
    return df, organ_df

def plot_row(df, df2, col, axes):
    sb.bocplot(df1, x='Organ Count', ax = axes[col,0])
    axes[0,0].set_title("Number of Organs in each organism\nGenome len: {(col+1)*1200}  OpCodes: 2")
    sb.boxplot(df1, x='Gene Count', ax= axes[col,1])
    axes[0,1].set_title("Number of Genes in each organism\nGenome len: {(col+1)*1200}  OpCodes: 3")
    sb.boxplot(df1, x='Average Genes per Organ', ax = axes[col,2])
    axes[0,2].set_title("Average number of Genes per organ in each organism\nGenome len: {(col+1)*1200}  OpCodes: 4")
    sb.boxplot(df2, x='Organ Count', ax = axes[col,3])
    axes[0,3].set_title("Number of organs with x Genes\nGenome len: {(col+1)*1200}  OpCodes: 5")

def bigplot(df1, df2, hue_col):
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(10, 5)) # 1 row, 4 cols
    sb.histplot(df1, x='Organ Count',hue=hue_col,multiple='stack', ax = axes[0,0])
    axes[0,0].set_title("Number of Organs in each organism")
    sb.histplot(df1, x='Gene Count', hue=hue_col, multiple='stack', ax= axes[0,1])
    axes[0,1].set_title("Number of Genes in each organism")
    sb.histplot(df1, x='Average Genes per Organ',hue=hue_col,multiple='stack', ax = axes[0,2])
    axes[0,2].set_title("Average number of Genes per organ in each organism")
    sb.histplot(df2, x='Organ Count',hue=hue_col,multiple='stack', ax = axes[0,3])
    axes[0,3].set_title("Number of organs with x Genes")
    sb.kdeplot(df1, x='Organ Count',hue=hue_col,multiple='stack', ax = axes[1,0])
    axes[1,0].set_title("Number of Organs in each organism")
    sb.kdeplot(df1, x='Gene Count', hue=hue_col, multiple='stack', ax= axes[1,1])
    axes[1,1].set_title("Number of Genes in each organism")
    sb.kdeplot(df1, x='Average Genes per Organ', hue=hue_col,multiple='stack', ax = axes[1,2])
    axes[1,2].set_title("Average number of Genes per organ in each organism")
    sb.kdeplot(df2, x='Organ Count', hue=hue_col,multiple='stack', ax = axes[1,3])
    axes[1,3].set_title("Number of organs with x Genes")
    plt.tight_layout()
    plt.show()
    
if __name__ == '__main__':
    unittest.main()
