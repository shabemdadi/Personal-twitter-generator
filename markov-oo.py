import sys
import random
import string


class SimpleMarkovGenerator(object):
    """Basic version of Markov generator; by default, has no length limit."""

    def read_file(self, filename):
        corpus = open(filename)
        word_list = corpus.read().split()                           # read in text of file as a list
        return word_list

    def make_chains(self, ngram, word_list):
        """Takes input text as string; returns dictionary of markov chains."""

        dictionary = {}                                             # initialize empty dictionary

        n = int(ngram)                                              # set n (number of items in tuples)
        for i in range(len(word_list)-n):                           # loop over list items to fill dictionary
            key = tuple(word_list[i:(i+n)])                         # make keys in dictionary tuples of n items
            dictionary.setdefault(key, []).append(word_list[i+n])   # use setdefault to create values of dictionary
        
        return dictionary

    def make_text(self, dictionary, limit=None):
        """Takes dictionary of markov chains; returns random text."""

        capital_keys_list = [key for key in dictionary.keys() if key[0][0].isupper()]   # create list of only keys that start with an uppercase letter
        starting_key = random.choice(capital_keys_list)             # choose key (tuple) to start at
        new_text_string = " ".join(starting_key)           # add items in that tuple to string of created text
       
        punctuation = "?.!"                                         # create punctuation string    

        while dictionary.get(starting_key) != None:             # removed: and next_word[-1] not in punctuation: # Continue until the key is not found in the dictionary and until the last word ends in punctuation
            value_list = dictionary[starting_key]               # assign value of key (list)
            rand_index = random.randrange(0, len(value_list))   # choose random int w/in length of list
            next_word = value_list[rand_index]                  # find item at that random index

            new_text_string = new_text_string + " " + next_word     # add next_word to list of created text

            if limit:
                if len(new_text_string) > int(limit):
                    for i in range(len(new_text_string)-1,-1,-1):
                        if new_text_string[i] in punctuation:
                           new_text_string = new_text_string[0:(i+1)]
                    if len(new_text_string) > int(limit):
                        new_text_string = new_text_string[:limit]
                    break

            starting_key = tuple(list(starting_key[1:]) + [next_word])   # create new tuple from second word of previous tuple + item at that index

        return new_text_string                                  # return new text


class RemovePunctuationMixin(object):
    """Reads file and removes punctuation from list of words."""

    def remove_punct(self, filename):                       # reads file and removes punctuation
        corpus = open(filename)
        word_list = corpus.read().split()
        formatted_list = []
        for word in word_list:
            new_word = ""
            for char in word:
                if char not in string.punctuation:
                    new_word = new_word + char
            formatted_list.append(new_word)
        return formatted_list

class LowercaseWordsMixin(object):
    """Reads file and makes all words in list lowercase."""

    def make_lower(self, filename):
        corpus = open(filename)
        word_list = corpus.read().lower().split()
        return word_list


class TweetableMarkovGenerator(LowercaseWordsMixin, RemovePunctuationMixin, SimpleMarkovGenerator):
    """Imposes 140 character limit on text created by SimpleMarkovGenerator."""

    limit = 140

    def make_text(self):                           
        dictionary = super(TweetableMarkovGenerator,self).make_chains(ngram, self.read_file(filename)) # to not remove punctuation, use read_file(filename). To remove punctuation, use remove_punct(filename)
        return super(TweetableMarkovGenerator, self).make_text(dictionary, self.limit)


class LowercaseMarkovGenerator(SimpleMarkovGenerator, LowercaseWordsMixin):
    """Markov generator that uses LowercaseWordsMixin."""

    def make_text(self):                           
        dictionary = super(LowercaseMarkovGenerator,self).make_chains(ngram, self.make_lower(filename)) # to not remove punctuation, use read_file(filename). To remove punctuation, use remove_punct(filename)
        return super(LowercaseMarkovGenerator, self).make_text(dictionary)

class PunctuationlessMarkovGenerator(SimpleMarkovGenerator, RemovePunctuationMixin):
    """Markov generator that uses RemovePunctuationMixin."""

    def make_text(self):                           
        dictionary = super(PunctuationlessMarkovGenerator,self).make_chains(ngram, self.remove_punct(filename)) # to not remove punctuation, use read_file(filename). To remove punctuation, use remove_punct(filename)
        return super(PunctuationlessMarkovGenerator, self).make_text(dictionary)

if __name__ == "__main__":
    script, filename, ngram = sys.argv                          # unpack sys.argv arguments
    generator = PunctuationlessMarkovGenerator()
    random_text = generator.make_text()                   # Produce random text

    print random_text
