import string
import random
import math

"""
Constants for health decay function
"""
P_ONE = -.05
Q_ONE = .96
P_TWO = .22
Q_TWO = .79
COEF_ONE = 3
COEF_TWO = 1.1
R = 1.5
V = 0



def generate_id(length=10):
    """
    Generate a 'unique' id for an object
    :param length: the length of the id
    :return: the id as a string
    """
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choices(characters, k=length))
    
"""
Add more functions or trim? Maybe give each one 2 bytecodes, but some only have 1?
"""

func_names = ['linear', 'inverse linear', 'exponential', 'inverse exponential', 'radical', 'inverse radical', 'sigmoid', 'inverse sigmoid', 'negative square root']
bits_needed = [(0), (0), (4), (4), (4), (4), (7,7), (7,7), (6,6)]
functions  = [linear, inverse_linear, exponential, inverse_exponential, radical, inverse_radical, sigmoid, reverse_sigmoid, reverse_square]

def linear():
    def linear_func(x):
        return x
    return linear_func

def inverse_linear():
    def inv(x):
        return 1-x
    return inv
    
def exponential(exponent):
    """
    Exponent in range of 1-16?
    """
    def exp(x):
        return x ** exponent
    return exp

def inverse_exponential(exponent):
    def inv_exp(x):
        return 1 - x ** exponent
    return inv_exp
    
def radical(radicand):
    """
    Radicand in range of 1-16
    """
    def rad(x):
        return x**(1/radicand)
    return rad

def inverse_radical(radicand):
    def rad(x):
        return 1 - x**(1/radicand)
    return rad

def sigmoid(coefficient, mean):
    """
    Coefficient is 1 to 128
    Mean is 0-1 maybe 1/(1 to 128) to avoid IEEE754
    """
    mean = 1/(1+mean)
    def sig(x):
        return 1 / (1 + math.e ** ((coefficient * x * -1) + (1/mean * coefficient)))
    return sig

def reverse_sigmoid(coefficient, mean):
    mean = 1/(1+mean)
    func = sigmoid(coefficient, mean)
    def sig(x):
        return (-1*func(x) + 1)
    return sig

def reverse_square(base, coefficient):
    """
    sqrt(base ^ (-tx))
    base = 1-65 -> 1+ base/16
    coefficient = 1-65
    """
    base = 1 + base/16
    coefficient = coefficient + 1
    def rev(x):
        return (base ** (coefficient * x * -1)) ** .5
    return rev

def health_decay(health, param):
    """
    Essentially functions like a halflife for organ health
    Forms an equation with 3 plateaus, one at param=0, one at param=health, and one at param=1
    equation parameters primarily control steepness of slopes and they y value of the 0 and 1 slopes. V controls  the position of center slope Ideal is around .04, but causes issues where f(health=param) < health., stability causes decay
    """

    def smoothstep(x):
        if x <= 0.0: return 0.0
        if x >= 1.0: return 1.0
        return 3 * x * x - 2 * x * x * x

    def terrace(a, b, q=2.0):
        # plateau maps (fit to examples)
        param_p_one = COEF_ONE * b**.5 * P_ONE
        param_p_two = COEF_TWO * b**.5 * P_TWO
        L = max(0.0, param_p_one + Q_ONE * b)
        M = min(1.0, param_p_two + Q_TWO * b)
        a = a + V
        if a <= b:
            t = 0.0 if b <= 0.0 else smoothstep(a / b) ** R
            return L * (1 - t) + b * t
        elif b < a <= 1-V:
            t = 0.0 if b >= 1.0 else smoothstep((a - b) / (1 - b)) ** R
            return b * (1 - t) + M * t
        else:
            return terrace(1-V,b)

    return terrace(param, health)
