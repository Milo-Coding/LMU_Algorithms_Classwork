import copy
from queue import *
from dataclasses import *
from typing import *
from byte_utils import *

# [!] Important: This is the character code of the End Transmission Block (ETB)
# Character -- use this constant to signal the end of a message
ETB_CHAR = "\x17"

class HuffmanNode:
    '''
    HuffmanNode class to be used in construction of the Huffman Trie
    employed by the ReusableHuffman encoder/decoder below.
    '''
    
    # Educational Note: traditional constructor rather than dataclass because of need
    # to set default values for children parameters
    def __init__(self, char: str, freq: int, 
                 zero_child: Optional["HuffmanNode"] = None, 
                 one_child: Optional["HuffmanNode"] = None):
        '''
        HuffNodes represent nodes in the HuffmanTrie used to create a lossless
        encoding map used for compression. Their properties are given in this
        constructor's arguments:
        
        Parameters:
            char (str):
                Really, a single character, storing the character represented
                by a leaf node in the trie
            freq (int):
                The frequency with which the character / characters in a subtree
                appear in the corpus
            zero_child, one_child (Optional[HuffmanNode]):
                The children of any non-leaf, or None if a leaf; the zero_child
                will always pertain to the 0 bit part of the prefix, and vice
                versa for the one_child (which will add a 1 bit to the prefix)
        '''
        self.char = char
        self.freq = freq
        self.zero_child = zero_child
        self.one_child = one_child

    def is_leaf(self) -> bool:
        '''
        Returns:
            bool:
                Whether or not the current node is a leaf
        '''
        return self.zero_child is None and self.one_child is None
    
    def tiebreakAlpha(self, other: "HuffmanNode") -> str:
        # ETB_CHAR has lowest tiebreaking order
        if self.char == ETB_CHAR:
            return ETB_CHAR
        elif other.char == ETB_CHAR:
            return ETB_CHAR
        elif self.char < other.char:
            return self.char
        return other.char
    
    def __lt__(self, other: "HuffmanNode") -> bool:
        # Tiebreaking for priority queue
        if self.freq != other.freq:
            # lowest frequecncy first
            return self.freq < other.freq
        elif self.char == ETB_CHAR:
            # ETB_CHAR has lowest tiebreaking order
            return True
        elif other.char == ETB_CHAR:
            return False
        else:
            # finally go in alphabetale order
            return self.char < other.char

