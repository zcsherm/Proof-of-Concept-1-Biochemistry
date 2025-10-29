"""
Creates a class for the genome in which the entire genome is saved into chunks and is a singly linked list
"""

class Node:
    """
    Each node points to the next node in the genome. Contains the bits as the start (opcode), the parameters of the structure, and then all non-coding sections following it. Genome segments must be passed as bytes, and then are prepended with 1 (to preserve leading 0s) and converted to binary(save space while stored in mem). Using the segments means needing to drop the leading 1
    """
    def __init__(self):
        self._start = None
        self._params = None 
        self._noncoding = None
        self.next = None

    def get_structure_genome(self):
        """
        Return the entire genome for this structure
        """
        return bytes(self._start[1:] + bytes(self._params[1:]) + bytes(self._noncoding[1:]))

    def set_start(self, start):
        self._start = bin(1+start)

    def set_params(self, params):
        self._params = bin(1+params)

    def set_noncoding(self, noncoding):
        self._noncoding = bin(1+noncoding)

    def get_start(self):
        return bytes(self._start)

    def get_params(self):
        return bytes(self._params)

    def get_noncoding(self):
        return bytes(self._noncoding)

    def get_next(self):
        return self.next

    def get_entire_genome(self):
        val = self.get_structure_genome()
        if self.next is not None:
            val += next.get_structure_genome()
        return val
