import enigma_bombe.cipher_attack as cipher_attack 
from enigma_bombe import cipher 
from enigma_bombe.cipher_attack import CipherAttack
import random 

def test_index_of_coincidence():
    h = {"Matthew":0.04762, "Matthew Is Awesome":0.06667, "The secret of getting ahead is getting started.":0.09177, "Run your dbt Core projects as Apache Airflow DAGs and Task Groups with a few lines of code":0.05061, "It's like everyone tells a story about themselves inside their own head. Always. All the time. That story makes you what you are. We build ourselves out of that story.":0.06986}

    for s in h:
        #Given 
        # s
        attack_vector = CipherAttack()

        #When
        ioc_score = attack_vector.ioc_score(s)

        #Then
        assert round(ioc_score,5) == h[s], "{} != {}".format(s, h[s])

        #GIVEN
        s = "innthisspaperriidescribeeaaciphertexttonlyyattackkeffectiveeforrshortttabouttttttletterrrmessagesswithhkeyssincludinggupptoosixxplugsssanddforrlongerrmessagessusinggupptootennplugssstheeunderlyinggtechniquesswereeknownnatttheetimeeebutttheenecessaryyhardwareemayynotthaveebeennavailableeesinceeittrequiressaccumulatinggginneffectttsquaressofffrequenciessforreachhoffseverallthousanddtriallplaintextssshoweverrrittwoulddnotthaveebeennsurprisinggforrtheeboffinssoffbletchleyytoocobbleetogetherraadeviceetoodoosomethinggsimilarrrtheeactuallprocessinggforrthissattackkrequiressfewerroperationssanddlessssophisticationnthanntheebombeeattackkksinceeittdoessnottneeddtootryymultipleecribss"

        #When
        ioc_score = attack_vector.ioc_score(s)

        #THEN 
        assert round(ioc_score,5) == 0.06812, "{} != 0.85345".format(s)

def test_percent_words_score():
   
    #Given 
    # s
    s = "mattwashere"
    attack_vector = CipherAttack()

    #When
    score = attack_vector.percent_words_score(s)

    #Then
    assert attack_vector.english_dictionary.tokenize_message_into_words(s) == ["matt", "washer", "e"]
    assert round(score,5) == 0.66667, "{} != 2/3".format(s)

    #GIVEN
    s = "innthisspaperriidescribeeaaciphertexttonlyyattackkeffectiveeforrshortttabouttttttletterrrmessagesswithhkeyssincludinggupptoosixxplugsssanddforrlongerrmessagessusinggupptootennplugssstheeunderlyinggtechniquesswereeknownnatttheetimeeebutttheenecessaryyhardwareemayynotthaveebeennavailableeesinceeittrequiressaccumulatinggginneffectttsquaressofffrequenciessforreachhoffseverallthousanddtriallplaintextssshoweverrrittwoulddnotthaveebeennsurprisinggforrtheeboffinssoffbletchleyytoocobbleetogetherraadeviceetoodoosomethinggsimilarrrtheeactuallprocessinggforrthissattackkrequiressfewerroperationssanddlessssophisticationnthanntheebombeeattackkksinceeittdoessnottneeddtootryymultipleecribss"

    #When
    score = attack_vector.percent_words_score(s)

    #THEN 
    assert round(score,5) == 0.85345, "{} != 0.85345".format(s)

def test_insert_score():  
    
    #given 
    attack_vector = CipherAttack()
    x1 = attack_vector.SettingScore(1, [],[])
    x2 = attack_vector.SettingScore(2, [],[])
    x3 = attack_vector.SettingScore(3, [],[])
    x4 = attack_vector.SettingScore(2.5, [],[])
    x5 = attack_vector.SettingScore(2.75, [],[])

    #When 
    attack_vector.insert_score(x1, 3)

    #then
    assert len(attack_vector.top_k_settings)==1
    assert attack_vector.top_k_settings[0].score == 1

    #When 
    attack_vector.insert_score(x2, 3)

    #then
    assert len(attack_vector.top_k_settings)==2
    assert attack_vector.top_k_settings[0].score == 1

    #When 
    attack_vector.insert_score(x3, 3)

    #then
    assert len(attack_vector.top_k_settings)==3
    assert attack_vector.top_k_settings[1].score == 2
    assert attack_vector.top_k_settings[2].score == 3

    #When 
    attack_vector.insert_score(x4, 3)

    #thens
    assert len(attack_vector.top_k_settings)==3
    assert attack_vector.top_k_settings[0].score == 2
    assert attack_vector.top_k_settings[1].score == 2.5
    assert attack_vector.top_k_settings[2].score == 3

    #When 
    attack_vector.insert_score(x5, 3)

    #then
    assert len(attack_vector.top_k_settings)==3
    assert attack_vector.top_k_settings[0].score == 2.5
    assert attack_vector.top_k_settings[1].score == 2.75
    assert attack_vector.top_k_settings[2].score == 3


def test_bulk_insert(): 
    #given 
    attack_vector = CipherAttack()

    #when     
    for i in range(1000):
        x1 = attack_vector.SettingScore(i, [],[])
        attack_vector.insert_score(x1, 3)

    #then
    assert attack_vector.top_k_settings[0].score == 997
    assert attack_vector.top_k_settings[1].score == 998
    assert attack_vector.top_k_settings[2].score == 999

    #when 
    for i in range(10000):
        x1 = attack_vector.SettingScore(random.random(), [],[])
        attack_vector.insert_score(x1, 3)

    #then
    assert attack_vector.top_k_settings[0].score == 997
    assert attack_vector.top_k_settings[1].score == 998
    assert attack_vector.top_k_settings[2].score == 999
    
"""
def test_attack_ciphertext_only():  
    cipher_attack = CipherAttack()

    with open("data/messages.txt", "r", encoding="utf-8") as f: 
        text = f.readline().strip()
        while len(text) > 0:
            
            #GIVEN 
            
            #pick a random set of rotors
            rotors = random.choices(all_rotors, k=3)
            #pick some random offsets (also called the ring)
            offsets = [random.randint(0, 25) for i in range(1,4) ]

            #WHEN 
            c = cipher.cipher_text(text, rotors, offsets)
            a = cipher_attack.attack_ciphertext_only(c, 3)

            #THEN 
            assert 1 == 2  
"""