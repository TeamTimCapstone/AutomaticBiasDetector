import mysql.connector
import json

class DatabaseFunctions:
  def __init__(self):
    self.username = "TeamTim"
    self.password = "TeamTim123!"
    self.connection = mysql.connector.connect(
            host="localhost",
            user='root',
            password=self.password,
            database="Bias_Detector")
    self.cursor = self.connection.cursor();

  def get_website_bias_rating(self, article_url="", website_url=""):
    
    try:
      if article_url != "":  
        self.cursor.execute('SELECT bias_rating FROM Website WHERE website_url = (SELECT website_url FROM Article WHERE article_url = "%s");' % (article_url))
        bias_rating = (float) (self.cursor.fetchall()[0][0])
        return bias_rating

      elif article_url != "":
        self.cursor.execute('SELECT bias_rating FROM Website WHERE website_url = "%s";' % (website_url))
        bias_rating = (float) (self.cursor.fetchall()[0][0])
        return bias_rating
    except:
      pass
    
    return 0


  def json_string_retrieve(self, article_url):

    # Return empty string if the article is not in the database

    self.cursor.execute('SELECT * FROM Article WHERE article_url = "%s";' % (article_url))
    article_in_database = self.cursor.fetchall()
    if article_in_database == []:
      return ""

    json_string = {}

    # Get Website
    self.cursor.execute('SELECT website_url, bias_rating FROM Website WHERE website_url = (SELECT website_url FROM Article WHERE article_url = "%s");' % (article_url))
    website = self.cursor.fetchall()
    if website != []:
      json_string.update({'website_url': website[0][0]})
      json_string.update({'website_bias_rating': (float) (website[0][1])})

    json_string['label'] = "Biased"
    
    json_string['article_url'] = article_url
    
    self.cursor.execute('SELECT bias_rating FROM Article WHERE article_url = "%s";' % (article_url))
    article_info = self.cursor.fetchall()
    json_string['article_bias_confidence'] = (float) (article_info[0][0])
    
    self.cursor.execute('SELECT id, sentence, bias_rating FROM Bias_Instances WHERE article_url = "%s" ORDER BY id ASC;' % (article_url))
    sentence_info = self.cursor.fetchall()

    json_string['biased_sentence_count'] = len(sentence_info)

    bias_info_by_sentence = []
    for sentence in sentence_info:
      sentence_info = {}
      sentence_info['text'] = sentence[1]
      sentence_info['sentence_bias_confidence'] = (float) (sentence[2])

      biased_groups = []
      self.cursor.execute('SELECT biased_group FROM Bias_Instance_Groups WHERE instance_id = %d;' % (sentence[0]))
      groups = self.cursor.fetchall()
      for group in groups:
        biased_groups.append(group[0])

      sentence_info['biased_groups'] = biased_groups

      bias_info_by_sentence.append(sentence_info)

    json_string['bias_info_by_sentence'] = bias_info_by_sentence

    return (json.dumps(json_string, indent=4))

  def json_string_insert(self, json_string):
    data = json.loads(json_string)

  # Delete tables; using so I can test these with the same data
    '''
    self.cursor.execute('delete from Biased_Words;')
    self.connection.commit()
    self.cursor.execute('delete from Bias_Instance_Groups;')
    self.connection.commit()
    self.cursor.execute('delete from Bias_Instances;')
    self.connection.commit()    
    self.cursor.execute('delete from Article;')
    self.connection.commit()
    '''
  # Check for duplicate article
    self.cursor.execute('SELECT * FROM Article where article_url = "%s";' % (data["article_url"]))
    article_instance = self.cursor.fetchall()
    if article_instance != []:
      return

  # Check for no bias; return
    if data["label"] != "Biased":
      return 

  # Update Website table
    if "website_url" in data:
      # If there is a website included, either make the website or increment the number of articles from the website
      self.cursor.execute('SELECT article_count, bias_rating FROM Website WHERE website_url = "%s"' % (data["website_url"]))
      article_count = self.cursor.fetchall()
      if article_count == []:
        self.cursor.execute('INSERT INTO Website (website_url, bias_rating, article_count) VALUES ("%s", %16.15f, %i);' % (data["website_url"], data["article_bias_confidence"], 1))
      else: 
        self.cursor.execute('UPDATE Website SET article_count = %i, bias_rating = %16.15f  WHERE website_url = "%s";' % (article_count[0][0]+1, ( (float) (article_count[0][1] * article_count[0][0]) + data["article_bias_confidence"]) / (float) (article_count[0][0] + 1), data["website_url"]))
     
      # Insert article with website
      self.cursor.execute('INSERT INTO Article (article_url, bias_rating, website_url) VALUES ("%s", %16.15f, "%s");' % (data["article_url"], data["article_bias_confidence"], data["website_url"]))
    
    else:
      # Insert article without website
      self.cursor.execute('INSERT INTO Article (article_url, bias_rating) VALUES ("%s", %16.15f);' % (data["article_url"], data["article_bias_confidence"]))
      
    self.connection.commit()

    for sentence in data["bias_info_by_sentence"]:
      try:
        # Insert each sentence bias info
        self.cursor.execute('INSERT INTO Bias_Instances (article_url, sentence, bias_rating) VALUES ("%s", "%s", %16.15f)' % (data["article_url"], sentence["text"].replace("\"", "").replace("'", ""), sentence["sentence_bias_confidence"]))
        self.connection.commit()

        self.cursor.execute('SELECT MAX(id) FROM Bias_Instances WHERE article_url = "%s";' % (data["article_url"]))
        instance_id = self.cursor.fetchall()[0][0]
     
        # Insert each group indicated in a sentence
        if "biased_groups" in sentence:
          for group in sentence["biased_groups"]:
            self.cursor.execute('INSERT INTO Bias_Instance_Groups (instance_id, biased_group) VALUES (%d, "%s");' % (instance_id, group))
            self.connection.commit()

        # Insert each word indicated in a sentence
        if "biased_words" in sentence:
          for word in sentence["biased_words"]:
            self.cursor.execute('INSERT INTO Biased_Words (instance_id, word) VALUES (%d, "%s");' % (instance_id, word))
            self.connection.commit()

      except:
        print("database sentence insertion messed up")
    print("inserted")


if __name__ == "__main__":
  d = DatabaseFunctions()
  with open('sample.json', 'r') as openfile:
    json_object = json.load(openfile)

  d.json_string_insert(json.dumps(json_object))
  d.json_string_retrieve("test.com/article")
