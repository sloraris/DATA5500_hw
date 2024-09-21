import requests
import json

example_url = "https://api.datamuse.com/words?ml=usu"

word_key = "word"
score_key = "score"

req = requests.get(example_url)
text = req.text

lst_dct = json.loads(text)

for dct in lst_dct:
    if dct[word_key] == "uva":
        print("uva score: ", dct[score_key])
