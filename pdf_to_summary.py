import numpy as np
import pandas as pd
import os
from transformers import pipeline
import re
import nltk
import textract
from summarizer import TransformerSummarizer
from difflib import SequenceMatcher
import spacy

text = textract.process("/content/5624475.pdf")
text = text.decode()
text = re.sub('[^a-zA-Z0-9.]', ' ', text)
text = re.sub('\s\s+', ' ', text)

summarizer = TransformerSummarizer(
    transformer_type="GPT2",
    transformer_model_key="gpt2-medium",
)

properties = {
    'openie.affinity_probability_cap': 2/3,
}

nlp = spacy.load('en_core_web_sm')

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_summary(text):
    summary = "".join(summarizer(text, min_length=20))
    return summary

def process(text):
  text = text.replace("\n", " ").replace("%20", " ")
  temp_text = text
  summary = get_summary(text)
  return summary

res = process(text)
while(len(res)>900):
    res = process(res)
print(res)

