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
        Test to confirm this works correctly and doesnt add or lose values.
        """
        return self.get_start() + self.get_params() + self.get_noncoding()

    def set_start(self, start):
        self._start = bin(b'1'+start)

    def set_params(self, params):
        self._params = bin(b'1'+params)

    def set_noncoding(self, noncoding):
        self._noncoding = bin(b'1'+noncoding)

    def get_start(self):
        return bytes(str(bin(int(self._start,2)))[3:],'utf-8')
        
    def get_params(self):
        return bytes(str(bin(int(self._start,2)))[3:],'utf-8')

    def get_noncoding(self):
        return bytes(str(bin(int(self._start,2)))[3:],'utf-8')

    def get_next(self):
        return self.next

    def get_entire_genome(self):
        val = self.get_structure_genome()
        if self.next is not None:
            val += next.get_structure_genome()
        return val
