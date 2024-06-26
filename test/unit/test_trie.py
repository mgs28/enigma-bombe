import pytest
import os 

from enigma_bombe.trienode import TrieNode

def test_trie_inserts():
    words = ['absolute', 'matthew', 'matt', 'blash', 'asdfa']

    root = TrieNode()

    for w in words:
        #Given 
        # w

        #when 
        root.insert(w)

        #then
        assert root.contains(w)
        assert not root.contains("asdf")

def test_trie_inserts_from_file():

    root = TrieNode()

    #Given 
    path = "data/words_test.txt" 

    #when 
    root.load_from_dictionary_file(path)

    #then
    assert root.contains("matthew")
    assert root.contains("totally")
    assert not root.contains("totall")
    assert not root.contains("asdf")
    assert not root.contains(" ")
    assert not root.contains("")
    assert root.find_longest_start_word("totally") == "totally"
    assert root.find_longest_start_word("totallym") == "totally"
    assert root.find_longest_start_word("totallm") == ""
    assert root.find_longest_start_word("stotally") == ""
    assert root.find_longest_start_word("matthewwashere") == "matthew"
    assert root.find_longest_start_word("mattheewashere") == "matt"
    
    assert root.find_longest_start_word("") == ""
    assert root.tokenize_message_into_words("matthewwas") == ["matthew","w","a","s"]
    assert root.tokenize_message_into_words("matthewwastotally") == ["matthew","w","a","s","totally"]

def test_full_dictionary():

    root = TrieNode()

    #Given 
    path = "data/words_alpha.txt" 
    
    #when 
    root.load_from_dictionary_file(path)

    #then
    assert root.contains("was")
    assert not root.contains("Matthew")
    assert root.tokenize_message_into_words("mattwashere") == ["matt", "washer", "e"]