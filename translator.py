import re
import json
import time
#establishes a file for stored word dictionaries
STORAGE_FILE = "data/dict_storage.json"

#loads the json storage file
FULL_JSON = dict = json.load(open(STORAGE_FILE, "r"))

#split message into parts that can and cannot be conjugated
def take_input(message):
    start = time.perf_counter()
    message = message.strip()
    message = message.lower()

    #changes all words & endings
    words_dict = get_word_dict()
    words_keys = list(words_dict.keys())  

    ends_dict = get_ends_dict()
    ends_keys = list(ends_dict.keys())
    
    for key in words_keys:
        message = re.sub(rf"\b({key})(r|d)", rf"\1e\2", message, re.IGNORECASE) #replaced english words that add 'r' to have 'er'
        for ekey in ends_keys:
            #this nested for loop increases the time considerably, however it gives a better result
            message = re.sub(rf"\b(?:{key})({ekey})\b", rf"{words_dict[key]}{ends_dict[ekey]}", message, re.IGNORECASE) #replaces words and their endings
            #this method stops the translation of endings to words that don't have a translation

    #conjugates all cons
    cons_dict = get_cons_dict()
    cons_keys = list(cons_dict.keys())
    for key in cons_keys:
        message = re.sub(rf"\b({key})( vona tna | voe ter | mognnen tna | zieden tna | zwe tna | voe | vona | mognnen | zieden | zwe | )(\w+)", rf"\1\2\3{cons_dict[key]}", message, flags=re.IGNORECASE)

    # #conjugates all owns
    owns_dict = get_owns_dict()
    owns_keys = list(owns_dict.keys())
    for key in owns_keys:
        message = re.sub(rf"\b{key} (\w+)", rf"\1{owns_dict[key]}", message, flags=re.IGNORECASE)

    #corrects words - pretty much unneeded now
    # corr_dict = get_corr_dict()
    # corr_keys = list(corr_dict.keys())
    # for key in corr_keys:
    #     message = re.sub(rf"\b{key}\b", rf"{corr_dict[key]}", message, flags=re.IGNORECASE)

    end = time.perf_counter()
    diff = round(end-start, 2)
    return message, diff

#gets a dictionary of english:naumarian words from the loaded json file
def get_word_dict():
    return FULL_JSON[0]

#gets a dictionary of english:naumarian endings from the loaded json file
def get_ends_dict():
    return FULL_JSON[1]

#gets a dictionary of english:naumarian ownership words from the loaded json file
def get_owns_dict():
    return FULL_JSON[2]

#gets a dictionary of english:naumarian pronouns from the loaded json file
def get_cons_dict():
    return FULL_JSON[3]

#gets a dictionary of english:naumarian pronouns from the loaded json file
def get_corr_dict():
    return FULL_JSON[4]

def main():
    inp = input("Give some input: ")
    print(take_input(inp))