class ReusableHuffman:
    '''
    ReusableHuffman encoder / decoder that is trained on some original
    corpus of text and can then be used to compress / decompress other
    text messages that have similar distributions of characters.
    '''
    
    def __init__(self, corpus: str):
        '''
        Constructor for a new ReusableHuffman encoder / decoder that is fit to
        the given text corpus and can then be used to compress and decompress
        messages with a similar distribution of characters.
        
        Parameters:
            corpus (str):
                The text corpus on which to fit the ReusableHuffman instance,
                which will be used to construct the encoding map
        '''
        freq_queue: PriorityQueue = self.get_letter_frequency(corpus)
        self._encoding_map: dict[str, str] = self.build_encoding_map(freq_queue)

    def get_letter_frequency(self, corpus: str) -> PriorityQueue:
        freq_dict: dict[str, int] = dict()
        # create a dict with all letters and thier frequencies
        for char in corpus:
            if char in freq_dict:
                freq_dict[char] += 1
            else:
                freq_dict[char] = 1
        # add ebt char with highest tiebreaking order
        freq_dict[ETB_CHAR] = 1
        
        # create a node for each item and add it to a priority queue to handle frequency order
        pqueue: PriorityQueue = PriorityQueue()
        for key in freq_dict:
            new_node: "HuffmanNode" = HuffmanNode(key, freq_dict[key])
            pqueue.put(new_node)
        return pqueue
    
    def build_encoding_map(self, freq_queue: PriorityQueue) -> dict[str, str]:
        # Build the Huffman Trie
        while freq_queue.qsize() > 1:
            child0 = freq_queue.get()
            child1 = freq_queue.get()
            merged_node = HuffmanNode(child0.tiebreakAlpha(child1), child0.freq + child1.freq, child0, child1)
            freq_queue.put(merged_node)
        
        # The root of the Huffman Trie is the last node in the priority queue
        root: "HuffmanNode" = freq_queue.get()

        en_map: dict[str, str] = dict()
        # start recursive function to turn the encoding trie into a dictionary
        self.build_recursive(root, "", en_map)
        return en_map
    
    def build_recursive(self, node: "HuffmanNode", current_path: str, en_map: dict) -> None:
        if node.is_leaf():
            # if we are at a leaf then we can add the char and path to the dict
            en_map[node.char] = current_path
        else:
            # otherwise check the children nodes
            if node.zero_child:
                self.build_recursive(node.zero_child, current_path + "0", en_map)
            if node.one_child:
                self.build_recursive(node.one_child, current_path + "1", en_map)
        # doesn't need to return anything because it just modifies the en_map dictionary
        return
    
    def get_encoding_map(self) -> dict[str, str]:
        '''
        Simple getter for the encoding map that, after the constructor is run,
        will be a dictionary of character keys mapping to their compressed
        bitstrings in this ReusableHuffman instance's encoding
        
        Example:
            {ETB_CHAR: 10, "A": 11, "B": 0}
            (see unit tests for more examples)
        
        Returns:
            dict[str, str]:
                A copy of this ReusableHuffman instance's encoding map
        '''
        return copy.deepcopy(self._encoding_map)
    
    # Compression
    # ---------------------------------------------------------------------------
    
    def compress_message(self, message: str) -> bytes:
        '''
        Compresses the given String message / text corpus into its Huffman-coded
        bitstring, and then converted into a Python bytes type.
        
        [!] Uses the _encoding_map attribute generated during construction.
        
        Parameters:
            message (str):
                String representing the corpus to compress
        
        Returns:
            bytes:
                Bytes storing the compressed corpus with the Huffman coded
                bytecode. Formatted as (1) the compressed message bytes themselves,
                (2) terminated by the ETB_CHAR, and (3) [Optional] padding of 0
                bits to ensure the final byte is 8 bits total.
        
        Example:
            huff_coder = ReusableHuffman("ABBBCC")
            compressed_message = huff_coder.compress_message("ABBBCC")
            # [!] Only first 5 bits of byte 1 are meaningful (rest are padding)
            # byte 0: 1010 0011 (100 = ETB, 101 = 'A', 0 = 'B', 11 = 'C')
            # byte 1: 1110 0000
            solution = bitstrings_to_bytes(['10100011', '11100000'])
            self.assertEqual(solution, compressed_message)
        '''
        # convert strings to a bitstring
        bitstring: str = ""
        for letter in message:
                bitstring += self._encoding_map[letter]
        # add ETB_CHAR to bitstring
        bitstring += self._encoding_map[ETB_CHAR]

        # split the bistring into byte sized chunks
        bitstrings: list[str] = []
        temp: str = ""
        for i in range(len(bitstring)):
            # track up to 8 bits then store it in the list and start again
            if i % 8 == 0 and i != 0:
                bitstrings.append(temp)
                temp = ""
            # add the new bit
            temp += bitstring[i]
        # after the loop store whatever is left in the list
        if temp != "":
            bitstrings.append(temp)

        # add padding if the last byte isn't 8 bits long
        if len(bitstrings[-1]) % 8 != 0:
            padding: str = "0" * (8 - (len(bitstrings[-1]) % 8))
            bitstrings[-1] += padding

        # convert bitstrings to byte and return it
        my_bytes: bytes = bitstrings_to_bytes(bitstrings)
        return my_bytes
    
    # Decompression
    # ---------------------------------------------------------------------------
    
    def decompress (self, compressed_msg: bytes) -> str:
        '''
        Decompresses the given bytes representing a compressed corpus into their
        original character format.
        
        [!] Should use the Huffman Trie generated during construction.
        
        Parameters:
            compressed_msg (bytes):
                Formatted as (1) the compressed message bytes themselves,
                (2) terminated by the ETB_CHAR, and (3) [Optional] padding of 0
                bits to ensure the final byte is 8 bits total.
        
        Returns:
            str:
                The decompressed message as a string.
        
        Example:
            huff_coder = ReusableHuffman("ABBBCC")
            # byte 0: 1010 0011 (100 = ETB, 101 = 'A', 0 = 'B', 11 = 'C')
            # byte 1: 1110 0000
            # [!] Only first 5 bits of byte 1 are meaningful (rest are padding)
            compressed_msg: bytes = bitstrings_to_bytes(['10100011', '11100000'])
            self.assertEqual("ABBBCC", huff_coder.decompress(compressed_msg))
        '''
        # convert bytes into one long bitstring
        bitstring: str = ""
        for b in compressed_msg:
            bitstring += byte_to_bitstring(b)
        
        # create two lists for the keys and values so we can access indexes
        key_list = list(self._encoding_map.keys())
        val_list = list(self._encoding_map.values())

        # loop through the bitstring collecting letters until we reach the ETB_CHAR
        restored_message: str = ""
        temp: str = ""
        for bit in bitstring:
            temp += bit
            # once we hit the ETB_CHAR we're done
            if temp == self._encoding_map[ETB_CHAR]:
                return restored_message
            
            # if we have decompressed a character add it to our message
            if temp in val_list:
                 restored_message += key_list[val_list.index(temp)]
                 temp = ""
        
        # the code should never reach here but just in case
        return restored_message
