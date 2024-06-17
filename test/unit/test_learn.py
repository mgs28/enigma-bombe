from enigma_bombe.learn_cipher_data import CipherDataSet 
import enigma_bombe.learn_cipher_rnn
from enigma_bombe.cipher import identity, RotorA

import torch 

def test_pd_dataset():
    #Given 
    cds = CipherDataSet(message_length=250)
    cds.add_class("identity", rotors=[identity, identity, identity], offset=[0,0,0])
    cds.add_class("none", rotors=None, offset=None)    

    #when 
    cds.append_examples("data/cipher_book_tests.txt")

    #then 
    assert len(cds.dataset) == 2
    assert len(cds.dataset["none"]) == 5
    
    identity_list = cds.dataset["identity"]
    none_list = cds.dataset["none"]

    assert identity_list[0] == "sgfgjtspqzpexbqsffntxjsgpddbtjpmtxgfqfsgfjmsfqdfosjpmpecjtobsdgftbmcpqcfqtxqjssfmjmokbjmkbmhvbhfgbtqftvksfcjmcfefbsbmccjtbtsfqepqsgfepqdfxgptfjmsfmsjpmtsgvtafdbnflmpxmbspmdfspsgffmfnz"

    assert none_list[0] == "thehistoryofwarteemswithoccasionswheretheinterceptionofdispatchesandorderswritteninplainlanguagehasresultedindefeatanddisasterfortheforcewhoseintentionsthusbecameknownatoncetotheenemy"

    assert none_list[1] == "forthisreasonprudentgeneralshaveusedcipherandcodemessagesfromtimeimmemorial"

    assert none_list[4] == "itmayaswellbestatedherethatnopracticablemilitarycipherismathematicallyindecipherableifinterceptedthemostthatcanbeexpectedistodelayforalongerorshortertimethedecipheringofthemessagebytheinterceptor"
    
def test_string_to_tensor():
    #given
    s = "m"

    #when
    n = enigma_bombe.learn_cipher_rnn.lineToTensor(s).numpy() 
    print(n.shape)

    #then
    assert n.sum() == 1
    assert n[0,0,12] == 1

    #given
    s = "matt"

    #when
    t = enigma_bombe.learn_cipher_rnn.lineToTensor(s)
    n = t.numpy()

    #then
    assert n.sum() == 4
    assert n[0,0,12] == 1
    assert n[1,0,0] == 1
    assert n[2,0,19] == 1
    assert n[3,0,19] == 1