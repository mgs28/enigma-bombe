class TrieNode:
    """
    This is a TrieNode to help with finding words from a dictionary
    """

    # Trie node class
    def __init__(self):
        # empty hashtable of children
        self.children = {}

        # is_end is True if node represent the end of the word
        self.is_end = False

    def insert(self, word):
        """
        Insert a word into the trie
        """
        curr_node = self

        for c in word:
            if c not in curr_node.children:
                temp_node = TrieNode()
                curr_node.children[c] = temp_node

            curr_node = curr_node.children[c]

        curr_node.is_end = True

    def contains(self, word):
        """
        Check if the trie contains the given word
        """
        curr_node = self

        for c in word:
            if c not in curr_node.children:
                return False
            curr_node = curr_node.children[c]

        return curr_node.is_end

    def load_from_dictionary_file(self, path):
        """
        Load the trie from a dictionary file (one word per line with blank at end)
        """

        with open(path, "r", encoding="utf-8") as f:
            s = f.readline().strip()
            while len(s) > 0:
                self.insert(s)
                s = f.readline().strip()

    def find_longest_start_word(self, message):
        """
        find the longest word that starts the message and is in the trie as a word
        """
        curr_node = self
        longest_word_candidate = ""
        curr_word = ""
        last_was_end = False

        #print(f"looking at '{message}'")
        for c in message:
            #print(f"...character={c}, is_end={curr_node.is_end}, longest_word_candidate={longest_word_candidate}, c in children = {c in curr_node.children}")
            if curr_node.is_end:
                longest_word_candidate = curr_word
            
            if c not in curr_node.children:
                return longest_word_candidate            
            else:
                curr_word += c 
                curr_node = curr_node.children[c]

        if curr_node.is_end:
            longest_word_candidate = curr_word

        return longest_word_candidate

    def tokenize_message_into_words(self, message):
        """
        find the longest word that starts the message and is in the trie as a word.
        If a character doesn't lead to a word then it is returned as a singleton in the array.
        """
        message = message.strip()
        i = 0
        r = []
        while i < len(message):
            #print(f"looking at message = {message[i:]}")
            s = self.find_longest_start_word(message[i:])
            if len(s) > 1:
                #print(f"... found {s}")
                i = i + len(s)
                r.append(s)
            else:
                r.append(message[i])
                i = i + 1

        return r
