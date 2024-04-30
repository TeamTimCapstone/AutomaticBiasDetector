# Imports

import sys

from Dbias.bias_classification import *
from Dbias.bias_recognition import *

import spacy
from transformers import pipeline

import json
from database_functions import DatabaseFunctions 
from web_scraper import scrape

import re
import pickle

# Load NLP and Zero-Shot Classification requirements
#nlp = spacy.load("en_core_web_lg")
#pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Thresholds for whether or not bias should be considered for articles and sentences
# and other information needed for bias detection
article_bias_threshold = 0.65
sentence_bias_threshold = 0.8
group_bias_threshold = 0.6

def get_bias_info(article_url="", article_text="", website_url="", groups=["woman", "african", "asian", "lgbt", "hispanic"]):

  nlp = None
  pipe = None

  try:
    with open("nlp.pkl", 'rb') as picklefile:
      nlp = pickle.load(picklefile)

  except:
    nlp = spacy.load("en_core_web_lg")
    
    try:
      with open("nlp.pkl", 'wb') as picklefile:
        pickle.dump(nlp, picklefile)

    except:
      print("Could not pickle nlp")

  try:
    with open("pipe.pkl", 'rb') as picklefile:
      pipe = pickle.load(picklefile)

  except:
    pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli") 
    
    try:
      with open("pipe.pkl", 'wb') as picklefile:
        pickle.dump(pipe, picklefile)

    except:
      print("Could not pickle pipe")

    

  # groups = ["woman", "african", "asian", "lgbt", "hispanic"]
  # Variables to hold info on bias of sentences
  article_bias_info = {}
  biased_sentence_info = []
  biased_sentence_count = 0

  if article_text == "":
    try:
      if article_url == "":
        article_url = str(sys.argv[1])
      article_text = scrape(article_url)
    except:
      article_bias_info["ERROR"] = "Invalid URL"
      return json.dumps(article_bias_info)

  dbf = DatabaseFunctions()
  previous_analysis = dbf.json_string_retrieve(article_url)  
  if previous_analysis != "":
    return previous_analysis

  article_text = article_text.replace("\n", "")
  # print(article_text)
  # Classify article bias, find label confidence and if is is classified as biased
  # Characters 0 - 2435 appears to be the sweet spot
  try:
    article_bias_info = classifier(article_text[0:511])[0]
  except:
    article_bias_info = classifier(article_text)[0]
  article_bias_confidence = article_bias_info["score"]
  article_is_biased = True if article_bias_info["label"] == "Biased" else False

  article_bias_info["article_url"] = article_url
  if website_url != "":
    article_bias_info["website_url"] = website_url

  # If article not biased, stop
  if article_bias_confidence < article_bias_threshold or not article_is_biased:
    # print("Insufficient bias detected.")
    article_bias_info["label"] = "Not Biased"
    return json.dumps(article_bias_info)

  website_bias = dbf.get_website_bias_rating(article_url=article_url)
  if website_bias != 0:
    article_bias_info["website_bias_rating"] = website_bias
    

  article_bias_info.pop("score")
  article_bias_info.update({"article_bias_confidence": article_bias_confidence})
  sentences = article_text.split(".")

  for sentence in sentences:

    # Clean up sentences
    sentence = sentence.replace("\n", "")
    sentence = (sentence[:511]) if len(sentence) > 511 else sentence
    sentence = sentence.strip()

    # Classify sentence bias, find label confidence and if is is classified as biased
    sentence_bias_info = classifier(sentence)[0]
    sentence_bias_confidence = sentence_bias_info["score"]
    sentence_is_biased = True if sentence_bias_info["label"] == "Biased" else False

    # If sentence not biased, skip that sentence
    if sentence_bias_confidence < sentence_bias_threshold or not sentence_is_biased:
      continue

    # Collect sentence data in dictionary form
    current_sentence_info = {}
    current_sentence_info.update({"text": sentence, "sentence_bias_confidence": sentence_bias_confidence})
    nouns = []
    sentence_parts = nlp(sentence)

    # Get nouns and pronouns out of the sentence, combine to one string
    for part in sentence_parts:
      if part.pos_ == "NOUN" or part.pos_ == "PROPN" or part.pos_=="PRON":
        nouns.append(part.text)
    nouns = " ".join(nouns)

    # If the sentence has nouns in it, classify what those nouns relate to
    try:
      if len(nouns) > 0:
        sentence_group_bias_confidences = pipe(nouns, groups, multi_label=True)
        group_scores = sentence_group_bias_confidences.get("scores")
        group_labels = sentence_group_bias_confidences.get("labels")
        groups = []

        # Decide which groups are implicated in the sentence
        for i in range(len(group_scores)):
          if group_scores[i] > group_bias_threshold:
            groups.append(group_labels[i])
          else:
            break

        # If no groups, skip this sentence
        if groups == []:
          continue

        current_sentence_info.update({"biased_groups": groups})
    except:
      pass

    # Get which words contribute to sentence bias
    biased_words = recognizer(sentence)
    biased_word_list = []

    for word in biased_words:
      if word.get("label") == "bias":
        biased_word_list.append(word.get("entity"))

    if biased_word_list != []:
      current_sentence_info.update({"biased_words": biased_word_list})

    # Add all of this sentence's info to the overall list and increase biased sentence count
    biased_sentence_info.append(current_sentence_info)
    biased_sentence_count += 1

  # Add the sentence bias info to article bias info and convert to JSON to send to frontend
  article_bias_info.update({"biased_sentence_count": biased_sentence_count, "bias_info_by_sentence": biased_sentence_info})
  json_bias_data = json.dumps(article_bias_info, indent=4)
  with open("sample.json", "w") as outfile:
    outfile.write(json_bias_data)

  dbf.json_string_insert(json_bias_data)
  return json_bias_data

if __name__ == "__main__":
  print(get_bias_info())
