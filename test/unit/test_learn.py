from enigma_bombe.learn_cipher import CipherDataSet 
from enigma_bombe.cipher import identity, RotorA

def test_pd_dataset():
    #Given 
    cds = CipherDataSet(message_length=250, filename="data/cipher_book_tests.txt")
    cds.add_class("identity", rotors=[identity, identity, identity], offset=[0,0,0])
    cds.add_class("none", rotors=None, offset=None)    

    #when 
    df = cds.createDataset() 

    #then 
    assert df.shape[0] == 10
    assert df.shape[1] == 2 
    
    x = df.iloc[0]
    assert x['class'] == "identity"
    assert x['text'] == "sgfgjtspqzpexbqsffntxjsgpddbtjpmtxgfqfsgfjmsfqdfosjpmpecjtobsdgftbmcpqcfqtxqjssfmjmokbjmkbmhvbhfgbtqftvksfcjmcfefbsbmccjtbtsfqepqsgfepqdfxgptfjmsfmsjpmtsgvtafdbnflmpxmbspmdfspsgffmfnz"

    x = df.iloc[1]
    assert x['class'] == "none"
    assert x['text'] == "thehistoryofwarteemswithoccasionswheretheinterceptionofdispatchesandorderswritteninplainlanguagehasresultedindefeatanddisasterfortheforcewhoseintentionsthusbecameknownatoncetotheenemy"

    x= df.iloc[3]
    assert x['class'] == "none"
    assert x['text'] == "forthisreasonprudentgeneralshaveusedcipherandcodemessagesfromtimeimmemorial"

    x = df.iloc[9]
    assert x['class'] == "none"
    assert x['text'] == "itmayaswellbestatedherethatnopracticablemilitarycipherismathematicallyindecipherableifinterceptedthemostthatcanbeexpectedistodelayforalongerorshortertimethedecipheringofthemessagebytheinterceptor"
    
