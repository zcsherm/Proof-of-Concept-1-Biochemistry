"""
Gives rules for genes that govern biochemistry properties. These produce constructs which are grouped together into an 'organ', each gene governs a potential reaction, monitors for a specific chemical, or affects the global attributes of the organ.
"""

"""
Notes:
Possible activation functions: x, x^2, sqrt(x^a) [0<a<1], 1/(1+e^(-ax+ba) [0<a<100] [0<b<1][sigmoid centered on .5 when b = .5], sqrt(A^(-Bx)) [1.2<A<5] [A<B<5B], -(1/(1+e^(-ax+.5a))+1 [inverse sigmoid], 1-x, 1-x^2

Possible types:
Receptors: Adjusts parameters of Organ based on concentration of chemical, each has an activation function that determines output
Emittors: Releases a given chemical based on a current parameter of the organ (rate, health, size)
Reactions: Converts chemicals into other chemicals, supports equations of multiple chemicals with varying coefficients
Processing: How quickly each chemical is broken down by or accumulated in the organ
Neuro-indicator: Possibly reads an attribute and links to a neuron in brain?
Absorption rates:
Initialcondition: HOw much of a chemical is present at birth, and the cost of reproduction
"""
class BioChemGene:
    def __init__(self, organ, type):
        self._organ = organ
        self._id = None  # Have a simple id creator in utilities
        self._type = type
    
    def set_activation(self, name, function):
        self._activation_function = function
        self._func_name = name

    def get_type(self):
        return self._type
        
class Receptor(BioChemGene):
    """
    I'm thinking that this gets passed in class methods for the organ, and adjusts the params by calling those functions
    """
    def set_positive(self, positive=True):
        """
        Can be toggled to have the signal be additive or negative
        """
        if positive:
            self._multiplier = 1
        else:
            self._multiplier = -1

    def set_negative(self, negative=True):
        if negative:
            self._multiplier = -1
        else:
            self._multiplier = 1
            
    def set_parameter(self, name, parameter):
        """
        Sets what this gene can adjust in the organ. Presently needs to be passed a function from the organ, such as organ.get_rate() or organ.get_health(), these are then averaged over all receptors in organ
        """
        self._param_name = name
        self._parameter = parameter

    def set_chemical(self, chemical):
        """
        Sets which chemical this gene detects
        """
        self._chemical = chemical

    def set_activation_function(self, name, function):
        """
        Sets the function that controls output, should already be parameterized if needed before assignment. Parameters are function specific and read from genome.
        """
        self._activation_function = function
        self._func_name = name

    def read_input(self):
        """
        Reads the current concentration of a chemical from the body
        """
        return self._organ.get_concentration(self._chemical)

    def get_output(self):
        return self._activation_function(self.read_input())
        
    def adjust_parameter(self):
        """
        outputs signal to the parameter it should effect
        """
        self._parameter(self.get_output())

    def describe(self):
        """
        Outputs all atttributes of the gene in an easy to read manner
        """
        s1 = f"\t\tGene {self._id}:"
        s2 = f"\t\t\t This gene monitors for chemical {self._chemical}. Based on the concentration it adjusts {self._param_name}."
        s3 = f"\t\t\t\t Organ parameter: {self._param_name}"
        s4 = f"\t\t\t\t Activation function: f{self._func_name}"
        s5 = f"\t\t\t\t Chemical read: {self._chemical}"
        s6 = f"\t\t\t\t Example: Chemical at .1 produces {self._activation_function(.1)}, Chemical at .5 produces {self._activation_function(.5)},  Chemical at .9 produces {self._activation_function(.9)}"
        print(s1,s2,s3,s4,s5,s6)

class Emitter(BioChemGene):
    """
    Reads a parameter from the host organ, and outputs a specific chemical with a strength modified by organ health
    """

    def set_parameter(self, name):
        """
        Sets the organs attribute to monitor
        """
        self._param_name = name

    def set_chemical(self, chemical):
        self._chemical = chemical

    def set_output_rate(self, rate):
        """
        Determines how much is released by default. I'm thinking a number between 0-10, mutations can increase? Outputs units, rather than concentrations
        """
        self._rate = rate/5

    def read_param(self):
        return self._organ.get_parameter(self.parameter_name)

    def get_output_amt(self):
        return self._activation_function(self.read_param()) * self._rate

    def release_chemical(self):
        self._organ.release_chemical(self._chemical, self.get_output_amt())

    def describe(self):
        """
        Outputs all atttributes of the gene in an easy to read manner
        """
        s1 = f"\t\tGene {self._id}:"
        s2 = f"\t\t\t This gene monitors the organ's {self._param_name}. Based on the rate it releases chemical {self._chemical}."
        s3 = f"\t\t\t\t Organ parameter: {self._param_name}"
        s4 = f"\t\t\t\t Activation function: f{self._func_name}"
        s5 = f"\t\t\t\t Chemical output: {self._chemical}"
        s7 = f"\t\t\t\t Output rate: {self._rate}"
        s6 = f"\t\t\t\t Example: {self._param_name} at .1 produces {self._activation_function(.1)*self._rate} units of {self._chemical}, {self._param_name} at .5 produces {self._activation_function(.5)*self._rate} units of {self._chemical},  {self._param_name} at .9 produces {self._activation_function(.9)*self._rate} units of {self._chemical}"
        print(s1,s2,s3,s4,s5,s7,s6)
