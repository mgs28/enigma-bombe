
import random
import string
from collections import namedtuple
from enigma_bombe import cipher
from enigma_bombe.cipher import cipher_text, ALL_ROTORS
from enigma_bombe.trienode import TrieNode

class CipherAttack: 

    SettingScore = namedtuple("SettingScore", "score rotors offset") 
    english_dictionary = None
    top_k_settings:list[SettingScore] = None 

    def __init__(self):
        self.english_dictionary = TrieNode()
        self.english_dictionary.load_from_dictionary_file("data/words_alpha.txt")
        self.top_k_settings = []
        self.ALL_ROTORS = ALL_ROTORS

    def ioc_score(self, s:string) -> float: 
        """
        Return the IC of a given piece of text, s, for english 
        """
        s_in = s.lower()

        # convert to only characters
        s = ""
        for c in s_in:
            if c in string.ascii_lowercase:
                s += c

        h = {}
        for c in s:
            if c in h:
                h[c] = h[c] + 1
            else:
                h[c] = 1

        index_of_coincidence_metric = 0
        for k in h:
            index_of_coincidence_metric += h[k] * (h[k] - 1)

        n = len(s)
        index_of_coincidence_metric = index_of_coincidence_metric / (n * (n - 1))

        return index_of_coincidence_metric

    def percent_words_score(self, s:string) -> float: 
        """
        Return the % of words found in the string
        """
        s_in = s.lower()
        tokens = self.english_dictionary.tokenize_message_into_words(s)
        n_tokens = len(tokens)
        n_words = sum(map(lambda x : len(x)>1, tokens))

        return n_words / n_tokens 

    
    def attack_ciphertext_only(self, s:string, top_k:int, rotors:list[int]=None, score_metric=ioc_score):
        """
        take a given string and return the k-best deciphered texts 
        """

        #if specified a set of rotors then
        if rotors is not None:
            print(f"attacking rotors {rotors}")
            rotors = [self.ALL_ROTORS[i] for i in rotors]
            for l in range(26):
                for m in range(26):
                    for n in range(26):
                        cipher = cipher_text(s,rotors,[l,m,n])
                        temp_score = self.SettingScore(score=score_metric(cipher), rotors=rotors, offset=[l,m,n])
                        self.insert_score(temp_score, top_k)    
        else:
            #find the best set of rotors
            for i in range(len(self.ALL_ROTORS)): 
                for j in range(len(self.ALL_ROTORS)):
                    for k in range(len(self.ALL_ROTORS)):

                        if i != j and j != k and k != i: 
                            print(f"attacking rotors {[i,j,k]}")
                            rotors = [self.ALL_ROTORS[i] for i in [i,j,k]]
                            for l in range(26):
                                for m in range(26):
                                    for n in range(26):
                                        cipher = cipher_text(s,rotors,[l,m,n])
                                        temp_score = self.SettingScore(score=score_metric(cipher), rotors=rotors, offset=[l,m,n])
                                        self.insert_score(temp_score, top_k)                                

    def insert_score(self, item: SettingScore, k=1):
        """
        insert item into the topk list and only keep k items 
        """
        if len(self.top_k_settings)==0:
            self.top_k_settings.append(item)
        else: 
            i = 0
            while i < len(self.top_k_settings):
                if self.top_k_settings[i].score >= item.score: 
                    break
                i+=1 

            self.top_k_settings.insert(i, item)

        while len(self.top_k_settings) > k:
            self.top_k_settings.pop(0)


# let's try an encoding
def main():
    
    text_items = []
    with open("data/messages.txt", "r", encoding="utf-8") as f: 
        text_items.append(f.readline().strip())


    text = random.choice(text_items)    

    print(f"for message: {text}")        
    
    #pick a random set of rotors
    rotor_indices = [] 
    rotors = []
    while len(rotor_indices)<3:

        temp = random.randrange(0, len(ALL_ROTORS))
        if temp not in rotor_indices:
            rotor_indices.append(temp)
            rotors.append(ALL_ROTORS[temp])
    
    #pick some random offsets (also called the ring)
    offsets = [random.randint(0, 25) for i in range(1,4) ]
    #Cipher the text 
    c = cipher.cipher_text(text, rotors, offsets)
    print(f"\t cipher = {c}")
    print(f"\t rotors={rotor_indices}")
    print(f"\t offsets={offsets}")

    #start deciphering
    attack_vector = CipherAttack()

    #simplified and show it the rotors used so we just need to find the offset
    #attack_vector.attack_ciphertext_only(c, 3, rotors=rotor_indices, score_metric=attack_vector.ioc_score)

    attack_vector.attack_ciphertext_only(c, 3, score_metric=attack_vector.ioc_score)  

    for item in attack_vector.top_k_settings:
        unciphered = cipher.cipher_text(c, item.rotors, item.offset)
        print(f"for {item}")
        print(f"\t{attack_vector.english_dictionary.tokenize_message_into_words(unciphered)}")


# Using the special variable
# __name__
if __name__=="__main__":
    main()