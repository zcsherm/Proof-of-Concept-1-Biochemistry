"""
Creates a simple organism for prototyping purposes
"""

from utilities import *
import Chemicals
import random

class Body:

    def __init__(self):
        self._id = generate_id()
        self._chems = {chem: 0 for chem in Chemicals.CHEMS}
        self._concentrations = {chem: 0 for chem in Chemicals.CHEMS}
        self._organs = []
        
    def add_organ(self, organ):
        self._organs.append(organ)

    def activate_organs(self):
        for organ in self._organs:
            roll = random.random()
            if roll <= organ.get_act_rate():
                organ.activate_organ()
        self.calc_concentrations()

    def calc_concentrations(self):
        total = 0
        for key, val in self._chems: 
            total += val
        if total == 0:
            total = 1
        self._concentrations = {chem: val/total for chem, val in self._chems}

    def get_concentration(self, chemical):
        try:
            return self._concentrations[chemical]
        except:
            print("\n!!!!!! An error occured !!!! An invalid chemical was requested!\n")
            return 0

    def add_chemical(self, chemical, amount):
        try:
            self._chems[chemical] += amount
        except:
            print("\n!!!!!! An error occured !!!! An invalid chemical was added to the body\n")
            return

    def rem_chemical(self, chemical, amount):
        try:
            self._chems[chemical] -= amount
            if self._chems[chemical] < 0:
                self._chems[chemical] = 0
        except:
            print("\n!!!!!! An error occured !!!! An invalid chemical was removed from the body the body\n")
            return

    def get_organs(self):
        return self._organs

    def descrie(self):
        print(f"Creature {self._id):")
        for organ in self._organs:
            organ.describe()

    def status(self):
        print(f"Creature {self._id):")
        for chemical in Chemical.CHEMS:
            print(f"Chemical {chemical} -- units: {self._chems{chemical}, concentrations: {self._concentrations{chemical}}"
        for organ in self._organs:
            organ.status()
