from enigma_bombe.cipher import cipher_text 
from enigma_bombe.cipher import identity, RotorA

import spacy
import pandas as pd 
from pathlib import Path

import torch 
torch.utils.data.datapipes.utils.common.DILL_AVAILABLE = torch.utils._import_utils.dill_available() #some error on macOS forces this
from torch import nn
from torch.utils.data import DataLoader

class CipherDataSet: 

    def __init__(self, message_length:int = 200, filename:str = "data/cipher_book_shortened.txt"):
        self.message_length = message_length
        self.filename = filename

        self.nlp = spacy.load("en_core_web_sm") # Load the English model to tokenize English text

        #classes
        self.labels_text = []
        self.rotors = []
        self.offsets = [] 

        self.df = pd.DataFrame()

    def add_class(self, label:str, rotors:list, offset:list): 
        """
        Add a class to be included in this dataset
        """
        self.labels_text.append(label)
        self.rotors.append(rotors)
        self.offsets.append(offset)

    def createDataset(self) -> pd.DataFrame:
        """
        Create the dataset using the specified text and classes
        """

        p = Path(self.filename)
        str = p.read_text()

        doc = self.nlp(str)
        buffer = ""
        dataset = [] 
        
        for sent in doc.sents:
            if buffer == "" and len(sent.text) > self.message_length:
                #buffer is empty but it is a very long sentence then make buffer = truncated sentence
                buffer = sent.text[0:self.message_length]
            elif (len(buffer) + len(sent.text)) < self.message_length:
                #buffer can contain this sentence and be under length limit
                buffer = buffer + sent.text
            else:
                #we have reached buffer size 

                #create all versions of this text 
                for i in range(len(self.labels_text)):
                    cipher = cipher_text(buffer, self.rotors[i], self.offsets[i])
                    temp = pd.Series([self.labels_text[i]] + list(cipher) + ([None]*(self.message_length-len(cipher))))
                    dataset.append(temp)

                buffer = sent.text[0:self.message_length]
        
        if buffer != "":
            for i in range(len(self.labels_text)):
                cipher = cipher_text(buffer, self.rotors[i], self.offsets[i])
                temp = pd.Series([self.labels_text[i]] + list(cipher) + ([None]*(self.message_length-len(cipher))))
                dataset.append(temp)

        #df = pd.DataFrame(dataset, columns = ['class'] + list(range(self.message_length)))
        
        df = pd.DataFrame(dataset)
        df.rename(columns={0: 'class'}, inplace=True)

        return df 

    def learnClasses(self, train_df:pd.DataFrame):
        tensor = torch.tensor(train_df.values)

if __name__ == "__main__":#

    cds = CipherDataSet(message_length=250, filename="data/cipher_book_tests.txt")
    cds.add_class("identity", rotors=[identity, identity, identity], offset=[0,0,0])
    cds.add_class("none", rotors=None, offset=None)    

    df = cds.createDataset() 
    print(f"The shape is {df.shape}")
    print(df.head())

    x = df.iloc[0]
    print("".join(str(a) if a else '' for a in x[1:].tolist()))
    df.to_csv("data/all.data")