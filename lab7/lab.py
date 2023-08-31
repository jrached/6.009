# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self, key_type):    
        self.value = None
        self.key_type = key_type
        self.children = {}

    def make_trie(self, key, set_ = False, counter = None):
        """ 
        Takes in a key to create a trie. Creates a trie instance 
        for each node and stores its children in the self.children dictionary.
        Returns the last node as an instance of an object so that the __setitem__ 
        and __getitem__functions can operate. Defaulting the set_ variable to False
        prevents a search through the trie for a particular key from generating a branch for 
        such key. This allows for __getitem__ to search through the trie without mutating it if 
        the key is not in the trie to begin with.
        """
        ###Verify the key is of the right type
        if isinstance(key, self.key_type) == False:
            raise TypeError(f'Keys in this trie are of {self.key_type} type')
        ###Start counter that iterates through key
        if counter == None:
            counter = 0
        ###Base case, exit once counter iterates through the key. Return node as instance of Trie class.
        if counter == len(key):
            if set_ == False and self.value == None:
                raise KeyError(f'{key} has no value')
            else:
                return self
          
        ###Decide whether it is setting, or getting an node. If getting, verify the key exists in the trie.
        if key[counter] not in self.children.keys() and set_ == True: 
            t = Trie(self.key_type) 
            self.children[key[counter]] = t 
        elif key[counter] in self.children.keys():
            t = self.children[key[counter]] 
        else:
            raise KeyError(f'{key} does not exist in trie')
        
        ###Recursive call: Increase counter by one, leave all other arguments the same.
        return t.make_trie(key, set_, counter + 1) 

    def __setitem__(self, key, value): 
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
        self_ = self.make_trie(key, True)
        self_.value = value

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError. 
        
        >>> t = Trie(str)
        >>> t['help'] = 10
        >>> result = t['help']
        >>> assert result == 10
        """
        
        return  self.make_trie(key).value

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists. If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        
        >>> t = Trie(str)
        >>> t['hello'] = 5
        >>> result = t['hello']
        >>> assert result == 5
        >>> del t['hello']
        >>> t['hello']
        Traceback (most recent call last):
        ...
        KeyError: 'hello has no value'
        """
        
        self_ = self.make_trie(key, True)
        if self_.value == None:
            raise KeyError(f'{key} is not a valid key')
        else:
            self_.value = None 

    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        
        >>> t = Trie(str)
        >>> t['help'] = 1
        >>> t['helicopter'] = 2
        >>> t['hello'] = 3
        >>> 'hello' in t
        True
        >>> 'helicopter' in t
        True
        >>> 'spongebob' in t
        False
        """
        try:
            try:
                self.make_trie(key).value
                return True 
            except TypeError:
                return False
        except KeyError:
            return False
            
    def __iter__(self, sofar = None):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        ###Base case: If node has no children stop generator.
        if sofar == None:
            sofar = self.key_type()
        ###For each child of a particular node, print the child and its value if it has one.
        for key, t in self.children.items():            
            if t.value is not None:  
                yield (sofar + key, t.value)   
            yield from t.__iter__(sofar + key) 
        
    def __repr__(self):
        return f'{self.children!r}'
    
    def __str__(self):
        return f'{self.children}'
                                    
def find_max(trie, max_num, ac = True):
    max_list = set()
    for iters in range(max_num): 
        maximum = 0
        max_sentence = None
        if ac:
            for i in trie:
                if i[1] >= maximum and i[0] not in max_list:
                    maximum = i[1]
                    max_sentence = i
            if max_sentence is not None:
                max_list.add(max_sentence[0])   
        else:
            max_sentence = None 
            for i in trie:
                if i[1] >= maximum and i not in max_list:
                    maximum = i[1]
                    max_sentence = i
            if max_sentence is not None:
                max_list.add(max_sentence)
        
    return list(max_list)

def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text

    >>> text = 'Hello my good friends.'
    >>> word_trie = make_word_trie(text)
    >>> word_trie 
    {'h': {'e': {'l': {'l': {'o': {}}}}}, 'm': {'y': {}}, 'g': {'o': {'o': {'d': {}}}}, 'f': {'r': {'i': {'e': {'n': {'d': {'s': {}}}}}}}}
    >>> 'hello' in word_trie
    True
    """
    t = Trie(str)
    sentences = tokenize_sentences(text)
    for sentence in sentences:
        words = sentence.split(' ')
        for word in words:
            if word in t: 
                t[word] += 1
            else:
                t[word] = 1
                
    return t


