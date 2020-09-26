import numpy as np
import pandas as pd
import nltk
import sys
from os import path

class TextAnalyzer:

    @staticmethod
    def prepare_data(df, text_column_id):
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        
        sentence_bag = []
        words_bag = []
        for col in text_column_id: # itero sulla lista di id di colonna in input
            for i in range(0, df[col].size):
                sentence = df[col][i]

                if type(sentence) == str: 
                    sentence = sentence.lower()
                    tokens = tokenizer.tokenize(sentence)
                    stopwords = open("./stopwords.txt", "r",
                                     encoding="utf-8").read().split()
                    tokens = [w for w in tokens if not w in stopwords]

                    sentence_bag.append(tokens)

                    for j in tokens:
                        words_bag.append(j)

        return words_bag, sentence_bag
