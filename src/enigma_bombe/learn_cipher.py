#import torch
#torch.utils.data.datapipes.utils.common.DILL_AVAILABLE = torch.utils._import_utils.dill_available()

import spacy
import pandas as pd 
from pathlib import Path
from enigma_bombe.cipher import cipher_text 

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
                    temp = {'class':self.labels_text[i], 'text':cipher}
                    dataset.append(temp)

                buffer = sent.text[0:self.message_length]
        
        if buffer != "":
            for i in range(len(self.labels_text)):
                cipher = cipher_text(buffer, self.rotors[i], self.offsets[i])
                temp = {'class':self.labels_text[i], 'text':cipher}
                dataset.append(temp)

        df = pd.DataFrame(dataset)

        return df 

    def engTokenize(self, text:str) ->list[str]:
        """
        Tokenize an English text and return a list of tokens
        """
        return [token.text for token in self.eng.tokenizer(text)]

