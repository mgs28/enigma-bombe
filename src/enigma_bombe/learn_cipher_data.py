from enigma_bombe.cipher import cipher_text 
from enigma_bombe.cipher import identity, RotorA

import glob
import os
import shutil
import spacy

from pathlib import Path
from io import open

import torch
from torch.utils.data import Dataset

class CipherDatasetGenerator: 

    def __init__(self, message_length:int = 200, message_length_min:int = 30):
        self.message_length = message_length
        self.message_length_min = message_length_min

        self.nlp = spacy.load("en_core_web_sm") # Load the English model to tokenize English text
        self.nlp.max_length = 1500000

        #classes
        self.labels_text = []
        self.rotors = []
        self.offsets = [] 

        self.dataset = {}

    def add_class(self, label:str, rotors:list, offset:list): 
        """
        Add a class to be included in this dataset
        """
        self.labels_text.append(label)
        self.rotors.append(rotors)
        self.offsets.append(offset)

        self.dataset[label] = list()
    
    def append_examples(self, filename:str): 
        """
        Create the dataset using the specified text and classes
        """
        print(f"...processing {filename}")
        p = Path(filename)
        str = p.read_text()

        doc = self.nlp(str)
        buffer = ""
        
        for sent in doc.sents:
            if buffer == "" and len(sent.text) > self.message_length:
                #buffer is empty but it is a very long sentence then make buffer = truncated sentence
                buffer = sent.text[0:self.message_length]
            elif (len(buffer) + len(sent.text)) < self.message_length:
                #buffer can contain this sentence and be under length limit
                buffer = buffer + sent.text
            else:
                #we have reached buffer size 
                
                if len(buffer) > self.message_length_min: 
                    #create all versions of this text 
                    for i in range(len(self.labels_text)):
                        cipher = cipher_text(buffer, self.rotors[i], self.offsets[i])
                        self.dataset[self.labels_text[i]].append(cipher) 

                buffer = sent.text[0:self.message_length]
        
        if buffer != "":
            if len(buffer) > self.message_length_min: 
                for i in range(len(self.labels_text)):
                    cipher = cipher_text(buffer, self.rotors[i], self.offsets[i])
                    self.dataset[self.labels_text[i]].append(cipher) 

    def write_dataset(self, data_directory:str): 
        datadir = Path(data_directory)

        #clean out the old directory
        shutil.rmtree(data_directory)
        datadir.mkdir(parents=True, exist_ok=True)

        for key in self.dataset:
            f = open(str(datadir.absolute()) + "/" + f"{key}.txt", "a")
            for line in self.dataset[key]:
                if len(line) >= self.message_length_min and len(line) < self.message_length:
                    f.write(line + "\n")
            f.close() 

if __name__ == "__main__":

    cds = CipherDatasetGenerator(message_length=250)
    cds.add_class("identity", rotors=[identity, identity, identity], offset=[0,0,0])
    cds.add_class("none", rotors=None, offset=None)    

    cds.append_examples("data/cipher_book_full.txt") 
    #cds.append_examples("data/moby.dick.txt")
    
    cds.write_dataset("data/learning")

