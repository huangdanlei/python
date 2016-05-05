# -*- coding: utf-8 -*-
import nltk
from nltk.tokenize import word_tokenize
train=[('I love this sandwich','pos'),('This is an amazing place','pos'),('I feel very good about these beers','pos'),('This is my best work','pos'),('What an awesome view','pos'),('I do not like this restaurant','neg'),('I am tired of this stuff','neg'),("I can't deal with this",'neg'),('He is my sworn enemy','neg'),('My boss is horrible','neg')]

all_words = set(word.lower() for passage in train for word in word_tokenize(passage[0]))
t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]

from nltk.classify import NaiveBayesClassifier
classifier= nltk.NaiveBayesClassifier.train(t)
test=[('The beer was good','pos'),('I do not enjoy my job','neg'),("I ain't feeling dandy today",'neg'),('I feel amazing','pos'),('Gary is a friend of mine','pos'),("I can't believe Im doing this",'neg')]
test_words = set(word.lower() for passage in test for word in word_tokenize(passage[0]))
testset = [({word: (word in word_tokenize(x[0])) for word in test_words}, x[1]) for x in test]
result= nltk.classify.accuracy(classifier,testset)
print {"classifier's accuracy": result}

testsentenceone='Their burgers are amazing'
test_features = {word.lower(): (word in word_tokenize(testsentenceone.lower())) for word in all_words}
print {'classification result 1':classifier.classify(test_features)}
testsentencetwo="I don't like their pizza"
test_features = {word.lower(): (word in word_tokenize(testsentencetwo.lower())) for word in all_words}
print {'classification result 2':classifier.classify(test_features)}