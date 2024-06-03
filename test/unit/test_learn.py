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
    assert df.shape[1] == 251 
    
    x = df.iloc[0]
    assert x['class'] == "identity"
    text = "".join(str(a) if a else '' for a in x[1:].tolist())
    assert text == "sgfgjtspqzpexbqsffntxjsgpddbtjpmtxgfqfsgfjmsfqdfosjpmpecjtobsdgftbmcpqcfqtxqjssfmjmokbjmkbmhvbhfgbtqftvksfcjmcfefbsbmccjtbtsfqepqsgfepqdfxgptfjmsfmsjpmtsgvtafdbnflmpxmbspmdfspsgffmfnz"

    x = df.iloc[1]
    assert x['class'] == "none"
    text = "".join(str(a) if a else '' for a in x[1:].tolist())
    assert text == "thehistoryofwarteemswithoccasionswheretheinterceptionofdispatchesandorderswritteninplainlanguagehasresultedindefeatanddisasterfortheforcewhoseintentionsthusbecameknownatoncetotheenemy"

    x= df.iloc[3]
    assert x['class'] == "none"
    text = "".join(str(a) if a else '' for a in x[1:].tolist())
    assert text == "forthisreasonprudentgeneralshaveusedcipherandcodemessagesfromtimeimmemorial"

    x = df.iloc[9]
    assert x['class'] == "none"
    text = "".join(str(a) if a else '' for a in x[1:].tolist())
    assert text == "itmayaswellbestatedherethatnopracticablemilitarycipherismathematicallyindecipherableifinterceptedthemostthatcanbeexpectedistodelayforalongerorshortertimethedecipheringofthemessagebytheinterceptor"
    
    