def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    
    >>> text = 'Hello friends. How are you?'
    >>> phrase_trie = make_phrase_trie(text)
    >>> phrase_trie 
    {'h': {'e': {'l': {'l': {'o': {' ': {'f': {'r': {'i': {'e': {'n': {'d': {'s': {}}}}}}}}}}}}, 'o': {'w': {' ': {'a': {'r': {'e': {' ': {'y': {'o': {'u': {}}}}}}}}}}}}
    >>> 'hello friends' in phrase_trie
    True
    >>> 'friends' in phrase_trie
    False
    """
    t = Trie(str)
    sentences = tokenize_sentences(text)
    for sentence in sentences:
        if sentence in t: 
            t[sentence] += 1
        else:
            t[sentence] = 1
                
    return t


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    
    >>> t = Trie(str)
    >>> t['help'] = 1
    >>> t['helicopter'] = 2
    >>> t['hello'] = 3
    >>> autocomplete(t, 'hel', 2)
    ['hello', 'helicopter']
    >>> autocomplete(t, 'hel', 1)
    ['hello']
    >>> autocomplete(t, 'hel')
    ['help', 'helicopter', 'hello']
    """
    
    self_ = trie.make_trie(prefix, True)
    if isinstance(prefix, self_.key_type) == False:
        raise TypeError(f'Keys in this trie are of {self_.key_type} type')
    empty = Trie(self_.key_type) 
    empty.children[prefix] = self_
        
    ###If max_count is None return all words that strt with the prefix.        
    ###Else, return the max_count most frequent words that start with the prefix.
    if max_count is not None: 
        if self_.children is not {}: 
            return find_max(empty, max_count)  
    else:
        max_list = []
        for i in empty:
            max_list.append(i[0]) 
        return max_list

def find_all_possible_replacements(word):
    if len(word) == 0:
        yield ''
        return
    
    first, rest = word[0], word[1:]
    for w in find_all_possible_replacements(rest):
        yield w 
        yield from (w[:ix] + first + w[ix:] for ix in range(len(w) +1))          


def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    result = autocomplete(trie, prefix, max_count)
    if max_count == None:
        return result
    
    replacements_gen = find_all_possible_replacements(prefix)
    replacements = {x for x in replacements_gen}
    maximum = 0
    max_sentence = None 
    for j in range(max_count - len(result)):
        for i in trie:
            if i[1] >= maximum and i[0] not in result and i[0] in replacements:    
                maximum = i[1]
                max_sentence = i
        if max_sentence is not None:
            result.add(max_sentence[0])
    
    return list(result) 


def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    raise NotImplementedError
            
    

# you can include test cases of your own in the block below.
if __name__ == '__main__':
    alice = "11-0.txt"
    metamorph = "pg5200.txt"
    dracula = 'pg345.txt'
    doctest.testmod()
    with open(metamorph, encoding="utf-8") as f:
        text = f.read()
        
    # trie = make_phrase_trie(text) 
    # count = 0
    # for i in trie: 
    #     count += 1
    # print(count)
    # max_num = 6
    # max_list = autocomplete(trie, 'he', max_num)
    
    # alphabet = a = "abcdefghijklmnopqrstuvwxyz"

    # word_list = ["aa" + l1 + l2 + l3 + l4 for l1 in a for l2 in a for l3 in a for l4 in a]
    # word_list.extend(["apple", "application", "apple", "apricot", "apricot", "apple"])
    # word_list.append("bruteforceisbad")
    # trie = make_word_trie(' '.join(word_list))
    
    
    # result1 = autocomplete(trie, 'ap', 1)
    # print(result1)
    
        