# Imports

from Dbias.bias_classification import *
from Dbias.bias_recognition import *

import spacy
from transformers import pipeline

import json

# Load NLP and Zero-Shot Classification requirements
nlp = spacy.load("en_core_web_lg")
pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Thresholds for whether or not bias should be considered for articles and sentences
# and other information needed for bias detection
article_bias_threshold = 0.65
sentence_bias_threshold = 0.6
group_bias_threshold = 0.6
group_label_list = ["woman", "african", "asian", "lgbt", "hispanic", ]

# Whole text of article
article_text = """
He also said labeling anyone who disagrees with the left as a White supremacist will cause the phrase to lose its meaning.

"If everything is racist, nothing is racist. If everything's labeled as White supremacist, nothing is White supremacist," Miyares said.

A 24-year-old graduate student from an Asian American immigrant neighborhood in Brooklyn said linking his community to White supremacy or calling Asians "White-adjacent" is an attempt to invalidate their views.

"I just find this narrative framing disturbing," Sheluyang Peng told Fox News. "It assumes that people from racial, ethnic or religious minority backgrounds — we can't have our own opinions.

"It's like our opinions have to be approved by big media conglomerates, by academia."
GOP presidential candidate Larry Elder said conservatives in minority communities "completely blow up" Democrats' narrative that they're the socially just party while Republicans are synonymous with racism.

"Now there are cracks in their foundation, so they're doubling down and tripling down," he said.
Los Angeles Times columnist Erika D. Smith called Elder "the Black face of White Supremacy" for his political views during his 2021 bid for California governor. Rolling Stone similarly published an article in December 2022 arguing that Herschel Walker, who was at the time running for U.S. Senate in Georgia, was aiding a racist agenda.

Elder called the idea that America is systemically racist a lie, "but it's a lie that Democrats push for stuff like reparations, critical race theory, diversity, equity and inclusion.

"This is really shameful conduct by the legacy media to suddenly say, because a new emerging voting bloc in the United States is starting to shift away from the Democratic Party, that somehow that means it's White supremacy," Miyares said.

"This is really shameful conduct by the legacy media to suddenly say, because a new emerging voting bloc in the United States is starting to shift away from the Democratic Party, that somehow that means it's White supremacy," Miyares said.

"This is really shameful conduct by the legacy media to suddenly say, because a new emerging voting bloc in the United States is starting to shift away from the Democratic Party, that somehow that means it's White supremacy," Miyares said.

"This is really shameful conduct by the legacy media to suddenly say, because a new emerging voting bloc in the United States is starting to shift away from the Democratic Party, that somehow that means it's White supremacy," Miyares said.
"This is really shameful conduct by the legacy media to suddenly say, because a new emerging voting bloc in the United States is starting to shift away from the Democratic Party, that somehow that means it's White supremacy," Miyares said.
"This is really shameful conduct by the legacy media to suddenly say, because a new emerging voting bloc in the United States is starting to shift away from the Democratic Party, that somehow that means it's White supremacy," Miyares said.
"This is really shameful conduct by the legacy media to suddenly say, because a new emerging voting bloc in the United States is starting to shift away from the Democratic Party, that somehow that means it's White supremacy," Miyares said.

"""

def get_bias_info(article_text):

  # Variables to hold info on bias of sentences
  article_bias_info = {}
  biased_sentence_info = []
  biased_sentence_count = 0

  # Classify article bias, find label confidence and if is is classified as biased
  # Characters 0 - 2435 appears to be the sweet spot
  article_bias_info = classifier(article_text[0:2000])[0]
  article_bias_confidence = article_bias_info["score"]
  article_is_biased = True if article_bias_info["label"] == "Biased" else False

  # If article not biased, stop
  if article_bias_confidence < article_bias_threshold or not article_is_biased:
    print("Insufficient bias detected.")
    exit()

  article_bias_info.pop("score")
  article_bias_info.update({"article_bias_confidence": article_bias_confidence})
  sentences = article_text.split(".")

  for sentence in sentences:

    # Clean up sentences
    sentence = sentence.replace("\n", "")

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
    if not len(nouns) == 0:

      sentence_group_bias_confidences = pipe(nouns, candidate_labels=group_label_list)
      group_scores = sentence_group_bias_confidences.get("scores")
      group_labels = sentence_group_bias_confidences.get("labels")
      groups = []

      # Decide which groups are implicated in the sentence
      for i in range(len(group_scores)):
        if group_scores[i] > group_bias_threshold:
          groups.append({group_labels[i]: group_scores[i]})
        else:
          break

      # If no groups, skip this sentence
      if groups == []:
        continue

      current_sentence_info.update({"group_bias_ratings": groups})

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
  return json_bias_data

print(get_bias_info(article_text))
