import json
from database_functions import DatabaseFunctions
from bias_detector import get_bias_info

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
def run_algorithm(article_text):
    article_url = "test.com/article1"
    dbf = DatabaseFunctions()
    article_json_string = dbf.json_string_retrieve(article_url)

    if article_json_string == "":
        print("analyzing")
        article_json_string = get_bias_info(article_text, article_url)
        dbf.json_string_insert(article_json_string)

    print("Here is the string")
    print(article_json_string)

if __name__ == "__main__":
    # Read input data from stdin if needed
    input_data = input()
    # Run the algorithm with input data
    run_algorithm(input_data)
# if __name__ == "__main__":

#   article_url = "test.com/article1"

#   dbf = DatabaseFunctions()
#   article_json_string = dbf.json_string_retrieve(article_url)

#   if article_json_string == "":
#     print("analyzing")
#     article_json_string = get_bias_info(article_text, article_url)
#     dbf.json_string_insert(article_json_string)

#   print("Here is the string")
#   print(article_json_string)
