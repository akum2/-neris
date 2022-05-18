import nltk
nltk.download()
# from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.collocations import *
# # from nltk.metrics import ()
# import logging
# import sys, os, time, io, re, traceback, warnings, weakref, collections.abc
# import linecache
# import tokenize
# from token import *
sentence_data = "The First sentence is about Python. The Second: about Django. You can learn Python,Django and Data Ananlysis here."
nltk_tokens = nltk.sent_tokenize(sentence_data)
print (nltk_tokens)