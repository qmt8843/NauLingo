import re
import json

#establishes a file for stored word dictionaries
STORAGE_FILE = "data/dict_storage.json"

#split message into parts that can and cannot be conjugated
def take_input(message):
    message.strip()

    #converts endings
    words_dict = get_word_dict()
    words_keys = list(words_dict.keys())  

    ends_dict = get_ends_dict()
    ends_keys = list(ends_dict.keys())
    ends_str = "|".join(ends_keys)
    for key in words_keys:
        message = re.sub(rf"\b{key}(\b|{ends_str})", rf"{words_dict[key]}\1", message, flags=re.IGNORECASE)

    #changes all words
    for key in ends_keys:
        message = re.sub(rf"{key}\b", rf"{ends_dict[key]}", message, flags=re.IGNORECASE)

    #conjugates all cons
    cons_dict = get_cons_dict()
    cons_keys = list(cons_dict.keys())
    for key in cons_keys:
        message = re.sub(rf"\b({key})( vona tna | voe ter | mognnen tna | zieden tna | zwe tna | )(\w+)", rf"\1\2\3{cons_dict[key]}", message, flags=re.IGNORECASE)

    # #conjugates all owns
    owns_dict = get_owns_dict()
    owns_keys = list(owns_dict.keys())
    for key in owns_keys:
        message = re.sub(rf"\b{key} (\w+)", rf"\1{owns_dict[key]}", message, flags=re.IGNORECASE)

    #corrects words
    corr_dict = get_corr_dict()
    corr_keys = list(corr_dict.keys())
    for key in corr_keys:
        message = re.sub(rf"{key}", rf"{corr_dict[key]}", message, flags=re.IGNORECASE)

    return message

#gets a dictionary of english:naumarian words from pickled storage file
def get_word_dict():
    dict = json.load(open(STORAGE_FILE, "r"))
    return dict[0]

#gets a dictionary of english:naumarian endings from pickled storage file
def get_ends_dict():
    dict = json.load(open(STORAGE_FILE, "r"))
    return dict[1]

#gets a dictionary of english:naumarian ownership words from pickled storage file
def get_owns_dict():
    dict = json.load(open(STORAGE_FILE, "r"))
    return dict[2]

#gets a dictionary of english:naumarian pronouns from pickled storage file
def get_cons_dict():
    dict = json.load(open(STORAGE_FILE, "r"))
    return dict[3]

#gets a dictionary of english:naumarian pronouns from pickled storage file
def get_corr_dict():
    dict = json.load(open(STORAGE_FILE, "r"))
    return dict[4]

#adds a english:naumarian keyset to words dictionary in pickled storage file
def add_word(english, naumarian):
    dict = json.load(open(STORAGE_FILE, "r"))
    dict[0][english] = naumarian
    with open(STORAGE_FILE, "wt") as f:
        json.dump(dict, f, indent=4)

def convert_word_doc(filename):
    with open(filename) as file:
        for line in file:
            first = line.split(")(?")
            second = line.split("?:")[0]
            #second = line.split(r"\b")[1].split(")(?:")[0]

            #second=first.split(")(")[1]
            print(second)
def mass_add_word(filename, filename2):
    with open(filename) as english_file:
        with open(filename2) as nau_file:
            eng = english_file.readlines()
            nau = nau_file.readlines()
            for i in range(len(eng)):
                add_word(eng[i].strip(), nau[i].strip())

def main():
    inp = input("Give some input: ")
    print(take_input(inp))
    #convert_word_doc("data/paste.txt")
    #mass_add_word("data/paste.txt", "data/paste2.txt")

main()